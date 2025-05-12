from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time
import pyperclip  # Para copiar o emoji para a área de transferência, se necessário

# 🔹 Configurar o emoji SOS (usando Unicode diretamente)
sos_emoji = "\U0001F198"  # Emoji SOS 🆘
print(sos_emoji)  # Deve exibir 🆘 no console

# 🔹 Configurar o WebDriver
chrome_user_data_dir = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
 
options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "localhost:9222")  # Conectar ao Chrome aberto
options.add_argument(f"user-data-dir={chrome_user_data_dir}")
 
# Iniciar WebDriver
driver = webdriver.Chrome(options=options)

# 🔹 Acessar o Microsoft Teams Web
teams_url = "https://teams.microsoft.com/"
driver.get(teams_url)
time.sleep(7)  # Tempo para login manual

# 🔹 Selecionar o grupo
grupo = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[@id='title-chat-list-item_19:0c84d034ef6f47f6a962f8935761172a@thread.v2']"))
)
grupo.click()

# 🔹 Expandir a caixa de composição
teste = driver.find_element(By.XPATH, '//button[@name="expand-compose"]')
teste.click()

# 🔹 Enviar mensagem no Teams
time.sleep(1)
chat_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"]')
chat_box.click()
time.sleep(1)

# Copiar o emoji para a área de transferência e colar (método mais confiável)

pyperclip.copy(sos_emoji)
chat_box.send_keys(Keys.CONTROL + 'v')  # Cola o emoji

# Opcional: Enviar a mensagem pressionando Enter
chat_box.send_keys(Keys.RETURN)

# Fechar o driver (se necessário)
# driver.quit()