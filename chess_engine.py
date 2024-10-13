import chess

# Função de avaliação simples: baseada no valor das peças
def avaliar_posicao(tabuleiro):
    valores_pecas = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0
    }
    avaliacao = 0
    for peca in tabuleiro.piece_map().values():
        if peca.color == chess.WHITE:
            avaliacao += valores_pecas[peca.piece_type]
        else:
            avaliacao -= valores_pecas[peca.piece_type]
    return avaliacao

# Função Minimax com poda alfa-beta
def minimax(tabuleiro, profundidade, alfa, beta, maximizando):
    if profundidade == 0 or tabuleiro.is_game_over():
        return avaliar_posicao(tabuleiro)

    if maximizando:
        max_eval = -float('inf')
        for movimento in tabuleiro.legal_moves:
            tabuleiro.push(movimento)
            avaliacao = minimax(tabuleiro, profundidade - 1, alfa, beta, False)
            tabuleiro.pop()
            max_eval = max(max_eval, avaliacao)
            alfa = max(alfa, avaliacao)
            if beta <= alfa:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for movimento in tabuleiro.legal_moves:
            tabuleiro.push(movimento)
            avaliacao = minimax(tabuleiro, profundidade - 1, alfa, beta, True)
            tabuleiro.pop()
            min_eval = min(min_eval, avaliacao)
            beta = min(beta, avaliacao)
            if beta <= alfa:
                break
        return min_eval

# Função para escolher o melhor movimento da engine
def melhor_movimento(tabuleiro, profundidade):
    melhor_movimento = None
    max_eval = -float('inf')
    for movimento in tabuleiro.legal_moves:
        tabuleiro.push(movimento)
        avaliacao = minimax(tabuleiro, profundidade - 1, -float('inf'), float('inf'), False)
        tabuleiro.pop()
        if avaliacao > max_eval:
            max_eval = avaliacao
            melhor_movimento = movimento
    return melhor_movimento

# Função para converter entrada de peça e posição em um movimento UCI
def converter_entrada_para_movimento(tabuleiro, entrada):
    entrada = entrada.lower().strip()
    pecas = {
        "peão": chess.PAWN,
        "cavalo": chess.KNIGHT,
        "bispo": chess.BISHOP,
        "torre": chess.ROOK,
        "rainha": chess.QUEEN,
        "rei": chess.KING
    }

    if entrada in ["roque curto", "0-0", "o-o"]:
        return chess.Move.from_uci("e1g1") if tabuleiro.turn == chess.WHITE else chess.Move.from_uci("e8g8")
    elif entrada in ["roque longo", "0-0-0", "o-o-o"]:
        return chess.Move.from_uci("e1c1") if tabuleiro.turn == chess.WHITE else chess.Move.from_uci("e8c8")

    # Extrai o nome da peça e a posição de destino (ex.: "cavalo para e4")
    partes = entrada.split()
    if len(partes) < 3 or partes[1] != "para":
        print("Formato inválido. Use: 'Peça para posição' (ex: 'Bispo para c4').")
        return None

    nome_peca = partes[0]
    destino = partes[2]

    if nome_peca not in pecas or not chess.SQUARE_NAMES.__contains__(destino):
        print("Peça ou posição inválida.")
        return None

    tipo_peca = pecas[nome_peca]

    # Verifica se o movimento é uma promoção de peão (ex.: "Peão para e8 rainha")
    if tipo_peca == chess.PAWN and destino.endswith("8") or destino.endswith("1"):
        # Verifica se há uma promoção especificada
        if len(partes) == 4:
            promocao = partes[3]
            promocoes = {
                "rainha": chess.QUEEN,
                "torre": chess.ROOK,
                "bispo": chess.BISHOP,
                "cavalo": chess.KNIGHT
            }
            if promocao in promocoes:
                for movimento in tabuleiro.legal_moves:
                    if (tabuleiro.piece_at(movimento.from_square).piece_type == tipo_peca and
                        chess.square_name(movimento.to_square) == destino and
                        movimento.promotion == promocoes[promocao]):
                        return movimento

    # Encontrar o movimento adequado com base na peça e posição de destino
    for movimento in tabuleiro.legal_moves:
        if (tabuleiro.piece_at(movimento.from_square) and 
            tabuleiro.piece_at(movimento.from_square).piece_type == tipo_peca and
            chess.square_name(movimento.to_square) == destino):
            return movimento

    print("Nenhum movimento válido encontrado para essa peça e posição.")
    return None
