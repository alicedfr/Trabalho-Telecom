import pygame
import speech_recognition as sr
import pyttsx3
import chess


# Função para converter entrada de voz em notação de xadrez
def converter_voz_para_notacao(voz):
    voz = voz.lower().strip()
    if ("roque curto" in voz or "0-0" in voz or "o-o" in voz) and tabuleiro.turn == chess.WHITE:
        return "e1g1" 
    elif "roque curto" in voz or "0-0" in voz or "o-o" in voz: 
        return "e8g8"
    elif ("roque longo" in voz or "0-0-0" in voz or "o-o-o" in voz) and tabuleiro.turn == chess.WHITE:
        return "e1c1" 
    elif "roque longo" in voz or "0-0-0" in voz or "o-o-o" in voz:
        return "e8c8"

    partes = voz.split()
    if len(partes) < 3 or partes[1] != "para":
        return None

    nome_peca = partes[0]
    destino = partes[2]

    pecas = {
        "peão": "p",
        "cavalo": "n",
        "bispo": "b",
        "torre": "r",
        "rainha": "q",
        "rei": "k"
    }

    if nome_peca not in pecas or not chess.SQUARE_NAMES.__contains__(destino):
        return None

    return destino

# Função para capturar entrada de voz do jogador
def ouvir_comando():
    reconhecedor = sr.Recognizer()
    with sr.Microphone() as fonte:
        print("Diga o seu movimento (ex.: 'Bispo para c4').")
        audio = reconhecedor.listen(fonte)

    try:
        comando = reconhecedor.recognize_google(audio, language='pt-BR')
        print(f"Você disse: {comando}")
        return comando
    except sr.UnknownValueError:
        print("Não entendi o que você disse.")
        return None
    except sr.RequestError:
        print("Erro ao conectar ao serviço de reconhecimento de voz.")
        return None

# Função para a engine falar
def falar(texto):
    engine = pyttsx3.init()
    engine.say(texto)
    engine.runAndWait()

