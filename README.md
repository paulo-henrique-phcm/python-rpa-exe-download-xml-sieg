### Olá comunidade!
Esta aplicação que fiz ajudará aqueles que precisam baixar grande quantidade de `XML's` de notas fiscais através do `SIEG`. Esper que seja útil!
Sinta-se a vontade para clonar o repositório e modificar a aplicação para suas necessidades.

# Download Automático de XMLs do SIEG

## Visão Geral
Bem-vindo à solução de automação que desenvolvi para simplificar o processo de download de grandes volumes de XMLs de notas fiscais do SIEG. Espero que essa aplicação seja útil para você!

Sinta-se à vontade para clonar o repositório e personalizar a aplicação conforme suas necessidades.

![image](https://github.com/paulo-henrique-phcm/python-rpa-exe-download-xml-sieg/assets/56412714/9294a56e-6a15-4429-bde9-8444b1b987a5)

## Motivação
O portal SIEG é amplamente utilizado no mundo fiscal, oferecendo APIs para baixar XMLs de notas fiscais. No entanto, essas APIs têm limitações, como a incapacidade de baixar `notas específicas em grande quantidade`. O mesmo desafio se aplica à interface do portal ao tentar baixar uma grande quantidade de notas.

Para superar essas limitações, desenvolvi essa automação para facilitar o processo de download automático!

## Interface
A imagem anterior apresenta a interface da aplicação, com campos numerados para referência:
1. Seleção do diretório para salvar os XMLs baixados.
2. Usuário e senha do SIEG para efetuar login automaticamente (as informações podem ser lembradas ou fornecidas a cada uso).
3. Opção para lembrar os dados preenchidos, armazenando-os em um arquivo chamado `cache.json`.
4. Opção para mostrar a interface web durante a execução da automação.
5. Abas para fornecer as chaves XML de NF-e e CT-e para download.

## Uso da Aplicação
Após preencher as informações, clique em "Baixar XMLs" para iniciar a automação. Qualquer erro será exibido abaixo do botão. Os arquivos baixados serão salvos no diretório selecionado ou em uma pasta chamada "xmls_baixados" se nenhum diretório for especificado.

## Tecnologias Utilizadas
A aplicação foi desenvolvida em Python, utilizando principalmente:
- `customtkinter` para criar a interface amigável;
- `selenium` para acessar o portal web e facilitar o download;
- `pyinstaller` para criar um executável da aplicação.

Ela foi contruida com classes separadas e organizadas por funções.

## Arquitetura e Estrutura
A estrutura segue padrões básicos de desenvolvimento Python, com diretórios para o aplicativo e suas dependências. O arquivo `SIEG_DOWNLOADER.spec` contém as configurações para a criação do executável com o pyinstaller.

`app/src/utils/frames_interfaces_downloader.py` contém a classe responssável por controlar as Threads com `threading` para realizar o download sem afetar a estabilidade da página. Ela contém todos os disparos que chamam a classe de RPA dentre outros.
`app/src/utils/frames_interfaces.py` contém todas as classes que representam os frames que quando juntos representarão conjuntos de funções no app. Por exemplo, a primeira classe `DiretorioSalvamentoFrame` que herda de `CTkFrame` contém o botão "Selecionar Diretório" e o campo que recebe este valor.
É interessante notar também que, por herdar de `CTkFrame` ele permite construir a estrutura dentro de sí própria com `self`, além de conter métodos personalizados `GET`, `SET` e `dialog_load_save_directory`. Todos os frames seguem a mesma ideia.

`app/src/utils/logger_custom.py` é um módulo de minha autoria que fiz para controlar logs em minhas aplicações. Neste caso é uma versão simplificada e modificada para simplesmente salvar os logas em um arquivo local.
A classe `LoggerRPA` pode fazer muito mais que isso. Mas neste caso ela, em conjunto com a classe de enumeração `LogTipo` usam `logging` do próprio python para ser chamado em qualquer lugar da aplicação e registrar o log. Ela pode ser modificada para enviar emails, registrar os logs em servidores dec ontrole como o `GrayLog` ou `DataLog`.

`app/src/utils/sieg_selenium_downloader.py` contém a automação selenium em sí. Aqui a classe `SiegDownloader` contém tudo que é necessário para acessar o protal SIEG, fazer o login e baixar os arquivos passados para a instancia.



## Desenvolvimento
Se deseja modificar a aplicação, basta clonar o repositório. Para executar em ambiente de desenvolvimento, crie um ambiente virtual com `python -m venv venv-downloader`, instale as dependências com  `pip install -r requirements.txt` e execute o arquivo `SIEG_DOWNLOADER.py`.

Para compilar um novo executável, utilize o pyinstaller com as configurações presentes no arquivo `.spec` em geral basta navegar até ele com `cd app/` (é importante estar dentro do diretório app para que ele possa copiar as dependencias corretamente) e depois executar `pyinstaller 'SIEG_DOWNLOADER.spec'`.

Espero que a aplicação seja útil! Em caso de dúvidas, entre em contato comigo pelo [LinkedIn](https://www.linkedin.com/in/paulo-henrique-cassiano-machado) vamos nos conhecer melhor e compartilhar experiências.




