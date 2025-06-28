from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service as ChromeService
from PIL import  Image
import win32clipboard  # Biblioteca para copiar a imagem para a área de transferência
from datetime import datetime, timedelta
from time import sleep
import time
#import tkinter as tk
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from tkinter import filedialog, messagebox
import pandas as pd
from collections import Counter
import subprocess
import re
import io
import os
import shutil
import pyperclip
import logging
import threading
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
import shutil
import customtkinter as ctk
from tkinter import filedialog, messagebox, StringVar, BooleanVar
import pyautogui
import pygetwindow as gw

#subprocess.Popen(r"C:\Users\ADQT0141\OneDrive - Banco BS2\Área de Trabalho\Lua\dist\monitoramento.exe")
# 🔹 Configurar logging
logging.basicConfig(filename="app.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# POP de alertas na tela 
def show_checkmark(self):
    # Show some positive message with the checkmark icon
    CTkMessagebox(message=self,
                  icon="check", option_1="Thanks")
    
def show_error(mensagem):
    # Show some error message
    CTkMessagebox(title="Error", message=mensagem, icon="cancel")
    
def show_info():
    # Default messagebox for showing some information
    CTkMessagebox(title="Info", message="Verificando se há um navegador aberto. Caso não haja, um novo será iniciado. Por favor, aguarde um momento...")


def chrome():
    chrome_user_data_dir = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "localhost:9222")
    options.add_argument(f"user-data-dir={chrome_user_data_dir}")

    driver = None  # 🔸 Define driver no escopo externo

    try: 
        driver = webdriver.Chrome(options=options)
        print("Entrou no navegador já aberto")
    except Exception:
        print("Falha ao conectar. Tentando abrir o Chrome no modo de depuração...")
        chrome_user_data_dir = r"C:\Users\Win10\AppData\Local\Google\Chrome\User Data"
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

        chrome_command = f'"{chrome_path}" --remote-debugging-port=9222 --user-data-dir="C:\\ChromeDebug"'

        try:
            subprocess.Popen(chrome_command, shell=True)
        except Exception as e:
            print(f"Erro ao abrir o Chrome: {e}")
            return None  # Caso falhe, retorna None

        sleep(2)

        options = webdriver.ChromeOptions()
        options.add_experimental_option("debuggerAddress", "localhost:9222")
        options.add_argument(f"user-data-dir={chrome_user_data_dir}")
        # Iniciar o navegador maximizado

        options.add_argument("--start-maximized")


        driver = webdriver.Chrome(options=options, service=ChromeService())
    
    return driver  # 🔸 Retorna o driver para uso externo

driver = chrome()

def path_image():

    imagem = "img"

    # Cria a pasta se ela ainda não existir
    if not os.path.exists(imagem):
        os.makedirs(imagem)
        print(f"Pasta '{imagem}' criada com sucesso!")
    else:
        print(f"A pasta '{imagem}' já existe.")

path_image()

# Configuração da janela principal
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("ACC Adiq - LUA")
app.geometry("800x500")

# Layout principal
frame_sidebar = ctk.CTkFrame(app, width=200, corner_radius=0)
frame_sidebar.pack(side="left", fill="y")

frame_main = ctk.CTkFrame(app)
frame_main.pack(side="right", expand=True, fill="both", padx=20, pady=20)

# Título no sidebar
label_title = ctk.CTkLabel(frame_sidebar, text="ACC Adiq", font=("Arial", 18, "bold"))
label_title.pack(pady=20)

driver = chrome()

def limpar_screenshots():
    files = ["fisico.png", "ecommerce.png", "unificada.png", "banese.png", "softpass.png", "pix.png", "arquivos.png", "zabbix.png", "uptime.png", "cecommerce.png", "cfisico.png", "wtnet.png", "snifferprd.png"]
    for file in files:
        if os.path.exists(file):
            try:
                os.remove(file)
                logging.info(f"Screenshot {file} removido")
            except:
                logging.warning(f"Não foi possível remover {file}")

# Função para mostrar apenas o frame selecionado
def mostrar_frame(frame):
    for widget in frame_main.winfo_children():
        widget.pack_forget()  # Esconde todos os widgets no frame_main
    frame.pack(fill="both", expand=True, padx=20, pady=20)  # Mostra apenas o frame selecionado

def forcar_foco_chrome():
    """Garante que a janela do navegador esteja em primeiro plano e limpa a tela de outras janelas visíveis."""
    time.sleep(1)  # Pequeno delay para carregar as janelas
    chrome_windows = [w for w in gw.getWindowsWithTitle(" - Google Chrome") if not w.isMinimized]

    if chrome_windows:
        chrome = chrome_windows[0]
        chrome.activate()
        chrome.maximize()
        time.sleep(1)

        # Minimiza outras janelas visíveis que não são o Chrome
        for w in gw.getAllWindows():
            if w != chrome and not w.isMinimized and w.title != '':
                try:
                    w.minimize()
                except:
                    pass
    else:
        print("❌ Janela do Chrome não encontrada.")

def capturar_screenshot(url=None, path="img/screenshot.png", wait_time=4, click_xpath=None):
    if url:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(wait_time)

        if click_xpath:
            try:
                zoom = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, click_xpath)))
                zoom.click()
                WebDriverWait(driver, 3).until(EC.staleness_of(zoom))
            except Exception as e:
                logging.warning(f"Erro ao clicar no botão: {e}")

    # forcar_foco_chrome()  # Garante foco na janela certa
    # time.sleep(1)

    os.makedirs(os.path.dirname(path), exist_ok=True)

    # Define resolução da tela e região para remover a barra de abas do navegador
    largura_tela, altura_tela = pyautogui.size()
    altura_barra_chrome = 70  # ajuste conforme necessário, geralmente entre 80-100

    region = (0, altura_barra_chrome, largura_tela, altura_tela - altura_barra_chrome)
    screenshot = pyautogui.screenshot(region=region)
    screenshot.save(path)
    logging.info(f"🖼️ Screenshot salva: {path}")


