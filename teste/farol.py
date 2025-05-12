from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from PIL import Image
import pyautogui
import win32clipboard
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
import logging
import threading
import schedule
from PIL import ImageGrab

# 🔹 Configurar logging
logging.basicConfig(filename="app.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 🔹 Configurar o WebDriver
chrome_user_data_dir = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
 
options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "localhost:9222")
options.add_argument(f"user-data-dir={chrome_user_data_dir}")
 
# Iniciar WebDriver
driver = webdriver.Chrome(options=options)

# Função para reiniciar o WebDriver
def reiniciar_webdriver(driver):
    logging.info("Reiniciando WebDriver")
    try:
        driver.quit()
    except:
        pass
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "localhost:9222")
    options.add_argument(f"user-data-dir={chrome_user_data_dir}")
    new_driver = webdriver.Chrome(options=options)
    logging.info("WebDriver reiniciado com sucesso")
    return new_driver

# Verificar se o WebDriver está ativo
def verificar_webdriver(driver):
    try:
        driver.title
        return driver
    except:
        logging.warning("WebDriver inativo, reiniciando...")
        return reiniciar_webdriver(driver)

# Função para manter o sistema ativo
def manter_sistema_ativo():
    while True:
        pyautogui.moveRel(10, 10, duration=0.1)
        pyautogui.moveRel(-10, -10, duration=0.1)
        time.sleep(300)  # A cada 5 minutos

# Iniciar thread para evitar inatividade
threading.Thread(target=manter_sistema_ativo, daemon=True).start()

# Função para executar com retentativas
def executar_com_retries(funcao, max_tentativas=3, delay=5):
    for tentativa in range(max_tentativas):
        try:
            return funcao()
        except Exception as e:
            logging.error(f"Tentativa {tentativa + 1} falhou: {e}")
            time.sleep(delay)
    raise Exception(f"Falha após {max_tentativas} tentativas")

# Função para limpar screenshots
def limpar_screenshots():
    files = ["fisico.png", "ecommerce.png", "unificada.png", "banese.png", "softpass.png", "pix.png", "arquivos.png", "zabbix.png", "uptime.png", "cecommerce.png", "cfisico.png", "wtnet.png", "snifferprd.png"]
    for file in files:
        if os.path.exists(file):
            try:
                os.remove(file)
                logging.info(f"Screenshot {file} removido")
            except:
                logging.warning(f"Não foi possível remover {file}")

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

# Função para mostrar apenas o frame selecionado
def mostrar_frame(frame):
    for widget in frame_main.winfo_children():
        widget.pack_forget()
    frame.pack(fill="both", expand=True, padx=20, pady=20)

