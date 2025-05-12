import google.generativeai as genai
import PIL.Image
import io
import os
import json
import re # Import regex for parsing

# --- Configuration ---
# IMPORTANT: Set your API key as an environment variable named GOOGLE_API_KEY
# How to set environment variables:
# Linux/macOS: export GOOGLE_API_KEY="YOUR_API_KEY_HERE"
# Windows (cmd): set GOOGLE_API_KEY=YOUR_API_KEY_HERE
# Windows (PowerShell): $env:GOOGLE_API_KEY="YOUR_API_KEY_HERE"
# Or use a .env file and python-dotenv library for development.

try:
    GOOGLE_API_KEY = "AIzaSyDojM3yGOE3ANUztNYRvik6bXgOwh9RsI4"
    genai.configure(api_key=GOOGLE_API_KEY)
except KeyError:
    print("Erro: A variável de ambiente GOOGLE_API_KEY não foi definida.")
    print("Por favor, defina sua chave de API do Google AI Studio como uma variável de ambiente.")
    exit() # Exit if the key is not found
except Exception as e:
    print(f"Erro ao configurar a API do Gemini: {e}")
    exit()

# Use the model capable of understanding images
#MODEL_NAME = 'gemini-pro-vision'
MODEL_NAME = 'gemini-1.5-flash-latest'
# You could also try newer models like 'gemini-1.5-flash-latest' or 'gemini-1.5-pro-latest'
# model = genai.GenerativeModel('gemini-1.5-flash-latest')

def extract_json_from_text(text):
    """Tries to extract a JSON list or object from a string, handling markdown code blocks."""
    # Look for ```json ... ``` or ``` ... ``` blocks
    match = re.search(r"```(json)?\s*([\s\S]*?)\s*```", text, re.IGNORECASE)
    if match:
        return match.group(2).strip() # Extract content within the backticks

    # If no markdown block, try to find the start of a list or object
    list_start = text.find('[')
    obj_start = text.find('{')

    if list_start != -1 and (obj_start == -1 or list_start < obj_start):
        # Assume it starts with a list
        match = re.search(r"(\[[\s\S]*\])", text[list_start:])
        if match:
            return match.group(1)
    elif obj_start != -1:
         # Assume it starts with an object (though we expect a list here)
         # This might need adjustment if a single dict is valid output
         match = re.search(r"(\{[\s\S]*\})", text[obj_start:])
         if match:
            return match.group(1)

    # If no clear JSON structure found, return the original text for the parser to try
    return text.strip()


