import os
import sys
from numpy.core.numeric import identity
from numpy.lib import stride_tricks
import pandas as pd 
import numpy as np
import matplotlib as mlt
import library as lib
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from datetime import datetime

        
class table(ttk.Frame):

    def __init__(self, parent, df):
        super().__init__(parent)
        self.df = df

        self.grid(column=0, row=0)

        self.hight = df.shape[0]
        self.width = df.shape[1]

        self.widgets_entry = np.empty(shape=(self.hight, self.width), dtype="O")    
        self.values_df = np.empty(shape=(self.hight, self.width), dtype="O")        
        self.rows_numbers = np.empty(shape=self.hight, dtype="O")                  

        canvas = tk.Canvas(self)
        scrollbar_x = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=canvas.xview)
        scrollbar_y = ttk.Scrollbar(self, orient=tk.VERTICAL, command=canvas.yview)
        sizegrip = ttk.Sizegrip(self)

        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion = canvas.bbox("all")))

        canvas.create_window((0,0), window=scrollable_frame, anchor="nw")
        canvas.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)
        
        scrollbar_x.pack(side="bottom", fill="x")
        scrollbar_y.pack(side="right", fill="y")
        sizegrip.pack(in_ = scrollbar_x, side="bottom", anchor="se")
        canvas.pack(side="left", fill="both", expand=True)
        
        for i in range(self.hight): 
            for j, column in enumerate(self.df.columns):

                columns_label = ttk.Label(scrollable_frame, text=column)
                columns_label.grid(row=0, column=j+1)

                self.values_df[i, j] = tk.StringVar()

                if j == 0:                                                      #creating lables for numbers of the rows
                    self.rows_numbers[i] = ttk.Label(scrollable_frame, text=i)      
                    self.rows_numbers[i].grid(row=i+1, column=j)
                
                self.widgets_entry[i, j] = tk.Entry(scrollable_frame, textvariable = self.values_df[i, j])
                self.widgets_entry[i, j].grid(row=i+1, column=j+1)

                cnt = self.df.iloc[i, j]
                self.values_df[i, j].set(str(cnt))
                
