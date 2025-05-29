import os
import subprocess
import pyautogui
import time
from pynput.keyboard import Controller

class ScreenInteractionAgent:
    """
    Agente responsável por interações com a tela do usuário, como abrir aplicativos, controlar slides,
    executar comandos no sistema e simular interações com o teclado e mouse.
    """

    def __init__(self):
        self.keyboard = Controller()

    def open_application(self, app_name):
        """
        Abre um aplicativo baseado no nome.
        :param app_name: Nome do aplicativo (por exemplo: "PowerPoint", "Chrome").
        """
        print(f"Abrindo o aplicativo {app_name}...")
        if app_name.lower() == "powerpoint":
            subprocess.Popen(['start', 'powerpnt'], shell=True)
        elif app_name.lower() == "navegador":
            subprocess.Popen(['start', 'edge'], shell=True)
        elif app_name.lower() == "explorer":
            subprocess.Popen(['start', 'explorer'], shell=True)
        elif app_name.lower() == "notepad":
            subprocess.Popen(['notepad'], shell=True)
        else:
            print(f"Aplicativo {app_name} não suportado.")
    
    def next_slide(self):
        """
        Avança para o próximo slide em uma apresentação de PowerPoint.
        """
        print("Avançando para o próximo slide...")
        pyautogui.press('right')  # Simula a tecla 'Right Arrow' para avançar slides
    
    def previous_slide(self):
        """
        Retorna ao slide anterior em uma apresentação de PowerPoint.
        """
        print("Voltando ao slide anterior...")
        pyautogui.press('left')  # Simula a tecla 'Left Arrow' para voltar slides

    def read_active_window(self):
        """
        Lê o nome do aplicativo ou janela que está ativa no momento.
        :return: Nome do aplicativo ativo.
        """
        print("Identificando a janela ativa...")
        active_window = pyautogui.getActiveWindow()
        if active_window:
            return active_window.title
        else:
            return "Nenhuma janela ativa identificada."

    def type_text(self, text):
        """
        Simula a digitação de texto na janela ativa.
        :param text: Texto a ser digitado.
        """
        print(f"Digitando o texto: {text}")
        for char in text:
            self.keyboard.press(char)
            self.keyboard.release(char)
            time.sleep(0.05)  # Adiciona um pequeno delay entre as teclas

    def screenshot(self, save_path="screenshot.png"):
        """
        Tira uma captura de tela do desktop e salva em um local específico.
        :param save_path: Caminho para salvar a captura de tela.
        """
        print(f"Tirando uma captura de tela e salvando em {save_path}...")
        screenshot = pyautogui.screenshot()
        screenshot.save(save_path)

    def close_application(self, app_name):
        """
        Fecha um aplicativo específico usando o nome do processo.
        :param app_name: Nome do aplicativo (por exemplo: "PowerPoint", "Chrome").
        """
        print(f"Fechando o aplicativo {app_name}...")
        if app_name.lower() == "powerpoint":
            subprocess.call(['taskkill', '/F', '/IM', 'powerpnt.exe'], shell=True)
        elif app_name.lower() == "chrome":
            subprocess.call(['taskkill', '/F', '/IM', 'chrome.exe'], shell=True)
        elif app_name.lower() == "notepad":
            subprocess.call(['taskkill', '/F', '/IM', 'notepad.exe'], shell=True)
        else:
            print(f"Aplicativo {app_name} não suportado.")

    def scroll_page(self, direction="down"):
        """
        Realiza a rolagem da página (para cima ou para baixo).
        :param direction: Direção da rolagem ('up' ou 'down').
        """
        if direction == "down":
            print("Rolando a página para baixo...")
            pyautogui.scroll(-500)  # Rola para baixo
        elif direction == "up":
            print("Rolando a página para cima...")
            pyautogui.scroll(500)  # Rola para cima
        else:
            print("Direção inválida. Use 'up' ou 'down'.")

    def switch_application(self, app_name):
        """
        Alterna entre janelas de aplicativos usando o nome do aplicativo.
        :param app_name: Nome do aplicativo (por exemplo: "PowerPoint", "Chrome").
        """
        print(f"Alternando para o aplicativo {app_name}...")
        pyautogui.hotkey('alt', 'tab')  # Simula 'Alt + Tab' para alternar entre janelas
        time.sleep(0.5)
        if app_name.lower() == "powerpoint":
            pyautogui.write("PowerPoint", interval=0.1)
        elif app_name.lower() == "edge":
            pyautogui.write("Microsoft Egde", interval=0.1)
        pyautogui.press('enter')

