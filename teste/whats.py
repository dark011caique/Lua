from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from PIL import  Image
import pyautogui
import win32clipboard  # Biblioteca para copiar a imagem para a área de transferência
from datetime import datetime, timedelta
from time import sleep
import time
import customtkinter as ctk
from tkinter import filedialog, messagebox
import pandas as pd
from collections import Counter
import subprocess
import re
import io
import os
import pyperclip



# 🔹 Configurar o WebDriver
chrome_user_data_dir = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
 
options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "localhost:9222")  # Conectar ao Chrome aberto
options.add_argument(f"user-data-dir={chrome_user_data_dir}")
 
# Iniciar WebDriver
driver = webdriver.Chrome(options=options)


# Configuração da janela principal
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("ACC Adiq - WhatsApp")
app.geometry("800x500")

# Layout principal
frame_sidebar = ctk.CTkFrame(app, width=200, corner_radius=0)
frame_sidebar.pack(side="left", fill="y")

frame_main = ctk.CTkFrame(app)
frame_main.pack(side="right", expand=True, fill="both", padx=20, pady=20)

# Título no sidebar
label_title = ctk.CTkLabel(frame_sidebar, text="ACC Adiq", font=("Arial", 18, "bold"))
label_title.pack(pady=20)

# Função para mostrar apenas o frame selecionado
def mostrar_frame(frame):
    for widget in frame_main.winfo_children():
        widget.pack_forget()  # Esconde todos os widgets no frame_main
    frame.pack(fill="both", expand=True, padx=20, pady=20)  # Mostra apenas o frame selecionado

data_hora = datetime.now()

# Arredondando o horário
if data_hora.minute > 30:
    data_hora = data_hora.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
else:
    data_hora = data_hora.replace(minute=0, second=0, microsecond=0)

# Formatando a data e hora no formato desejado
data_formatada = data_hora.strftime("%d/%m")

# Criando a string com a data e hora arredondada
aa = f'🔊 *BS2 PAYMENTS*. {data_formatada}\n'

# Lista de mensagens (iniciando com o ícone ✅)
mensagens = [f"{aa}",
    "✅ ASLC029 (Liquidação Débito)",
    "✅ ENVELOPES AGENDADOS (Antecipação)",
    "✅ ARQUIVOS CONTAS A RECEBER (Financeiro)",
    "✅ ARQUIVOS EDI (Conciliação)",
    "✅ ASLC031 (Antecipação 1ª Janela Adiq Remessa)",
    "✅ ASLC027 (Liquidação Crédito)",
    "✅ ASLC031 (Antecipação 2ª Janela Adiq Remessa)",
    "✅ ENVELOPES ANTECIPADOS (1º janela)",
    "✅ ASLC031 (Antecipação 1ª Janela ADQUIRENCIA)",
    "✅ ASLC031 (Antecipação 3ª Janela Adiq Remessa)",
    "✅ ENVELOPES ANTECIPADOS (2ª janela)",
    "✅ ASLC031 (Antecipação 2ª Janela ADQUIRENCIA)"
]

# Ícones disponíveis para seleção
icones = ["✅", "⚠", "🚫", "❌","🔄"]

# frame whatsapp
frame_whatsapp = ctk.CTkFrame(frame_main, fg_color="gray20", corner_radius=10)
label_whatsapp = ctk.CTkLabel(frame_whatsapp, text="WhatsApp", font=("Arial", 24, "bold"))
label_whatsapp.pack(pady=10)

# Scrollable Frame para adicionar os checkboxes
scrollable_frame = ctk.CTkScrollableFrame(frame_whatsapp, width=500, height=300, corner_radius=10)
scrollable_frame.pack(pady=10)

# Checkboxes com variáveis para verificar o estado
checkbox_vars = []
checkboxes = []

# Criando os checkboxes para cada mensagem
for i, mensagem in enumerate(mensagens):
    var = ctk.BooleanVar(value=False)  # Inicialmente desmarcado
    checkbox = ctk.CTkCheckBox(scrollable_frame, text=mensagem, variable=var, onvalue=True, offvalue=False)
    checkbox.pack(anchor="w", pady=5)  # Alinha à esquerda
    checkbox_vars.append(var)
    checkboxes.append(checkbox)