# Funções para serem chamadas
def checklist():
    # Obtendo a data e o horário atuais
    data_hora = datetime.now()

    # Arredondando o horário
    if data_hora.minute > 30:
        data_hora = data_hora.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    else:
        data_hora = data_hora.replace(minute=0, second=0, microsecond=0)

    # Formatando a data e hora no formato desejado
    data_formatada = data_hora.strftime("%d/%m/%Y - %Hh%M")

    # Criando a string com a data e hora arredondada
    mensagem = f'ACC ADIQ: ⏰⏰ Checklist Ambientes {data_formatada}'

    # 🔹 Configurar o emoji SOS (usando Unicode diretamente)
    sos_emoji = "\U0001F198"  # Emoji SOS 🆘

    data_url = data_hora.strftime("%Y-%m-%d")

    # VARIAVEIS
    px = f"https://grafana-ocp4.adiq.io/d/f5067f59-9f90-4e0f-b86c-8c2ba32fc3a8/monitor-pix-gw-bancario-geral?orgId=1&from=1740997996000&to=1741040658000"
    t_fisico = "✅ [Transacional Físico](https://grafana-monitoring-hml-grafana-monitoring-hml.apps.svs.adiq.local/d/ee9atfdxwhg5cf/visao-geral-transacional-fisico-sniffer-dxc?orgId=1&from=now-30m&to=now&refresh=5s)"
    t_ecommerce = "✅ [Transacional E-commerce](https://grafana-monitoring-hml-grafana-monitoring-hml.apps.svs.adiq.local/d/fe97u788lyneob/visao-geral-transacional-e-commerce?from=now-1h&to=now&orgId=1&refresh=5s)"
    t_unificada = "✅ [Tela Unificada](https://grafana-monitoring-hml-grafana-monitoring-hml.apps.svs.adiq.local/d/eeie77hr8msxsf/4442ba7d-ef52-5118-988d-71a7dd3f9a5a?orgId=1&refresh=1m)"
    t_banese = "✅ [Transacional Hub On-Us Banese](https://adqtrjvpkbn01.adiq.local:5601/app/dashboards#/view/3cf45840-2021-11ee-a5b4-81e7ec0febaf)"
    t_spftpass = "✅ [Transacional Softpass](https://adqtrjvpkbn01.adiq.local:5601/app/dashboards#/view/73b07c60-2395-11ef-a2fe-31640ea6f96c)"
    t_pix = "✅ [Transacional PIX](https://grafana-ocp4.adiq.io/d/f5067f59-9f90-4e0f-b86c-8c2ba32fc3a8/monitor-pix-gw-bancario-geral?orgId=1&from=1740997996000&to=1741040658000&var-dataselecionada=2025-03-07)"
    t_atquivos = "✅ [Grafana - Arquivos](https://grafana-ocp4.adiq.io/d/uAoTFkJMzr/monitoracao-arquivos-geral-ambiente-de-prd?orgId=1&var-DiaNaoUtil=1&var-JanelaMarcacao=Janela%201%20Ida&var-JanelaMarcacao=Janela%202%20Ida&var-JanelaMarcacao=Janela%203%20Ida&var-JanelaMarcacao=Janela%201%20Volta&var-JanelaMarcacao=Janela%202%20Volta&var-JanelaMarcacao=Janela%203%20Volta&var-DataMarcacao=2025-02-14&from=now-1h&to=now&refresh=10s)"
    t_zabbix = "✅ [Zabbix](http://radar.adiq.local/zabbix/zabbix.php?action=dashboard.view)"
    t_uptime = "✅ [Uptime](https://dashboard.uptimerobot.com/monitors)"

    # def capturar_screenshot(url, path, wait_time=6, click_xpath=None):
    #         driver.get(url)
    #         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    #         time.sleep(wait_time)
    #         if click_xpath:
    #             try:
    #                 zoom = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, click_xpath)))
    #                 zoom.click()
    #                 WebDriverWait(driver, 3).until(EC.staleness_of(zoom))
    #             except Exception:
    #                 logging.warning(f"Erro ao clicar no zoom PIX {url}")
    #         driver.save_screenshot(path)
    #         #logging.info(f"Screenshot salvo: {path}")

    # Capturar screenshots
    capturar_screenshot(
        "https://grafana-monitoring-hml-grafana-monitoring-hml.apps.svs.adiq.local/d/ee9atfdxwhg5cf/visao-geral-transacional-fisico-sniffer-dxc?orgId=1&from=now-30m&to=now&refresh=5s",
        "img/fisico.png"
        
    )
    capturar_screenshot(
        "https://grafana-monitoring-hml-grafana-monitoring-hml.apps.svs.adiq.local/d/fe97u788lyneob/visao-geral-transacional-e-commerce?from=now-1h&to=now&orgId=1&refresh=5s",
        "img/ecommerce.png"
    )
    capturar_screenshot(
        "https://grafana-ocp4.adiq.io/d/uAoTFkJMzr/monitoracao-arquivos-geral-ambiente-de-prd?orgId=1&from=now-1h&to=now&refresh=10s",
        "img/arquivos.png"
    )
    capturar_screenshot(
        "https://adqtrjvpkbn01.adiq.local:5601/app/dashboards#/view/3cf45840-2021-11ee-a5b4-81e7ec0febaf?_g=(filters:!(),refreshInterval:(pause:!t,value:60000),time:(from:now-1h,to:now))",
        "img/banese.png",
        wait_time=8
    )
    capturar_screenshot(
        "https://grafana-monitoring-hml-grafana-monitoring-hml.apps.svs.adiq.local/d/eeie77hr8msxsf/4442ba7d-ef52-5118-988d-71a7dd3f9a5a?orgId=1&refresh=1m",
        "img/unificada.png",
        
    )
    capturar_screenshot(
        "https://adqtrjvpkbn01.adiq.local:5601/app/dashboards#/view/73b07c60-2395-11ef-a2fe-31640ea6f96c?_g=(filters:!(),refreshInterval:(pause:!f,value:10000),time:(from:now-24h%2Fh,to:now))",
        "img/softpass.png",
        wait_time=8
    )
    capturar_screenshot(
        px,
        "img/pix.png",
        click_xpath="//span[contains(@class, 'css-1riaxdn') and contains(text(), 'Zoom to data')]"
    )
    capturar_screenshot(
        "http://radar.adiq.local/zabbix/zabbix.php?action=dashboard.view",
        "img/zabbix.png"
    )
    capturar_screenshot(
        "https://dashboard.uptimerobot.com/monitors",
        "img/uptime.png"
    )
  
    ######################################################################################################### TEAMS

    # 🔹 Acessar o Microsoft Teams Web
    teams_url = "https://teams.microsoft.com/"
    driver.get(teams_url)
    time.sleep(7)  # Tempo para login manual
    grupo = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@id='title-chat-list-item_19:0c84d034ef6f47f6a962f8935761172a@thread.v2']"))
        )
    #driver.find_element(By.XPATH, '//span[@title="Checklist Adiq / Kalendae"]')
    grupo.click()

    teste = driver.find_element(By.XPATH, '//button[@name="expand-compose"]')
    teste.click()

    sos_emoji = "\U0001F198"  # Emoji SOS 🆘
    # 🔹 Enviar mensagem no Teams
    try:

        # Aguarda o campo de texto
        time.sleep(1)
        chat_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"]')
        chat_box.click()
        time.sleep(1)
        

        # Digitar a mensagem
        texto = f"""
{mensagem}

{t_fisico}
{t_ecommerce}
{t_unificada}
{t_banese}
{t_spftpass}
{t_pix}
{t_atquivos}
{t_zabbix}
{t_uptime}
        """

        chat_box.send_keys(texto)
        chat_box.send_keys(Keys.SHIFT + Keys.RETURN)
        Legenda = f"""
Legenda:
✅ Ambiente OK
{sos_emoji} Incidente em Andamento

"""
        pyperclip.copy(Legenda)
        chat_box.send_keys(Keys.CONTROL + 'v')  # Cola o emoji
        chat_box.send_keys(Keys.SHIFT + Keys.RETURN)  # Pressiona enter para enviar tudo de uma vez

        # 🔹 Função para copiar a imagem para a área de transferência e colar no chat
        def copiar_e_enviar_imagem(caminho_imagem, chat_texto):
            chat_box.send_keys(chat_texto)
            chat_box.send_keys(Keys.SHIFT + Keys.RETURN)
            
            # Abrir a imagem
            imagem = Image.open(caminho_imagem)
            output = io.BytesIO()
            imagem.save(output, format="BMP")
            data = output.getvalue()[14:]  # Remove os primeiros bytes do cabeçalho BMP
            output.close()

            # Copiar a imagem para a área de transferência
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
            win32clipboard.CloseClipboard()

            #print(f"✅ Screenshot '{caminho_imagem}' copiado para a área de transferência!")

            # Colar no chat e enviar
            action = ActionChains(driver)
            action.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
            
            chat_box.send_keys(Keys.SHIFT + Keys.RETURN)
            chat_box.send_keys(Keys.SHIFT + Keys.RETURN)

        # 🔹 Chamadas para cada imagem
        copiar_e_enviar_imagem("img/fisico.png", t_fisico)
        copiar_e_enviar_imagem("img/ecommerce.png", t_ecommerce)
        copiar_e_enviar_imagem("img/unificada.png", t_unificada)
        copiar_e_enviar_imagem("img/banese.png", t_banese)
        copiar_e_enviar_imagem("img/softpass.png", t_spftpass)
        copiar_e_enviar_imagem("img/pix.png", t_pix)
        copiar_e_enviar_imagem("img/arquivos.png", t_atquivos)
        copiar_e_enviar_imagem("img/zabbix.png", t_zabbix)
        copiar_e_enviar_imagem("img/uptime.png", t_uptime)

        logging.warning("#CHECKLIST - Mensagem e imagem enviadas no Teams!")
        show_checkmark("remember to send the checklist")

    except Exception as e:
        messagebox.showerror(f"❌ Erro ao enviar mensagem e imagem: {e}")
        logging.warning(f"❌ Erro ao enviar mensagem e imagem: {e}")

