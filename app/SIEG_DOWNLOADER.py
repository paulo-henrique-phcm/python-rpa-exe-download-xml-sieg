"""para criar um executavel usei o pyinstaller da forma mais simples possivel

- USAREMOS O PYINSTALLER, ENTÃO INSTALE-O
pip install pyinstaller

- USANDO COMAND LINE
pyinstaller --noconsole --onefile --icon='./src/images/logo.ico' 'SIEG_DOWNLOADER.py'

- USANDO O SPEC (RECOMENDADO)
cd app
pyinstaller 'SIEG_DOWNLOADER.spec'

"""

from src.utils.frames_interfaces import *
from src.utils.frames_interfaces_downloader import *
import threading, time, json, base64, platform
from customtkinter import CTkFont
import logging, os

from src.config import LOGS, LogTipo


class App(CTk):
    def __init__(self):
        super().__init__()
        self.full_screen()
        self.current_path = os.path.dirname(os.path.abspath(sys.argv[0]))
        self.ico_logo_img = os.path.join(
            self.current_path, "src", "images", "logo.ico"
        )

        # ----------------- CONFIGURAÇÃO DE LOGGER

        if platform.system() == "Linux":
            logger_file_path = "./src/logs_xml_sieg_downloader.log"
        else:
            path = os.path.join(
                self.current_path, "src", "logs_xml_sieg_downloader.log"
            )
            if not os.path.exists(path):
                os.mkdir(path)

            logger_file_path = path

        logging.basicConfig(
            filename=logger_file_path,
            format="%(asctime)s %(message)s",
            filemode="a",
            encoding="utf-8",
        )
        logging.info(f"------------- INICIO")
        self.logger = logging.getLogger()  # Creating an object
        self.logger.setLevel(logging.INFO)

        # ----------------- CONFIGURAÇÃO DE LOGGER

        # fonte_padrao = CTkFont(family="Montserrat", size=18)
        # self.configure(font=fonte_padrao)

        # padrao_fonte = CTkFont(family="Montserrat", size=18)
        # self.option_add("*Font", padrao_fonte)

        self.VARS: dict = {}

        self.BAIXANDO: bool = False
        self.msg_erro_text: str = ""

        self.cache_file_path: str
        # CONFIGURAÇÃO DE CACHE JSON
        if platform.system() == "Linux":
            self.cache_file_path = "./src/cache.json"
        else:
            self.cache_file_path = os.path.join(self.current_path, "src", "cache.json")

        self.iconbitmap(self.ico_logo_img)

        self.title("Download SIEG")
        # self.grid_columnconfigure((0, 1), weight=1)

        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 5), weight=0)
        self.grid_rowconfigure(4, weight=2)

        # CABEÇALHO
        self.cabecaclho = CabecalhoFrame(self)
        self.cabecaclho.grid(row=0, column=0, padx=(0, 0), pady=(0, 10), sticky="nwe")
        # DIRETORIO
        self.dir_salva = DiretorioSalvamentoFrame(self)
        self.dir_salva.grid(row=1, column=0, padx=(0, 0), pady=(0, 10), sticky="nwe")
        # USUARIO SENHA
        self.usuario = UsuarioSenhaFrame(self)
        self.usuario.grid(row=2, column=0, padx=(0, 0), pady=(0, 10), sticky="nwe")
        # COMBOBOX
        self.combobox = ComboBoxFrame(self)
        self.combobox.grid(row=3, column=0, padx=(0, 0), pady=(0, 10), sticky="nwe")
        # TEXTAREA NFE, CTE...
        self.textarea = TextAreaFrame(self)
        self.textarea.grid(row=4, column=0, padx=(0, 0), pady=(0, 10), sticky="nswe")
        # # RODAPE
        # self.rodape = RodaPeFrame(self)
        # self.rodape.grid(row=5, column=0, padx=(0, 0), pady=(0, 10))

        # carrega para os campos da tela, os dados do cache.json caso exista
        self.load_cache_from_json()

        # com os dados carregados no dict, setta eles para a tela
        self.set_all_vars_to_tela_from_VARS()

        self.rodape_status = StatusDownloadFrame(self)
        self.rodape_status.grid(row=5, column=0, padx=(0, 0), pady=(0, 10), sticky="we")

        # print(json.dumps(self.get_all_vars_from_tela(), indent=4))

        # MOSTRA UMA MENSAGEM DE BOAS VINDAS
        ToplevelWindow(
            TITULO="Download",
            SUBTITULO="Esta aplicação te ajudará a baixar XML's do portal SIEG",
            MENSAGEM="""\nPara baixar XML's do tipo NFE ou CTE, basta colar na aba NF-e e/ou CT-e, as chaves que deseja baixar.

Você pode separar os itens por vírgula ',' ou Enter (um por linha).

Ao clicar em baixar, aguarde o processo, e pronto!""",
            TEXTO_BOTAO="Entendi!",
        )

    def get_VARS(self):
        """retorna uma copia do atual VARS dessa classe"""
        return self.VARS

    def set_all_vars_to_tela_from_VARS(self):
        """Pega os dados carregados no dict self.VARS e preenche nos campos da tela"""
        self.cabecaclho.set_custom()
        self.dir_salva.set_custom()
        self.usuario.set_custom()
        self.combobox.set_custom()
        self.textarea.set_custom()

        # self.usuario.set_usuario_current_value()
        # self.usuario.set_senha_current_value()

    def get_all_vars_from_tela(self):
        """Carega em um dict com todas as variaveis dos campos da tela"""
        all_vars = {}

        all_vars.update(self.cabecaclho.get_custom())
        all_vars.update(self.dir_salva.get_custom())
        user, psw = self.usuario.get_custom()
        all_vars.update(
            {
                "USERNAME_": self.codificar_base64(user),
                "PASSWORD_": self.codificar_base64(psw),
            }
        )
        all_vars.update(self.combobox.get_custom())
        all_vars.update(self.textarea.get_custom())

        return all_vars

        # https://cofre.sieg.com/ajax/downloadxml?nfe=51230900445400000100550010006725131901091010
        # https://cofre.sieg.com/ajax/downloadxml?cte=51230940065524000185570010000080371142643545

        # self.USERNAME = "ti@agroamazonia.com"
        # self.PASSWORD = "@!35#aZ67"

    def define_VARS_from_tela(self):
        """Obtém os dados da tela e depois atualiza o VARS com esses novos dados"""
        all_vars = self.get_all_vars_from_tela()
        self.VARS = all_vars

    def full_screen(self):
        # Obtém as dimensões da tela
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Define as dimensões da janela para as dimensões da tela
        self.geometry(f"{screen_width-100}x{screen_height-150}+0+0")
        # self.attributes("-fullscreen", True)

    def alternar_tema(self):
        # Verifica se está no tema "dark" e alterna para "light", e vice-versa
        if self.cabecaclho.switch.get() == "off":
            customtkinter.set_appearance_mode("light")
        else:
            customtkinter.set_appearance_mode("dark")

    def load_cache_from_json(self):
        # carrega os dados armazenados no json da aplicação
        try:
            if os.path.exists(self.cache_file_path):
                with open(self.cache_file_path, "r") as file:
                    data: dict = json.load(file)

                    # if USERNAME := data.get("USERNAME_", ""):
                    #     data["USERNAME"] = self.decodificar_base64(USERNAME)
                    # if PASSWORD := data.get("PASSWORD_", ""):
                    #     data["PASSWORD"] = self.decodificar_base64(PASSWORD)

                    self.VARS.update(data)

        except Exception as error:
            # raise ValueError(error)

            LOGS.registra_log(
                f"Ocorreu um erro durante o load dos dados do usuario \n    {error}",
                LogTipo.ERROR,
            )

    def save_cache_to_json(self):
        try:
            if self.VARS:
                # Salva os dados no arquivo JSON da aplicação

                # Carrega os dados existentes, se o arquivo existir
                if os.path.exists(self.cache_file_path):
                    try:
                        with open(self.cache_file_path, "r") as file:
                            existing_data = json.load(file)
                    except:
                        # caso nao consiga carregar o json, cria um novo
                        existing_data = {}
                else:
                    # caso nao exista nenhum json, cria um novo
                    existing_data = {}

                existing_data.update(self.VARS)

            else:
                # caso nao exista VARS por algum motivo, cria um novo
                existing_data = {}

            # Salva os dados atualizados no arquivo
            with open(self.cache_file_path, "w") as file:
                json.dump(existing_data, file, indent=4)

        except Exception as error:
            # raise ValueError(error)
            LOGS.registra_log(
                f"Ocorreu um erro durante o save dos dados do usuario \n    {error}",
                LogTipo.ERROR,
            )

    def start_check_salva(self):
        # define VARS
        self.define_VARS_from_tela()

        if not self.VARS.get("SALVA_USR_PSW"):
            # salva um novo arquivo sem nenhum dado de usuario e senha
            self.VARS["USERNAME_"] = ""
            self.VARS["PASSWORD_"] = ""

        self.save_cache_to_json()

    def codificar_base64(self, senha):
        """Codifica uma string usando base64."""
        senha_bytes = senha.encode()
        senha_codificada = base64.b64encode(senha_bytes).decode()
        return senha_codificada

    def decodificar_base64(self, senha_codificada):
        """Decodifica uma string previamente codificada em base64."""
        senha_bytes = base64.b64decode(senha_codificada.encode())
        senha_decodificada = senha_bytes.decode()
        return senha_decodificada


if __name__ == "__main__":
    app = App()
    app.mainloop()
