# BlockVision
Ferramenta educacional para ensino de processamento digital de imagens utilizando diagrama de blcos

## Descrição

BlockVision é uma ferramenta educacional desenvolvida em Python utilizando PyQt5. A aplicação permite a criação de diagramas de blocos para ilustrar operações de processamento digital de imagens. Cada bloco representa uma função específica da biblioteca OpenCV, como carregar uma imagem, aplicar um kernel de convolução e visualizar o resultado.

## Funcionalidades

- **Carregar Imagem:** Permite carregar uma imagem a partir do sistema de arquivos.
- **Exibir Imagem:** Mostra a imagem carregada na interface do usuário.
- **Kernel de Convolução:** Define e aplica um kernel de convolução personalizado à imagem carregada.
- **Convolução:** Aplica a operação de convolução usando o kernel definido.
- **Conectar Blocos:** Conecta diferentes blocos para criar um fluxo de operações.

## Instalação

Para instalar e executar a aplicação, siga os passos abaixo:

1. Clone o repositório:
   ```bash
   git clone https://github.com/AugustMatt/BlockVision.git

2. Navegue até o diretório do projeto:
    ```bash
    cd BlockVision

3. Crie um ambiente virtual (opcional, mas recomendado):
    ```bash
    python -m venv venv

4. Ative o ambiente virtual:
    * No Windows (PowerShell):
        c

    Ou, no cmd (Prompt de Comando):
        ```bash
        venv\Scripts\activate

    * No macOS e Linux:
        ```bash
        source venv/bin/activate

5. Instale as dependências:
    ```bash
    pip install -r requirements.txt

## Como Usar

1. Execute o arquivo principal para iniciar a aplicação:
    ```bash
    python main.py

2. Utilize a interface gráfica para carregar imagens, aplicar convoluções e visualizar os resultados.

## Contribuição

Contribuições são bem-vindas! Se você deseja contribuir, por favor siga os passos abaixo:

1. Faça um fork do repositório.

2. Crie uma nova branch:
    ```bash
    git checkout -b minha-nova-funcionalidade

3. Faça suas modificações e commit:
    ```bash
    git commit -m 'Adiciona nova funcionalidade'

4. Envie para o branch original:
    ```bash
    git push origin minha-nova-funcionalidade

5. Crie um pull request.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.