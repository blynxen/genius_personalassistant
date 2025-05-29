import os
import sys
import subprocess
from queue import Queue
import sounddevice as sd
import wave
import numpy as np
import torch
from pynput import keyboard
from agent import DmGeniusAgent
from agents.web_search_agent import WebSearchAgent  # Agente de Busca Web
from agents.legal_agent import LegalAgent  # Agente especializado em legislação
from agents.safety_agent import SafetyAgent  # Agente especializado em segurança do trabalho
from agents.data_governance_agent import DataGovernanceAgent  # Agente especializado em governança de dados
from agents.knowledge_agent import KnowledgeAgent
import whisper
import soundfile as sf
from TTS.api import TTS
from datetime import datetime
from dotenv import load_dotenv

# Adicionar o diretório raiz do projeto ao sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Carrega variáveis de ambiente
load_dotenv()

# Configuração da pasta de saída para os arquivos de áudio e transcrições
AUDIO_DIR = "audios"
TRANSCRIPTIONS_DIR = "transcriptions"

# Cria pastas se não existirem
if not os.path.exists(AUDIO_DIR):
    os.makedirs(AUDIO_DIR)
if not os.path.exists(TRANSCRIPTIONS_DIR):
    os.makedirs(TRANSCRIPTIONS_DIR)

# Variável global para contar o tempo total de áudio
total_audio_duration = 0

# Função para reproduzir áudio
def play_audio(file_path):
    data, samplerate = sf.read(file_path)
    sd.play(data, samplerate)
    sd.wait()