# Funções para serem chamadas
def checklist():
    global driver
    logging.info("Iniciando checklist")
    driver = verificar_webdriver(driver)
    
    # Obtendo a data e o horário atuais
    data_hora = datetime.now()
    if data_hora.minute > 30:
        data_hora = data_hora.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    else:
        data_hora = data_hora.replace(minute=0, second=0, microsecond=0)

    data_formatada = data_hora.strftime("%d/%m/%Y - %Hh%M")
    mensagem = f'ACC ADIQ: ⏰⏰ Checklist Ambientes {data_formatada}'
    data_url = data_hora.strftime("%Y-%m-%d")

    px = f"https://grafana-ocp4.adiq.io/d/f5067f59-9f90-4e0f-b86c-8c2ba32fc3a8/monitor-pix-gw-bancario-geral?orgId=1&from=1740997996000&to=1741040658000&var-dataselecionada={data_url}"
    
    t_fisico = "✅ [Transacional Físico](https://grafana-monitoring-hml-grafana-monitoring-hml.apps.svs.adiq.local/d/ee9atfdxwhg5cf/visao-geral-transacional-fisico-sniffer-dxc?orgId=1&from=now-30m&to=now&refresh=5s)"
    t_ecommerce = "✅ [Transacional E-commerce](https://grafana-monitoring-hml-grafana-monitoring-hml.apps.svs.adiq.local/d/fe97u788lyneob/visao-geral-transacional-e-commerce?from=now-1h&to=now&orgId=1&refresh=5s)"
    t_unificada = "✅ [Tela Unificada](https://adqtrjvpkbn01.adiq.local:5601/app/dashboards#/view/f1b3c7d4-22a4-4956-be94-1a8c6103d4d4)"
    t_banese = "✅ [Transacional Hub On-Us Banese](https://adqtrjvpkbn01.adiq.local:5601/app/dashboards#/view/3cf45840-2021-11ee-a5b4-81e7ec0febaf)"
    t_spftpass = "✅ [Transacional Softpass](https://adqtrjvpkbn01.adiq.local:5601/app/dashboards#/view/73b07c60-2395-11ef-a2fe-31640ea6f96c)"
    t_pix = "✅ [Transacional PIX](https://grafana-ocp4.adiq.io/d/f5067f59-9f90-4e0f-b86c-8c2ba32fc3a8/monitor-pix-gw-bancario-geral?orgId=1&from=1740997996000&to=1741040658000&var-dataselecionada=2025-03-07)"
    t_atquivos = "✅ [Grafana - Arquivos](https://grafana-ocp4.adiq.io/d/uAoTFkJMzr/monitoracao-arquivos-geral-ambiente-de-prd?orgId=1&var-DiaNaoUtil=1&var-JanelaMarcacao=Janela%201%20Ida&var-JanelaMarcacao=Janela%202%20Ida&var-JanelaMarcacao=Janela%203%20Ida&var-JanelaMarcacao=Janela%201%20Volta&var-JanelaMarcacao=Janela%202%20Volta&var-JanelaMarcacao=Janela%203%20Volta&var-DataMarcacao=2025-02-14&from=now-1h&to=now&refresh=10s)"
    t_zabbix = "✅ [Zabbix](http://radar.adiq.local/zabbix/zabbix.php?action=dashboard.view)"
    t_uptime = "✅ [Uptime](https://dashboard.uptimerobot.com/monitors)"

    def capturar_screenshot(url, path, wait_time=3, click_xpath=None):
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(wait_time)
        if click_xpath:
            try:
                zoom = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, click_xpath)))
                zoom.click()
                WebDriverWait(driver, 3).until(EC.staleness_of(zoom))
            except Exception as e:
                logging.error(f"Erro ao clicar em {url}: {e}")
        driver.save_screenshot(path)
        logging.info(f"Screenshot salvo: {path}")

    # Capturar screenshots
    capturar_screenshot(
        "https://grafana-monitoring-hml-grafana-monitoring-hml.apps.svs.adiq.local/d/ee9atfdxwhg5cf/visao-geral-transacional-fisico-sniffer-dxc?orgId=1&from=now-30m&to=now&refresh=5s",
        "fisico.png"
    )
    capturar_screenshot(
        "https://grafana-monitoring-hml-grafana-monitoring-hml.apps.svs.adiq.local/d/fe97u788lyneob/visao-geral-transacional-e-commerce?from=now-1h&to=now&orgId=1&refresh=5s",
        "ecommerce.png"
    )
    capturar_screenshot(
        "https://grafana-ocp4.adiq.io/d/uAoTFkJMzr/monitoracao-arquivos-geral-ambiente-de-prd?orgId=1&from=now-1h&to=now&refresh=10s",
        "arquivos.png"
    )
    capturar_screenshot(
        "https://adqtrjvpkbn01.adiq.local:5601/app/dashboards#/view/3cf45840-2021-11ee-a5b4-81e7ec0febaf?_g=(filters:!(),refreshInterval:(pause:!t,value:60000),time:(from:now-1h,to:now))",
        "banese.png",
        wait_time=8
    )
    capturar_screenshot(
        "https://adqtrjvpkbn01.adiq.local:5601/app/dashboards#/view/f1b3c7d4-22a4-4956-be94-1a8c6103d4d4",
        "unificada.png",
        wait_time=6
    )
    capturar_screenshot(
        "https://adqtrjvpkbn01.adiq.local:5601/app/dashboards#/view/73b07c60-2395-11ef-a2fe-31640ea6f96c?_g=(filters:!(),refreshInterval:(pause:!f,value:10000),time:(from:now-24h%2Fh,to:now))",
        "softpass.png",
        wait_time=6
    )
    capturar_screenshot(
        px,
        "pix.png",
        click_xpath="//span[contains(@class, 'css-1riaxdn') and contains(text(), 'Zoom to data')]"
    )
    capturar_screenshot(
        "http://radar.adiq.local/zabbix/zabbix.php?action=dashboard.view",
        "zabbix.png"
    )
    capturar_screenshot(
        "https://dashboard.uptimerobot.com/monitors",
        "uptime.png"
    )

    uptime_url = "https://dashboard.uptimerobot.com/monitors"
    driver.get(uptime_url)
    time.sleep(3)  # Tempo para carregar a página

    # 🔹 Capturar apenas a janela do navegador (evita pegar a tela inteira)
    uptime = ImageGrab.grab()
    uptime_path = "uptime.png"
    uptime.save(uptime_path)

    # Acessar o Microsoft Teams
    driver.get("https://teams.microsoft.com/")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(7)

    def acessar_grupo():
        grupo = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@id='title-chat-list-item_19:0c84d034ef6f47f6a962f8935761172a@thread.v2']"))
        )
        grupo.click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@name="expand-compose"]'))).click()

    executar_com_retries(acessar_grupo)

    try:
        chat_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@contenteditable="true"]')))
        chat_box.click()
        time.sleep(1)

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

