import time
import requests
import PIL.Image
import os
from io import BytesIO

# google generative dependence
import google.generativeai as genai
from google.api_core.exceptions import InternalServerError
from google.ai.generativelanguage import HarmCategory
from google.ai.generativelanguage import SafetySetting
from google.api_core.exceptions import DeadlineExceeded, InternalServerError


class GeminiAnalyzer:
    """
    Classe responsável pela análise de postagens do Instagram utilizando o modelo de IA generativa do Google (Google's Generative AI model).
    
    Esta classe integra funcionalidades para gerar respostas baseadas em texto e análise de imagens a partir de postagens específicas, utilizando
    diferentes configurações de segurança para filtrar conteúdos indesejados. Além disso, a classe oferece métodos para processar e analisar
    detalhadamente cada postagem, identificando categorias, resumos, promessas e tipos de fala associados ao conteúdo analisado.
    
    Métodos Principais:
    - generate_google_response: Gera respostas textuais a partir de instruções e conteúdos específicos utilizando o modelo de IA generativa do Google.
    - generate_image_analysis: Realiza a análise de imagens fornecidas, gerando descrições ou informações pertinentes com base no modelo de IA para visão computacional.
    - process_post: Processa uma postagem específica, aplicando análises textuais e de imagem para extrair informações relevantes como categoria, resumo, promessas, entre outras.
    - analyze_post: Analisa uma única postagem baseada nos dados fornecidos, utilizando os métodos de processamento e geração de respostas da classe.
    
    A classe é inicializada configurando-se os modelos de IA para texto e imagem, assim como as definições de segurança para o processamento do conteúdo.
    """

    def __init__(self):
        genai.configure(api_key="AIzaSyAyuSbfRF7B2wLtnyr8Et1i78n7XyVdRaQ")
        self.client = genai.GenerativeModel('gemini-pro')
        self.client_image = genai.GenerativeModel('gemini-pro-vision')

        self.safety_settings = {
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: SafetySetting.HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: SafetySetting.HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: SafetySetting.HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: SafetySetting.HarmBlockThreshold.BLOCK_NONE,
        }

        self.candidate_count = 1
        # self.define_explain()

    def generate_google_response(self, messages):
        """
        Gera uma resposta usando o modelo de IA generativa do Google.

        Parâmetros:
        - messages (list): Uma lista contendo as instruções e o conteúdo da postagem.

        Retorna:
        - Uma tupla contendo o texto da resposta gerada e o objeto de resposta completo.
        """

        try:
            response = self.client.generate_content(
                messages,
                generation_config=genai.types.GenerationConfig(
                    candidate_count=self.candidate_count,
                    temperature=0,
                ),
                safety_settings=self.safety_settings
            )
        except InternalServerError:
            time.sleep(60)
            response = self.client.generate_content(
                messages,
                generation_config=genai.types.GenerationConfig(
                    candidate_count=self.candidate_count,
                    temperature=0,
                ),
                safety_settings=self.safety_settings
            )
        try:
            return response.text, response
        except IndexError:
            print("Erro em response.text")
            return None, None
        

    def generate_image_analysis(self, image_data, prompt):
        try:
            response = self.client_image.generate_content(
                [prompt, image_data]
            )
        except InternalServerError:
            time.sleep(60)  # Aguarda um minuto antes de tentar novamente
            return self.generate_image_analysis(image_data, prompt)  # Tentativa recursiva
        except DeadlineExceeded:
            time.sleep(60)  # Aguarda um minuto antes de tentar novamente
            return self.generate_image_analysis(image_data, prompt)  # Tentativa recursiva

        return response.text
    

    def processed_text_image(self, 
                             url: str,
                             prompt: str = "Extraia o texto da imagem. Caso não haja texto, retorne um texto vazio."):
        """
        Extrai texto de uma imagem específica a partir de sua URL.

        Parâmetros:
        - url (str): URL da imagem da qual o texto será extraído.

        Realiza uma solicitação para obter a imagem pela URL, e utiliza um modelo de IA para extrair o texto presente.
        Caso não haja texto na imagem, retorna um texto vazio.

        Retorna:
        - str: Texto extraído da imagem ou um texto vazio se não houver texto.
        """
        try:
            response = requests.get(url)
            img = PIL.Image.open(BytesIO(response.content))
            answer = self.generate_image_analysis(image_data=img, 
                                                  prompt=prompt)
            
            return answer
        except Exception as e:
            print(f"Erro ao obter o texto na imagem: {e}")
            return ""


    def initialize_chat(self):
        global chat
        chat = self.client.start_chat(history=[])


    def generate_chat_response(self, messages, temperature=0.0):
        global chat
        try:
            response = chat.send_message(
                messages,
                generation_config=genai.types.GenerationConfig(
                    candidate_count=self.candidate_count,
                    temperature=temperature,
                ),
                safety_settings=self.safety_settings
            )
        except InternalServerError:
            time.sleep(60)
            response = chat.send_message(
                messages,
                generation_config=genai.types.GenerationConfig(
                    candidate_count=self.candidate_count,
                    temperature=temperature,
                ),
                safety_settings=self.safety_settings
            )
        try:
            return response.text, response
        except IndexError:
            print("Erro em response.text")
            return None, None
    