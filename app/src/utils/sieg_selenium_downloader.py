from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import logging

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

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
)
from PIL import Image
import customtkinter, os, sys
from src.utils.popup_message import *

from src.config import LOGS, LogTipo


class SiegDownloader:
    def __init__(self, master):
        self.master = master
        self.lista_chaves_a_serem_baixadas: list = []
        self.dict_todas_listas: dict = {}
        self.total_a_baixar: int = 0

    def baixar_xmls(self):
        try:
            self.iniciar_listas_de_downloads()

            # desabilita o botao salvar para nao clicar denovo
            self.master.botao_salvar.configure(state=customtkinter.DISABLED)

            # pass
            # print(
            #     f'---: {self.master.dir_salva.input_diretorio.get("1.0", "end-1c")}'
            #     f'---: {}'
            # )

            chrome_options = Options()
            # Configurar as opções para evitar a mensagem de aviso de download
            salva = self.master.get_VARS().get("DOWNLOAD_DIR")

            chrome_options.add_experimental_option(
                "prefs",
                {
                    "download.default_directory": salva,
                    "profile.default_content_settings.popups": 0,
                    "profile.default_content_setting_values.automatic_downloads": 1,
                    "profile.default_content_settings.popups": 2,
                    "profile.default_content_settings.javascript": 1,
                    "credentials_enable_service": False,
                    "download.prompt_for_download": False,
                    "profile.content_settings.exceptions.automatic_downloads.*.setting": 1,
                    "safebrowsing.enabled": True,
                },
            )

            if not self.master.get_VARS().get("MODO_SEM_CABECA"):
                chrome_options.add_argument("--headless")

            servico = ChromeService(ChromeDriverManager().install())

            self.driver = webdriver.Chrome(service=servico, options=chrome_options)

            # define o status de que o download iniciou
            self.master.get_VARS()["BAIXANDO"] = True
            # self.master.botao_salvar.configure(text="Cancelar Download") # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            self.master.msg_erro_text = f"Aguarde enquanto o download acontece..."
            self.master.atualiza_texto_label_info()

            # Navegar para o URL desejado
            url = "https://auth.sieg.com/login"  # Substitua pelo seu URL desejado
            self.driver.get(url)

            usr = self.master.master.decodificar_base64(
                self.master.get_VARS().get("USERNAME_")
            )
            psw = self.master.master.decodificar_base64(
                self.master.get_VARS().get("PASSWORD_")
            )

            self.master.msg_erro_text = f"Realizando Login no SIEG..."
            self.master.atualiza_texto_label_info()

            self.driver.find_element(By.NAME, "txtEmail").send_keys(usr)
            self.driver.find_element(By.NAME, "txtPassword").send_keys(psw)
            self.driver.find_element(By.NAME, "btnSubmit").click()
            sleep(1)

            # VERIFICA SE USER E SENHA ESTAO INCORRETOS
            try:
                WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            '//div[contains(text(), "senha ou e-mail fornecido não é válido")]',
                        )
                    )
                )
                senha_invalida = True
            except TimeoutException:
                senha_invalida = False

            if senha_invalida:
                # erro nos usuarios fornecidos
                msg = f"Erro ao realizar login. Parece que o usuario ou senha fonecidos não são válidos!"
                LOGS.registra_log(f"{msg}", LogTipo.ERROR)

                self.master.msg_erro_text = msg
                self.master.atualiza_texto_label_info()

                raise ValueError(msg)

            # VERIFICA SE ENTROU NA TELA PRINCIPAL (SE O LOGIN OCORREU CORRETAMENTE)
            try:
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//span[.="Todos os Serviços"]')
                    )
                )
                success_login = True
            except TimeoutException:
                success_login = False

            if not success_login:
                # não conseguiu fazer o login
                msg = (
                    f"Ocorreu ao realizar login. Algum erro ocorreu e o Sieg não logou!"
                )

                LOGS.registra_log(f"{msg}", LogTipo.ERROR)

                self.master.msg_erro_text = msg
                self.master.atualiza_texto_label_info()

                raise ValueError(msg)

            LOGS.registra_log(f"Iniciando download dos itens.", LogTipo.INFO)

            # PASSA A MOSTRAR A PROGRESSBAR SOMENTE NESSE MOMENTO
            self.master.progressbar.grid(
                row=3, column=0, padx=(40, 40), pady=10, sticky="sew"
            )
            self.master.progressbar.set(0)

            for nome_tipo_lista, lista in self.dict_todas_listas.items():
                prefix = "nfe"
                if nome_tipo_lista == "NFE_TEXT_AREA":
                    prefix = "nfe"
                elif nome_tipo_lista == "CTE_TEXT_AREA":
                    prefix = "cte"

                for i, chave in enumerate(lista):
                    try:
                        msg = f"Realizando download de [{i}/{str(self.total_a_baixar)}] - {chave}"

                        self.master.progressbar.set(i / self.total_a_baixar)

                        LOGS.registra_log(f"{msg}", LogTipo.INFO)
                        self.master.msg_erro_text = msg

                        self.master.atualiza_texto_label_info()

                        sleep(0.1)
                        url_download_xml = (
                            f"https://cofre.sieg.com/ajax/downloadxml?{prefix}={chave}"
                        )
                        self.driver.get(url_download_xml)

                        # se baixar com sucesso, remove da lista de falhas, no fim nao pode ter nenhuma

                        sleep(0.1)
                    except Exception as erro:
                        LOGS.registra_log(
                            f"Ocorreu algum erro no download de {chave}. \n{erro}",
                            LogTipo.ERROR,
                        )

            # remove o progress bar e reabilita o botao baixar
            self.master.progressbar.set(0)
            self.master.progressbar.grid_remove()
            self.master.botao_salvar.configure(state=customtkinter.NORMAL)

            # AGUARDA DOWNLOADS QUE POSSAM DEMORAR, ANTES DE VERIFICAR SE FORAM TODOS BAIXADOS,
            # E FEHAR O NAVEGADOR SOMENTE DEPOIS DISSO
            sleep(6)

            self.verifica_download_final()

            self.driver.quit()
        except Exception as error:
            try:
                sleep(1)
                # remove o progress bar e reabilita o botao baixar
                self.master.progressbar.set(0)
                self.master.progressbar.grid_remove()
                self.master.botao_salvar.configure(state=customtkinter.NORMAL)

                self.verifica_download_final()

                self.driver.quit()
            except:
                pass
            raise ValueError(
                f"Ocorreu um erro durante o download usando o navegador! \n    {error}"
            )

            # raise ValueError(error)

    def verifica_todas_chaves_foram_baixadas(self):
        """utiliza a lista_chaves_a_serem_baixadas criada em iniciar_listas_de_downloads
        e ve se todas elas estao no diretorio de downloads.
        Case algum nao esteja no diretorio, ela sera mantida na lista lista_chaves_a_serem_baixadas
        indicando que nao foi baixada, ou seja será um erro."""
        # Lista os arquivos no diretório
        arquivos_no_diretorio = os.listdir(self.master.get_VARS().get("DOWNLOAD_DIR"))
        # Obtendo apenas os nomes dos arquivos sem a extensão
        arquivos_no_diretorio = [
            os.path.splitext(arquivo)[0] for arquivo in arquivos_no_diretorio
        ]

        LOGS.registra_log(
            f"Arquivos no diretorio: {arquivos_no_diretorio}", LogTipo.INFO
        )

        # lista temporaria que sera apagada
        temp_lista_chaves_a_serem_baixadas = self.lista_chaves_a_serem_baixadas.copy()

        # Verifica a existência dos arquivos na lista dentro do diretório
        for chave in temp_lista_chaves_a_serem_baixadas:
            # se estiver no diretorio, quer dizer que baixou corretamente
            print(f"------ {chave}")
            if chave in arquivos_no_diretorio:
                print(f"removendo - {chave}")
                self.lista_chaves_a_serem_baixadas.remove(chave)
            else:
                print(f" mantendo - {chave}")

        # for arquivo in arquivos_no_diretorio:
        #     if not (arquivo in self.lista_chaves_a_serem_baixadas):
        #         print(f"removendo - {arquivo}")
        #         self.lista_chaves_a_serem_baixadas.remove(arquivo)
        #     else:
        #         print(f" mantendo - {arquivo}")

        print(self.lista_chaves_a_serem_baixadas)

        return self.lista_chaves_a_serem_baixadas

    def verifica_download_final(self):
        """verifica o diretorio se todas as chaves foram baixadas
        caso falte alguma, cria um popup mostrando quais estao faltando"""
        if self.verifica_todas_chaves_foram_baixadas():
            # se holveram falhas
            self.master.msg_erro_text = f"Download concluído, porém alguns não foram baixadas corretamente. Confira na mensagem de alerta."

            # monta mensagem com a lista de itens com erro (nao baixados)
            msg = ""
            for chave in self.lista_chaves_a_serem_baixadas:
                msg += f" - {chave}\n"

            LOGS.registra_log(
                f"Estas chaves não foram encontradas no diretorio: \n{msg}",
                LogTipo.WARNING,
            )

            ToplevelWindow(
                TITULO="Download Incompleto!",
                SUBTITULO="As chaves abaixo não foram baixadas,\nverifique se são válidas.",
                MENSAGEM=msg,
            )
        else:
            self.master.msg_erro_text = f"Download concluído!"
        # self.show_button()
        self.master.atualiza_texto_label_info()

    def iniciar_listas_de_downloads(self):
        """através da dict com várias listas de NFS (CTE, NFE...) já montadas
        concatena todas em uma unica lista de strings (chaves) para verificar depois e saber
        quantos xml no total serao baixados"""
        self.dict_todas_listas = self.master.get_VARS().get("LISTAS_NFS")

        self.total_a_baixar = 0

        # Cria um CONJUNTO
        conjunto_temporario = set(self.lista_chaves_a_serem_baixadas)

        for _, lista in self.dict_todas_listas.items():
            self.total_a_baixar += len(lista)

            # Estende o conjunto temporário com os itens da lista (isso removerá as duplicações)
            conjunto_temporario.update(lista)

        # Ao final do loop, atualizar self.lista_chaves_a_serem_baixadas com os valores únicos
        self.lista_chaves_a_serem_baixadas = list(conjunto_temporario)