# Função para enviar mensagens e gravar no arquivo txt
# Função para enviar mensagens no WhatsApp Web via Selenium
def enviar_mensagens():
    mensagens_selecionadas = [mensagens[i] for i, var in enumerate(checkbox_vars) if var.get()]

    if not mensagens_selecionadas:
        messagebox.showinfo("Nenhuma Seleção", "Você não selecionou nenhuma mensagem para enviar!")
        return

    mensagem = "\n".join(mensagens_selecionadas)
    caminho_arquivo = "mensagens_selecionadas.txt"
    
    try:
        # Verificando se o diretório onde o arquivo será salvo existe
        diretorio_arquivo = os.path.dirname(caminho_arquivo)
        if diretorio_arquivo and not os.path.exists(diretorio_arquivo):
            os.makedirs(diretorio_arquivo)  # Cria o diretório caso não exista

        # Gravar as mensagens no arquivo .txt com a codificação UTF-8
        with open(caminho_arquivo, "w", encoding="utf-8") as file:
            file.write(mensagem)

        # Verificar se o arquivo foi criado e exibir o conteúdo
        if os.path.exists(caminho_arquivo):
            with open(caminho_arquivo, "r", encoding="utf-8") as file:
                conteudo_arquivo = file.read()
                print("Conteúdo do arquivo:")
                print(conteudo_arquivo)
        else:
            messagebox.showerror("Erro", "O arquivo não foi criado corretamente.")
    except Exception as e:
        # Exibindo mais detalhes sobre o erro
        messagebox.showerror("Erro", f"Ocorreu um erro ao gravar no arquivo: {str(e)}")
        print(f"Erro ao gravar no arquivo: {str(e)}")  # Para depuração no terminal
        messagebox.showerror("Erro", f"Ocorreu um erro ao gravar no arquivo: {str(e)}")
        
    # Acessar o WhatsApp Web
    driver.get("https://web.whatsapp.com")

    nome_grupo = "Lucas ACC"  # Defina o nome do grupo que você deseja buscar no WhatsApp Web

    # Aguardar o WhatsApp Web carregar e permitir o login
    time.sleep(15)  # Aumente esse tempo se necessário para escanear o QR Code

    try:
        # Aguardar até que a lista de chats esteja visível e procurar pelo grupo
        grupo = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//span[@title="{}"]'.format(nome_grupo)))
        )
        
        # Clicar no grupo encontrado
        grupo.click()

        time.sleep(2)

        campo_mensagem = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div[2]/div[1]/p'))
        )

        # Garantir que o campo de texto está focado antes de colar
        campo_mensagem.click()

        # Lendo o conteúdo do arquivo de texto
        with open(caminho_arquivo, "r", encoding="utf-8") as file:
            conteudo = file.read()

        # Usar o pyperclip para copiar o conteúdo do arquivo para a área de transferência
        pyperclip.copy(conteudo)

        # Garantir que a área de texto está limpa antes de colar
        campo_mensagem.clear()

        # Simular a ação de "Ctrl + V" (colar) usando o ActionChains
        action = ActionChains(driver)
        action.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

        # Aguardar um momento para garantir que a mensagem foi colada
        time.sleep(2)


        # Enviar a mensagem após colar
        #campo_mensagem.send_keys(Keys.RETURN)

        # Notificação de sucesso
        messagebox.showinfo("Mensagem Enviada", "A mensagem foi enviada com sucesso!")

    except Exception as e:
        messagebox.showinfo("Erro", f"Não foi possível encontrar o grupo: {nome_grupo}. Erro: {e}")
        print(f"Erro", f"Não foi possível encontrar o grupo: {nome_grupo}. Erro: {e}")
    finally:
        # Não feche 
        pass


