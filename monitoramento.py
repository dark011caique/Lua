import os
from datetime import datetime
import customtkinter as ctk
from tkinter import filedialog
from CTkMessagebox import CTkMessagebox

# ================= Inicializar Interface ==================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Monitor de Arquivos Parados")
app.geometry("950x650")

# ================= Variáveis ==================
folder_list = [
    r"\\adqtspvpfs01\integracao\Nuclea-SLC-Cred\NucleaSaida",
    r"\\adqtspvpfs01\Integracao\Connect\DXC\RECEBE",
]

limite_minutos = 1
intervalo_verificacao_ms = 600000  # 10 minutos padrão
verificacao_ativa = True

extensoes_disponiveis = [".xml", ".txt", ".csv", ".json", ".log", ".xlsx", ".docx", ".pdf", ".zip", ".rar", ".DAT"]
extensoes_monitoradas = [".xml", ".txt", ".DAT"]


# ================= Layout ==================
frame_sidebar = ctk.CTkFrame(app, width=230, corner_radius=0)
frame_sidebar.pack(side="left", fill="y")

frame_main = ctk.CTkFrame(app)
frame_main.pack(side="right", expand=True, fill="both", padx=20, pady=20)

frame_arquivo_parado_pasta = ctk.CTkFrame(frame_main)
frame_arquivo_parado_pasta.pack(expand=True, fill="both")

# ================= Header ==================
titulo_label = ctk.CTkLabel(frame_arquivo_parado_pasta, text="Arquivos Parados nas Pastas",
                             font=ctk.CTkFont(size=18, weight="bold"))
titulo_label.pack(pady=(10, 5))

contador_label = ctk.CTkLabel(frame_arquivo_parado_pasta, text="Verificando arquivos...",
                               font=ctk.CTkFont(size=14))
contador_label.pack(pady=(0, 10))


# ================== Funções =====================
def pausar_verificacao():
    global verificacao_ativa
    verificacao_ativa = False
    contador_label.configure(text="🔴 Verificação PAUSADA")
    CTkMessagebox(title="Pausado", message="Verificação foi pausada!", icon="info")


def retomar_verificacao():
    global verificacao_ativa
    verificacao_ativa = True
    contador_label.configure(text="🟢 Verificação ATIVA")
    CTkMessagebox(title="Ativado", message="Verificação retomada!", icon="info")


def forcar_verificacao():
    verificar_arquivos()


def adicionar_pasta():
    pasta = filedialog.askdirectory()
    if pasta:
        folder_list.append(pasta)
        CTkMessagebox(title="Pasta adicionada", message=f"Pasta adicionada:\n{pasta}", icon="check")


def atualizar_intervalo():
    try:
        minutos = int(intervalo_entry.get())
        global intervalo_verificacao_ms
        intervalo_verificacao_ms = minutos * 60000
        CTkMessagebox(title="Intervalo atualizado", message=f"Novo intervalo: {minutos} minutos", icon="check")
    except ValueError:
        CTkMessagebox(title="Erro", message="Digite um valor numérico para minutos!", icon="cancel")


def atualizar_extensoes(opcao):
    if opcao not in extensoes_monitoradas:
        extensoes_monitoradas.append(opcao)


def criar_item_lista(nome_arquivo, caminho):
    item_frame = ctk.CTkFrame(frame_arquivo_parado_pasta, fg_color="#314c67", corner_radius=10)
    item_frame.pack(fill="x", pady=8, padx=5)

    icon_label = ctk.CTkLabel(item_frame, text="📄", font=ctk.CTkFont(size=24))
    icon_label.grid(row=0, column=0, rowspan=2, padx=(10, 8), sticky="n")

    nome_label = ctk.CTkLabel(item_frame, text=nome_arquivo, text_color="black",
                               font=ctk.CTkFont(size=14, weight="bold"))
    nome_label.grid(row=0, column=1, sticky="w")

    caminho_label = ctk.CTkLabel(item_frame, text=caminho, text_color="black",
                                  font=ctk.CTkFont(size=10))
    caminho_label.grid(row=1, column=1, sticky="w", padx=(0, 10))

    tag = ctk.CTkLabel(item_frame, text=",".join(extensoes_monitoradas), fg_color="gray",
                        text_color="black", corner_radius=5, padx=4, font=ctk.CTkFont(size=8))
    tag.grid(row=0, column=2, padx=5)

    abrir_button = ctk.CTkButton(item_frame, text="Abrir", width=60,
                                  command=lambda: os.startfile(os.path.dirname(caminho)))
    abrir_button.grid(row=0, column=3, rowspan=2, padx=10)


