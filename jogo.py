import chess
from chess_engine import *
from controle_de_voz import *


# Função para exibir o tabuleiro de forma mais amigável
def exibir_tabuleiro(tabuleiro):
    #print(tabuleiro)
    print("  a b c d e f g h")
    for i, linha in enumerate(str(tabuleiro).split("\n"), 1):
        print(f"{9-i} {linha}")

# Loop do jogo entre humano e engine
def jogar_humano_vs_engine():
    tabuleiro = chess.Board()
    profundidade = 3  # Profundidade da busca Minimax

    while not tabuleiro.is_game_over():
        exibir_tabuleiro(tabuleiro)
        print("Jogadas legais:", [str(m) for m in tabuleiro.legal_moves])

        if tabuleiro.turn == chess.WHITE:
            # Turno do humano (brancas)
            audio = ouvir_comando()
            #print(audio)
            #entrada = converter_voz_para_notacao(audio) #retorna o destino
            #print(entrada)
            movimento = converter_entrada_para_movimento(tabuleiro, audio)
            if movimento:
                tabuleiro.push(movimento)
            else:
                print("Movimento inválido. Tente novamente.")
        else:
            # Turno da engine (pretas)
            movimento = melhor_movimento(tabuleiro, profundidade)
            print(f"A engine joga: {movimento}")
            tabuleiro.push(movimento)

    print("Jogo finalizado!")
    print("Resultado:", tabuleiro.result())
    exibir_tabuleiro(tabuleiro)

if __name__ == "__main__":
    jogar_humano_vs_engine()

