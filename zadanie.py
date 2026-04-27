import tkinter as tk
from tkinter import messagebox, ttk
import json
import os


class WeatherDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary")
        self.data_file = "weather_data.json"
        self.history = self.load_data()

        tk.Label(root, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0)
        self.date_entry = tk.Entry(root)
        self.date_entry.grid(row=0, column=1)

        tk.Label(root, text="Температура (°C):").grid(row=1, column=0)
        self.temp_entry = tk.Entry(root)
        self.temp_entry.grid(row=1, column=1)

        tk.Label(root, text="Описание:").grid(row=2, column=0)
        self.desc_entry = tk.Entry(root)
        self.desc_entry.grid(row=2, column=1)

        self.precip_var = tk.BooleanVar()
        tk.Checkbutton(root, text="Осадки", variable=self.precip_var).grid(row=3, column=1)

        tk.Button(root, text="Добавить запись", command=self.add_entry).grid(row=4, column=0, columnspan=2, pady=5)

        tk.Label(root, text="Фильтр (Т > X):").grid(row=5, column=0)
        self.filter_temp = tk.Entry(root)
        self.filter_temp.grid(row=5, column=1)
        tk.Button(root, text="Применить фильтр", command=self.apply_filter).grid(row=6, column=0, columnspan=2)

        self.tree = ttk.Treeview(root, columns=("Date", "Temp", "Desc", "Precip"), show='headings')
        self.tree.heading("Date", text="Дата")
        self.tree.heading("Temp", text="Темп.")
        self.tree.heading("Desc", text="Описание")
        self.tree.heading("Precip", text="Осадки")
        self.tree.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        self.update_table(self.history)

    def add_entry(self):
        date = self.date_entry.get()
        temp = self.temp_entry.get()
        desc = self.desc_entry.get()
        precip = "Да" if self.precip_var.get() else "Нет"

        if not date or not desc:
            messagebox.showerror("Ошибка", "Заполните дату и описание!")
            return
        try:
            temp = float(temp)
        except ValueError:
            messagebox.showerror("Ошибка", "Температура должна быть числом!")
            return

        new_record = {"date": date, "temp": temp, "desc": desc, "precip": precip}
        self.history.append(new_record)
        self.save_data()
        self.update_table(self.history)

        self.date_entry.delete(0, tk.END)
        self.temp_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.precip_var.set(False)

    def apply_filter(self):
        val = self.filter_temp.get()
        if not val:
            self.update_table(self.history)
            return
        try:
            limit = float(val)
            filtered = [r for r in self.history if r['temp'] > limit]
            self.update_table(filtered)
        except ValueError:
            self.update_table(self.history)

    def update_table(self, data):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for item in data:
            self.tree.insert("", "end", values=(item['date'], item['temp'], item['desc'], item['precip']))

    def save_data(self):
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiary(root)
    root.mainloop()
