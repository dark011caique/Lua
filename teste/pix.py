import customtkinter as ctk
from tkinter import filedialog, messagebox
import pandas as pd
import re
from collections import Counter

# Inicializa a janela
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.geometry("600x400")
root.title("Upload File & Process Errors")

selected_file = None  # Variável para armazenar o caminho do arquivo

# Função para selecionar o arquivo
def upload_file():
    global selected_file
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        selected_file = file_path
        label_file.configure(text=f"Arquivo selecionado:\n{file_path}")
        button_process.configure(state="normal")  # Ativa o botão de processar

# Função para extrair mensagens de erro
def extract_messages(content):
    pattern = r'Message"":""(.*?)"","'
    messages = [match.group(1) for line in content for match in re.finditer(pattern, line)]
    
    grouped_messages = Counter()
    for msg in messages:
        key = msg.split(".")[0]  # Pega apenas a parte inicial da mensagem para agrupar
        grouped_messages[key] += 1
    
    return grouped_messages  # Retorna mensagens agrupadas

# Função para processar o arquivo e exibir os resultados
def process_file():
    if selected_file:
        try:
            with open(selected_file, "r", encoding="utf-8") as file:
                raw_content = file.readlines()

            # Extração e contagem das mensagens de erro
            message_counts = extract_messages(raw_content)

            # Criar o texto do relatório formatado
            error_summary = "\n".join([f"{count:03d} - {message}" for message, count in message_counts.items()])
            
            # Variável para somar os números divididos
            total_sum = 0
            formatted_error_summary = ""
            for line in error_summary.split('\n'):
                count, message = line.split(" - ", 1)  # Divide em duas partes: quantidade e descrição
                
                # Ignora mensagens com "Name or service not known"
                # Ignora mensagens com "Name or service not known", "Connection reset by peer" ou "A network-related or instance-specific error occurred while establishing a connection to SQL Server"
                if any(ignore_phrase in message for ignore_phrase in [
                        "Name or service not known", 
                        "Connection reset by peer",
                        "Error parsing Infinity value", 
                        "A network-related or instance-specific error occurred while establishing a connection to SQL Server"]):
                    continue  # Pula para o próximo erro
                
                count_divided = int(count) // 2  # Divide o número por 2
                total_sum += count_divided  # Soma o número dividido
                formatted_error_summary += f"{count_divided:03d} - {message}\n"

            # Adiciona o total no final
            formatted_error_summary += f"\nTotal: {total_sum}"

            # Exibir o resultado na interface
            result_label.configure(text=formatted_error_summary.strip(), justify="left")
            
            # Exibir também no terminal
            print("\nResumo dos erros:")
            print(formatted_error_summary)
            
            messagebox.showinfo("Sucesso", "Arquivo processado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar o arquivo:\n{str(e)}")
    else:
        messagebox.showwarning("Aviso", "Nenhum arquivo selecionado.")

# Botão de upload
button_upload = ctk.CTkButton(root, text="Upload File", command=upload_file)
button_upload.pack(pady=10)

# Label que mostra o caminho do arquivo
label_file = ctk.CTkLabel(root, text="Nenhum arquivo selecionado", wraplength=500)
label_file.pack(pady=10)

# Botão para processar o arquivo (inicia desativado)
button_process = ctk.CTkButton(root, text="Processar Arquivo", command=process_file, state="disabled")
button_process.pack(pady=10)

# Label para exibir os resultados
result_label = ctk.CTkLabel(root, text="", wraplength=550)
result_label.pack(pady=10)

root.mainloop()