# Classe TalkingLLM que captura áudio, transcreve, envia para o modelo LLM e responde por voz
class TalkingLLM:
    def __init__(self, whisper_size="small", ollama_model="geniusv1:latest", knowledge_base_agent=None):
        self.is_recording = False
        self.audio_data = []
        self.samplerate = 44100
        self.channels = 1
        self.dtype = 'int16'
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.whisper = whisper.load_model(whisper_size).to(device)
        self.llm_queue = Queue()

        # Inicializa o agente principal com a base de conhecimento local
        self.agent = DmGeniusAgent(ollama_model, knowledge_base_agent=knowledge_base_agent)

        # Inicializando os agentes especializados
        self.legal_agent = LegalAgent()
        self.safety_agent = SafetyAgent()
        self.data_governance_agent = DataGovernanceAgent()

        # WebSearchAgent para consultas online
        self.web_search_agent = WebSearchAgent()

        # Configuração do TTS: utilizando o modelo XXTS multilingual v2
        self.tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", gpu=torch.cuda.is_available())

        # Caminho para o arquivo de áudio de exemplo
        self.tts_sample = r"D:\Personal_Assistent\data\voice_sampler\sample_male_voice.mp3"

        # Lista de variações de palavras de ativação
        self.activation_words = ["genius", "genios", "gênius", "dineos", "díneos", "gineos", "Chíneos", 
                                 "jeenyuhs", "gênio", "Ginhos", "Tinhos", "gênios", "genious", "jinious", 
                                 "jenius", "ginnos", "ginos", "gíneos", "gini", "díneas", "gênios"]

        # Variável para controle de ativação contínua
        self.active = False  # Estado inativo por padrão

    def process_query(self, query):
        """
        Decide qual agente utilizar para processar a consulta com base no conteúdo.
        Primeiro, busca no MongoDB (base de conhecimento local).
        """
        # Primeiro tenta a base de conhecimento (MongoDB)
        response = self.agent.query(query)
        
        if response:
            print("Resposta encontrada no MongoDB.")
            return response

        # Se não encontrado no MongoDB, verifica o tipo de consulta
        if "legislação" in query or "lei" in query or "jurisprudência" in query:
            print("Consultando agente de legislação...")
            response = self.legal_agent.query(query)
        elif "segurança no trabalho" in query or "NR" in query or "norma regulamentadora" in query:
            print("Consultando agente de segurança no trabalho...")
            response = self.safety_agent.query(query)
        elif "LGPD" in query or "governança de dados" in query or "proteção de dados" in query:
            print("Consultando agente de governança de dados...")
            response = self.data_governance_agent.query(query)
        else:
            # Se nenhum agente especializado puder tratar, faz busca na web
            print("Nenhum agente especializado identificado. Consultando modelo ou web.")
            response = self.web_search_agent.query_web(query, use_tavily=True)

        return response

    def save_and_transcribe(self):
        global total_audio_duration

        print("Salvando a gravação...")

        # Usar timestamp para garantir que o nome do arquivo seja único
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_wav = os.path.join(AUDIO_DIR, f"audio_{timestamp}.wav")
        transcription_file = os.path.join(TRANSCRIPTIONS_DIR, f"transcription_{timestamp}.txt")
        
        # Salvando o arquivo de áudio
        wav_file = wave.open(temp_wav, 'wb')
        wav_file.setnchannels(self.channels)
        wav_file.setsampwidth(2)
        wav_file.setframerate(self.samplerate)
        wav_file.writeframes(np.array(self.audio_data, dtype=self.dtype))
        wav_file.close()

        print(f"Áudio gravado em {temp_wav}")

        print("Transcrevendo...")
        result = self.whisper.transcribe(temp_wav, fp16=False)
        transcribed_text = result["text"].lower()
        print("Usuário:", transcribed_text)

        # Salvando a transcrição em um arquivo de texto
        with open(transcription_file, 'w', encoding='utf-8') as f:
            f.write(transcribed_text)

        print(f"Transcrição salva em {transcription_file}")

        # Desativação do assistente com "pode descansar"
        if "pode descansar" in transcribed_text:
            print("Assistente desativado.")
            self.active = False
            return

        # Ativação contínua ou ativação por palavra-chave
        if self.active or any(word in transcribed_text for word in self.activation_words):
            self.active = True  # Mantém o estado ativado
            print(f"Palavra de ativação detectada no texto: {transcribed_text}")

            # Agora vamos consultar o agente correto
            response = self.process_query(transcribed_text)

            print("Resposta do AI:", response)
            self.convert_text_to_speech(response)
        else:
            print("Nenhuma palavra de ativação detectada no texto transcrito.")

    def convert_text_to_speech(self, text):
        global total_audio_duration

        print("Convertendo resposta para voz...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_wav = os.path.join(AUDIO_DIR, f"response_{timestamp}.wav")

        self.tts.tts_to_file(text=text, speaker_wav=self.tts_sample, language="pt", file_path=output_wav)
        self.play_audio(output_wav)

        # Adiciona a duração deste arquivo ao total de áudio
        audio_data, samplerate = sf.read(output_wav)
        duration = len(audio_data) / samplerate
        total_audio_duration += duration

        print(f"Áudio de resposta salvo em {output_wav}, duração: {duration:.2f} segundos.")
        print(f"Duração total de áudio: {total_audio_duration / 60:.2f} minutos")

        if total_audio_duration >= 600:
            print("Você já tem 10 minutos de áudio! Hora de treinar seu modelo TTS.")

    def play_audio(self, file_path):
        data, samplerate = sf.read(file_path)
        sd.play(data, samplerate)
        sd.wait()

    def run(self):
        print("Programa rodando. Pressione F7 para iniciar e parar a gravação e F8 para sair.")

        def callback(indata, frame_count, time_info, status):
            if self.is_recording:
                self.audio_data.extend(indata.copy())

        try:
            with sd.InputStream(samplerate=self.samplerate, channels=self.channels, dtype=self.dtype, callback=callback):
                def on_activate(key):
                    if key == keyboard.Key.f7:
                        if self.is_recording:
                            self.is_recording = False
                            print("Parando a gravação...")
                            self.save_and_transcribe()
                            self.audio_data = []
                        else:
                            print("Iniciando gravação...")
                            self.audio_data = []
                            self.is_recording = True
                    elif key == keyboard.Key.f8:
                        print("F8 pressionado. Encerrando o programa.")
                        sys.exit(0)

                with keyboard.Listener(on_press=on_activate) as listener:
                    listener.join()

        except KeyboardInterrupt:
            print("Interrompido pelo usuário (Ctrl+C)")

if __name__ == "__main__":
    talking_llm = TalkingLLM(knowledge_base_agent=KnowledgeAgent())  # Aqui você passa o KnowledgeAgent
    talking_llm.run()
