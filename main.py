import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
import os
import random
from datetime import datetime

class RandomPasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор случайных паролей")
        self.history = []
        self.load_history()
        self.create_ui()

    def create_ui(self):
        # --- Настройки ---
        settings_frame = tk.Frame(self.root)
        settings_frame.pack(pady=10, padx=10, fill='x')

        # Длина пароля
        tk.Label(settings_frame, text="Длина пароля (6-32):").grid(row=0, column=0, sticky='w', pady=2)
        self.length_var = tk.IntVar(value=12)
        self.length_slider = tk.Scale(settings_frame, from_=6, to=32, orient=tk.HORIZONTAL,
                                     variable=self.length_var, length=250)
        self.length_slider.grid(row=0, column=1, columnspan=2, pady=2)

        # Наборы символов
        tk.Label(settings_frame, text="Использовать:").grid(row=1, column=0, sticky='w', pady=5)

        self.use_digits = tk.BooleanVar(value=True)
        self.use_lower = tk.BooleanVar(value=True)
        self.use_upper = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=True)

        tk.Checkbutton(settings_frame, text="Цифры (0-9)", variable=self.use_digits).grid(row=2, column=0, sticky='w')
        tk.Checkbutton(settings_frame, text="Строчные (a-z)", variable=self.use_lower).grid(row=3, column=0, sticky='w')
        tk.Checkbutton(settings_frame, text="Прописные (A-Z)", variable=self.use_upper).grid(row=4, column=0, sticky='w')
        tk.Checkbutton(settings_frame, text="Спецсимволы (!@#$%^&*)", variable=self.use_special).grid(row=5, column=0, sticky='w')

        # --- Генерация ---
        gen_frame = tk.Frame(self.root)
        gen_frame.pack(pady=10)

        self.password_entry = tk.Entry(gen_frame, width=40, font=('Arial', 12), state='readonly')
        self.password_entry.pack(side='left', padx=(0, 10))

        tk.Button(gen_frame, text="Сгенерировать", command=self.generate_password).pack(side='left')

        # --- История ---
        history_frame = tk.Frame(self.root)
        history_frame.pack(pady=10, padx=10, fill='both', expand=True)

        tk.Label(history_frame, text="История паролей:").pack(anchor='w')

        self.history_list = scrolledtext.ScrolledText(history_frame,
                                                      height=10,
                                                      width=60,
                                                      state='disabled')
        self.history_list.pack(fill='both', expand=True)

    def generate_password(self):
         length = self.length_var.get()
         chars = ''
         if self.use_digits.get(): chars += '0123456789'
         if self.use_lower.get(): chars += 'abcdefghijklmnopqrstuvwxyz'
         if self.use_upper.get(): chars += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
         if self.use_special.get(): chars += '!@#$%^&*'

         if not chars:
             messagebox.showerror("Ошибка", "Выберите хотя бы один набор символов!")
             return

         password = ''.join(random.choices(chars, k=length))
         self.password_entry.config(state='normal')
         self.password_entry.delete(0, tk.END)
         self.password_entry.insert(0, password)
         self.password_entry.config(state='readonly')

         # Запись в историю
         entry = {
             "length": length,
             "chars": [name for name, var in {
                 "Цифры": self.use_digits.get(),
                 "Строчные": self.use_lower.get(),
                 "Прописные": self.use_upper.get(),
                 "Спецсимволы": self.use_special.get()
             }.items() if var],
             "password": password,
             "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
         }
         self.history.append(entry)
         self.update_history_display()
         self.save_history()

    def update_history_display(self):
         self.history_list.config(state='normal')
         self.history_list.delete(1.0, tk.END)
         for i, entry in enumerate(self.history[-20:], 1):
             self.history_list.insert(tk.END,
                                     f"{i}. Длина: {entry['length']} | Набор: {', '.join(entry['chars'])} | Пароль: {entry['password']} | [{entry['timestamp']}]\n\n")
         self.history_list.config(state='disabled')

    def save_history(self):
         with open("password_history.json", "w", encoding="utf-8") as f:
             json.dump(self.history, f, ensure_ascii=False, indent=4)

    def load_history(self):
         if os.path.exists("password_history.json"):
             try:
                 with open("password_history.json", "r", encoding="utf-8") as f:
                     self.history = json.load(f)
             except Exception as e:
                 messagebox.showerror("Ошибка загрузки", f"Не удалось загрузить историю: {e}")

if __name__ == "__main__":
     root = tk.Tk()
     app = RandomPasswordGenerator(root)
     root.mainloop()