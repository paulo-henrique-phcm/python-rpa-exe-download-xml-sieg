## Olá comunidade!
Esta aplicação que fiz ajudará aqueles que precisam baixar grande quantidade de XML's de notas fiscais através do SIEG. Esper que seja útil!
Sinta-se a vontade para clonar o repositório e modificar a aplicação para suas necessidades.

# Motivação para criar a aplicação
O portal SIEG é muito usado no mundo fiscal. Ele disponibiliza API's que nos possibilitam baixar XML's de notas fiscais, porém com limitações. Por exemplo, não podemos baixar notas específicas, somente todas as notas cadastradas num intervalo específico.
O mesmo problema acontece quando se trata de baixar pela sua interface. Se desejar baixar uma grande quantidade de notas, como >= 100, você precisa criar 1 filtro para cada uma e buscar de forma maçante.

Pensando nesse problema enfrentado, decidi usar automação para fazer esse papel para você de forma automática!

# Apresentação da interface
A imagem abaixo mostra como é a interface da aplicação. Nela podemos ver os seguintes campos:
- 1 - Seleção do diretório onde serão salvos os arquivos XML baixados
- 2 - Usuário e Senha do Sieg. Essas informações somente serão usadas pela automação para realizar login no portal e usar a sessão aberta para fazer os downloads.
	- Elas somente serão salvas codificadas em base64 em um arquivo chamado cache.json caso você escolha a opção "Lembrar Dados preenchidos", caso contrário, você terá que fornecer usuário e senha sempre que for usar.
- 3 - "Lembrar Dados preenchidos" armazena todasas informações preenchidas incluindo diretório de salvamento, usuário, senha, checkbox e chaves de XML preenchidas. Tudo fica salvo no arquivo cache.json.
- 4 - "Mostrar interface Web" Mostra a automação sendo executada no navegador.
- 5 - NF-e e CT-e, são as abas onde você fornecerá as chaves XML válidas para serem baixadas, note que existe a separação entre os tipos de nota.
	- Você pode separar as chaves por "," (vírgula) e/ou "Enter", por exemplo:
		- 00000000000000000000000000000000000000000000, 00000000000000000000000000000000000000000000
![image](https://github.com/paulo-henrique-phcm/python-rpa-exe-download-xml-sieg/assets/56412714/9294a56e-6a15-4429-bde9-8444b1b987a5)

Após as informações preenchidas corretamente, Basta clicar em Baixar XML's, que a automação se inicia. Caso alguma informação estiver incorreta o erro será informado no texto logo abaixo do botão.
Os arquivos baixados estarão disponíveis no diretório selecionado. Caso nenhum for selecionado, a própria aplicação criará uma pasta chamada "xmls_baixados" no seu próprio diretório.

# Aplicação
A solução foi desenvolvida em Python usando principalmente:
- `costomtkinter` para contruir a interface amigável para o usuário;
- `selenium` para acessar o portal web e criar uma sessão para permitir o download;
- `pyinstaller` para criar um executável de toda a estrutura.

## Arquitetura e estrutura
Como foi uma das minhas primeiras aplicações do tipo, usei uma arquitetura básica para aplicações python que consiste:
- Diretório `app` onde está o entrypoint, sendo ele o arquivo `SIEG_DOWNLOAD.py`, que contém a estrutura base da aplicação tkinter e chama os frames que compõem a interface e suas funcionalidades.
- `src` que contém dependencias como `packages`, `modules` e outros arquivos personalizados necessários.
	- Dentro dele temos `utils` onde encontram-se módulos que compoêm frames do tkinter, classes de Logs, Popups e outros.
O arquivo `SIEG_DOWNLOADER.spec` contém as configuraões usadas pelo pyinstaller para criar o exe.

## Exceutando desenvolvimento
Caso deseje modificar a aplicação, basta clonar o repositório.
Assumindo que você está no windows, após clonar, você precisará criar um ambiente virtual com as dependências, poara isso poderá usar `python -m venv venv-downloader` por exemplo.

Após acessar o ambiente, instale as dependências que eu usei usando `pip install -r requirements.txt`. Com isso bastará executar `SIEG_DOWNLOADER.py` que a aplicação iniciará diretamente.

## Compilando um novo .exe
Feitas suas modificações, basta usar o pyinstaller. O arquivo .spec possui as expecificações de compilação, portanto basta navegar até a pasta onde ele se encontra `cd app/` (é importante estar dentro do diretório app para que ele possa copiar as dependencias corretamente) em seguida executar `pyinstaller 'SIEG_DOWNLOADER.spec'`.

Espero que a aplicação seja útil para muitos. Caso tenham dúvidas, entrem em contato comigo em https://www.linkedin.com/in/paulo-henrique-cassiano-machado