def pix():
    data_hora = datetime.now()
    if data_hora.minute > 10:
        data_hora = data_hora.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    else:
        data_hora = data_hora.replace(minute=0, second=0, microsecond=0)

    data_url = data_hora.strftime("%Y-%m-%d")

    px = f"https://grafana-ocp4.adiq.io/d/f5067f59-9f90-4e0f-b86c-8c2ba32fc3a8/monitor-pix-gw-bancario-geral?orgId=1&from=1740997996000&to=1741040658000&var-dataselecionada={data_url}"

    capturar_screenshot(
        "https://grafana-monitoring-hml-grafana-monitoring-hml.apps.svs.adiq.local/d/fekpaesnn26f4b/monitoria-pix-rotina?orgId=1&refresh=5s",
        "img/pix_prd.png"
    )
    capturar_screenshot(
        "https://adqtrjvpkbn01.adiq.local:5601/app/dashboards#/view/258de11b-8b70-4481-a058-e08ea1277df2?_g=(filters:!(),refreshInterval:(pause:!t,value:60000),time:(from:now-1h,to:now))",
        "img/pix_status.png",
        wait_time=8
    )
    capturar_screenshot(
        px,
        "img/pix.png",
        click_xpath="//span[contains(@class, 'css-1riaxdn') and contains(text(), 'Zoom to data')]"
    )
    
    # 🔹 Acessar o Microsoft Teams Web
    teams_url = "https://teams.microsoft.com/"
    driver.get(teams_url)
    time.sleep(7)  # Tempo para login manual
    grupo = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@id='title-chat-list-item_19:61690aabe8554ab48105cbb42f22f7a1@thread.v2']"))
        )
    
    #driver.find_element(By.XPATH, '//span[@title="Checklist Adiq / Kalendae"]')
    grupo.click()

    teste = driver.find_element(By.XPATH, '//button[@name="expand-compose"]')
    teste.click()

    # 🔹 Enviar mensagem no Teams
    try:

        # Aguarda o campo de texto
        time.sleep(1)
        chat_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"]')
        chat_box.click()
        time.sleep(1)
        
        def copiar_e_enviar_imagem(caminho_imagem, chat_texto):
            action = ActionChains(driver)
            action.key_down(Keys.CONTROL).send_keys('b').key_up(Keys.CONTROL).perform()
            chat_box.send_keys(chat_texto)
            action = ActionChains(driver)
            action.key_down(Keys.CONTROL).send_keys('b').key_up(Keys.CONTROL).perform()
            chat_box.send_keys(Keys.SHIFT + Keys.RETURN)
            

                # Abrir a imagem
            imagem = Image.open(caminho_imagem)
            output = io.BytesIO()
            imagem.save(output, format="BMP")
            data = output.getvalue()[14:]  # Remove os primeiros bytes do cabeçalho BMP
            output.close()

                # Copiar a imagem para a área de transferência
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
            win32clipboard.CloseClipboard()

            #print(f"✅ Screenshot '{caminho_imagem}' copiado para a área de transferência!")

            # Colar no chat e enviar
            action = ActionChains(driver)
            action.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

            chat_box.send_keys(Keys.SHIFT + Keys.RETURN)
            chat_box.send_keys(Keys.SHIFT + Keys.RETURN)
            
        
        copiar_e_enviar_imagem("img/pix.png", "ACC INFORMA:")
        copiar_e_enviar_imagem("img/pix_prd.png", "Monitoria PIX - Rotina")
        copiar_e_enviar_imagem("img/pix_status.png", "STATUS Erro 500 - PIX")

        sleep(3)
        enviar = driver.find_element(By.XPATH, '//button[@title="Enviar (Ctrl+Enter)" and @name="send"]')
        enviar.click()
        logging.warning("#PIX - Mensagem e imagem enviadas no Teams!")
    except Exception as e:
        messagebox.showerror(f"❌ Erro ao enviar mensagem e imagem: {e}")
        logging.warning(f"❌ Erro ao enviar mensagem e imagem: {e}")