Legenda: 
✅ Ambiente OK
❌ Incidente em Andamento
        """
        chat_box.send_keys(texto)
        chat_box.send_keys(Keys.RETURN)

        def copiar_e_enviar_imagem(caminho_imagem, chat_texto):
            chat_box.send_keys(chat_texto)
            chat_box.send_keys(Keys.RETURN)
            imagem = Image.open(caminho_imagem)
            output = io.BytesIO()
            imagem.save(output, format="BMP")
            data = output.getvalue()[14:]
            output.close()
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
            win32clipboard.CloseClipboard()
            logging.info(f"Screenshot {caminho_imagem} copiado para área de transferência")
            ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
            chat_box.send_keys(Keys.RETURN)
            chat_box.send_keys(Keys.RETURN)

        for img, txt in [
            ("fisico.png", t_fisico), ("ecommerce.png", t_ecommerce), ("unificada.png", t_unificada),
            ("banese.png", t_banese), ("softpass.png", t_spftpass), ("pix.png", t_pix),
            ("arquivos.png", t_atquivos), ("zabbix.png", t_zabbix), ("uptime.png", t_uptime)
        ]:
            executar_com_retries(lambda: copiar_e_enviar_imagem(img, txt))

        logging.info("Mensagem e imagens enviadas no Teams")
    except Exception as e:
        logging.error(f"Erro ao enviar mensagem no Teams: {e}")
        messagebox.showerror("Erro", f"Erro ao enviar mensagem no Teams: {e}")
    finally:
        limpar_screenshots()

def pix():
    global driver
    logging.info("Iniciando tarefa PIX")
    driver = verificar_webdriver(driver)
    
    driver.get("https://teams.microsoft.com/")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(7)

    def acessar_grupo_pix():
        grupo = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@id='title-chat-list-item_19:61690aabe8554ab48105cbb42f22f7a1@thread.v2']"))
        )
        grupo.click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@name="expand-compose"]'))).click()

    executar_com_retries(acessar_grupo_pix)

    try:
        chat_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@contenteditable="true"]')))
        chat_box.click()
        time.sleep(1)

        def copiar_e_enviar_imagem(caminho_imagem, chat_texto):
            ActionChains(driver).key_down(Keys.CONTROL).send_keys('b').key_up(Keys.CONTROL).perform()
            chat_box.send_keys(chat_texto)
            ActionChains(driver).key_down(Keys.CONTROL).send_keys('b').key_up(Keys.CONTROL).perform()
            chat_box.send_keys(Keys.RETURN)
            imagem = Image.open(caminho_imagem)
            output = io.BytesIO()
            imagem.save(output, format="BMP")
            data = output.getvalue()[14:]
            output.close()
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
            win32clipboard.CloseClipboard()
            logging.info(f"Screenshot {caminho_imagem} copiado para área de transferência")
            ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
            chat_box.send_keys(Keys.RETURN)

        executar_com_retries(lambda: copiar_e_enviar_imagem("pix.png", "ACC INFORMA:"))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@title="Enviar (Ctrl+Enter)" and @name="send"]'))).click()
        logging.info("Mensagem PIX enviada no Teams")
    except Exception as e:
        logging.error(f"Erro ao enviar mensagem PIX: {e}")
        messagebox.showerror("Erro", f"Erro ao enviar mensagem PIX: {e}")

def comparativo():
    global driver
    logging.info("Iniciando tarefa Comparativo")
    driver = verificar_webdriver(driver)
    
    hoje = datetime.today()
    data_7_dias_atras = hoje - timedelta(days=7)
    hora_inicio = data_7_dias_atras.replace(hour=3, minute=0, second=0, microsecond=0)
    hora_atual = datetime.now()

    if hora_atual.hour >= 20:
        hora_fim = hora_atual.replace(hour=23, minute=30, second=0, microsecond=0)
        if hora_atual >= hora_fim:
            hora_fim = (hoje + timedelta(days=1)).replace(hour=3, minute=0, second=0, microsecond=0)
    elif hora_atual.hour >= 23:
        hora_fim = (hoje + timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0)
    elif hora_atual.hour == 0:
        hora_fim = hora_atual.replace(hour=3, minute=30, second=0, microsecond=0)
    elif hora_atual.hour == 1:
        hora_fim = hora_atual.replace(hour=4, minute=30, second=0, microsecond=0)
    elif hora_atual.hour == 2:
        hora_fim = hora_atual.replace(hour=5, minute=30, second=0, microsecond=0)
    elif hora_atual.hour == 3:
        hora_fim = hora_atual.replace(hour=6, minute=30, second=0, microsecond=0)
    elif hora_atual.hour == 4:
        hora_fim = hora_atual.replace(hour=7, minute=30, second=0, microsecond=0)
    elif hora_atual.hour == 5:
        hora_fim = hora_atual.replace(hour=8, minute=30, second=0, microsecond=0)
    elif hora_atual.hour == 6:
        hora_fim = hora_atual.replace(hour=9, minute=30, second=0, microsecond=0)
    elif hora_atual.hour == 7:
        hora_fim = hora_atual.replace(hour=10, minute=30, second=0, microsecond=0)
    elif hora_atual.hour == 8:
        hora_fim = hora_atual.replace(hour=11, minute=30, second=0, microsecond=0)
    elif hora_atual.hour == 9:
        hora_fim = hora_atual.replace(hour=12, minute=30, second=0, microsecond=0)
    elif hora_atual.hour == 10:
        hora_fim = hora_atual.replace(hour=13, minute=30, second=0, microsecond=0)
    elif hora_atual.hour == 11:
        hora_fim = hora_atual.replace(hour=14, minute=30, second=0, microsecond=0)
    elif hora_atual.hour == 12:
        hora_fim = hora_atual.replace(hour=15, minute=30, second=0, microsecond=0)
    elif hora_atual.hour == 13:
        hora_fim = hora_atual.replace(hour=16, minute=30, second=0, microsecond=0)
    elif hora_atual.hour == 14:
        hora_fim = hora_atual.replace(hour=17, minute=30, second=0, microsecond=0)
    elif hora_atual.hour == 15:
        hora_fim = hora_atual.replace(hour=18, minute=30, second=0, microsecond=0)
    elif hora_atual.hour == 16:
        hora_fim = hora_atual.replace(hour=19, minute=30, second=0, microsecond=0)
    elif hora_atual.hour == 17:
        hora_fim = hora_atual.replace(hour=20, minute=30, second=0, microsecond=0)
    elif hora_atual.hour == 18:
        hora_fim = hora_atual.replace(hour=21, minute=30, second=0, microsecond=0)
    elif hora_atual.hour == 19:
        hora_fim = hora_atual.replace(hour=22, minute=30, second=0, microsecond=0)
    else:
        minutos = (hora_atual.minute // 30) * 30
        if hora_atual.minute % 30 != 0:
            minutos += 30
        hora_fim = hora_atual.replace(minute=minutos, second=0, microsecond=0)

    hora_fim = hora_fim.replace(year=hora_inicio.year, month=hora_inicio.month, day=hora_inicio.day)
    hora_inicio_str = hora_inicio.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    hora_fim_str = hora_fim.strftime('%Y-%m-%dT%H:%M:%S.000Z')

    cecomerce = f"https://adqtrjvpkbn01.adiq.local:5601/app/dashboards#/view/b959fda0-d0d8-11ee-b2b0-07a2f1811222?_g=(filters:!(),refreshInterval:(pause:!t,value:60000),time:(from:'{hora_inicio_str}',to:'{hora_fim_str}'))"
    cfisicos = f"https://adqtrjvpkbn01.adiq.local:5601/app/dashboards#/view/8eb71160-1b5f-11ef-bc95-f133a691effe?_g=(filters:!(),refreshInterval:(pause:!t,value:60000),time:(from:'{hora_inicio_str}',to:'{hora_fim_str}'))"

    driver.get(cecomerce)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(10)
    driver.save_screenshot("cecommerce.png")
    
    driver.get(cfisicos)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(10)
    driver.save_screenshot("cfisico.png")
    
    driver.get("https://teams.microsoft.com/")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(7)
    
    def acessar_grupo_comparativo():
        grupo = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@id='title-chat-list-item_19:43975b8185a94f76a78f370d9d332bdb@thread.v2']"))
        )
        grupo.click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@name="expand-compose"]'))).click()
    
    executar_com_retries(acessar_grupo_comparativo)
    
    try:
        chat_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@contenteditable="true"]')))
        chat_box.click()
        time.sleep(1)
        ActionChains(driver).key_down(Keys.CONTROL).send_keys('b').key_up(Keys.CONTROL).perform()
        chat_box.send_keys("ACC INFORMA")
        ActionChains(driver).key_down(Keys.CONTROL).send_keys('b').key_up(Keys.CONTROL).perform()
        chat_box.send_keys(Keys.RETURN)
        chat_box.send_keys(Keys.RETURN)
        
        def copiar_e_enviar_imagem(caminho_imagem, chat_texto):
            ActionChains(driver).key_down(Keys.CONTROL).send_keys('b').key_up(Keys.CONTROL).perform()
            chat_box.send_keys(chat_texto)
            ActionChains(driver).key_down(Keys.CONTROL).send_keys('b').key_up(Keys.CONTROL).perform()
            chat_box.send_keys(Keys.RETURN)
            imagem = Image.open(caminho_imagem)
            output = io.BytesIO()
            imagem.save(output, format="BMP")
            data = output.getvalue()[14:]
            output.close()
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
            win32clipboard.CloseClipboard()
            logging.info(f"Screenshot {caminho_imagem} copiado para área de transferência")
            ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
            chat_box.send_keys(Keys.RETURN)
            chat_box.send_keys(Keys.RETURN)
        
        executar_com_retries(lambda: copiar_e_enviar_imagem("cfisico.png", "Físico:"))
        executar_com_retries(lambda: copiar_e_enviar_imagem("cecommerce.png", "E-commerce:"))
        
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@title="Enviar (Ctrl+Enter)" and @name="send"]'))).click()
        logging.info("Mensagem Comparativo enviada no Teams")
    except Exception as e:
        logging.error(f"Erro ao enviar mensagem Comparativo: {e}")
        messagebox.showerror("Erro", f"Erro ao enviar mensagem Comparativo: {e}")
    finally:
        limpar_screenshots()

def adiqPlus():
    global driver
    logging.info("Iniciando tarefa Adiq+")
    driver = verificar_webdriver(driver)
    
    hoje = datetime.today()
    hora_inicio = hoje.replace(hour=3, minute=0, second=0, microsecond=0)
    hora_atual = datetime.now()
    
    if hora_atual.hour >= 20:
        hora_fim = hora_atual.replace(hour=23, minute=30, second=0, microsecond=0)
        if hora_atual >= hora_fim:
            hora_fim = (hoje + timedelta(days=1)).replace(hour=3, minute=0, second=0, microsecond=0)
    elif hora_atual.hour >= 23:
        hora_fim = (hoje + timedelta(days=1)).replace(hour=3, minute=30, second=0, microsecond=0)
    elif hora_atual.hour == 0:
        hora_fim = hora_atual.replace(hour=3, minute=30, second=0, microsecond=0)
    elif hora_atual.hour == 1:
        hora_fim = hora_atual.replace(hour=4, minute=30, second=0, microsecond=0)
    elif hora_atual.hour == 2:
        hora_fim = hora_atual.replace(hour=5, minute=30, second=0, microsecond=0)
    elif hora_atual.hour == 3:
        hora_fim = hora_atual.replace(hour=6, minute=30, second=0, microsecond=0)
    elif hora_atual.hour == 4:
        hora_fim = hora_atual.replace(hour=7, minute=30, second=0, microsecond=0)
    elif hora_atual.hour == 5:
        hora_fim = hora_atual.replace(hour=8, minute=30, second=0, microsecond=0)
    elif hora_atual.hour == 6:
        hora_fim = hora_atual.replace(hour=9, minute=30, second=0, microsecond=0)
    elif hora_atual.hour == 7:
        hora_fim = hora_atual.replace(hour=10, minute=30, second=0, microsecond=0)
    elif hora_atual.hour == 8:
        hora_fim = hora_atual.replace(hour=11, minute=30, second=0, microsecond=0)
    elif hora_atual.hour == 9:
        hora_fim = hora_atual.replace(hour=12, minute=30, second=0, microsecond=0)
    elif hora_atual.hour == 10:
        hora_fim = hora_atual.replace(hour=13, minute=30, second=0, microsecond=0)
    elif hora_atual.hour == 11:
        hora_fim = hora_atual.replace(hour=14, minute=30, second=0, microsecond=0)
    elif hora_atual.hour == 12:
        hora_fim = hora_atual.replace(hour=15, minute=30, second=0, microsecond=0)
    elif hora_atual.hour == 13:
        hora_fim = hora_atual.replace(hour=16, minute=30, second=0, microsecond=0)
    elif hora_atual.hour == 14:
        hora_fim = hora_atual.replace(hour=17, minute=30, second=0, microsecond=0)
    elif hora_atual.hour == 15:
        hora_fim = hora_atual.replace(hour=18, minute=30, second=0, microsecond=0)
    elif hora_atual.hour == 16:
        hora_fim = hora_atual.replace(hour=19, minute=30, second=0, microsecond=0)
    elif hora_atual.hour == 17:
        hora_fim = hora_atual.replace(hour=20, minute=30, second=0, microsecond=0)
    elif hora_atual.hour == 18:
        hora_fim = hora_atual.replace(hour=21, minute=30, second=0, microsecond=0)
    elif hora_atual.hour == 19:
        hora_fim = hora_atual.replace(hour=22, minute=30, second=0, microsecond=0)
    else:
        minutos = (hora_atual.minute // 30) * 30
        if hora_atual.minute % 30 != 0:
            minutos += 30
        hora_fim = hora_atual.replace(minute=minutos, second=0, microsecond=0)
    
    hora_inicio_str = hora_inicio.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    hora_fim_str = hora_fim.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    
    net = f"https://adqtrjvpkbn01.adiq.local:5601/app/dashboards#/view/3dbdd3a0-0884-11ee-bd3d-d543ccf9c199?_g=(filters:!(),refreshInterval:(pause:!t,value:60000),time:(from:'{hora_inicio_str}',to:'{hora_fim_str}'))"
    sniffer = f"https://adqtrjvpkbn01.adiq.local:5601/app/dashboards#/view/0d97d310-9aa1-11ee-bdd8-a3ff6f253f69?_g=(filters:!(),refreshInterval:(pause:!t,value:60000),time:(from:'{hora_inicio_str}',to:'{hora_fim_str}'))"
    
    driver.get(net)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(10)
    driver.save_screenshot("wtnet.png")
    
    driver.get(sniffer)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(10)
    driver.save_screenshot("snifferprd.png")
    
    driver.get("https://teams.microsoft.com/")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(7)
    
    def acessar_grupo_adiqplus():
        grupo = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@id='title-chat-list-item_19:4487e86e8e574b8dbeff3e607b5eeb18@thread.v2']"))
        )
        grupo.click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@name="expand-compose"]'))).click()
    
    executar_com_retries(acessar_grupo_adiqplus)
    
    try:
        chat_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@contenteditable="true"]')))
        chat_box.click()
        time.sleep(1)
        ActionChains(driver).key_down(Keys.CONTROL).send_keys('b').key_up(Keys.CONTROL).perform()
        chat_box.send_keys("ACC INFORMA:")
        ActionChains(driver).key_down(Keys.CONTROL).send_keys('b').key_up(Keys.CONTROL).perform()
        chat_box.send_keys(Keys.RETURN)
        chat_box.send_keys(Keys.RETURN)
        
        def copiar_e_enviar_imagem(caminho_imagem, chat_texto):
            ActionChains(driver).key_down(Keys.CONTROL).send_keys('b').key_up(Keys.CONTROL).perform()
            chat_box.send_keys(chat_texto)
            ActionChains(driver).key_down(Keys.CONTROL).send_keys('b').key_up(Keys.CONTROL).perform()
            chat_box.send_keys(Keys.RETURN)
            imagem = Image.open(caminho_imagem)
            output = io.BytesIO()
            imagem.save(output, format="BMP")
            data = output.getvalue()[14:]
            output.close()
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
            win32clipboard.CloseClipboard()
            logging.info(f"Screenshot {caminho_imagem} copiado para área de transferência")
            ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
            chat_box.send_keys(Keys.RETURN)
            chat_box.send_keys(Keys.RETURN)
        
        executar_com_retries(lambda: copiar_e_enviar_imagem("wtnet.png", "Origem WTnet:"))
        executar_com_retries(lambda: copiar_e_enviar_imagem("snifferprd.png", "Eagle Sniffer (PRD):"))
        
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@title="Enviar (Ctrl+Enter)" and @name="send"]'))).click()
        logging.info("Mensagem Adiq+ enviada no Teams")
    except Exception as e:
        logging.error(f"Erro ao enviar mensagem Adiq+: {e}")
        messagebox.showerror("Erro", f"Erro ao enviar mensagem Adiq+: {e}")
    finally:
        limpar_screenshots()

def tarefa5():
    logging.info("Tarefa 5 realizada")
    print("Tarefa 5 realizada!")

# Frame do checklist
frame_checklist = ctk.CTkFrame(frame_main, fg_color="gray20", corner_radius=10)
label_checklist = ctk.CTkLabel(frame_checklist, text="Checklist", font=("Arial", 24, "bold"))
label_checklist.pack(pady=10)

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

# Campo para intervalo de execução
intervalo_var = ctk.StringVar(value="60")
intervalo_entry = ctk.CTkEntry(frame_checklist, textvariable=intervalo_var, placeholder_text="Intervalo (minutos)")
intervalo_entry.pack(pady=5)

# Label de status
status_label = ctk.CTkLabel(frame_checklist, text="Pronto")
status_label.pack(pady=5)

# Variável para controle de execução
rodando = False

# Função para executar as tarefas
def executar_tarefas():
    global driver, rodando
    logging.info("Iniciando execução de tarefas")
    status_label.configure(text="Executando...")
    app.update()
    driver = verificar_webdriver(driver)
    
    try:
        if checkbox_var1.get():
            checklist()
            time.sleep(5)
        if checkbox_var2.get():
            pix()
            time.sleep(5)
        if checkbox_var3.get():
            comparativo()
            time.sleep(5)
        if checkbox_var4.get():
            adiqPlus()
            time.sleep(5)
        if checkbox_var5.get():
            tarefa5()
        logging.info("Tarefas concluídas com sucesso")
        status_label.configure(text="Concluído!")
    except Exception as e:
        logging.error(f"Erro durante execução de tarefas: {e}")
        status_label.configure(text="Erro!")
        messagebox.showerror("Erro", f"Erro durante execução: {e}")
    app.update()

# Função para iniciar o loop contínuo
def iniciar_tarefas():
    global rodando
    rodando = True
    try:
        intervalo = int(intervalo_var.get())
        schedule.every(intervalo).minutes.do(executar_tarefas)
        logging.info(f"Tarefas agendadas a cada {intervalo} minutos")
        status_label.configure(text="Rodando...")
        app.update()
    except ValueError:
        messagebox.showerror("Erro", "Intervalo deve ser um número válido!")
        rodando = False

# Função para parar o loop
def parar_tarefas():
    global rodando
    rodando = False
    schedule.clear()
    status_label.configure(text="Parado")
    logging.info("Execução parada")
    app.update()

# Botões de controle
btn_iniciar = ctk.CTkButton(frame_checklist, text="Iniciar Tarefas", command=lambda: threading.Thread(target=iniciar_tarefas, daemon=True).start())
btn_iniciar.pack(pady=5)
btn_parar = ctk.CTkButton(frame_checklist, text="Parar Tarefas", command=parar_tarefas)
btn_parar.pack(pady=5)
btn_executar_checklist = ctk.CTkButton(frame_checklist, text="Executar Agora", command=executar_tarefas)
btn_executar_checklist.pack(pady=20)

# Frame inicial
frame_home = ctk.CTkFrame(frame_main)
label_home = ctk.CTkLabel(frame_home, text="Home Page", font=("Arial", 24, "bold"))
label_home.pack(pady=10)

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
    * Certifique-se de estar logado no Chrome correto antes de iniciar.
    * Quando for executar o código, lembre-se de clicar na tela do Chrome para garantir que tudo ocorra sem problemas.
    * Caso encontre algum erro, reinicie a aplicação e tente novamente.

Agradecemos por utilizar nosso sistema! Qualquer dúvida, estou aqui para ajudar. 😄
"""

