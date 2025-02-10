<div align="center"> 
  <img  src="https://t.ctcdn.com.br/c9F96TE3HjZQlnWtgkcZI8fd_3w=/768x432/smart/i817043.jpeg" height="auto" width="100%"/> 
</div>

## 🎮 Sobre o jogo

Super Mario Bros é um dos jogos mais icônicos e influentes da história dos videogames, lançado pela Nintendo em 1985 para o console Nintendo Entertainment System (NES). O jogo foi criado por Shigeru Miyamoto e foi um dos primeiros jogos de plataforma a ganhar popularidade em massa, definindo o gênero e estabelecendo a base para muitos dos jogos modernos.

## 🕹️ Como o jogo funciona?

No jogo, você controla o personagem Mario, um encanador italiano, que embarca em uma jornada para salvar a Princesa Peach do vilão Bowser, o Rei dos Koopas. A história se passa no Reino do Cogumelo, onde Bowser sequestrou a princesa e transformou seus habitantes em blocos e objetos mágicos.

## 🛠️ Instalação e dependências

Para executar o código, é necessário instalar algumas dependências. Siga os passos abaixo para preparar seu ambiente:

### 📌 Instalando as dependências

Execute os seguintes comandos no terminal:

```sh
pip install pygame
pip install pyfiglet
```

### 🔊 Verificando e instalando o PulseAudio (Linux)

Para garantir que o PulseAudio esteja instalado corretamente, execute:

```sh
pulseaudio --version
```

Se o PulseAudio não estiver instalado, use os seguintes comandos para atualizar os pacotes e instalar:

```sh
sudo apt update && sudo apt install pulseaudio
```

## 🐳 Configuração do Docker

O projeto utiliza Docker para facilitar a configuração do banco de dados. Para rodar os serviços necessários, utilize o seguinte arquivo `docker-compose.yml`:

```yaml
services:
  db:
    image: postgres
    container_name: banco_supermario
    restart: always
    shm_size: 128mb
    ports:
      - 5432:5432
    environment:
      POSTGRES_USER: root
      POSTGRES_PASSWORD: 123456
    volumes:
      - ./sql:/docker-entrypoint-initdb.d

  adminer:
    image: adminer
    restart: always
    ports:
      - 8080:8080
```

Para iniciar os serviços, execute:

```sh
docker-compose up -d
```

## 🎬 Apresentações

  - [Apresentação Módulo 1]()
  - [Apresentação Módulo 2]()
  - [Apresentação Módulo 3]()

## 👨‍💻 Equipe do Projeto

<div align="center">
  <table>
    <tr>
      <td align="center">
        <img src="https://github.com/alanagabriele.png" width="150px" alt="Alana Gabriele"/><br>
        <a href="https://github.com/alanagabriele"><b>Alana Gabriele</b></a>
      </td>
      <td align="center">
        <img src="https://github.com/renantfm4.png" width="150px" alt="Renan Araújo"/><br>
        <a href="https://github.com/renantfm4"><b>Renan Araújo</b></a>
      </td>
      <td align="center">
        <img src="https://github.com/gustaallves.png" width="150px" alt="Gustavo Alves"/><br>
        <a href="https://github.com/gustaallves"><b>Gustavo Alves</b></a>
      </td>
      <td align="center">
        <img src="https://github.com/fabiofonteles1.png" width="150px" alt="Fabio Fonteneles"/><br>
        <a href="https://github.com/fabiofonteles1"><b>Fabio Fonteneles</b></a>
      </td>
      <td align="center">
        <img src="https://github.com/yabamiah.png" width="150px" alt="Vinícius Mendes"/><br>
        <a href="https://github.com/yabamiah"><b>Vinícius Mendes</b></a>
      </td>
    </tr>
  </table>
</div>