def comparativo(): 
    hoje = datetime.today()

    # Obter a data de 7 dias atrás
    data_7_dias_atras = hoje - timedelta(days=7)
    

    # Definir o horário inicial para T03:00:00 (meia-noite UTC de 7 dias atrás)
    hora_inicio = data_7_dias_atras.replace(hour=3, minute=0, second=0, microsecond=0)
    
    # Obter o horário atual
    hora_atual = hoje - timedelta(days=7)
    
    # Definir a hora de fim (hora_fim será ajustada conforme a hora_atual)
    if hora_atual.hour >= 20  and hora_atual.hour < 21:
        # Se for após 20:00, o fim será arredondado para 23:30 no mesmo dia
        hora_fim = hora_atual.replace(hour=23, minute=30, second=0, microsecond=0)
        # Se a hora atual for após 23:30, então o fim será no próximo dia às 03:00 UTC
        if hora_atual >= hora_fim:
            hora_fim = (hoje + timedelta(days=-6)).replace(hour=3, minute=0, second=0, microsecond=0)
    elif hora_atual.hour >= 23:
        # Se o horário atual for após 23:00, ajustar para o próximo dia às 03:00
        hora_fim = (hoje + timedelta(days=-6)).replace(hour=2, minute=30, second=0, microsecond=0)
    elif hora_atual.hour >= 8:
        # Se for 05:00, ajusta para 06:00 do mesmo dia
        hora_fim = hora_atual.replace(hour=11, minute=30, second=0, microsecond=0)
    elif hora_atual.hour >= 12:
        # Se for 05:00, ajusta para 06:00 do mesmo dia
        hora_fim = hora_atual.replace(hour=15, minute=30, second=0, microsecond=0)
    elif hora_atual.hour >= 16:
        # Se for 05:00, ajusta para 06:00 do mesmo dia
        hora_fim = hora_atual.replace(hour=19, minute=30, second=0, microsecond=0)    
    else:
        # Caso contrário, o fim será no mesmo dia, mas arredondado para o próximo múltiplo de 30 minutos
        minutos = (hora_atual.minute // 30) * 30
        if hora_atual.minute % 30 != 0:
            minutos += 30
        hora_fim = hora_atual.replace(minute=minutos, second=0, microsecond=0)
    
    # Formatar como string no formato que você precisa para a URL
    hora_inicio_str = hora_inicio.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    hora_fim_str = hora_fim.strftime('%Y-%m-%dT%H:%M:%S.000Z')

    # Exibir resultados
    print(f"hora_inicio: {hora_inicio_str}")
    print(f"hora_fim: {hora_fim_str}")

    # Exibir o resultado
    print(f"from:'{hora_inicio_str}',to:'{hora_fim_str}'")

    cecomerce = f"https://adqtrjvpkbn01.adiq.local:5601/app/dashboards#/view/b959fda0-d0d8-11ee-b2b0-07a2f1811222?_g=(filters:!(),refreshInterval:(pause:!t,value:60000),time:(from:'{hora_inicio_str}',to:'{hora_fim_str}'))"
    cfisicos = f"https://adqtrjvpkbn01.adiq.local:5601/app/dashboards#/view/8eb71160-1b5f-11ef-bc95-f133a691effe?_g=(filters:!(),refreshInterval:(pause:!t,value:60000),time:(from:'{hora_inicio_str}',to:'{hora_fim_str}'))"

    print(f"CEcomerce URL: {cecomerce}")
    print(f"CFisicos URL: {cfisicos}")

    # def capturar_screenshot(url, path, wait_time=10):
    #     driver.get(url)
    #     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    #     time.sleep(wait_time)
    #     driver.save_screenshot(path)

    capturar_screenshot(
        cecomerce,
        "img/cecommerce.png",
        wait_time=10
    )

    capturar_screenshot(
        cfisicos,
        "img/cfisico.png",
        wait_time=10
    )


    # 🔹 Acessar o Microsoft Teams Web
    teams_url = "https://teams.microsoft.com/"
    driver.get(teams_url)
    time.sleep(7)  # Tempo para login manual

    grupo = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@id='title-chat-list-item_19:43975b8185a94f76a78f370d9d332bdb@thread.v2']"))
        )
    
    #driver.find_element(By.XPATH, '//span[@title="Checklist Adiq / Kalendae"]')
    grupo.click()

    teste = driver.find_element(By.XPATH, '//button[@name="expand-compose"]')
    teste.click()

    # 🔹 Enviar mensagem no Teams
    try:

        # Aguarda o campo de texto
        time.sleep(1)
        chat_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"]')
        chat_box.click()
        time.sleep(1)

        action = ActionChains(driver)
        action.key_down(Keys.CONTROL).send_keys('b').key_up(Keys.CONTROL).perform()
        chat_box.send_keys("ACC INFORMA")
        action = ActionChains(driver)
        action.key_down(Keys.CONTROL).send_keys('b').key_up(Keys.CONTROL).perform()
        chat_box.send_keys(Keys.SHIFT + Keys.RETURN)
        chat_box.send_keys(Keys.SHIFT + Keys.RETURN)
        time.sleep(1)
        
        def copiar_e_enviar_imagem(caminho_imagem, chat_texto):
            action = ActionChains(driver)
            action.key_down(Keys.CONTROL).send_keys('b').key_up(Keys.CONTROL).perform()
            chat_box.send_keys(chat_texto)
            action = ActionChains(driver)
            action.key_down(Keys.CONTROL).send_keys('b').key_up(Keys.CONTROL).perform()
            chat_box.send_keys(Keys.SHIFT + Keys.RETURN)

                # Abrir a imagem
            imagem = Image.open(caminho_imagem)
            output = io.BytesIO()
            imagem.save(output, format="BMP")
            data = output.getvalue()[14:]  # Remove os primeiros bytes do cabeçalho BMP
            output.close()

                # Copiar a imagem para a área de transferência
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
            win32clipboard.CloseClipboard()

            #print(f"✅ Screenshot '{caminho_imagem}' copiado para a área de transferência!")
            # Colar no chat e enviar
            action = ActionChains(driver)
            action.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
            
            chat_box.send_keys(Keys.SHIFT + Keys.RETURN)
            chat_box.send_keys(Keys.SHIFT + Keys.RETURN)
        
        copiar_e_enviar_imagem("img/cfisico.png", "Físico:")
        copiar_e_enviar_imagem("img/cecommerce.png", "E-commerce:")

        sleep(3)
        
        enviar = driver.find_element(By.XPATH, '//button[@title="Enviar (Ctrl+Enter)" and @name="send"]')
        enviar.click()
        logging.warning("#COMPARATIVO - Mensagem e imagem enviadas no Teams!")
    except Exception as e:
        messagebox.showerror(f"❌ Erro ao enviar mensagem e imagem: {e}")
        logging.warning(f"❌ Erro ao enviar mensagem e imagem: {e}")