class table_manage(ttk.Frame):
 
    def __init__(self, parent, df, file):
        super().__init__(parent)
        self.df = df
        self.file = file #file name for default saving

        self.grid(column=0, row=0)

        self.hight = df.shape[0]
        self.width = df.shape[1]

        self.widgets_entry = np.empty(shape=(self.hight, self.width), dtype="O")    #widgets to show values of the table
        self.values_df = np.empty(shape=(self.hight, self.width), dtype="O")        #values of the table
        self.rows_numbers = np.empty(shape=self.hight, dtype="O")                   #array for keeping the numbers of the rows
        self.widgets_entry_insert = np.empty(shape=(self.df.shape[1]), dtype="O")   #widgets for insert in the table

        self.initTable()
        self.initMenu()

        self.grid_columnconfigure(0, weight=1, uniform="group1")
        self.rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1, uniform="group1")
    
    def initTable(self):

        frame = table(self, self.df)
        frame.grid(column=0, row=0, sticky="nsew")

        self.widgets_entry = frame.widgets_entry
        self.values_df = frame.values_df
        self.rows_numbers = frame.rows_numbers
                
    def initMenu(self):
        #editor table
        menu = ttk.Frame(self, relief="ridge")
        menu.grid(column=1, row=0, sticky="nsew")
        
        button_save = ttk.Button(menu, text="Применить", command=self.save_changes)
        button_save.grid(column=0, row=0, padx=10, pady=10)

        label_delete = ttk.Label(menu, text="Введите номер строчки для удаления: ")
        label_delete.grid(column=0, row=1, padx=10, pady=10)

        self.entry_to_delete = ttk.Entry(menu)
        self.entry_to_delete.grid(column=1, row=1, padx=10, pady=10)

        button_delete = ttk.Button(menu, text="Удалить", command=self.delete)
        button_delete.grid(column=2, row=1, padx=10, pady=10)

        label_delete = ttk.Label(menu, text="Введите данные строчки для добавления: ")
        label_delete.grid(column=0, row=2, padx=10, pady=10)

        for i, column in enumerate(self.df.columns):
            label_column = ttk.Label(menu, text=column)
            label_column.grid(column=0, row=3+i, padx=10, pady=10)

        for i in range(self.df.shape[1]):
            self.widgets_entry_insert[i] = ttk.Entry(menu)
            self.widgets_entry_insert[i].grid(column=1, row=3+i, padx=10, pady=10)

        button_save_insert = ttk.Button(menu, text="Добавить", command=self.save_insert)
        button_save_insert.grid(column=2, row = self.width+2, padx=10, pady=10)

        label_save_as = ttk.Label(menu, text="Сохранить как: ")
        label_save_as.grid(column=0, row=self.width+3, padx=10, pady=10)

        button_save_csv = ttk.Button(menu, text=".csv", command=self.save_as_csv)
        button_save_csv.grid(column=1, row=self.width+3, padx=10, pady=10, sticky="e")

        button_save_xlsx = ttk.Button(menu, text=".xlsx", command=self.save_as_xlsx)
        button_save_xlsx.grid(column=2, row=self.width+3, padx=10, pady=10)

        button_save_pic = ttk.Button(menu, text=".pic", command=self.save_as_pic)
        button_save_pic.grid(column=3, row=self.width+3, padx=10, pady=10)

    def save_as_pic(self):
        file_name = fd.asksaveasfilename(
        filetypes=(("Picle files", "*.pic"),
                   ("All files", "*.*")))
        f = open(file_name, 'w')
        self.df.to_pickle(file_name)
        f.close()

        f_default = open(self.file+f"{datetime.now().time()}.pic", 'w')
        print(self.file+f"{datetime.now()}")
        self.df.to_pickle(f_default)
        f_default.close()

    def save_as_csv(self):
        file_name = fd.asksaveasfilename(
        filetypes=(("CSV files", "*.csv"),
                   ("All files", "*.*")))
        f = open(file_name, 'w')
        self.df.to_csv(file_name, sep = ",", index = False)
        f.close()

        f_default = open(self.file+f"{datetime.now()}", 'w')
        self.df.to_csv(f_default)
        f_default.close()

    def save_as_xlsx(self):
        file_name = fd.asksaveasfilename(
        filetypes=(("Excel files", "*.xls"),
                   ("All files", "*.*")))
        f = open(file_name, 'w')
        writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
        self.df.to_excel(writer, index = False)
        writer.save()
        f.close()

        f_default = open(self.file+f"{datetime.now()}", 'w')
        writer = pd.ExcelWriter(f_default, engine='xlsxwriter')
        self.df.to_excel(writer, index = False)
        f_default.close()

    def delete(self):
        entry = self.entry_to_delete.get()
        try:
            self.df = self.df.drop(index=[int(entry)])
            self.rows_numbers = np.delete(self.rows_numbers, -1)
            print(self.df)

            self.entry_to_delete.delete(0, 'end')
            self.initTable()
        except (ValueError,KeyError):
            mb.showerror(
                "Ошибка", 
                "Ты ввел неверные данные!")

    def clear(self, entries):
        for i in range(len(entries)):
            entries[i].delete(0, 'end')

    def save_insert(self):
        for j in range(self.width):
            if not self.widgets_entry_insert[j].get():
                mb.showerror(
                        "Ошибка", 
                        "Твое поле пустое!")
                return 0

        for j, column in enumerate(self.df.columns): 
            self.df.loc[self.hight, column] = self.widgets_entry_insert[j].get()

        self.initTable()
        self.clear(self.widgets_entry_insert)
        

    def save_changes(self):
        for i in range(self.hight): 
            for j in range(self.width): 
                self.df.iloc[i, j] = self.widgets_entry[i, j].get() 
        print(self.df)
        self.initTable()
    
   
def main():
    file_name = "output/"
    df_tracks = pd.read_excel("data/tracks.xlsx")
    df_albums = pd.read_excel("data/albums.xlsx")
    df_artists = pd.read_excel("data/artists.xlsx")
    df_genres = pd.read_excel("data/genres.xlsx")

    root = tk.Tk()
    root.geometry('1200x600+200+150')
    root.title("Менеджер")
    n = ttk.Notebook(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())

    tracks = table_manage(root, df_tracks, file_name)
    albums = table_manage(root, df_albums, file_name)
    artists = table_manage(root, df_artists, file_name)
    genres = table_manage(root, df_genres, file_name)


    n.add(tracks, text='Треки')
    n.add(albums, text='Альбомы')
    n.add(artists, text='Артисты')
    n.add(genres, text='Жанры')

    n.pack()
    root.mainloop()
 
 
if __name__ == '__main__':
    main()