text_frame = ctk.CTkFrame(frame_home)
text_frame.pack(pady=20, padx=20)
scrollbar = ctk.CTkScrollbar(text_frame)
scrollbar.pack(side="right", fill="y")
text_box = ctk.CTkTextbox(text_frame, wrap="word", height=700, width=700, font=("Arial", 16))
text_box.pack(side="left", fill="both", expand=True)
text_box.insert("1.0", manual_text)

# Frame WhatsApp
data_hora = datetime.now()
if data_hora.minute > 30:
    data_hora = data_hora.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
else:
    data_hora = data_hora.replace(minute=0, second=0, microsecond=0)
data_formatada = data_hora.strftime("%d/%m")
aa = f'🔊 *BS2 PAYMENTS*. {data_formatada}\n'

mensagens = [
    f"{aa}",
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

icones = ["✅", "⚠", "🚫", "❌", "🔄"]

frame_whatsapp = ctk.CTkFrame(frame_main, fg_color="gray20", corner_radius=10)
label_whatsapp = ctk.CTkLabel(frame_whatsapp, text="WhatsApp", font=("Arial", 24, "bold"))
label_whatsapp.pack(pady=10)

scrollable_frame = ctk.CTkScrollableFrame(frame_whatsapp, width=500, height=200, corner_radius=10)
scrollable_frame.pack(pady=10)

checkbox_vars = []
checkboxes = []
for i, mensagem in enumerate(mensagens):
    var = ctk.BooleanVar(value=False)
    checkbox = ctk.CTkCheckBox(scrollable_frame, text=mensagem, variable=var, onvalue=True, offvalue=False)
    checkbox.pack(anchor="w", pady=5)
    checkbox_vars.append(var)
    checkboxes.append(checkbox)

def enviar_mensagens():
    global driver
    logging.info("Iniciando envio de mensagens WhatsApp")
    driver = verificar_webdriver(driver)
    
    mensagens_selecionadas = [mensagens[i] for i, var in enumerate(checkbox_vars) if var.get()]
    if not mensagens_selecionadas:
        messagebox.showinfo("Nenhuma Seleção", "Você não selecionou nenhuma mensagem para enviar!")
        return
    
    mensagem = "\n".join(mensagens_selecionadas)
    caminho_arquivo = "mensagens_selecionadas.txt"
    
    try:
        diretorio_arquivo = os.path.dirname(caminho_arquivo)
        if diretorio_arquivo and not os.path.exists(diretorio_arquivo):
            os.makedirs(diretorio_arquivo)
        with open(caminho_arquivo, "w", encoding="utf-8") as file:
            file.write(mensagem)
        logging.info(f"Mensagens salvas em {caminho_arquivo}")
    except Exception as e:
        logging.error(f"Erro ao gravar arquivo: {e}")
        messagebox.showerror("Erro", f"Erro ao gravar arquivo: {e}")
        return
    
    driver.get("https://web.whatsapp.com")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(15)
    
    nome_grupo = "BS2 - Checklist - TI"
    try:
        grupo = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//span[@title="{}"]'.format(nome_grupo)))
        )
        grupo.click()
        time.sleep(2)
        campo_mensagem = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div[2]/div[1]/p'))
        )
        campo_mensagem.click()
        with open(caminho_arquivo, "r", encoding="utf-8") as file:
            conteudo = file.read()
        pyperclip.copy(conteudo)
        campo_mensagem.clear()
        ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
        time.sleep(2)
        campo_mensagem.send_keys(Keys.RETURN)
        logging.info("Mensagem enviada no WhatsApp")
        messagebox.showinfo("Sucesso", "Mensagem enviada com sucesso!")
    except Exception as e:
        logging.error(f"Erro ao enviar mensagem no WhatsApp: {e}")
        messagebox.showerror("Erro", f"Erro ao enviar mensagem: {e}")