def adiqPlus():
    # Obter data e hora de hoje
    hoje = datetime.today()
    hora_atual = datetime.now()

    # Definir o horário inicial
    hora_inicio = hoje.replace(hour=3, minute=0, second=0, microsecond=0)

    # Definir a hora de fim de acordo com o intervalo
    if hora_atual.hour >= 20:
        hora_fim = hora_atual.replace(hour=23, minute=30, second=0, microsecond=0)
        if hora_atual >= hora_fim:
            hora_fim = (hoje + timedelta(days=1)).replace(hour=3, minute=0, second=0, microsecond=0)
    elif hora_atual.hour >= 23:
        hora_fim = (hoje + timedelta(days=1)).replace(hour=3, minute=30, second=0, microsecond=0)
    elif hora_atual.hour >= 16:
        hora_fim = hora_atual.replace(hour=19, minute=30, second=0, microsecond=0)
    elif hora_atual.hour >= 12:
        hora_fim = hora_atual.replace(hour=15, minute=30, second=0, microsecond=0)
    elif hora_atual.hour >= 8:
        hora_fim = hora_atual.replace(hour=11, minute=30, second=0, microsecond=0)
    else:
        minutos = (hora_atual.minute // 30) * 30
        if hora_atual.minute % 30 != 0:
            minutos += 30
        hora_fim = hora_atual.replace(minute=minutos, second=0, microsecond=0)

    # Formatar datas
    hora_inicio_str = hora_inicio.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    hora_fim_str = hora_fim.strftime('%Y-%m-%dT%H:%M:%S.000Z')

    # URLs dinâmicas com intervalo
    net = f"https://adqtrjvpkbn01.adiq.local:5601/app/dashboards#/view/3dbdd3a0-0884-11ee-bd3d-d543ccf9c199?_g=(filters:!(),refreshInterval:(pause:!t,value:60000),time:(from:'{hora_inicio_str}',to:'{hora_fim_str}'))"
    sniffer = f"https://adqtrjvpkbn01.adiq.local:5601/app/dashboards#/view/0d97d310-9aa1-11ee-bdd8-a3ff6f253f69?_g=(filters:!(),refreshInterval:(pause:!t,value:60000),time:(from:'{hora_inicio_str}',to:'{hora_fim_str}'))"

    # Capturas usando a função com foco e corte da barra
    capturar_screenshot(url=net, path="img/wtnet.png", wait_time=10)
    capturar_screenshot(url=sniffer, path="img/snifferprd.png", wait_time=10)

    # 🔹 Acessar o Microsoft Teams Web
    teams_url = "https://teams.microsoft.com/"
    driver.get(teams_url)
    time.sleep(7)  # Tempo para login manual

    grupo = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@id='title-chat-list-item_19:4487e86e8e574b8dbeff3e607b5eeb18@thread.v2']"))
        )
    
    #driver.find_element(By.XPATH, '//span[@title="Checklist Adiq / Kalendae"]')
    grupo.click()

    teste = driver.find_element(By.XPATH, '//button[@name="expand-compose"]')
    teste.click()

    # 🔹 Enviar mensagem no Teams
    try:

        # Aguarda o campo de texto
        time.sleep(1)
        chat_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"]')
        chat_box.click()
        time.sleep(1)

        action = ActionChains(driver)
        action.key_down(Keys.CONTROL).send_keys('b').key_up(Keys.CONTROL).perform()
        chat_box.send_keys("ACC INFORMA:")
        action = ActionChains(driver)
        action.key_down(Keys.CONTROL).send_keys('b').key_up(Keys.CONTROL).perform()
        chat_box.send_keys(Keys.SHIFT + Keys.RETURN)
        chat_box.send_keys(Keys.SHIFT + Keys.RETURN)
        time.sleep(1)
        
        def copiar_e_enviar_imagem(caminho_imagem, chat_texto):
            action = ActionChains(driver)
            action.key_down(Keys.CONTROL).send_keys('b').key_up(Keys.CONTROL).perform()
            chat_box.send_keys(chat_texto)
            action = ActionChains(driver)
            action.key_down(Keys.CONTROL).send_keys('b').key_up(Keys.CONTROL).perform()
            chat_box.send_keys(Keys.SHIFT + Keys.RETURN)

                # Abrir a imagem
            imagem = Image.open(caminho_imagem)
            output = io.BytesIO()
            imagem.save(output, format="BMP")
            data = output.getvalue()[14:]  # Remove os primeiros bytes do cabeçalho BMP
            output.close()

                # Copiar a imagem para a área de transferência
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
            win32clipboard.CloseClipboard()

            #print(f"✅ Screenshot '{caminho_imagem}' copiado para a área de transferência!")

            # Colar no chat e enviar
            action = ActionChains(driver)
            action.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
            
            chat_box.send_keys(Keys.SHIFT + Keys.RETURN)
            chat_box.send_keys(Keys.SHIFT + Keys.RETURN)
        
        copiar_e_enviar_imagem("img/wtnet.png", "Origem WTnet:")
        copiar_e_enviar_imagem("img/snifferprd.png", "Eagle Sniffer (PRD):")

        sleep(3)
        enviar = driver.find_element(By.XPATH, '//button[@title="Enviar (Ctrl+Enter)" and @name="send"]')
        enviar.click()
        logging.warning("#ADIQ+ - Mensagem e imagem enviadas no Teams!")
    except Exception as e:
        messagebox.showerror(f"❌ Erro ao enviar mensagem e imagem: {e}")
        logging.warning(f"❌ Erro ao enviar mensagem e imagem: {e}")

def tarefa5():
    print("Tarefa 3 realizada!")

# Frame do checklist
frame_checklist = ctk.CTkFrame(frame_main, fg_color="gray20", corner_radius=10)

label_checklist = ctk.CTkLabel(frame_checklist, text="Checklist", font=("Arial", 24, "bold"))
label_checklist.pack(pady=10)

# Checkboxes com variáveis para verificar o estado
checkbox_var1 = ctk.BooleanVar()
checkbox_var2 = ctk.BooleanVar()
checkbox_var3 = ctk.BooleanVar()
checkbox_var4 = ctk.BooleanVar()
checkbox_var5 = ctk.BooleanVar()

checkbox1 = ctk.CTkCheckBox(frame_checklist, text="Checklist", variable=checkbox_var1)
checkbox1.pack(pady=5)
checkbox2 = ctk.CTkCheckBox(frame_checklist, text="Pix", variable=checkbox_var2)
checkbox2.pack(pady=5)
checkbox3 = ctk.CTkCheckBox(frame_checklist, text="Comparativo", variable=checkbox_var3)
checkbox3.pack(pady=5)
checkbox4 = ctk.CTkCheckBox(frame_checklist, text="Adiq+", variable=checkbox_var4)
checkbox4.pack(pady=5)
#checkbox5 = ctk.CTkCheckBox(frame_checklist, text="Farol (EM CONSTRUÇÃO)", variable=checkbox_var5)
#checkbox5.pack(pady=5)

