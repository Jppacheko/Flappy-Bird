

# Flappy Bird Personalizado

Esse projeto é uma versão personalizada do clássico **Flappy Bird**, desenvolvido em Python com a biblioteca Pygame. A principal adição é uma tela de login interativa que permite ao jogador inserir seu nome antes de começar o jogo, junto com diversas melhorias de interface e jogabilidade.

## 🕹️ Funcionalidades

- **Tela de Login Personalizada**: Ao iniciar o jogo, o jogador é recebido com uma tela onde pode inserir seu nome em um campo de texto, juntamente com um botão "Enter" para iniciar a partida.
- **Pontuação em Tempo Real**: A pontuação é exibida no topo da tela durante o jogo, com base na quantidade de obstáculos ultrapassados.
- **Ajustes de Dificuldade Dinâmica**: A velocidade do jogo aumenta conforme o jogador acumula pontos, adicionando um nível crescente de desafio.
- **Tela de Game Over**: Ao perder, o jogador recebe a opção de reiniciar ou voltar para a tela de login, permitindo a troca de jogador sem reiniciar o jogo.

## 📂 Estrutura do Código

- **Classes Principais**:
  - `Passaro`: Define o comportamento do personagem principal, incluindo animações de voo e física.
  - `Cano`: Responsável pela criação e movimentação dos obstáculos.
  - `Chao`: Gera o efeito de movimento contínuo do chão.
  - `Tela de Login`: Interface inicial onde o jogador insere seu nome antes de começar a partida.
- **Funções Auxiliares**:
  - `desenhar_tela`: Atualiza a tela do jogo com todos os elementos (pássaro, canos, chão, pontuação).
  - `tela_login`: Renderiza a interface de login com campo de texto e botão para iniciar o jogo.

## ⚙️ Tecnologias Utilizadas

- **Python**: Linguagem de programação principal.
- **Pygame**: Biblioteca usada para desenvolver jogos em 2D, proporcionando fácil manipulação de gráficos e eventos.

## 🚀 Como Executar o Jogo

1. **Pré-requisitos**:
   - Certifique-se de ter o Python 3.13.0 instalado.
   - Instale a biblioteca Pygame:
     ```bash
     pip install pygame
     ```

2. **Clonar o Repositório**:
   ```bash
   git clone https://github.com/seuusuario/flappy-bird-personalizado.git
   cd flappy-bird-personalizado
   ```

3. **Iniciar o Jogo**:
   ```bash
   python main.py
   ```

4. **Imagens**:
   - Certifique-se de que as imagens (background, pássaro, canos e base) estão na pasta `imgs`. Ajuste o caminho no código, se necessário.

## 📈 Futuras Melhorias

Algumas ideias para melhorar ainda mais o projeto:

- Adicionar um sistema de ranking para os melhores jogadores.
- Implementar níveis de dificuldade e modos de jogo.
- Integrar sons e efeitos visuais adicionais para tornar o jogo ainda mais envolvente.

---

Com esse README, qualquer pessoa interessada poderá entender o que seu projeto faz, como funciona e como rodá-lo. Se precisar de mais algum ajuste ou quiser adicionar alguma seção extra, é só avisar!