def verificar_arquivos():
    global verificacao_ativa
    try:
        if not verificacao_ativa:
            contador_label.configure(text="🔴 Verificação PAUSADA")
            return

        agora = datetime.now()
        arquivos_parados = []
        arquivos_encontrados = False

        for pasta in folder_list:
            if os.path.exists(pasta):
                count = 0  # contador de arquivos analisados

                with os.scandir(pasta) as entries:
                    for entry in entries:
                        if count >= 100:
                            break  # para após 100 arquivos

                        if entry.is_file() and entry.name.lower().endswith(tuple(extensoes_monitoradas)):
                            arquivos_encontrados = True
                            ultima_modificacao = datetime.fromtimestamp(entry.stat().st_mtime)

                            # pula arquivos que não são de hoje
                            if ultima_modificacao.date() != agora.date():
                                continue

                            minutos = (agora - ultima_modificacao).total_seconds() / 60
                            if minutos > limite_minutos:
                                arquivos_parados.append((entry.name, entry.path))

                            count += 1

        for widget in frame_arquivo_parado_pasta.winfo_children():
            if widget not in [titulo_label, contador_label, btn_forcar, btn_pausar, btn_retomar,
                               intervalo_label, intervalo_entry, btn_atualizar_intervalo,
                               btn_adicionar_pasta, extensao_option]:
                widget.destroy()

        if arquivos_parados:
            contador_label.configure(text=f"{len(arquivos_parados)} arquivos parados")
            lista_alerta = "\n".join([c for _, c in arquivos_parados])
            for nome, caminho in arquivos_parados:
                criar_item_lista(nome, caminho)
            CTkMessagebox(title="Arquivos Parados ⚠️", message=f"Arquivos Parados ⚠️", icon="warning")
        else:
            if not arquivos_encontrados:
                contador_label.configure(text="⚠️ Nenhum arquivo encontrado nas pastas.")
            else:
                contador_label.configure(text="Nenhum arquivo parado.")

    except Exception as e:
        CTkMessagebox(title="Erro", message=f"Erro na verificação:\n{e}", icon="cancel")
    finally:
        app.after(intervalo_verificacao_ms, verificar_arquivos)


# ================= Botões Sidebar ==================
btn_arquivos = ctk.CTkButton(frame_sidebar, text="Arquivo parado na pasta", fg_color="gray30",
                              hover_color="gray40", command=lambda: frame_arquivo_parado_pasta.lift())
btn_arquivos.pack(fill="x", pady=5, padx=10)



btn_adicionar_pasta = ctk.CTkButton(frame_sidebar, text="➕ Adicionar Pasta", command=adicionar_pasta)
btn_adicionar_pasta.pack(pady=5, padx=10, fill="x")

extensao_option = ctk.CTkOptionMenu(frame_sidebar, values=extensoes_disponiveis,
                                     command=atualizar_extensoes)
extensao_option.pack(pady=5, padx=10, fill="x")
extensao_option.set(".xml")

intervalo_label = ctk.CTkLabel(frame_sidebar, text="⏳ Intervalo (min):")
intervalo_label.pack(pady=(15, 0), padx=10)

intervalo_entry = ctk.CTkEntry(frame_sidebar, placeholder_text="10")
intervalo_entry.pack(padx=10, fill="x")

btn_atualizar_intervalo = ctk.CTkButton(frame_sidebar, text="Atualizar Intervalo", command=atualizar_intervalo)
btn_atualizar_intervalo.pack(pady=5, padx=10, fill="x")



btn_forcar = ctk.CTkButton(frame_arquivo_parado_pasta, text="Forçar Verificação Agora",
                            fg_color="#1a8cff", hover_color="#0059b3", command=forcar_verificacao)
btn_forcar.pack(pady=5, padx=10, fill="x")

btn_pausar = ctk.CTkButton(frame_arquivo_parado_pasta, text="⏸️ Pausar Verificação",
                            fg_color="#b30000", hover_color="#800000", command=pausar_verificacao)
btn_pausar.pack(pady=5, padx=10, fill="x")

btn_retomar = ctk.CTkButton(frame_arquivo_parado_pasta, text="▶️ Retomar Verificação",
                             fg_color="#007a33", hover_color="#005226", command=retomar_verificacao)
btn_retomar.pack(pady=5, padx=10, fill="x")

# ================= Start ==================
verificar_arquivos()

app.mainloop()
