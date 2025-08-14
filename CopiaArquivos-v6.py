# Importação de bibliotecas padrão e externas
from pathlib import Path        # Manipulação de caminhos de arquivos e pastas
import shutil                   # Copiar arquivos e diretórios
import ttkbootstrap as ttk     # Biblioteca para interface gráfica (tema bootstrap)
import tkinter as tk           # Biblioteca GUI básica do Python
from ttkbootstrap.constants import *  # Constantes para ttkbootstrap
from tkinter import filedialog, messagebox  # Caixa de diálogo de arquivos e mensagens
from datetime import datetime, timedelta    # Data e hora
import win32com.client as win32  # Automação do Outlook via COM
import threading               # Para rodar processos em threads separadas (não travar GUI)

# ================== Definição das bandeiras e seus dados ===================
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
            Path(r"\\adqtspvpfs01\Integracao\Connect\ELO\RECEBE\BACKUP"),
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

# Variáveis globais usadas para controle e estado
copied_files = []        # Lista de arquivos copiados para possível rollback
arquivos_para_copiar = {}  # Dicionário com arquivos a copiar por bandeira
log_path = ""            # Caminho do arquivo de log escolhido pelo usuário
stop_process = False     # Flag para interromper processos quando o usuário clicar "parar"


# Função para registrar mensagens no arquivo de log
def log(msg):
    if not log_path:
        return
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {msg}\n")


# Função para adicionar texto na área de status da interface
def add_status(text):
    text_status.config(state='normal')        # Liberar edição temporariamente
    text_status.insert('end', text + '\n')    # Inserir texto no final
    text_status.see('end')                     # Rolar para a última linha
    text_status.config(state='disabled')      # Bloquear edição novamente


# Função para selecionar onde salvar o arquivo de log (caixa de diálogo)
def selecionar_log():
    global log_path
    path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Log Files", "*.txt")],
        title="Escolha onde salvar o log",
        initialfile=f"CopiaArquivos_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    )
    if path:
        log_path = path
        log(f"Arquivo de log criado: {path}")
        add_status(f"Arquivo de log criado: {path}")


# Função para abrir o Outlook e montar email para ELO avisando arquivos ausentes
def enviar_email_elo(tipos_faltantes):
    # Monta o assunto e corpo conforme tipos de arquivo faltantes
    if tipos_faltantes == {"debito"}:
        assunto = "Não recebimento dos arquivos AGECRED ELO DÉBITO"
        corpo = (
            "Bom dia.\n"
            "Até o momento não recebemos os arquivos AGECRED de Débito da ELO.\n"
            "Poderiam verificar por gentileza?\n"
            "Máscara dos arquivos:\n"
            "AGECRED_D_5190*\n"
            "AGECRED_D_5030*\n\n"
        )
    elif tipos_faltantes == {"credito"}:
        assunto = "Não recebimento dos arquivos AGECRED ELO CRÉDITO"
        corpo = (
            "Bom dia.\n"
            "Até o momento não recebemos os arquivos AGECRED de Crédito da ELO.\n"
            "Poderiam verificar por gentileza?\n"
            "Máscara dos arquivos:\n"
            "AGECRED_C_5190*\n"
            "AGECRED_C_5030*\n\n"
        )
    else:
        assunto = "Não recebimento dos arquivos AGECRED ELO CRÉDITO E DÉBITO"
        corpo = (
            "Bom dia.\n"
            "Até o momento não recebemos os arquivos AGECRED de Débito e Crédito da ELO.\n"
            "Poderiam verificar por gentileza?\n"
            "Máscara dos arquivos:\n"
            "AGECRED_C_5190*\n"
            "AGECRED_C_5030*\n"
            "AGECRED_D_5190*\n"
            "AGECRED_D_5030*\n\n"
        )
    try:
        outlook = win32.Dispatch('Outlook.Application')
        mail = outlook.CreateItem(0)  # 0 indica e-mail
        mail.To = 'cce@elo.com.br; Acc@adiq.com.br'
        mail.CC = 'diego.carvalho@adiq.com.br; eli.junior@bs2tecnologia.com.br'
        mail.Subject = assunto
        mail.Body = corpo + mail.Session.CurrentUser.Name
        mail.Display(True)  # Abre para o usuário revisar e enviar
        add_status("Email do Outlook aberto para envio.")
        log("Email do Outlook aberto para envio.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao abrir o Outlook: {e}")
        log(f"Erro ao abrir Outlook: {e}")
