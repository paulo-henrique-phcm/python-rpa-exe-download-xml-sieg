import sys, os, logging
from datetime import datetime


class LogTipo:
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LoggerRPA:
    def __init__(
        self,
        folder_logs: str = "",
        nome_arq_log: str = "",
        mostra_logs: bool = True,
        nivel_logger=logging.INFO,
    ):
        """Classe responsável por gerenciar logs. Ela printa na tela
        e salva no arquivo de log. Ela também controla o registro de prints em caso de erros
        Args:
            - folder_logs: O direório onde serão salvos os LOGS/prints
                - Dentro dele sera criado o diretorio images, onde ficarão os prints
            - nome_arq_log: Nome do arquivo .log com a extensão, a ser gerado no diretorio
            - mostra_logs: Se os logs serão mostrados no output do sistema.
            - nivel_logger: define o nivel de logs de logging do python.
            - bot: Recebe a instancia do bot (pode ser direto ou por self)
                - (Obrigatório) será atribuido ao usar o metodo do PBot (atribuir_logger())
        Returns:
            - Não possui retorno
        """
        self.folder_logs = folder_logs
        if not os.path.exists(self.folder_logs):
            os.makedirs(self.folder_logs)

        self.nome_arq_log = nome_arq_log
        self.mostra_logs = mostra_logs
        # self.logger = logging.getLogger(name)
        # self.logger.setLevel(logging.DEBUG)
        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # ch = logging.StreamHandler()
        # ch.setFormatter(formatter)
        # self.logger.addHandler(ch)

        self.full_file_path = os.path.join(self.folder_logs, self.nome_arq_log)
        # with open(self.full_file_path, "w") as arquivo_log:
        #     pass  # Isso cria um arquivo vazio, já que não há conteúdo a ser escrito

        logging.basicConfig(
            filename=self.full_file_path,
            format="%(asctime)s %(message)s",
            filemode="a",
            encoding="utf-8",
        )
        logging.info(f"------------- INICIO   ->  {self.nome_arq_log}")
        self.logger = logging.getLogger()  # Creating an object
        self.logger.setLevel(nivel_logger)  # Setting the threshold of logger to DEBUG
        # self.logger.setLevel(logging.ERROR)  # Setting the threshold of logger to DEBUG

    # def log(self, message):
    #     self.logger.info(message)

    def gerar_string_now(self):
        """Gera uma string contendo data e hora atuais
        Returns:
            - string no formato  %Y-%m-%d_%H-%M-%S
        """
        agora = datetime.now()
        data_completa = agora.strftime("%Y-%m-%d")
        hora = agora.strftime("%H-%M-%S")
        return f"{data_completa}_{hora}"

    def registra_log(self, msg: str, type: LogTipo):
        """Registra o log em sí. Cria a mensagem com um prefixo;
        registra print e mostra a mensagem na tela.
        Args:
            - msg: A mensagem em sí que será registrada
            - type: o tipo de log
        Returns:
            - O caminho do print gerado caso registra_print for True
            - Caso contrário, não retorna nada
        """

        try:
            if type == LogTipo.DEBUG:
                self.logger.debug("[D] " + msg)
            elif type == LogTipo.INFO:
                self.logger.info("[I] " + msg)
            elif type == LogTipo.WARNING:
                self.logger.warning("[W] " + msg)
            elif type == LogTipo.ERROR:
                self.logger.error("[E] " + msg)
            elif type == LogTipo.CRITICAL:
                self.logger.critical("[C] " + msg)

            else:
                print("------------ [erro interno de codigo] tipo de log invalido")

            if self.mostra_logs == True:
                print(msg)

        except Exception as e2:
            print(f"Erro ao registrar print:\n    -> {e2}")
