import tkinter as tk
from tkinter import filedialog
import sqlite3
from cryptography.fernet import Fernet
import os
import zlib

class App:
    def __init__(self, window):
        self.window = window
        self.window.title("IA Geradora de Histórias")

        self.description_entry = tk.Entry(window, width=70)
        self.description_entry.pack(pady=20)

        self.load_file_button = tk.Button(window, text="Carregar arquivo", command=self.load_file)
        self.load_file_button.pack(pady=20)

        self.search_entry = tk.Entry(window, width=70)
        self.search_entry.pack(pady=20)

        self.search_button = tk.Button(window, text="Buscar", command=self.search)
        self.search_button.pack(pady=20)

        self.save_file_button = tk.Button(window, text="Salvar arquivo", command=self.save_file)
        self.save_file_button.pack(pady=20)

        self.search_results_label = tk.Label(window, text="")
        self.search_results_label.pack(pady=20)

        # Verifica se o arquivo de chave existe, se não, cria uma nova chave
        if not os.path.exists('key.key'):
            key = Fernet.generate_key()
            with open('key.key', 'wb') as key_file:
                key_file.write(key)
        else:
            with open('key.key', 'rb') as key_file:
                key = key_file.read()
        self.cipher_suite = Fernet(key)

        # Conecta ao banco de dados SQLite
        self.conn = sqlite3.connect('files.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS files (
                description TEXT NOT NULL,
                file BLOB NOT NULL
            );
        ''')

        # Variável para armazenar os resultados da busca
        self.results = []
        self.current_result_index = 0

    def load_file(self):
        self.file_path = filedialog.askopenfilename()

        # Lê o arquivo como bytes
        with open(self.file_path, 'rb') as file:
            file_bytes = file.read()

        # Compacta o arquivo
        compressed_file_bytes = zlib.compress(file_bytes)

        # Criptografa o arquivo
        encrypted_file = self.cipher_suite.encrypt(compressed_file_bytes)

        # Insere a descrição e o arquivo criptografado no banco de dados
        description = self.description_entry.get()
        self.cursor.execute('''
            INSERT INTO files (description, file) VALUES (?, ?);
        ''', (description, encrypted_file))
        self.conn.commit()

    def search(self):
        search_term = self.search_entry.get().lower()

        if search_term:
            # Pesquisa os arquivos cuja descrição é exatamente igual ao termo de busca
            self.cursor.execute('''
                SELECT * FROM files WHERE description = ?;
            ''', (search_term,))
            self.results = self.cursor.fetchall()

            if self.results:
                self.current_result_index = 0
                self.show_search_result()
            else:
                self.search_results_label.configure(text="Nenhum arquivo encontrado.")

    def show_search_result(self):
        # Exibe o resultado da busca
        result = self.results[self.current_result_index]
        description = result[0]

        self.search_results_label.configure(text=description)

    def save_file(self):
        # Salva o arquivo em um local escolhido pelo usuário
        if self.results:
            result = self.results[self.current_result_index]
            encrypted_file = result[1]

            # Descriptografa o arquivo
            decrypted_file = self.cipher_suite.decrypt(encrypted_file)

            # Descompacta o arquivo
            decompressed_file = zlib.decompress(decrypted_file)

            # Abre a caixa de diálogo para salvar o arquivo
            save_path = filedialog.asksaveasfilename(defaultextension=".txt")
            with open(save_path, 'wb') as file:
                file.write(decompressed_file)


root = tk.Tk()
app = App(root)
root.mainloop()