# Função para executar as tarefas associadas aos itens marcados
try:
    def executar_tarefas():
        if checkbox_var1.get():
            try:
                checklist()
                sleep(5)
            except:
                show_error()
        if checkbox_var2.get():
            try:
                pix()
                sleep(5)
            except:
                show_error()
        if checkbox_var3.get():
            try:
                comparativo()
                sleep(5)
            except:
                show_error()
        if checkbox_var4.get():
            try:
                adiqPlus()
                sleep(5)
            except:
                show_error()
        if checkbox_var5.get():
            tarefa5()
except:
    show_error()
        
# Botão dentro do checklist para rodar as funções
btn_executar_checklist = ctk.CTkButton(frame_checklist, text="Executar Tarefas", command=executar_tarefas)
btn_executar_checklist.pack(pady=20)

# =========================================  MENU LUA ================================================

# Frame inicial
frame_home = ctk.CTkFrame(frame_main)

label_home = ctk.CTkLabel(frame_home, text="Manual - LUA ", font=("Arial", 24, "bold"))
label_home.pack(pady=10)

# Manual de instruções (em uma string longa, por exemplo)
manual_text = """
Bem-vindo ao Manual de Instruções - Lua!

Olá! Eu sou a Lua, sua assistente virtual, e fui criada para facilitar suas tarefas do dia a dia. 😊

Abaixo estão os principais botões e suas funcionalidades:

HOME:
Aqui você encontra todas as instruções gerais para navegar pelo sistema e tirar dúvidas. Se precisar de algo, esse é o ponto de partida! 🏠

CHECKLIST:
Acesso rápido a alguns dos principais checklists. Para enviar um checklist para o Teams, basta preencher o que deseja e enviar diretamente no aplicativo. 

    * Checklist Time: 2m10s
    * Adiq+: 40s
    * Comparativo: 40s
    * PIX: 20s

É só escolher o checklist e enviar rapidamente. ⏱️

WHATSAPP:

    * Envio de mensagens para o grupo BS2 - Checklist - TI diretamente pelo sistema. 📲

    Legenda:
    ✅ - Tudo OK
    🔄 - Dentro da janela
    ❌ - Não recebido
    ⚠ - Atraso / Eventos
    🚫 - Sem movimentação

FECHAMENTO PIX:
Extração de informações a partir de arquivos CSV.

    * Insira o arquivo CSV baixado do Elastic e clique em "Processar".

    * Após isso, basta copiar as informações. (Tempo estimado: 2s)

Notas Importantes:

    * Certifique-se de estar logado no Chrome correto antes de iniciar .

    * 

    * Quando for executar o código, lembre-se de clicar na tela do Chrome para garantir que tudo ocorra sem problemas.

    * Caso encontre algum erro, reinicie a aplicação e tente novamente.

Agradecemos por utilizar nosso sistema! Qualquer dúvida, estou aqui para ajudar. 😄
"""

# Adicionando a área de texto com rolagem
text_frame = ctk.CTkFrame(frame_home)
text_frame.pack(pady=20, padx=20)

# Criar o widget de rolagem
scrollbar = ctk.CTkScrollbar(text_frame)
scrollbar.pack(side="right", fill="y")

# Criar o widget de TextBox
text_box = ctk.CTkTextbox(text_frame, wrap="word", height=700, width=700, font=("Arial", 16))
text_box.pack(side="left", fill="both", expand=True)

# Inserir o texto no TextBox
text_box.insert("1.0", manual_text)

# Exibir o frame inicial por padrão
mostrar_frame(frame_home)

# ================================ WHATSAPP ======================================================

# frame whatsapp
data_hora = datetime.now()

# Arredondando o horário
if data_hora.minute > 30:
    data_hora = data_hora.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
else:
    data_hora = data_hora.replace(minute=0, second=0, microsecond=0)

# Formatando a data e hora no formato desejado
data_formatada = data_hora.strftime("%d/%m")

# Criando a string com a data e hora arredondada
aa = f'🔊 *BS2 PAYMENTS. {data_formatada}*\n'

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
label_whatsapp = ctk.CTkLabel(frame_whatsapp, text="BS2 - Checklist - TI", font=("Arial", 24, "bold"))
label_whatsapp.pack(pady=10)

# Scrollable Frame para adicionar os checkboxes
scrollable_frame = ctk.CTkScrollableFrame(frame_whatsapp, width=500, height=200, corner_radius=10)
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

    nome_grupo = "BS2 - Checklist - TI"  # Defina o nome do grupo que você deseja buscar no WhatsApp Web
    #nome_grupo = "Lucas ACC"

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
        logging.warning("Mensagem Enviada", "A mensagem foi enviada com sucesso!")

    except Exception as e:
        messagebox.showinfo("Erro", f"Não foi possível encontrar o grupo: {nome_grupo}. Erro: {e}")
        print(f"Erro", f"Não foi possível encontrar o grupo: {nome_grupo}. Erro: {e}")
        logging.warning("Erro", f"Não foi possível encontrar o grupo: {nome_grupo}. Erro: {e}")
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
btn_enviar_mensagens.pack(pady=10)

# Botão dentro do checklist para abrir a tela de alteração
btn_alterar_checklist = ctk.CTkButton(frame_whatsapp, text="Alterar Mensagens", command=alterar_icone_na_tela)
btn_alterar_checklist.pack(pady=10)

selected_file = None  # Variável para armazenar o caminho do arquivo

# =========================== PROCESSAMENTO PIX =====================================

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
            result_text.delete(1.0, "end")  # Limpa o conteúdo atual
            result_text.insert("end", formatted_error_summary.strip())  # Insere o novo conteúdo na caixa de texto
            
            # Exibir também no terminal
            print("\nResumo dos erros:")
            print(formatted_error_summary)
            
            messagebox.showinfo("Sucesso", "Arquivo processado com sucesso!")
            logging.warning("Sucesso", "Arquivo processado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao processar o arquivo:\n{str(e)}")
            logging.warning("Erro", f"Erro ao processar o arquivo:\n{str(e)}")
    else:
        messagebox.showwarning("Aviso", "Nenhum arquivo selecionado.")

# Função para copiar o conteúdo da caixa de texto para a área de transferência
def copiar_resultado():
    resultado = result_text.get(1.0, "end-1c")  # Obtém o texto da caixa de texto
    app.clipboard_clear()  # Limpa a área de transferência
    app.clipboard_append(resultado)  # Adiciona o conteúdo à área de transferência
    app.update()  # Atualiza a área de transferência
    messagebox.showinfo("Sucesso", "Conteúdo copiado para a área de transferência!")  # Exibe confirmação

# frame Fechamento Pix
frame_pix_fechamento = ctk.CTkFrame(frame_main, fg_color="gray20", corner_radius=10)

label_pix_fechamento = ctk.CTkLabel(frame_pix_fechamento, text="Fechamento Pix", font=("Arial", 24, "bold"))
label_pix_fechamento.pack(pady=10)

