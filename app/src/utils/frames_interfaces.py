from customtkinter import (
    CTk,
    CTkFrame,
    CTkCheckBox,
    CTkButton,
    CTkLabel,
    StringVar,
    CTkRadioButton,
    BooleanVar,
    CTkEntry,
    CTkTextbox,
    CTkSwitch,
    CTkImage,
    CTkLabel,
    filedialog,
)
from PIL import Image
import customtkinter, os, sys


class CabecalhoFrame(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grid_columnconfigure(0, weight=1)
        self.configure(fg_color="transparent")
        self.logo_img = os.path.join(master.current_path, "src", "images", "logo.png")

        self.var_modo_escuro = StringVar(value="on")

        self.my_image = CTkImage(
            light_image=Image.open(self.logo_img),
            dark_image=Image.open(self.logo_img),
            size=(30, 30),
        )

        self.image_label = CTkLabel(
            master, image=self.my_image, text=""
        )  # display image with a CTkLabel
        self.image_label.grid(
            row=0, column=0, padx=(10, 10), pady=(10, 20), sticky="nw"
        )

        self.switch = CTkSwitch(
            self,
            text="Modo Escuro",
            command=master.alternar_tema,
            variable=self.var_modo_escuro,
            onvalue="on",
            offvalue="off",
        )
        self.switch.grid(row=0, column=1, padx=(10, 10), pady=(10, 10), sticky="ne")

    def get_custom(self) -> dict:
        return {"MODO_ESCURO": self.var_modo_escuro.get()}

    def set_custom(self):
        self.var_modo_escuro.set(self.master.VARS.get("MODO_ESCURO", "on"))


class DiretorioSalvamentoFrame(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grid_columnconfigure(0, weight=1)
        self.configure(fg_color="transparent")

        self.var_input_diretorio = customtkinter.StringVar(value="")

        self.label_diretorio = CTkLabel(
            self, text="Diretório de Salvamento", fg_color="transparent"
        )
        self.label_diretorio.grid(
            row=0, column=0, padx=(10, 10), pady=(0, 0), sticky="w"
        )

        frame_horizontal = CTkFrame(self)
        # faz a sefgunda coluna desse frame ter prioridade na expansao
        frame_horizontal.grid_columnconfigure(1, weight=2)
        frame_horizontal.grid(row=1, column=0, padx=(10, 10), pady=(5, 0), sticky="new")
        frame_horizontal.configure(fg_color="transparent")

        self.label_diretorio = CTkButton(
            frame_horizontal,
            text="Selecionar Diretório",
            command=self.dialog_load_save_directory,
        )
        self.label_diretorio.grid(
            row=0, column=0, padx=(10, 10), pady=(5, 5), sticky="w"
        )

        self.input_diretorio = CTkEntry(
            frame_horizontal,
            placeholder_text="Ex.: C:\Documentos\...",
            placeholder_text_color="gray40",
            textvariable=self.var_input_diretorio,
        )
        self.input_diretorio.grid(
            row=0, column=1, padx=(10, 10), pady=(5, 5), sticky="we"
        )

    def dialog_load_save_directory(self):
        DOWNLOAD_DIR_temp = filedialog.askdirectory()

        self.DOWNLOAD_DIR = os.path.normpath(DOWNLOAD_DIR_temp)

        self.input_diretorio.delete(0, customtkinter.END)
        self.input_diretorio.insert(0, self.DOWNLOAD_DIR)

    def get_custom(self) -> dict:
        return {"DOWNLOAD_DIR": self.var_input_diretorio.get()}

    def set_custom(self):
        self.var_input_diretorio.set(self.master.VARS.get("DOWNLOAD_DIR", ""))

    def set_direct(self):
        self.input_diretorio.delete(0, customtkinter.END)
        self.input_diretorio.insert(0, self.master.DOWNLOAD_DIR)


class UsuarioSenhaFrame(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grid_columnconfigure((0, 1), weight=1)

        self.var_input_usuario = customtkinter.StringVar(value="")
        self.var_input_senha = customtkinter.StringVar(value="")

        # CAMPO USUARIO
        self.label_usuario = CTkLabel(
            self, text="* Usuário Sieg:", fg_color="transparent"
        )
        self.label_usuario.grid(row=0, column=0, padx=(10, 10), pady=(0, 0), sticky="w")

        self.input_usuario = CTkEntry(
            self,
            placeholder_text="Ex.: email@email.com",
            placeholder_text_color="gray40",
            textvariable=self.var_input_usuario,
        )
        self.input_usuario.grid(
            row=1, column=0, padx=(10, 10), pady=(5, 10), sticky="we"
        )

        # CAMPO SENHA
        self.label_senha = CTkLabel(self, text="* Senha Sieg:", fg_color="transparent")
        self.label_senha.grid(row=0, column=1, padx=(10, 10), pady=(0, 0), sticky="w")

        self.input_senha = CTkEntry(
            self,
            placeholder_text="****",
            placeholder_text_color="gray40",
            show="*",
            textvariable=self.var_input_senha,
        )
        self.input_senha.grid(row=1, column=1, padx=(10, 10), pady=(5, 10), sticky="we")

    def get_custom(self) -> dict:
        return self.var_input_usuario.get(), self.var_input_senha.get()

    def set_custom(self):
        self.var_input_usuario.set(
            self.master.decodificar_base64(self.master.VARS.get("USERNAME_", ""))
        )
        self.var_input_senha.set(
            self.master.decodificar_base64(self.master.VARS.get("PASSWORD_", ""))
        )

    # def set_usuario_current_value(self):
    #     self.input_usuario.delete(0, customtkinter.END)
    #     self.input_usuario.insert(0, self.master.USERNAME)

    # def set_senha_current_value(self):
    #     self.input_senha.delete(0, customtkinter.END)
    #     self.input_senha.insert(0, self.master.PASSWORD)


class ComboBoxFrame(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grid_columnconfigure((0, 1), weight=1)
        self.configure(fg_color="transparent")

        self.var_check_salva = customtkinter.BooleanVar(value=False)
        self.var_check_web = customtkinter.BooleanVar(value=False)

        # CHECK SALVA USUARIO SENHA
        self.check_salvar = CTkCheckBox(
            self,
            text="Lembrar dados preenchidos? (essas informações ficarão gravadas explicitamente na aplicação)",
            variable=self.var_check_salva,
            command=self.master.start_check_salva,
        )
        self.check_salvar.grid(row=0, column=0, padx=(10, 10), pady=(5, 5), sticky="w")

        # CHECK MOSTRA WEB
        self.check_web = CTkCheckBox(
            self,
            text="Mostrar interface web? (no headless)",
            variable=self.var_check_web,
        )
        self.check_web.grid(row=1, column=0, padx=(10, 10), pady=(5, 5), sticky="w")

    def get_custom(self) -> dict:
        return {
            "SALVA_USR_PSW": self.var_check_salva.get(),
            "MODO_SEM_CABECA": self.var_check_web.get(),
        }

    def set_custom(self):
        self.var_check_salva.set(self.master.VARS.get("SALVA_USR_PSW", False))
        self.var_check_web.set(self.master.VARS.get("MODO_SEM_CABECA", False))


class TextAreaFrame(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.configure(fg_color="transparent")

        # self.var_nfe_text_area = customtkinter.StringVar(value="")
        # self.var_cte_text_area = customtkinter.StringVar(value="")

        # TABELA DE EXIBICAO
        self.tabview = customtkinter.CTkTabview(master=self)
        self.tabview.grid(row=0, column=0, padx=(10, 10), pady=(5, 5), sticky="nswe")

        self.tabview.add("NF-e")  # cria a tab nfe
        self.tabview.add("CT-e")  # cria a tab cte
        # self.tabview.add("MDF-e")  # cria a tab cte
        # self.tabview.add("NFC-e")  # cria a tab cte
        # self.tabview.add("NFS-e")  # cria a tab cte

        self.tabview.set("NF-e")  # set currently visible tab

        # adiciona prioridades de expansão para cada linha/coluna
        self.tabview.tab("NF-e").grid_columnconfigure(0, weight=1)
        self.tabview.tab("NF-e").grid_rowconfigure(1, weight=2)

        self.tabview.tab("CT-e").grid_columnconfigure(0, weight=1)
        self.tabview.tab("CT-e").grid_rowconfigure(1, weight=2)

        # LABEL TEXTAREA NFE
        self.nfe_label = CTkLabel(
            self.tabview.tab("NF-e"),
            text="* Cole aqui as chaves XML de NF-E separadas por virgula ',' ou 'enter'",
        )
        self.nfe_label.grid(row=0, column=0, padx=(10, 10), pady=(5, 5), sticky="w")

        # TEXTAREA NFE
        self.nfe_text_area = CTkTextbox(
            master=self.tabview.tab("NF-e"), corner_radius=0, wrap="word"
        )
        self.nfe_text_area.grid(
            row=1, column=0, padx=(10, 10), pady=(5, 5), sticky="nsew"
        )

        # LABEL TEXTAREA CTE
        self.cte_label = CTkLabel(
            self.tabview.tab("CT-e"),
            text="* Cole aqui as chaves XML de CT-E separadas por ','",
        )
        self.cte_label.grid(row=0, column=0, padx=(10, 10), pady=(5, 5), sticky="w")

        # TEXTAREA CTE
        self.cte_text_area = CTkTextbox(
            master=self.tabview.tab("CT-e"), corner_radius=0, wrap="word"
        )
        self.cte_text_area.grid(
            row=1, column=0, padx=(10, 10), pady=(5, 5), sticky="nsew"
        )

    def get_custom(self) -> dict:
        # return {
        #     "CTE_TEXT_AREA": self.var_nfe_text_area.get(),
        #     "NFE_TEXT_AREA": self.var_cte_text_area.get(),
        # }
        return {
            "NFE_TEXT_AREA": self.nfe_text_area.get("1.0", "end-1c"),
            "CTE_TEXT_AREA": self.cte_text_area.get("1.0", "end-1c"),
        }

    def set_custom(self):
        # self.var_nfe_text_area.set(self.master.VARS.get("CTE_TEXT_AREA", ""))
        # self.var_cte_text_area.set(self.master.VARS.get("NFE_TEXT_AREA", ""))
        self.nfe_text_area.delete(1.0, customtkinter.END)
        self.nfe_text_area.insert(1.0, self.master.VARS.get("NFE_TEXT_AREA", ""))

        self.cte_text_area.delete(1.0, customtkinter.END)
        self.cte_text_area.insert(1.0, self.master.VARS.get("CTE_TEXT_AREA", ""))


class RodaPeFrame(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grid_columnconfigure(0, weight=1)
        self.configure(fg_color="transparent")

        # BOTAO baixar
        self.botao_salvar = CTkButton(
            # self, text="Baixar XML's", command=master.start_download
            self,
            text="Baixar XML's",
        )
        self.botao_salvar.grid(row=0, column=0, padx=(10, 10), pady=10)

        # # TEXTAREA
        # self.check_salvar = CTkTextbox(master=self, corner_radius=0, wrap="word")
        # self.check_salvar.grid(row=1, column=0, padx=(10,5), pady=(5, 5), sticky="nsew")