# Função para verificar os arquivos de todas as bandeiras selecionadas
def verificar_arquivos():
    global arquivos_para_copiar
    arquivos_para_copiar.clear()  # Limpa lista anterior
    text_status.config(state='normal')
    text_status.delete('1.0', 'end')  # Limpa área de status
    add_status("Iniciando verificação de arquivos...")
    log("=== Início da verificação ===")

    hoje_yyMMdd = datetime.now().strftime('%y%m%d')    # Ex: 250703 (ano curto)
    hoje_yyyMMdd = datetime.now().strftime('%Y%m%d')   # Ex: 20250703 (ano completo)

    # Seleciona só as bandeiras que o usuário marcou para verificar
    bandeiras_selecionadas = [nome for nome in BANDEIRAS if chk_bandeiras[nome].get()]
    total_bandeiras = len(bandeiras_selecionadas)

    progress_bar['maximum'] = total_bandeiras
    progress_bar['value'] = 0
    barra_var.set(f"Verificando: 0 / {total_bandeiras}")

    for idx, nome in enumerate(bandeiras_selecionadas, start=1):
        dados = BANDEIRAS[nome]
        arquivos = []

        # Tratamento especial para Amex, que verifica pasta de data anterior
        if nome == "Amex":
            data_pasta = (datetime.now() - timedelta(days=1)).strftime('%Y.%m.%d')
            pasta_origem = dados['origem'][0] / data_pasta
            if pasta_origem.exists() and pasta_origem.is_dir():
                arquivos_para_copiar[nome] = [pasta_origem]
                msg = f"Pasta encontrada para {nome}: {pasta_origem}"
            else:
                msg = f"Nenhuma pasta encontrada para {nome} com nome {data_pasta}."
            log(msg)
            add_status(msg)
            # Continua para próxima bandeira, pois não faz busca por arquivos aqui
            continue

        # Para as outras bandeiras, procura arquivos que batem com as máscaras da data atual
        for origem in dados['origem']:
            data_formatada = hoje_yyMMdd if nome in ["Hipercard", "Mastercard"] else hoje_yyyMMdd
            for mascara in dados['mascaras']:
                padrao = mascara.format(data_formatada)
                if origem.exists():
                    arquivos.extend(origem.glob(padrao))

        if arquivos:
            arquivos_para_copiar[nome] = arquivos
            msg = f"{len(arquivos)} arquivos encontrados para {nome}."
        else:
            msg = f"Nenhum arquivo encontrado para {nome}."

            # Aqui dispara o popup para ELO se for após 05:00 e não encontrou arquivos
            if nome == "Elo" and datetime.now().hour >= 5:
                tipos = {"credito", "debito"}
                popup_msg = (
                    "Arquivos AGECRED da ELO não foram encontrados após 05:00.\n\n"
                    "Deseja abrir um e-mail para a ELO?"
                )
                if messagebox.askyesno("AGECRED ausente", popup_msg):
                    enviar_email_elo(tipos)

        log(msg)
        add_status(msg)

        progress_bar['value'] = idx
        barra_var.set(f"Verificando: {idx} / {total_bandeiras}")
        root.update_idletasks()  # Atualiza a interface para mostrar progresso

    log("=== Fim da verificação ===")
    add_status("Verificação concluída.")
    barra_var.set("Verificação concluída.")


# Função para iniciar a cópia dos arquivos encontrados para as pastas destino
def iniciar_copia():
    global stop_process
    stop_process = False
    copied_files.clear()

    total = sum(len(v) for v in arquivos_para_copiar.values())
    atual = 0

    if total == 0:
        messagebox.showinfo("Info", "Nenhum arquivo para copiar.")
        add_status("Nenhum arquivo para copiar.")
        return

    barra_var.set(f"Progresso: 0/{total}")

    for nome, itens in arquivos_para_copiar.items():
        destino = BANDEIRAS[nome]['destino']
        if not itens:
            continue
        # Confirma se usuário quer copiar para esta bandeira
        if not messagebox.askyesno("Confirmação", f"Deseja copiar arquivos para {nome}?"):
            add_status(f"Cópia para {nome} cancelada pelo usuário.")
            log(f"Cópia para {nome} cancelada pelo usuário.")
            continue

        for item in itens:
            if stop_process:
                add_status("Processo interrompido pelo usuário.")
                log("Processo interrompido pelo usuário.")
                return
            try:
                destino.mkdir(parents=True, exist_ok=True)  # Cria pasta destino se não existir
                dest_path = destino / item.name
                if dest_path.exists():
                    msg = f"Arquivo ou pasta já existe e não será copiado: {dest_path}"
                    log(msg)
                    add_status(msg)
                    continue
                # Copia arquivo ou pasta
                if item.is_dir():
                    shutil.copytree(item, dest_path)
                else:
                    shutil.copy2(item, dest_path)
                copied_files.append(dest_path)
                atual += 1
                barra_var.set(f"Progresso: {atual}/{total}")
                log(f"Copiado: {item}")
                add_status(f"Copiado: {item}")
                root.update_idletasks()
            except Exception as e:
                msg = f"Erro ao copiar {item}: {str(e)}"
                log(msg)
                add_status(msg)
                messagebox.showerror("Erro", msg)

    add_status("Cópia concluída.")
    log("Cópia concluída.")


