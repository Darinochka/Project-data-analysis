import os
import sys
from numpy.core.numeric import identity
import pandas as pd 
import numpy as np
import matplotlib as mlt
import library as lib
import tkinter as tk
import tkinter.ttk as ttk

# class MenuTable(ttk.Frame(width=500, height=600)):

#     def __init__(self, df):
        
# class table(ttk.Frame):

#     def __init__(self, parent, df):
#         super().__init__(parent)
#         self.df = df

#         self.grid(column=0, row=0)

#         hight = df.shape[0]
#         weight = df.shape[1]

#         widgets_entry = np.empty(shape=(hight, weight), dtype="O")
#         values_df = np.empty(shape=(hight, weight), dtype="O")
#         rows_numbers = np.empty(shape=hight, dtype="O")
        
#         #creation canvas for scrollbar
#         canvas = tk.Canvas(frame)
#         scrollbar_x = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=canvas.xview)
#         scrollbar_y = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
#         sizegrip = ttk.Sizegrip(frame)

#         scrollable_frame = ttk.Frame(canvas)
#         scrollable_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion = canvas.bbox("all")))

#         canvas.create_window((0,0), window=scrollable_frame, anchor="nw")
#         canvas.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)
        
#         scrollbar_x.pack(side="bottom", fill="x")
#         scrollbar_y.pack(side="right", fill="y")
#         sizegrip.pack(in_ = scrollbar_x, side="bottom", anchor="se")
#         canvas.pack(side="left", fill="both", expand=True)
        
#         for i in range(hight): 
#             for j, column in enumerate(df.columns):

#                 columns_label = ttk.Label(scrollable_frame, text=column)
#                 columns_label.grid(row=0, column=j+1)

#                 values_df[i, j] = tk.StringVar()

#                 if j == 0:
#                     rows_numbers[i] = ttk.Label(scrollable_frame, text=i)
#                     rows_numbers[i].grid(row=i+1, column=j)
                
#                 widgets_entry[i, j] = tk.Entry(scrollable_frame, textvariable = values_df[i, j])
#                 widgets_entry[i, j].grid(row=i+1, column=j+1)

#                 cnt = df.iloc[i, j]
#                 values_df[i, j].set(str(cnt))
#                 # cell = ttk.Entry(scrollable_frame)
#                 # cell.insert(0,self.df[column][j])
#                 # cell.grid(row=j+1, column=i+1)
                
class table_manage(ttk.Frame):
 
    def __init__(self, parent, df):
        super().__init__(parent)
        self.df = df

        self.grid(column=0, row=0)

        self.hight = df.shape[0]
        self.width = df.shape[1]

        self.widgets_entry = np.empty(shape=(self.hight, self.width), dtype="O")
        self.values_df = np.empty(shape=(self.hight, self.width), dtype="O")
        self.rows_numbers = np.empty(shape=self.hight, dtype="O")
       
        self.initTable()
        self.initMenu()

        #config grod of the main frame
        self.grid_columnconfigure(0, weight=1, uniform="group1")
        self.rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1, uniform="group1")
        # self.rowconfigure(1, weight=1)

    def initTable(self):
        #frame with table
        frame = ttk.Frame(self, relief="ridge")
        frame.grid(column=0, row=0, sticky="nsew")

        # #creation canvas for scrollbar
        canvas = tk.Canvas(frame)
        scrollbar_x = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=canvas.xview)
        scrollbar_y = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
        sizegrip = ttk.Sizegrip(frame)

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

                if j == 0:
                    self.rows_numbers[i] = ttk.Label(scrollable_frame, text=i)
                    self.rows_numbers[i].grid(row=i+1, column=j)
                
                self.widgets_entry[i, j] = tk.Entry(scrollable_frame, textvariable = self.values_df[i, j])
                self.widgets_entry[i, j].grid(row=i+1, column=j+1)

                cnt = self.df.iloc[i, j]
                self.values_df[i, j].set(str(cnt))
                
    def initMenu(self):
        #editor table
        menu = ttk.Frame(self, relief="ridge")
        menu.grid(column=1, row=0, sticky="nsew")
        
        button_save = ttk.Button(menu, text="Применить", command=self.save)
        button_save.grid(column=0, row=0)

        self.entry_to_delete = ttk.Entry(menu)
        button_delete = ttk.Button(menu, text="Удалить", command=self.delete)

        self.entry_to_delete.grid(column=0, row=1)
        button_delete.grid(column=1, row=1)

    def delete(self):
        self.df = self.df.drop(index=[int(self.entry_to_delete.get())])
        self.rows_numbers = np.delete(self.rows_numbers, -1)
        print(self.df)
        self.initTable()

    def save(self):
        for i in range(self.hight): 
            for j in range(self.width): 
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