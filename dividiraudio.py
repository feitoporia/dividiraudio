from pydub import AudioSegment
import math
import os
import logging
import argparse
import sys
from tkinter import Tk, filedialog, Label, Button
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Função para dividir o áudio em partes
def dividir_audio(arquivo_entrada, pasta_saida, duracao_pedaco):
    """
    Divide um arquivo de áudio em partes menores de duração especificada.

    Args:
        arquivo_entrada (str): Caminho do arquivo de áudio de entrada.
        pasta_saida (str): Diretório onde as partes divididas serão salvas.
        duracao_pedaco (int): Duração de cada parte em milissegundos.
    """
    try:
        # Carregar o áudio
        audio = AudioSegment.from_file(arquivo_entrada)
        
        # Calcular o número de partes
        numero_partes = math.ceil(len(audio) / duracao_pedaco)

        # Criar pasta de saída se não existir
        if not os.path.exists(pasta_saida):
            os.makedirs(pasta_saida, exist_ok=True)

        # Dividir e exportar cada parte
        for i in range(numero_partes):
            inicio = i * duracao_pedaco
            fim = min((i + 1) * duracao_pedaco, len(audio))
            parte = audio[inicio:fim]
            
            # Nome do arquivo de saída
            arquivo_saida = os.path.join(pasta_saida, f"parte_{i + 1:02}.mp3")
            
            # Exportar a parte do áudio
            parte.export(arquivo_saida, format="mp3")
            logging.info(f"Parte {i + 1} exportada: {arquivo_saida}")

    except FileNotFoundError:
        logging.error(f"Arquivo não encontrado: {arquivo_entrada}")
    except Exception as e:
        logging.error(f"Erro ao processar o arquivo: {str(e)}")

# Função para criar a interface gráfica
def criar_interface():
    root = Tk()
    root.title("Divisor de Áudio - Versão Moderna")
    root.geometry("750x450")
    root.configure(bg="#f0f0f0")
    root.resizable(False, False)

    estilo = ttk.Style()
    estilo.theme_use("clam")
    estilo.configure("TButton", font=("Helvetica", 10), padding=10)
    estilo.configure("TLabel", background="#f0f0f0", font=("Helvetica", 12))
    estilo.configure("TFrame", background="#f0f0f0")

    frame = ttk.Frame(root, padding="10")
    frame.pack(fill=tk.BOTH, expand=True)

    def selecionar_arquivo():
        arquivo = filedialog.askopenfilename(title="Selecione o arquivo de áudio", filetypes=[("Arquivos de áudio", "*.mp3 *.wav *.ogg")])
        if arquivo:
            entrada_label.config(text=arquivo)

    def selecionar_pasta():
        pasta = filedialog.askdirectory(title="Selecione a pasta de saída")
        if pasta:
            pasta_label.config(text=pasta)

    def dividir():
        arquivo_entrada = entrada_label.cget("text")
        pasta_saida = pasta_label.cget("text")
        duracao_pedaco = 180 * 1000  # 3 minutos em milissegundos

        if not arquivo_entrada or not pasta_saida:
            messagebox.showwarning("Atenção", "Por favor, selecione o arquivo de entrada e a pasta de saída.")
            return

        dividir_audio(arquivo_entrada, pasta_saida, duracao_pedaco)
        messagebox.showinfo("Sucesso", "Áudio dividido com sucesso!")

    ttk.Label(frame, text="Selecione o arquivo de áudio:").grid(row=0, column=0, sticky=tk.W, pady=5)
    entrada_label = ttk.Label(frame, text="", relief="sunken", width=50)
    entrada_label.grid(row=1, column=0, columnspan=2, pady=5)
    ttk.Button(frame, text="Selecionar Arquivo", command=selecionar_arquivo).grid(row=1, column=2, padx=5)

    ttk.Label(frame, text="Selecione a pasta de saída:").grid(row=2, column=0, sticky=tk.W, pady=5)
    pasta_label = ttk.Label(frame, text="", relief="sunken", width=50)
    pasta_label.grid(row=3, column=0, columnspan=2, pady=5)
    ttk.Button(frame, text="Selecionar Pasta", command=selecionar_pasta).grid(row=3, column=2, padx=5)

    dividir_button = ttk.Button(frame, text="Dividir Áudio", command=dividir)
    dividir_button.grid(row=4, column=0, columnspan=3, pady=20)

    root.mainloop()

# Exemplo de uso pela linha de comando
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dividir um arquivo de áudio em partes menores.")
    parser.add_argument("--interface", action="store_true", help="Inicia a interface gráfica do aplicativo.")
    parser.add_argument("--arquivo", type=str, help="Caminho para o arquivo de áudio original.")
    parser.add_argument("--pasta", type=str, help="Pasta onde os arquivos serão salvos.")
    parser.add_argument("--duracao", type=int, default=180, help="Duração de cada parte em segundos (padrão: 180).")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        # Se nenhum argumento for passado, iniciar a interface gráfica
        criar_interface()
    elif args.interface:
        criar_interface()
    elif args.arquivo and args.pasta:
        duracao_ms = args.duracao * 1000
        dividir_audio(args.arquivo, args.pasta, duracao_ms)
    else:
        print("Por favor, forneça --interface para iniciar a interface gráfica ou --arquivo e --pasta para dividir um áudio via linha de comando.")