def analyze_image_data(image_path):
    """
    Analisa uma imagem de tabela usando a API do Gemini e verifica a consistência dos dados.

    Args:
        image_path (str): O caminho para o arquivo de imagem.

    Returns:
        dict or str: Um dicionário onde as chaves são as origens dos clientes e os valores são
                     dicionários contendo os dados lidos e o status de consistência,
                     ou uma string de erro.
    """
    print(f"Tentando analisar a imagem: {image_path}")

    if not os.path.exists(image_path):
        return f"Erro: Arquivo de imagem não encontrado em '{image_path}'"

    model = genai.GenerativeModel(MODEL_NAME)

    try:
        # It's safer to open the image directly with PIL first, then get bytes
        img = PIL.Image.open(image_path)
        # You might want to uncomment the next line if you need to explicitly
        # pass the image data bytes, but generate_content usually handles PIL Images.
        # img_byte_arr = io.BytesIO()
        # img.save(img_byte_arr, format=img.format or 'PNG') # Use original format or default to PNG
        # image_data = img_byte_arr.getvalue()

        # Prepare the prompt - be very specific about the output format
        prompt = """
Analise os dados da tabela presente nesta imagem.
Extraia as informações de cada linha, focando nas colunas:
ORIGEM, QTD_REG_ENVIO_CMG, TOT_ENVIO_NUCLI, TOT_PRO_RETORNADO_NUCLI, TOT_RET_GER_NACLI, STATUS_ARQUIVOS.

Formate a resposta *exclusivamente* como uma lista de dicionários Python no formato JSON.
Cada dicionário na lista deve representar uma linha da tabela com as chaves correspondentes aos nomes das colunas mencionadas.
Certifique-se de que os valores numéricos sejam representados como números (inteiros), não strings.

Exemplo de formato de saída esperado:
[
  {"ORIGEM": "CLIENTE_A", "QTD_REG_ENVIO_CMG": 1500, "TOT_ENVIO_NUCLI": 1500, "TOT_PRO_RETORNADO_NUCLI": 1500, "TOT_RET_GER_NACLI": 1500, "STATUS_ARQUIVOS": "OK"},
  {"ORIGEM": "CLIENTE_B", "QTD_REG_ENVIO_CMG": 200, "TOT_ENVIO_NUCLI": 200, "TOT_PRO_RETORNADO_NUCLI": 199, "TOT_RET_GER_NACLI": 199, "STATUS_ARQUIVOS": "PROCESSANDO"}
]

Não inclua nenhuma explicação, introdução, texto adicional, ou marcadores de código (```json ... ```) na sua resposta final. Retorne *apenas* a lista JSON.
"""

        print("Enviando requisição para a API Gemini...")
        # Pass the prompt and the PIL Image object directly
        response = model.generate_content([prompt, img])

        # Access the generated text
        # Check safety ratings if necessary: response.prompt_feedback
        # if response.prompt_feedback.block_reason:
        #    return f"Erro: Requisição bloqueada pela API. Razão: {response.prompt_feedback.block_reason}"
        # Check for candidate errors if needed:
        # if not response.candidates or response.candidates[0].finish_reason != 'STOP':
        #    return f"Erro: Resposta da API não foi gerada completamente. Finish Reason: {response.candidates[0].finish_reason if response.candidates else 'N/A'}"

        extracted_text = response.text
        print("Resposta recebida da API Gemini:")
        print("------------------------------------")
        print(extracted_text)
        print("------------------------------------")
        print("Tentando extrair e decodificar JSON...")

        # Attempt to clean and extract JSON from the response
        json_text = extract_json_from_text(extracted_text)

        # Try to parse the cleaned text as JSON
        try:
            data_list = json.loads(json_text)
            if not isinstance(data_list, list):
                 return f"Erro: O JSON decodificado não é uma lista. Resposta processada:\n{json_text}"

            print(f"JSON decodificado com sucesso. {len(data_list)} itens encontrados.")
            processed_data = {}
            for item in data_list:
                if not isinstance(item, dict):
                    print(f"Aviso: Item na lista JSON não é um dicionário: {item}")
                    continue # Skip non-dict items

                origin = item.get('ORIGEM')
                if origin:
                    # Use .get with default 0 and handle potential non-integer values gracefully
                    try:
                        qtd_enviada = int(item.get('QTD_REG_ENVIO_CMG', 0))
                        tot_envio = int(item.get('TOT_ENVIO_NUCLI', 0))
                        tot_pro = int(item.get('TOT_PRO_RETORNADO_NUCLI', 0))
                        tot_ret = int(item.get('TOT_RET_GER_NACLI', 0))
                    except (ValueError, TypeError) as e:
                         print(f"Aviso: Erro ao converter valor para inteiro para ORIGEM '{origin}'. Item: {item}. Erro: {e}. Usando 0.")
                         qtd_enviada = tot_envio = tot_pro = tot_ret = 0 # Reset on conversion error

                    status = item.get('STATUS_ARQUIVOS', 'N/A') # Default status if missing

                    # Perform consistency check
                    consistente = (qtd_enviada == tot_envio and
                                   qtd_enviada == tot_pro and
                                   qtd_enviada == tot_ret and
                                   qtd_enviada > 0) # Maybe add check > 0 if 0 shouldn't be consistent

                    processed_data[origin] = {
                        'qtd_enviada': qtd_enviada,
                        'tot_envio': tot_envio,
                        'tot_pro': tot_pro,
                        'tot_ret': tot_ret,
                        'status': status,
                        'consistente': consistente
                    }
                else:
                    print(f"Aviso: Item na lista JSON não possui a chave 'ORIGEM': {item}")

            if not processed_data:
                 return f"Erro: Nenhum dado válido com 'ORIGEM' foi extraído da resposta JSON.\nResposta processada:\n{json_text}"

            return processed_data

        except json.JSONDecodeError as json_err:
            # Provide more context on JSON decode error
            error_line = getattr(json_err, 'lineno', 'N/A')
            error_col = getattr(json_err, 'colno', 'N/A')
            return (f"Erro fatal ao decodificar a resposta JSON da API.\n"
                    f"Erro: {json_err}\n"
                    f"Posição (aprox): Linha {error_line}, Coluna {error_col}\n"
                    f"--- Texto que falhou na decodificação ---\n"
                    f"{json_text}\n"
                    f"--- Resposta Bruta da API ---\n"
                    f"{extracted_text}")
        except Exception as e:
             # Catch other potential errors during processing
             return f"Erro inesperado ao processar a lista de dados: {e}\nDados recebidos (pré-processamento): {data_list if 'data_list' in locals() else 'N/A'}"

    except FileNotFoundError:
        return f"Erro: Arquivo de imagem não encontrado em '{image_path}'"
    except PIL.UnidentifiedImageError:
         return f"Erro: Não foi possível identificar ou abrir o arquivo de imagem em '{image_path}'. Verifique se é um formato de imagem válido (PNG, JPG, etc.)."
    except genai.types.generation_types.StopCandidateException as stop_ex:
         # Handle cases where the generation was stopped by the API (e.g., safety)
         return f"Erro: Geração de conteúdo interrompida pela API. Detalhes: {stop_ex}"
    except Exception as e:
        # Catch-all for other potential errors (API connection, etc.)
        return f"Ocorreu um erro inesperado ao analisar a imagem: {e}"

# --- Main Execution ---
if __name__ == "__main__":
    # SUBSTITUA PELO CAMINHO CORRETO DA SUA IMAGEM
    image_file_path = "dark.png"

    print(f"Iniciando análise da imagem: {image_file_path}")
    analysis_result = analyze_image_data(image_file_path)

    print("\n--- Resultado da Análise ---")
    if isinstance(analysis_result, str):
        # It's an error message
        print(analysis_result)
    elif not analysis_result:
        print("Nenhum dado foi extraído ou processado.")
    else:
        for origin, details in analysis_result.items():
            print(f"\nAnálise para ORIGEM: {origin}")
            print(f"  QTD_REG_ENVIO_CMG: {details['qtd_enviada']}")
            print(f"  TOT_ENVIO_NUCLI: {details['tot_envio']}")
            print(f"  TOT_PRO_RETORNADO_NUCLI: {details['tot_pro']}")
            print(f"  TOT_RET_GER_NACLI: {details['tot_ret']}")
            print(f"  STATUS_ARQUIVOS: {details['status']}")
            if details['consistente']:
                print("  Consistência dos Totais: \033[92mOK\033[0m (Quantidades coincidem)") # Green OK
            else:
                print("  Consistência dos Totais: \033[91mERRO\033[0m (Quantidades não coincidem)") # Red ERRO
            print("-" * 35)