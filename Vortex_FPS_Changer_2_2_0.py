import customtkinter as ctk
import re
import os
import sys

VERSAO_APP = "2.2.0"
DESENVOLVEDOR = "Developed By NocDark"

def obter_caminho_roblox():
    return os.path.join(
        os.environ["LOCALAPPDATA"],
        "Roblox",
        "GlobalBasicSettings_13.xml"
    )

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
        
    return os.path.join(base_path, relative_path)


class FPSChangerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        COR_BARRA_LATERAL = "#E53935"
        COR_FUNDO_PRINCIPAL = "#424242"
        COR_FUNDO_JANELA = "#2E2E2E"
        COR_TEXTO_PADRAO = "white"
        COR_BOTAO_APLICAR = "#007bff"

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue") 

        self.title(f"Vortex - Roblox FPS Changer v{VERSAO_APP}")
        
        self.geometry("600x400") 
        self.resizable(False, False)
        self.configure(fg_color=COR_FUNDO_JANELA)
        
        try:
            caminho_icone = resource_path('Vortex_icon.ico')
            self.iconbitmap(caminho_icone)
        except Exception:
            pass
        
        self.entrada_var = ctk.StringVar(value="")
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, 
                                          width=150, 
                                          corner_radius=0, 
                                          fg_color=COR_BARRA_LATERAL)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, 
                                       text="VORTEX", 
                                       font=ctk.CTkFont(size=20, weight="bold"),
                                       text_color="white")
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.sidebar_button_fps = ctk.CTkButton(self.sidebar_frame, 
                                                text="FPS Changer",
                                                command=lambda: None,
                                                fg_color=COR_FUNDO_PRINCIPAL,
                                                hover_color=COR_FUNDO_PRINCIPAL,
                                                text_color=COR_TEXTO_PADRAO,
                                                corner_radius=0,
                                                height=40)
        self.sidebar_button_fps.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        self.main_frame = ctk.CTkFrame(self, 
                                       corner_radius=0, 
                                       fg_color=COR_FUNDO_PRINCIPAL)
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=0)
        self.main_frame.grid_rowconfigure(2, weight=5)
        
        self.label_fps_atual = ctk.CTkLabel(self.main_frame, 
                                            text="Current FPS: Reading...",
                                            text_color="gray",
                                            font=ctk.CTkFont(size=12))
        self.label_fps_atual.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="nw")
        
        self.input_container = ctk.CTkFrame(self.main_frame, fg_color=COR_FUNDO_PRINCIPAL)
        self.input_container.grid(row=1, column=0, padx=20, pady=(20, 5), sticky="") 

        self.label_fps_limit = ctk.CTkLabel(self.input_container,
                                            text="FPS Limit:",
                                            font=ctk.CTkFont(size=18),
                                            text_color=COR_TEXTO_PADRAO)
        self.label_fps_limit.pack(side="left", padx=(0, 10))

        self.entry_fps = ctk.CTkEntry(self.input_container,
                                            textvariable=self.entrada_var,
                                            width=100,
                                            height=35,
                                            corner_radius=20,
                                            fg_color=COR_TEXTO_PADRAO,
                                            text_color=COR_FUNDO_PRINCIPAL,
                                            justify='center',
                                            font=ctk.CTkFont(size=16, weight="bold"))
        self.entry_fps.pack(side="left")
        self.entry_fps.focus_set()
        
        self.btn_aplicar_fps = ctk.CTkButton(self.input_container, 
                                            text="Apply FPS",
                                            command=self.apply_fps,
                                            fg_color=COR_BOTAO_APLICAR,
                                            hover_color="#0056b3",
                                            text_color="white",
                                            corner_radius=20,
                                            height=35,
                                            font=ctk.CTkFont(size=14, weight="bold"))
        self.btn_aplicar_fps.pack(side="left", padx=(15, 0))

        self.button_reset = ctk.CTkButton(self.main_frame,
                                          text="Reset to 60 FPS (Default)",
                                          command=lambda: self.apply_fps(valor="60"),
                                          fg_color="#333333", 
                                          hover_color="#555555",
                                          corner_radius=10,
                                          width=200,
                                          height=30,
                                          font=ctk.CTkFont(size=12))
        self.button_reset.grid(row=2, column=0, pady=(10, 0), sticky="n")

        self.label_status = ctk.CTkLabel(self.main_frame, 
                                         text="", 
                                         text_color="white",
                                         font=ctk.CTkFont(size=14, weight="bold"))
        self.label_status.grid(row=2, column=0, pady=(0, 20), sticky="s")

        
        self.label_version = ctk.CTkLabel(self,
                                            text=f"Version {VERSAO_APP}",
                                            font=ctk.CTkFont(size=12),
                                            text_color="gray")
        self.label_version.grid(row=1, column=0, padx=(45, 5), pady=5, sticky="sw") 

        self.label_developer = ctk.CTkLabel(self,
                                                text=DESENVOLVEDOR,
                                                font=ctk.CTkFont(size=12),
                                                text_color="gray")
        self.label_developer.grid(row=1, column=1, padx=(5, 45), pady=5, sticky="se")


        self.get_current_fps()

    def exibir_status(self, mensagem, cor):
        self.label_status.configure(text=mensagem, text_color=cor)
        self.label_status.after(4000, lambda: self.label_status.configure(text=""))

    def obter_caminho_roblox(self):
        return os.path.join(
            os.environ["LOCALAPPDATA"],
            "Roblox",
            "GlobalBasicSettings_13.xml"
        )
    
    def get_current_fps(self):
        caminho = self.obter_caminho_roblox()
        
        try:
            with open(caminho, "r", encoding="utf-8") as arquivo:
                conteudo = arquivo.read()

            match = re.search(r'<int name="FramerateCap">(\d+)</int>', conteudo)
            
            if match:
                fps_atual = match.group(1)
                self.label_fps_atual.configure(text=f"Current FPS: {fps_atual}")
            else:
                self.label_fps_atual.configure(text="Current FPS: Not found in file.")
                self.exibir_status("WARNING: FPS Cap not found. Apply to create.", "yellow")
        
        except FileNotFoundError:
            self.label_fps_atual.configure(text="Current FPS: File not found.")
            self.exibir_status("ERROR: Roblox file not found. Open the game first.", "red")
        except Exception:
            self.label_fps_atual.configure(text="Current FPS: Reading error.")

    def apply_fps(self, valor=None):
        caminho = self.obter_caminho_roblox()
        
        novo_valor = valor if valor is not None else self.entrada_var.get().strip()

        if not novo_valor.isdigit():
            self.exibir_status("ERROR: Enter numbers only (e.g., 540)", "red")
            return

        try:
            with open(caminho, "r", encoding="utf-8") as arquivo:
                conteudo = arquivo.read()

            novo_conteudo = re.sub(
                r'(<int name="FramerateCap">)\d+(</int>)',
                rf'\g<1>{novo_valor}\2',
                conteudo
            )

            if conteudo == novo_conteudo:
                tag_inserir = f'\n    <int name="FramerateCap">{novo_valor}</int>'
                
                if '</Settings>' in conteudo:
                    novo_conteudo = conteudo.replace('</Settings>', f'{tag_inserir}\n</Settings>')
                else:
                    self.exibir_status("ERROR: Unexpected Roblox XML structure.", "red")
                    return

            with open(caminho, "w", encoding="utf-8") as arquivo:
                arquivo.write(novo_conteudo)

            self.exibir_status(f"Success! FPS changed to {novo_valor}", "#4CAF50") 
            self.get_current_fps()

        except FileNotFoundError:
            self.exibir_status(
                "ERROR: File not found. Make sure Roblox has been opened.", 
                "red"
            )
        except PermissionError:
            self.exibir_status(
                "CRITICAL ERROR: Run the program as Administrator!", 
                COR_BARRA_LATERAL
            )
        except Exception as e:
            self.exibir_status(f"Unexpected Error: {e}", "red")

if __name__ == "__main__":
    app = FPSChangerApp()
    app.mainloop()