# Função para desfazer as cópias feitas (rollback)
def desfazer():
    if not copied_files:
        messagebox.showinfo("Info", "Nenhum arquivo para desfazer.")
        return
    if not messagebox.askyesno("Confirmação", "Deseja desfazer as cópias realizadas?"):
        return
    for f in copied_files:
        try:
            if f.is_file():
                f.unlink()
            elif f.is_dir():
                shutil.rmtree(f)
            log(f"Removido no rollback: {f}")
            add_status(f"Removido no rollback: {f}")
        except Exception as e:
            log(f"Erro ao remover {f}: {str(e)}")
            add_status(f"Erro ao remover {f}: {str(e)}")
    copied_files.clear()
    add_status("Rollback executado: arquivos removidos.")
    messagebox.showinfo("Rollback", "Arquivos removidos com sucesso.")


# Função para parar os processos longos (cópia, verificação)
def parar():
    global stop_process
    stop_process = True
    add_status("Processo interrompido pelo usuário.")
    log("Processo interrompido pelo usuário.")


# Para rodar a verificação em thread separada e não travar a GUI
def iniciar_verificacao_thread():
    thread = threading.Thread(target=verificar_arquivos, daemon=True)
    thread.start()
# ---------------- Construção da interface gráfica ------------------

# Janela principal com tema 'darkly'
root = ttk.Window(themename="darkly")
root.title("Cópia Arquivos Bandeiras")
root.geometry("850x520")
root.resizable(False, False)

# Frame esquerdo para botões e checkbuttons
frame_left = tk.Frame(root, bg="#1f2937")
frame_left.pack(side="left", fill="y", padx=12, pady=12)

# # Botão para selecionar arquivo de log
# btn_selecionar_log = ttk.Button(frame_left, text="Selecionar arquivo de log",
#                                 bootstyle="info-outline", command=selecionar_log)
# btn_selecionar_log.pack(pady=6, fill='x')

# Botão para iniciar a verificação dos arquivos
btn_verificar = ttk.Button(frame_left, text="Verificar Arquivos",
                           bootstyle="info-outline",  command=lambda: [selecionar_log(), verificar_arquivos()])
btn_verificar.pack(pady=6, fill='x')

# Botão para iniciar a cópia dos arquivos
btn_iniciar = ttk.Button(frame_left, text="Iniciar Cópia",
                         bootstyle="success-outline", command=iniciar_copia)
btn_iniciar.pack(pady=6, fill='x')

# Botão para parar processos em execução
btn_parar = ttk.Button(frame_left, text="Parar Processo",
                       bootstyle="danger-outline", command=parar)
btn_parar.pack(pady=6, fill='x')

# Botão para desfazer cópias realizadas
btn_desfazer = ttk.Button(frame_left, text="Desfazer Cópia",
                          bootstyle="warning-outline", command=desfazer)
btn_desfazer.pack(pady=6, fill='x')

# Botão para fechar o programa
btn_sair = ttk.Button(frame_left, text="Fechar", bootstyle="secondary", command=root.quit)
btn_sair.pack(pady=20, fill='x')

# Checkbuttons para seleção das bandeiras
chk_bandeiras = {}
for nome in BANDEIRAS:
    var = tk.BooleanVar(value=True)  # Por padrão todos selecionados
    chk = ttk.Checkbutton(frame_left, text=nome, variable=var, bootstyle="info-toolbutton")
    chk.pack(anchor='w', pady=3)
    chk_bandeiras[nome] = var

# Frame direito para área de status (text widget)
frame_right = tk.Frame(root)
frame_right.pack(fill='both', expand=True, padx=10, pady=10)

text_status = tk.Text(frame_right, height=25, wrap='word', state='disabled',
                      bg="#111827", fg="#d1d5db", font=("Consolas", 10))
text_status.pack(fill='both', expand=True)

# Barra de progresso (progressbar)
progress_bar = ttk.Progressbar(root, maximum=100, mode='determinate')
progress_bar.pack(side='bottom', fill='x', padx=10, pady=(0, 5))

# Label para texto de progresso abaixo da barra
barra_var = tk.StringVar(value="Progresso: 0/0")
label_progress = ttk.Label(root, textvariable=barra_var, anchor='center',
                           font=('Consolas', 13), bootstyle="inverse-secondary")
label_progress.pack(side='bottom', fill='x', pady=(0, 10))

# Inicia a interface gráfica (loop principal)
root.mainloop()
