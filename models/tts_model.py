from models.tts_model import TTSModel

def main():
    tts_model = TTSModel()
    text = "Olá, como posso ajudar você?"
    
    # Converte o texto para fala e salva o áudio
    audio_file = tts_model.text_to_speech(text, output_filename="welcome_message.wav")
    
    if audio_file:
        print(f"Áudio salvo em: {audio_file}")
    else:
        print("Erro ao gerar o áudio.")

if __name__ == "__main__":
    main()
