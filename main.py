import os
import sys
from numpy.core.numeric import identity
import pandas as pd 
import numpy as np
import matplotlib as mlt
import library as lib
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as mb
from tkinter import filedialog as fd

# class MenuTable(ttk.Frame(width=500, height=600)):

#     def __init__(self, df):
        
class table(ttk.Frame):

    def __init__(self, parent, df):
        super().__init__(parent)
        self.df = df

        self.grid(column=0, row=0)

        self.hight = df.shape[0] #quantity of the rows
        self.width = df.shape[1] #quantity of the columns

        self.widgets_entry = np.empty(shape=(self.hight, self.width), dtype="O")    #widgets to show values of the table
        self.values_df = np.empty(shape=(self.hight, self.width), dtype="O")        #values of the table
        self.rows_numbers = np.empty(shape=self.hight, dtype="O")                   #array for keeping the numbers of the rows
        self.widgets_entry_insert = np.empty(shape=(self.df.shape[1]), dtype="O")
        # #creation canvas for scrollbar
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
        
        #creating the table
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
 
    def __init__(self, parent, df):
        super().__init__(parent)
        self.df = df

        self.grid(column=0, row=0)

        self.hight = df.shape[0] #quantity of the rows
        self.width = df.shape[1] #quantity of the columns

        self.widgets_entry = np.empty(shape=(self.hight, self.width), dtype="O")    #widgets to show values of the table
        self.values_df = np.empty(shape=(self.hight, self.width), dtype="O")        #values of the table
        self.rows_numbers = np.empty(shape=self.hight, dtype="O")                   #array for keeping the numbers of the rows
        self.widgets_entry_insert = np.empty(shape=(self.df.shape[1]), dtype="O")   #wodgets for insert in the table

        self.initTable()
        self.initMenu()

        #config grod of the main frame
        self.grid_columnconfigure(0, weight=1, uniform="group1")
        self.rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1, uniform="group1")
        # self.rowconfigure(1, weight=1)
    
    def initTable(self):

        # self.hight = self.df.shape[0]
        # self.width = self.df.shape[1]

        # self.widgets_entry = np.empty(shape=(self.hight, self.width), dtype="O")
        # self.values_df = np.empty(shape=(self.hight, self.width), dtype="O")
        # self.rows_numbers = np.empty(shape=self.hight, dtype="O")

        frame = table(self, self.df)
        frame.grid(column=0, row=0, sticky="nsew")

        self.widgets_entry = frame.widgets_entry
        self.values_df = frame.values_df
        self.rows_numbers = frame.rows_numbers
        self.widgets_entry_insert = frame.widgets_entry_insert
        #frame with table
        # frame = ttk.Frame(self, relief="ridge")
        # frame.grid(column=0, row=0, sticky="nsew")

        # #creation canvas for scrollbar
        # canvas = tk.Canvas(frame)
        # scrollbar_x = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=canvas.xview)
        # scrollbar_y = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
        # sizegrip = ttk.Sizegrip(frame)

        # scrollable_frame = ttk.Frame(canvas)
        # scrollable_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion = canvas.bbox("all")))

        # canvas.create_window((0,0), window=scrollable_frame, anchor="nw")
        # canvas.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)
        
        # scrollbar_x.pack(side="bottom", fill="x")
        # scrollbar_y.pack(side="right", fill="y")
        # sizegrip.pack(in_ = scrollbar_x, side="bottom", anchor="se")
        # canvas.pack(side="left", fill="both", expand=True)
        
        # #creating the table
        # for i in range(self.hight): 
        #     for j, column in enumerate(self.df.columns):

        #         columns_label = ttk.Label(scrollable_frame, text=column)
        #         columns_label.grid(row=0, column=j+1)

        #         self.values_df[i, j] = tk.StringVar()

        #         if j == 0:                                                      #creating lables for numbers of the rows
        #             self.rows_numbers[i] = ttk.Label(scrollable_frame, text=i)      
        #             self.rows_numbers[i].grid(row=i+1, column=j)
                
        #         self.widgets_entry[i, j] = tk.Entry(scrollable_frame, textvariable = self.values_df[i, j])
        #         self.widgets_entry[i, j].grid(row=i+1, column=j+1)

        #         cnt = self.df.iloc[i, j]
        #         self.values_df[i, j].set(str(cnt))
                
    def initMenu(self):
        #editor table
        menu = ttk.Frame(self, relief="ridge")
        menu.grid(column=1, row=0, sticky="nsew")
        
        button_save = ttk.Button(menu, text="Применить", command=self.save)
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

        label_save_as = ttk.Label(menu, text="Сохранить как: ")
        label_save_as.grid(column=0, row=self.df.shape[1]+3, padx=10, pady=1)

        button_save_csv = ttk.Button(menu, text=".csv", command=self.save_as_csv)
        button_save_csv.grid(column=1, row=self.df.shape[1]+3, padx=10, pady=10)

        button_save_xlsx = ttk.Button(menu, text=".xlsx", command=self.save_as_xlsx)
        button_save_xlsx.grid(column=2, row=self.df.shape[1]+3, padx=10, pady=10)

    def save_as_csv(self):
        file_name = fd.asksaveasfilename(
        filetypes=(("CSV files", "*.csv"),
                   ("All files", "*.*")))
        f = open(file_name, 'w')
        self.df.to_csv(file_name, sep = ",", index = False)
        f.close()

    def save_as_xlsx(self):
        file_name = fd.asksaveasfilename(
        filetypes=(("Excel files", "*.xls"),
                   ("All files", "*.*")))
        f = open(file_name, 'w')
        writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
        self.df.to_excel(writer, index = False)
        writer.save()
        f.close()

    def delete(self):
        self.df = self.df.drop(index=[int(self.entry_to_delete.get())])
        self.rows_numbers = np.delete(self.rows_numbers, -1)
        print(self.df)
        self.initTable()

    def save(self):
        hight = self.hight
        
        for i in range(self.hight): 
            for j, column in enumerate(self.df.columns): 
                self.df.loc[hight, column] = self.widgets_entry_insert[j].get()
                self.df.iloc[i, j] = self.widgets_entry[i, j].get() 
        print(self.df)
        self.initTable()
    
    
   
def main():
    df_tracks = pd.read_excel("data/tracks.xlsx")
    df_albums = pd.read_excel("data/albums.xlsx")
    df_artists = pd.read_excel("data/artists.xlsx")
    df_genres = pd.read_excel("data/genres.xlsx")

    root = tk.Tk()
    root.geometry('1000x600+200+150')
    root.title("Менеджер")
    n = ttk.Notebook(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())

    tracks = table_manage(root, df_tracks)
    albums = table_manage(root, df_albums)
    artists = table_manage(root, df_artists)
    genres = table_manage(root, df_genres)


    n.add(tracks, text='Треки')
    n.add(albums, text='Альбомы')
    n.add(artists, text='Артисты')
    n.add(genres, text='Жанры')

    n.pack()
    root.mainloop()
 
 
if __name__ == '__main__':
    main()