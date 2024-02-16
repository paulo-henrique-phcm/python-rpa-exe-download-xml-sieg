

from src.utils.logger_custo import LogTipo, LoggerRPA
import os, sys

# o diretorio do config no pyinstaller é um diretorio temporario, nao serve
# logger_path = os.path.dirname(os.path.abspath(__file__)) 

# este ja pega o diretorio do primeiro arquivo executado .exe. então é melhor
# pegar ele e adicionar os diretorios internos
logger_path = os.path.dirname(os.path.abspath(sys.argv[0]))

LOGS = LoggerRPA(folder_logs=os.path.join(logger_path, "src"), nome_arq_log="logs_xml_sieg_downloader.log")

