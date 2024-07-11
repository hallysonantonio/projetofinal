import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
from _gemini import GeminiAnalyzer

# pip install requests beautifulsoup4 tkinter

def analyze_url():
    url = url_entry.get().strip()
    if url:
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            text_content = ' '.join(p.get_text() for p in soup.find_all('p'))

            if text_content:
                analyzer = GeminiAnalyzer()
                prompt = f"Analise o seguinte texto jornalístico e forneça um resumo e dê uma nota de 0 a 10 com base na qualidade da escrita, clareza e conteúdo informativo e informe qual o seu publico alvo e sua finalidade: {text_content}"
                _, score = analyzer.generate_google_response(prompt)
                result_label.config(text=f"Nota do Texto: {_}")
            else:
                result_label.config(text="Não foi possível extrair texto significativo da URL.")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"Erro ao acessar a URL: {e}")
    else:
        result_label.config(text="Por favor, insira uma URL.")

def reset_fields():
    url_entry.delete(0, tk.END)
    result_label.config(text="")

def create_window():
    window = tk.Tk()
    window.title("Fact Check")

    frame = tk.Frame(window, padx=10, pady=10)
    frame.pack(padx=10, pady=10)

    url_label = tk.Label(frame, text="Insira a URL do texto:")
    url_label.pack()

    global url_entry
    url_entry = tk.Entry(frame, width=50)
    url_entry.pack()

    analyze_button = tk.Button(frame, text="Analisar URL", command=analyze_url)
    analyze_button.pack(pady=5)

    reset_button = tk.Button(frame, text="Resetar", command=reset_fields)
    reset_button.pack(pady=5)

    global result_label
    result_label = tk.Label(frame, text="", wraplength=400, justify="left")
    result_label.pack(pady=10)

    window.mainloop()

if __name__ == "__main__":
    create_window()