def alterar_icone_na_tela():
    mensagens_selecionadas = [mensagens[i] for i, var in enumerate(checkbox_vars) if var.get()]
    if not mensagens_selecionadas:
        messagebox.showinfo("Nenhuma Seleção", "Você não selecionou nenhuma mensagem para alterar!")
        return
    
    janela_alteracao = ctk.CTkToplevel(app)
    janela_alteracao.title("Alteração de Ícone")
    janela_alteracao.geometry("400x400")
    
    label_titulo = ctk.CTkLabel(janela_alteracao, text="Selecione uma mensagem para alterar o ícone", font=("Arial", 18, "bold"))
    label_titulo.pack(pady=10)
    
    checkbox_vars_selecionados = []
    checkboxes_selecionados = []
    for i, mensagem in enumerate(mensagens_selecionadas):
        var = ctk.BooleanVar(value=False)
        checkbox = ctk.CTkCheckBox(janela_alteracao, text=mensagem, variable=var, onvalue=True, offvalue=False)
        checkbox.pack(anchor="w", pady=5)
        checkbox_vars_selecionados.append(var)
        checkboxes_selecionados.append(checkbox)
    
    def aplicar_icone():
        mensagens_a_alterar = [mensagens_selecionadas[i] for i, var in enumerate(checkbox_vars_selecionados) if var.get()]
        if not mensagens_a_alterar:
            messagebox.showinfo("Nenhuma Seleção", "Você não selecionou nenhuma mensagem para alterar o ícone!")
            return
        
        icone_selecionado = ctk.CTkOptionMenu(janela_alteracao, values=icones)
        icone_selecionado.pack(pady=10)
        campo_texto = ctk.CTkEntry(janela_alteracao, placeholder_text="Digite o novo conteúdo")
        campo_texto.pack(pady=10)
        
        def confirmar_icone():
            icone = icone_selecionado.get()
            novo_conteudo = campo_texto.get()
            if novo_conteudo:
                for i, mensagem in enumerate(mensagens):
                    if mensagens[i] in mensagens_a_alterar:
                        partes = mensagem.split("(", 1)
                        if len(partes) > 1:
                            partes_antes_parenteses = partes[0].strip()
                            if partes_antes_parenteses and partes_antes_parenteses[0] in icones:
                                icone_preservado = partes_antes_parenteses.split(" ", 1)[0]
                                texto_antes_parenteses = partes_antes_parenteses[len(icone_preservado):].strip()
                            else:
                                icone_preservado = ""
                                texto_antes_parenteses = partes_antes_parenteses.strip()
                            mensagens[i] = icone + " " + texto_antes_parenteses + f"({novo_conteudo})"
                        else:
                            mensagens[i] = icone + " " + partes[0] + f"({novo_conteudo})"
                        for j, checkbox in enumerate(checkboxes):
                            if checkbox_vars[j].get() and mensagens[j] == mensagens[i]:
                                checkbox.configure(text=mensagens[i])
                messagebox.showinfo("Sucesso", f"Ícone alterado para '{icone}' e conteúdo para '{novo_conteudo}'!")
                janela_alteracao.destroy()
        
        btn_confirmar = ctk.CTkButton(janela_alteracao, text="Confirmar Alteração", command=confirmar_icone)
        btn_confirmar.pack(pady=20)
    
    btn_aplicar = ctk.CTkButton(janela_alteracao, text="Aplicar Alteração", command=aplicar_icone)
    btn_aplicar.pack(pady=20)
    janela_alteracao.grab_set()

