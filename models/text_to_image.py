import os
from ollama import Client  # MiniCPM está integrado ao Ollama para consulta local

# Diretório de saída para salvar as imagens geradas
IMAGE_OUTPUT_DIR = "image_responses"
if not os.path.exists(IMAGE_OUTPUT_DIR):
    os.makedirs(IMAGE_OUTPUT_DIR)

class TextToImageModel:
    def __init__(self, model_name="minicpm-v:8b-2.6-q8_0", image_size="1024x1024", n_images=1):
        """
        Inicializa o modelo de conversão de texto para imagem usando o MiniCPM-V.
        :param model_name: Nome do modelo a ser usado (padrão: minicpm-v).
        :param image_size: Tamanho da imagem gerada (padrão: 1024x1024).
        :param n_images: Número de imagens a serem geradas (padrão: 1).
        """
        self.model_name = model_name
        self.image_size = image_size
        self.n_images = n_images
        self.client = Client()  # Cliente Ollama que gerencia o MiniCPM-V localmente

    def generate_image_from_text(self, text_description, output_filename="generated_image.png"):
        """
        Gera uma imagem com base na descrição de texto e salva o arquivo.
        :param text_description: Descrição textual da imagem a ser gerada.
        :param output_filename: Nome do arquivo de saída onde a imagem será salva.
        :return: Caminho completo do arquivo da imagem gerada.
        """
        try:
            # Gera a imagem usando o MiniCPM-V integrado no Ollama
            response = self.client.create_image(
                model=self.model_name,
                prompt=text_description,
                size=self.image_size
            )
            
            # Extrai a imagem gerada da resposta
            image_data = response.get('image', None)

            if image_data:
                output_file_path = os.path.join(IMAGE_OUTPUT_DIR, output_filename)

                # Salva a imagem em arquivo
                with open(output_file_path, "wb") as f:
                    f.write(image_data)

                return output_file_path
            else:
                print("Falha na geração da imagem")
                return None

        except Exception as e:
            print(f"Erro ao gerar imagem a partir do texto: {e}")
            return None
