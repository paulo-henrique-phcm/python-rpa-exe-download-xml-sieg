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
    CTkProgressBar,
)
from PIL import Image
import customtkinter, os, sys, json, threading
from pathlib import Path

from src.utils.sieg_selenium_downloader import *
from src.utils.popup_message import *

from src.config import LOGS, LogTipo


class StatusDownloadFrame(CTkFrame):
    """Contém um componente que exibirá e conterá as ações de download,
    ou seja, controla a os processos de selenium. Será chamado pelo botao de download
    da tela principal."""

    def __init__(self, master):
        super().__init__(master)
        # self.master = master
        self.grid_columnconfigure(0, weight=1)
        self.configure(fg_color="transparent")

        self.toplevel_window = None

        self.SIEG = None

        self.msg_erro_text: str = ""

        # BOTAO BAIXAR
        self.botao_salvar = CTkButton(
            self,
            text="Baixar XML's",
            command=self.start_download,
        )
        self.botao_salvar.grid(row=0, column=0, padx=(10, 10), pady=10)

        # BOTAO BAIXAR
        # self.botao_cancelar = CTkButton(
        #     self,
        #     command=self.cancelar_download,
        #     text="Cancelar",
        # )
        # self.botao_cancelar.grid(row=1, column=0, padx=(10, 10), pady=10)

        # CONFIGURAÇÃO DOS BOTÕES SALVAR E CANCELAR (OCULAR)
        self.botao_salvar.configure(state=customtkinter.NORMAL)
        # self.botao_cancelar.configure(state=customtkinter.DISABLED)

        # inicialmente o botão cancelar não será exibido
        # self.botao_cancelar.grid_remove()

        # STATUS
        self.label_status = CTkLabel(
            self,
            text="Caso não informar o diretório de Salvamento, os arquivos serão baixados para o mesmo diretório da aplicação em 'xmls_baixados'.",
            text_color="gray40",
        )
        self.label_status.grid(row=2, column=0, padx=(10, 10), pady=10, sticky="we")

        self.progressbar = CTkProgressBar(self, orientation="horizontal")
        self.progressbar.grid(row=3, column=0, padx=(40, 40), pady=10, sticky="sew")
        self.progressbar.set(0)
        self.progressbar.grid_remove()

        self.VARS_STATUS: dict = master.get_VARS()

        # transforma as str em listas de chaves para serem lançadas depois. salva em self.VARS_STATUS
        self.verifica_todas_str_listas_chaves()

    def get_VARS(self):
        """retorna uma copia do atual VARS dessa classe"""
        return self.VARS_STATUS

    def atualizar_e_obter_VARS_principal(self):
        # carrega VARS da tela principal antes de iniciar o processo
        self.master.define_VARS_from_tela()

        # adiciona os novos dados carregados na tela principal na veriavel dessa classe local
        self.VARS_STATUS = self.master.get_VARS()

    def verifica_todas_str_listas_chaves(
        self, procurar_areas=["NFE_TEXT_AREA", "CTE_TEXT_AREA"]
    ):
        """Cria as listas em si de chaves já validadas para serem baixadas"""

        for area in procurar_areas:
            if str_area := self.master.VARS.get(area):
                self.VARS_STATUS.setdefault("LISTAS_NFS", {})
                self.VARS_STATUS["LISTAS_NFS"][area] = self.converte_lista(str_area)

    def converte_lista(self, str_de_lista: str) -> list:
        LISTA_CHAVES_XML = []  # limpa a lista

        def validar_chave(chave):
            """realiza o calculo para verificar se uma chave NFE, CTE é valida (usando o digito verificador)"""
            multiplicadores = [2, 3, 4, 5, 6, 7, 8, 9]
            chave_invertida = chave[::-1]  # Inverte a chave para facilitar os cálculos
            soma = 0

            for i, digito in enumerate(chave_invertida):
                multiplicador = multiplicadores[i % len(multiplicadores)]
                soma += int(digito) * multiplicador

            resto = soma % 11

            if resto in (0, 1):
                dv = 0
            else:
                dv = 11 - resto

            return dv == int(
                chave[-1]
            )  # Verifica se o dígito verificador calculado é igual ao último dígito da chave

        str_de_lista = str_de_lista.replace(" ", "")  # remove espaços
        str_de_lista = str_de_lista.replace("\n", ",")  # remove enter
        tmp_lista_chaves = str_de_lista.split(",")

        qtd_caracteres = (44, 46)
        # verifica se todos tem 44 ou 46 caracteres,
        # verifica se todos são string
        # verifica se todos são validos (digio verificador)
        # e adiciona na lista
        for chave in tmp_lista_chaves:
            if (
                isinstance(chave, str)
                and (len(chave) in qtd_caracteres)
                # and validar_chave(chave)
            ):
                LISTA_CHAVES_XML.append(chave)

        return LISTA_CHAVES_XML

    ############################
    ############################
    ######################################################## GERENCIAMENTO DO DOWNLOAD
    ############################
    ############################

    def cancelar_download():
        pass

    def start_download(self):
        self.SIEG = SiegDownloader(self)

        self.atualizar_e_obter_VARS_principal()
        erro = self.valida_campos()

        LOGS.registra_log(f"{json.dumps(self.VARS_STATUS, indent=4)}", LogTipo.INFO)

        if not erro:
            # AJUSTA ALGUNS DADOS ANTES DE PROSSEGUI

            # cria o diretorio padrao de download
            # se nao for informado
            if not self.VARS_STATUS.get("DOWNLOAD_DIR"):
                # adiciona o padrão
                self.VARS_STATUS["DOWNLOAD_DIR"] = os.path.join(
                    self.master.current_path, "xmls_baixados"
                )

            # depois de alterar a variavel, mostra ela na tela (atualizada)
            self.master.set_all_vars_to_tela_from_VARS()

            if not os.path.exists(self.VARS_STATUS.get("DOWNLOAD_DIR")):
                os.mkdir(self.VARS_STATUS.get("DOWNLOAD_DIR"))

            # SALVA OS DADOS RECEM AJUSTADOS
            if self.VARS_STATUS.get("SALVA_USR_PSW"):
                # salva os dados recem carregado em VARS somente se o check estiver marcado
                self.master.save_cache_to_json()

            # processa as srings antes de iniciar o download, pois, alguma pode ter sido digitada antes
            self.verifica_todas_str_listas_chaves()

            try:
                # self.baixar_xmls()
                LOGS.registra_log(f"Iniciando thread de download", LogTipo.INFO)
                self.thread = threading.Thread(target=self.SIEG.baixar_xmls)
                self.thread.start()

                # self.running = False
                # self.get_credentials_button.config(text="Baixar XML's")

                LOGS.registra_log(f"processo de download iniciado", LogTipo.INFO)
                self.msg_erro_text = f"Processo de download iniciado"
                self.atualiza_texto_label_info()

            except Exception as e:
                # self.get_credentials_button.config(text="Tentar baixar XML's novamente")

                self.msg_erro_text += f"""\n\nOcorreu algum erro no processo de Download usando o navegador!
        Verifique os dados fornecidos acima e tente novamente.\n
        Veja os motivos do erro nos logs em "logs_xml_sieg_downloader.log"."""

                self.atualiza_texto_label_info()
                LOGS.registra_log(
                    f"Ocorreu um erro ao tentar baixar os xmls informados: \n    {e}",
                    LogTipo.ERROR,
                )

    def atualiza_texto_label_info(self):
        self.label_status.configure(text=self.msg_erro_text)

    def valida_campos(self):
        erro = False
        self.msg_erro_text = ""

        if not self.VARS_STATUS.get("DOWNLOAD_DIR"):
            self.msg_erro_text += f"\n - Por padrão os XML's serão baixados no mesmo diretório da aplicação, pois, nenhum diretório de salvamento foi fornecido."
            # erro = True # isso nao caracteriza um erro, por isso esta desativado
        else:
            if not os.path.isdir(self.VARS_STATUS.get("DOWNLOAD_DIR")):
                erro = True
                self.msg_erro_text += f"\n - [Atenção] Forneça um diretório Válido Existente onde os arquivos serão salvos"
        if not self.VARS_STATUS.get("USERNAME_"):
            self.msg_erro_text += f"\n - [CAMPO OBRIGATÓRIO] Preencha um nome de usuário para logar no Sieg"
            erro = True
        if not self.VARS_STATUS.get("PASSWORD_"):
            self.msg_erro_text += (
                f"\n - [CAMPO OBRIGATÓRIO] Preencha uma senha para logar no Sieg"
            )
            erro = True

        # se todos os textarea de chaves esiverem vazios
        if (not self.VARS_STATUS.get("NFE_TEXT_AREA")) and (
            not self.VARS_STATUS.get("CTE_TEXT_AREA")
        ):
            erro = True
            self.msg_erro_text += f"\n - [CAMPO OBRIGATÓRIO] Forneça uma lista de chaves de XML's, separados por vírgula ','."
        # else:
        #     # converte a string fornecida em uma lista com as chaves. retorna lista vazia caso nenhum esteja válido
        #     self.converte_lista()
        #     if len(self.LISTA_CHAVES_XML) == 0:
        #         # se a lista retornar vazia
        #         erro = True
        #         self.msg_erro_text += f"""\n - [CAMPO INVÁLIDO] A lista fornecida não contém nenhuma chave válida\n
        #         voce pode seguir o exemplo: 52231040727732000100550020000004441531696880,52231040727732000100550020000004641081189691,...
        #         Não tem problema se holverem Enter ou espaços, mas as chaves devem conter 44 números."""
        #     else:
        #         # não é um erro, somente deverá mostrar quantos itens serão analisados
        #         self.msg_erro_text += f"\n {str(len(self.LISTA_CHAVES_XML))} chaves de XML foram validadas e serão baixadas."

        self.atualiza_texto_label_info()

        return erro