btn_enviar_mensagens = ctk.CTkButton(frame_whatsapp, text="Enviar Mensagens", command=enviar_mensagens)
btn_enviar_mensagens.pack(pady=10)
btn_alterar_checklist = ctk.CTkButton(frame_whatsapp, text="Alterar Mensagens", command=alterar_icone_na_tela)
btn_alterar_checklist.pack(pady=10)

selected_file = None

def upload_file():
    global selected_file
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        selected_file = file_path
        label_file.configure(text=f"Arquivo selecionado:\n{file_path}")
        button_process.configure(state="normal")

def extract_messages(content):
    pattern = r'Message"":""(.*?)"","'
    messages = [match.group(1) for line in content for match in re.finditer(pattern, line)]
    grouped_messages = Counter()
    for msg in messages:
        key = msg.split(".")[0]
        grouped_messages[key] += 1
    return grouped_messages

def process_file():
    if selected_file:
        try:
            with open(selected_file, "r", encoding="utf-8") as file:
                raw_content = file.readlines()
            message_counts = extract_messages(raw_content)
            error_summary = "\n".join([f"{count:03d} - {message}" for message, count in message_counts.items()])
            total_sum = 0
            formatted_error_summary = ""
            for line in error_summary.split('\n'):
                count, message = line.split(" - ", 1)
                if any(ignore_phrase in message for ignore_phrase in [
                        "Name or service not known",
                        "Connection reset by peer",
                        "Error parsing Infinity value",
                        "A network-related or instance-specific error occurred while establishing a connection to SQL Server"]):
                    continue
                count_divided = int(count) // 2
                total_sum += count_divided
                formatted_error_summary += f"{count_divided:03d} - {message}\n"
            formatted_error_summary += f"\nTotal: {total_sum}"
            result_text.delete(1.0, "end")
            result_text.insert("end", formatted_error_summary.strip())
            logging.info("Arquivo processado com sucesso")
            messagebox.showinfo("Sucesso", "Arquivo processado com sucesso!")
        except Exception as e:
            logging.error(f"Erro ao processar arquivo: {e}")
            messagebox.showerror("Erro", f"Erro ao processar arquivo: {e}")
    else:
        messagebox.showwarning("Aviso", "Nenhum arquivo selecionado.")

