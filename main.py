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
import random as rd
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
                    label_num_row = ttk.Label(scrollable_frame, text=i)      
                    label_num_row.grid(row=i+1, column=j)
                
                self.widgets_entry[i, j] = tk.Entry(scrollable_frame, textvariable = self.values_df[i, j])
                self.widgets_entry[i, j].grid(row=i+1, column=j+1)

                cnt = self.df.iloc[i, j]
                self.values_df[i, j].set(str(cnt))
                
class table_manage(ttk.Frame):
 
    def __init__(self, parent, df, file_path):
        super().__init__(parent)
        self.df = df
        self.file_path = file_path #file name for default saving
        self.df_types = [x for x in df.dtypes]
        self.grid(column=0, row=0)

        self.hight = df.shape[0]
        self.width = df.shape[1]

        self.widgets_entry = np.empty(shape=(self.hight, self.width), dtype="O")    #widgets to show values of the table
        self.values_df = np.empty(shape=(self.hight, self.width), dtype="O")        #values of the table
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

    def save_default(self, format):
        file_name_default = datetime.now().strftime("%Y%m%d-%H%M%S")
        f_default = open(self.file_path+file_name_default+format, 'w', encoding='utf-8')
        return f_default

    def save_as_csv(self):
        file_name = fd.asksaveasfilename(
        filetypes=(("CSV files", "*.csv"),
                   ("All files", "*.*")))
        f = open(file_name, 'w')
        self.df.to_csv(file_name, sep = ",", index = False)
        f.close()

        self.df.to_csv(self.save_default(".csv"), index = False)

    def save_as_xlsx(self):
        file_name = fd.asksaveasfilename(
        filetypes=(("Excel files", "*.xls"),
                   ("All files", "*.*")))
        f = open(file_name, 'w')
        writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
        self.df.to_excel(writer, index = False, encoding='utf-8')
        writer.save()
        f.close()

        file_name_default = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.df.to_excel(self.file_path+file_name_default+".xlsx", index = False)
    
    def save_as_pic(self):
        file_name = fd.asksaveasfilename(
        filetypes=(("Picle files", "*.pic"),
                   ("All files", "*.*")))
        f = open(file_name, 'w')
        self.df.to_pickle(file_name)
        f.close()

        self.df.to_pickle(self.save_default(".pic"), index=False)

    def delete(self):
        entry = self.entry_to_delete.get()
        try:
            self.df = self.df.drop(index=[int(entry)])

            self.df = self.df.reset_index(drop=True)
            print(self.df)
            self.initTable()
        except (ValueError,KeyError):
            mb.showerror(
                "Ошибка", 
                "Ты ввел неверные данные!")
        self.entry_to_delete.delete(0, 'end')

    def clear(self, entries):
        for i in range(len(entries)):
            entries[i].delete(0, 'end')

    def save_insert(self):
        self.hight = self.df.shape[0]
        self.width = self.df.shape[1]
        
        try:
            for j in range(self.width): #check empty entries
                if not self.widgets_entry_insert[j].get():
                    raise ValueError         
            for j, column in enumerate(self.df.columns): 
                entry = self.widgets_entry_insert[j].get()

                if self.df_types[j] == np.dtype('int64'):
                    entry = int(self.widgets_entry_insert[j].get())
                elif self.df_types[j] == np.dtype('datetime64[ns]'):
                    entry = datetime.strptime(self.widgets_entry_insert[j].get(), "%Y-%m-%d")

                self.df.loc[self.hight, column] = entry

            self.df = self.transform_type(self.df, self.df_types)
            self.df = self.df.reset_index(drop=True)
            print(self.df)
            self.initTable()

        except ValueError:
            mb.showerror(
                "Ошибка", 
                "Ты ввел данные не того типа!")
                
        self.clear(self.widgets_entry_insert)
        
    def transform_type(self, df, df_types):
        for i, column in enumerate(df.columns):
            df = df.astype({column:df_types[i]})
        return df

    def save_changes(self):
        self.hight = self.df.shape[0]
        self.width = self.df.shape[1]

        try:
            for i in range(self.hight): 
                for j in range(self.width): 
                    entry = self.widgets_entry[i, j].get()

                    if self.df_types[j] == np.dtype('int64'):
                        entry = int(self.widgets_entry[i, j].get())
                    elif self.df_types[j] == np.dtype('datetime64[ns]'):
                        entry = datetime.strptime(self.widgets_entry[i, j].get(), "%Y-%m-%d")

                    self.df.iloc[i, j] = entry

            self.df = self.transform_type(self.df, self.df_types)
            print(self.df)
            self.initTable()
        except ValueError:
            mb.showerror(
                "Ошибка", 
                "Ты ввел данные не того типа!")

    
def main():
    file_path = "output/"
    df_tracks = pd.read_excel("data/tracks.xlsx")
    df_albums = pd.read_excel("data/albums.xlsx")
    df_artists = pd.read_excel("data/artists.xlsx")
    df_genres = pd.read_excel("data/genres.xlsx")

    root = tk.Tk()
    root.geometry('1200x600+200+150')
    root.title("Менеджер")
    n = ttk.Notebook(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())

    tracks = table_manage(root, df_tracks, file_path)
    albums = table_manage(root, df_albums, file_path)
    artists = table_manage(root, df_artists, file_path)
    genres = table_manage(root, df_genres, file_path)


    n.add(tracks, text='Треки')
    n.add(albums, text='Альбомы')
    n.add(artists, text='Артисты')
    n.add(genres, text='Жанры')

    n.pack()
    root.mainloop()
 
 
if __name__ == '__main__':
    main()