# Botão de upload
button_upload = ctk.CTkButton(frame_pix_fechamento, text="Upload File", command=upload_file)
button_upload.pack(pady=10)

# Label que mostra o caminho do arquivo
label_file = ctk.CTkLabel(frame_pix_fechamento, text="Nenhum arquivo selecionado", wraplength=500)
label_file.pack(pady=10)

# Botão para processar o arquivo (inicia desativado)
button_process = ctk.CTkButton(frame_pix_fechamento, text="Processar Arquivo", command=process_file, state="disabled")
button_process.pack(pady=10)

# Botão para copiar o conteúdo da caixa de texto
button_copy = ctk.CTkButton(frame_pix_fechamento, text="Copiar Resultados", command=copiar_resultado)
button_copy.pack(pady=10)

# Label para exibir os resultados
# Caixa de texto rolável para exibir os resultados
result_text = ctk.CTkTextbox(frame_pix_fechamento, height=200, width=700)  # Caixa de texto com rolagem
result_text.pack(pady=10)

# ========================== ARQUIVOS RECEBIDOS DA FROG =============================================

frame_frog = ctk.CTkFrame(frame_main)

label_titulo = ctk.CTkLabel(frame_frog, text="Monitoramento de Arquivos - Frog Pay", font=("Arial", 24, "bold"))
label_titulo.pack(pady=20)

# Caminho da pasta
folder_path = Path(r"\\adqtspvpfs01\appfiles\Adquirencia\Legados\Sub\FP\Entrada\ENV_OK_FP")

tipos = {
    'Antecipação': 'A',
    'Debito': 'D',
    'Credito': 'C'
}

entry_refs = {}

for nome, sigla in tipos.items():
    label = ctk.CTkLabel(frame_frog, text=f"{nome}:", anchor="w", font=("Arial", 14))
    label.pack(pady=(5, 0), anchor="w", padx=20)

    entry = ctk.CTkEntry(frame_frog, width=500)
    entry.pack(pady=5, padx=20)
    entry.configure(state="disabled")
    entry_refs[sigla] = entry

# ========== FUNÇÃO DE CONTAGEM ==========
def atualizar_contagem():
    hoje = datetime.now().strftime("%Y%m%d")
    for tipo, sigla in tipos.items():
        pattern = f"ADQ001_{sigla}_FP_{hoje}_*_*.txt"
        try:
            count = len(list(folder_path.glob(pattern)))
            entry = entry_refs[sigla]
            entry.configure(state="normal")
            entry.delete(0, 'end')
            entry.insert(0, f"{count} arquivo(s)")
            entry.configure(state="disabled")
        except Exception:
            entry = entry_refs[sigla]
            entry.configure(state="normal")
            entry.delete(0, 'end')
            entry.insert(0, "Erro ao acessar")
            entry.configure(state="disabled")

# ========== MONITORAMENTO ==========
class NovoArquivoHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith(".txt"):
            time.sleep(0.5)
            app.after(100, atualizar_contagem)

def iniciar_monitoramento():
    event_handler = NovoArquivoHandler()
    observer = Observer()
    observer.schedule(event_handler, str(folder_path), recursive=False)
    observer.start()
    return observer

observer = iniciar_monitoramento()

# Botão para atualizar manualmente
btn_frog = ctk.CTkButton(frame_frog, text="Frog Pay", command=atualizar_contagem)
btn_frog.pack(pady=20)


# ================= Frame da aba ==================
frame_mover_arquivos = ctk.CTkFrame(frame_main)

# ================= Dados dos caminhos ==================
BANDEIRAS = {
    "Mastercard": {
        "origem": [Path(r"\\adqtspvpfs01\Integracao\Connect\MASTERCARD\RECEBE\BACKUP")],
        "destino": Path.home() / "Banco BS2/Externo_Adiq_BS2 - Projeto CMM/Mastercard",
        "mascaras": ["PRD_MST_T140_D{0}.*_A001", "PRD_MST_T140_D{0}.*_A002", "PRD_MST_T140_D{0}.*_A003"]
    },
    "Hipercard": {
        "origem": [Path(r"\\adqtspvpfs01\Integracao\Connect\MASTERCARD\RECEBE")],
        "destino": Path.home() / "Banco BS2/Externo_Adiq_BS2 - Projeto CMM/Hipercard",
        "mascaras": ["PRD_HIP_T140_D{0}.*_A001", "PRD_HIP_T140_D{0}.*_A002", "PRD_HIP_T140_D{0}.*_A003"]
    },
    "Elo": {
        "origem": [
            Path(r"\\adqtspvpfs01\Integracao\Connect\ELO\RECEBE"),
            Path(r"\\adqtspvpfs01\Integracao\Connect\ELO\RECEBE\BACKUP")
        ],
        "destino": Path.home() / "Banco BS2/Externo_Adiq_BS2 - Projeto CMM/ELO",
        "mascaras": [
            "AGECRED_C_5190_{0}_*.TXT", "AGECRED_D_5190_{0}_*.TXT",
            "AGECRED_C_5030_{0}_*.TXT", "AGECRED_D_5030_{0}_*.TXT"
        ]
    },
    "Amex": {
        "origem": [Path(r"\\adqtspvpfs01\appfiles\PAC_PRD\INCOMING\AMEX")],
        "destino": Path.home() / "Banco BS2/Externo_Adiq_BS2 - Projeto CMM/AMEX/AMEX-INCOMING",
        "mascaras": []
    }
}

# ================= Variáveis globais ==================
copied_files = []
arquivos_para_copiar = {}
log_path = ""
stop_process = False


# ================= Funções ==================

def log(mensagem):
    if log_path:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {mensagem}\n")


def add_status(text):
    text_status.configure(state="normal")
    text_status.insert("end", text + "\n")
    text_status.see("end")
    text_status.configure(state="disabled")


log_path = None  # variável global

def selecionar_log():
    global log_path

    # ✅ Caminho fixo informado por você
    log_dir = r"C:\Users\ADQT0141\OneDrive - Banco BS2\Área de Trabalho\Lua"

    # ✅ Garante que a pasta exista
    os.makedirs(log_dir, exist_ok=True)

    # ✅ Nome automático com timestamp
    log_filename = f"CopiaArquivos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    log_path = os.path.join(log_dir, log_filename)

    # ✅ Cria o log com a primeira entrada
    log(f"Arquivo de log criado automaticamente em: {log_path}")