def copiar_resultado():
    resultado = result_text.get(1.0, "end-1c")
    app.clipboard_clear()
    app.clipboard_append(resultado)
    app.update()
    messagebox.showinfo("Sucesso", "Conteúdo copiado para a área de transferência!")

frame_pix_fechamento = ctk.CTkFrame(frame_main, fg_color="gray20", corner_radius=10)
label_pix_fechamento = ctk.CTkLabel(frame_pix_fechamento, text="Fechamento Pix", font=("Arial", 24, "bold"))
label_pix_fechamento.pack(pady=10)
button_upload = ctk.CTkButton(frame_pix_fechamento, text="Upload File", command=upload_file)
button_upload.pack(pady=10)
label_file = ctk.CTkLabel(frame_pix_fechamento, text="Nenhum arquivo selecionado", wraplength=500)
label_file.pack(pady=10)
button_process = ctk.CTkButton(frame_pix_fechamento, text="Processar Arquivo", command=process_file, state="disabled")
button_process.pack(pady=10)
button_copy = ctk.CTkButton(frame_pix_fechamento, text="Copiar Resultados", command=copiar_resultado)
button_copy.pack(pady=10)
result_text = ctk.CTkTextbox(frame_pix_fechamento, height=200, width=700)
result_text.pack(pady=10)