# Função para abrir a tela de alteração
def alterar_icone_na_tela():
    # Coletando as mensagens selecionadas
    mensagens_selecionadas = []
    for i, var in enumerate(checkbox_vars):
        if var.get():  # Se o checkbox estiver marcado
            mensagens_selecionadas.append(mensagens[i])  # Adiciona a mensagem à lista selecionada

    if not mensagens_selecionadas:
        messagebox.showinfo("Nenhuma Seleção", "Você não selecionou nenhuma mensagem para alterar!")
        return

    # Criar uma nova janela para alteração do ícone
    janela_alteracao = ctk.CTkToplevel(app)
    janela_alteracao.title("Alteração de Ícone")
    janela_alteracao.geometry("400x400")

    # Título na nova janela
    label_titulo = ctk.CTkLabel(janela_alteracao, text="Selecione uma mensagem para alterar o ícone", font=("Arial", 18, "bold"))
    label_titulo.pack(pady=10)

    # Adicionando checkboxes para as mensagens selecionadas
    checkbox_vars_selecionados = []
    checkboxes_selecionados = []

    for i, mensagem in enumerate(mensagens_selecionadas):
        var = ctk.BooleanVar(value=False)  # Inicialmente desmarcado
        checkbox = ctk.CTkCheckBox(janela_alteracao, text=mensagem, variable=var, onvalue=True, offvalue=False)
        checkbox.pack(anchor="w", pady=5)  # Alinha à esquerda
        checkbox_vars_selecionados.append(var)
        checkboxes_selecionados.append(checkbox)

    # Função para aplicar o ícone e alterar o conteúdo dentro dos parênteses
    def aplicar_icone():
        # Coletando as mensagens selecionadas para alteração
        mensagens_a_alterar = []
        for i, var in enumerate(checkbox_vars_selecionados):
            if var.get():  # Se o checkbox estiver marcado
                mensagens_a_alterar.append(mensagens_selecionadas[i])  # Adiciona a mensagem à lista selecionada

        if not mensagens_a_alterar:
            messagebox.showinfo("Nenhuma Seleção", "Você não selecionou nenhuma mensagem para alterar o ícone!")
            return

        # Criar um menu suspenso para escolher o ícone
        icone_selecionado = ctk.CTkOptionMenu(janela_alteracao, values=icones)
        icone_selecionado.pack(pady=10)

        # Campo de texto para editar o conteúdo dentro dos parênteses
        campo_texto = ctk.CTkEntry(janela_alteracao, placeholder_text="Digite o novo conteúdo")
        campo_texto.pack(pady=10)

        def confirmar_icone():
            # Pegando o ícone selecionado
            icone = icone_selecionado.get()

            # Atualizando as mensagens (somente o conteúdo dentro dos parênteses será alterado)
            novo_conteudo = campo_texto.get()  # Pegando o novo conteúdo dos parênteses
            if novo_conteudo:
                for i, mensagem in enumerate(mensagens):
                    if mensagens[i] in mensagens_a_alterar:
                        # Dividindo a string em ícone + conteúdo antes dos parênteses e dentro dos parênteses
                        partes = mensagem.split("(", 1)
                        if len(partes) > 1:
                            # Mantém o ícone e o texto antes dos parênteses, altera apenas o conteúdo dentro dos parênteses
                            partes_antes_parenteses = partes[0].strip()  # Mantém o ícone e o texto antes dos parênteses

                            # Verifica se o texto antes dos parênteses começa com um ícone
                            if partes_antes_parenteses and partes_antes_parenteses[0] in icones:
                                # Mantém o ícone correto e preserva o texto após o ícone
                                icone_preservado = partes_antes_parenteses.split(" ", 1)[0]
                                texto_antes_parenteses = partes_antes_parenteses[len(icone_preservado):].strip()
                            else:
                                # Se não houver ícone, apenas preserva o texto
                                icone_preservado = ""
                                texto_antes_parenteses = partes_antes_parenteses.strip()

                            # Agora, alteramos o ícone para o novo ícone selecionado, e o conteúdo entre parênteses
                            mensagens[i] = icone + " " + texto_antes_parenteses + f"({novo_conteudo})"
                        else:
                            # Caso não haja parênteses, cria-os com o novo conteúdo
                            mensagens[i] = icone + " " + partes[0] + f"({novo_conteudo})"

                        # Atualiza os textos dos checkboxes na tela principal
                        for j, checkbox in enumerate(checkboxes):
                            if checkbox_vars[j].get() and mensagens[j] == mensagens[i]:
                                checkbox.configure(text=mensagens[i])  # Atualiza o texto com o novo ícone e conteúdo

                # Confirmando a alteração
                messagebox.showinfo("Alteração Concluída", f"O ícone foi alterado para '{icone}' e o conteúdo dentro dos parênteses foi alterado para '{novo_conteudo}' nas mensagens selecionadas!")
                janela_alteracao.destroy()

        # Botão para confirmar a alteração de ícone
        btn_confirmar = ctk.CTkButton(janela_alteracao, text="Confirmar Alteração", command=confirmar_icone)
        btn_confirmar.pack(pady=20)

    # Botão para aplicar as alterações
    btn_aplicar = ctk.CTkButton(janela_alteracao, text="Aplicar Alteração", command=aplicar_icone)
    btn_aplicar.pack(pady=20)

    # Tornar a janela de alteração modal (bloqueia a janela principal)
    janela_alteracao.grab_set()

# Botão para enviar as mensagens selecionadas na tela principal
btn_enviar_mensagens = ctk.CTkButton(frame_whatsapp, text="Enviar Mensagens", command=enviar_mensagens)
btn_enviar_mensagens.pack(pady=20)

# Botão dentro do checklist para abrir a tela de alteração
btn_alterar_checklist = ctk.CTkButton(frame_whatsapp, text="Alterar Mensagens", command=alterar_icone_na_tela)
btn_alterar_checklist.pack(pady=20)

# Exibir o frame do WhatsApp por padrão
mostrar_frame(frame_whatsapp)

# Botões da sidebar
btn_whatsapp = ctk.CTkButton(frame_sidebar, text="WhatsApp", fg_color="gray30", hover_color="gray40", command=lambda: mostrar_frame(frame_whatsapp))
btn_whatsapp.pack(fill="x", pady=5, padx=10)

app.mainloop()