def verificar_arquivos():
    arquivos_para_copiar.clear()
    text_status.configure(state="normal")
    text_status.delete("1.0", "end")
    add_status("Iniciando verificação de arquivos...")
    log("=== Início da verificação ===")

    hoje_yyMMdd = datetime.now().strftime('%y%m%d')
    hoje_yyyMMdd = datetime.now().strftime('%Y%m%d')

    for nome, dados in BANDEIRAS.items():
        if not chk_bandeiras[nome].get():
            continue

        arquivos = []

        for origem in dados['origem']:
            if nome == "Amex":
                data_pasta = (datetime.now() - timedelta(days=1)).strftime('%Y.%m.%d')
                pasta_origem = origem / data_pasta
                if pasta_origem.exists() and pasta_origem.is_dir():
                    arquivos_para_copiar[nome] = [pasta_origem]
                    msg = f"Pasta encontrada para {nome}: {pasta_origem}"
                else:
                    msg = f"Nenhuma pasta encontrada para {nome} com nome {data_pasta}."
                log(msg)
                add_status(msg)
            else:
                data_formatada = hoje_yyMMdd if nome in ["Hipercard", "Mastercard"] else hoje_yyyMMdd
                for mascara in dados['mascaras']:
                    padrao = mascara.format(data_formatada)
                    arquivos.extend(origem.glob(padrao))

        if arquivos:
            arquivos_para_copiar[nome] = arquivos
            msg = f"{len(arquivos)} arquivos encontrados para {nome}."
        else:
            msg = f"Nenhum arquivo encontrado para {nome}."
        log(msg)
        add_status(msg)

    log("=== Fim da verificação ===")
    add_status("Verificação concluída.")


def iniciar_copia():
    global stop_process
    stop_process = False
    copied_files.clear()

    total = sum(len(v) for v in arquivos_para_copiar.values())
    atual = 0

    for nome, itens in arquivos_para_copiar.items():
        destino = BANDEIRAS[nome]['destino']
        if not itens:
            continue
        if not messagebox.askyesno("Confirmação", f"Deseja copiar arquivos para {nome}?"):
            continue
        for item in itens:
            if stop_process:
                return
            try:
                destino.mkdir(parents=True, exist_ok=True)
                dest_path = destino / item.name
                if dest_path.exists():
                    msg = f"Arquivo ou pasta já existe e não será copiado: {dest_path}"
                    log(msg)
                    add_status(msg)
                    continue
                if item.is_dir():
                    shutil.copytree(item, dest_path)
                else:
                    shutil.copy2(item, dest_path)
                copied_files.append(dest_path)
                atual += 1
                msg = f"Copiado: {item}"
                log(msg)
                add_status(msg)
                barra_var.set(f"Progresso: {atual}/{total}")
                frame_mover_arquivos.update_idletasks()
            except Exception as e:
                log(f"Erro ao copiar {item}: {str(e)}")
                messagebox.showerror("Erro", f"Erro ao copiar {item}: {str(e)}")


def desfazer():
    if not copied_files:
        messagebox.showinfo("Info", "Nenhum arquivo para desfazer.")
        return
    if not messagebox.askyesno("Confirmação", "Deseja desfazer as cópias realizadas?"):
        return
    for f in copied_files:
        try:
            f.unlink()
            log(f"Removido no rollback: {f}")
        except Exception as e:
            log(f"Erro ao remover {f}: {str(e)}")
    copied_files.clear()
    add_status("Rollback executado: arquivos removidos.")
    messagebox.showinfo("Rollback", "Arquivos removidos com sucesso.")


# def parar():
#     global stop_process
#     stop_process = True
#     add_status("Processo interrompido pelo usuário.")
#     log("Processo interrompido pelo usuário.")


# ================= Layout ==================

# 👉 Área esquerda (botões + checklist)
frame_left = ctk.CTkFrame(frame_mover_arquivos)
frame_left.pack(side="left", fill="y", padx=10, pady=10)

btn_verificar = ctk.CTkButton(frame_left, text="Verificar Arquivos", command=lambda: [selecionar_log(), verificar_arquivos()])
btn_verificar.pack(pady=5, fill='x')

btn_iniciar = ctk.CTkButton(frame_left, text="Iniciar Cópia", command=iniciar_copia)
btn_iniciar.pack(pady=5, fill='x')

# btn_parar = ctk.CTkButton(frame_left, text="Parar Processo", command=parar)
# btn_parar.pack(pady=5, fill='x')

btn_desfazer = ctk.CTkButton(frame_left, text="Desfazer Cópia", command=desfazer)
btn_desfazer.pack(pady=5, fill='x')

chk_bandeiras = {nome: BooleanVar(value=True) for nome in BANDEIRAS}
for nome in chk_bandeiras:
    chk = ctk.CTkCheckBox(frame_left, text=nome, variable=chk_bandeiras[nome])
    chk.pack(anchor='w', pady=5)


# 👉 Área direita (status)
frame_right = ctk.CTkFrame(frame_mover_arquivos)
frame_right.pack(fill="both", expand=True, padx=10, pady=10)

text_status = ctk.CTkTextbox(frame_right, height=20, state='disabled')
text_status.pack(fill='both', expand=True)

barra_var = StringVar(value="Progresso: 0/0")
label_progress = ctk.CTkLabel(frame_mover_arquivos, textvariable=barra_var, font=("Consolas", 12))
label_progress.pack(side="bottom", fill="x", pady=5)

# Botões da sidebar
btn_home = ctk.CTkButton(frame_sidebar, text="Home", fg_color="gray30", hover_color="gray40", command=lambda: mostrar_frame(frame_home))
btn_home.pack(fill="x", pady=5, padx=10)

btn_checklist = ctk.CTkButton(frame_sidebar, text="CheckList", fg_color="gray30", hover_color="gray40", command=lambda: mostrar_frame(frame_checklist))
btn_checklist.pack(fill="x", pady=5, padx=10)

btn_whatsapp = ctk.CTkButton(frame_sidebar, text="WhatsApp", fg_color="gray30", hover_color="gray40", command=lambda: mostrar_frame(frame_whatsapp))
btn_whatsapp.pack(fill="x", pady=5, padx=10)

btn_pix_fechamento = ctk.CTkButton(frame_sidebar, text="Fechamento pix", fg_color="gray30", hover_color="gray40", command=lambda: mostrar_frame(frame_pix_fechamento))
btn_pix_fechamento.pack(fill="x", pady=5, padx=10)

btn_frog = ctk.CTkButton(frame_sidebar, text="Frog Pay", fg_color="gray30", hover_color="gray40", command=lambda: mostrar_frame(frame_frog))
btn_frog.pack(fill="x", pady=5, padx=10)


btn_mover_arquivos = ctk.CTkButton(frame_sidebar, text="Movimentação de arquivos ", fg_color="gray30", hover_color="gray40", command=lambda: mostrar_frame(frame_mover_arquivos))
btn_mover_arquivos.pack(fill="x", pady=5, padx=10)

# Botão do sistema
btn_system = ctk.CTkOptionMenu(frame_sidebar, values=["System"])
btn_system.pack(side="bottom", pady=10)

app.mainloop()