# Botões da sidebar
btn_home = ctk.CTkButton(frame_sidebar, text="Home", fg_color="gray30", hover_color="gray40", command=lambda: mostrar_frame(frame_home))
btn_home.pack(fill="x", pady=5, padx=10)
btn_checklist = ctk.CTkButton(frame_sidebar, text="CheckList", fg_color="gray30", hover_color="gray40", command=lambda: mostrar_frame(frame_checklist))
btn_checklist.pack(fill="x", pady=5, padx=10)
btn_whatsapp = ctk.CTkButton(frame_sidebar, text="WhatsApp", fg_color="gray30", hover_color="gray40", command=lambda: mostrar_frame(frame_whatsapp))
btn_whatsapp.pack(fill="x", pady=5, padx=10)
btn_pix_fechamento = ctk.CTkButton(frame_sidebar, text="Fechamento pix", fg_color="gray30", hover_color="gray40", command=lambda: mostrar_frame(frame_pix_fechamento))
btn_pix_fechamento.pack(fill="x", pady=5, padx=10)
btn_system = ctk.CTkOptionMenu(frame_sidebar, values=["System"])
btn_system.pack(side="bottom", pady=10)

# Exibir frame inicial
mostrar_frame(frame_home)

# Loop principal para agendamento
def main_loop():
    while True:
        schedule.run_pending()
        time.sleep(60)

threading.Thread(target=main_loop, daemon=True).start()

app.mainloop()

# Fechar WebDriver ao encerrar
try:
    driver.quit()
except:
    pass