import os
import sys
import pandas as pd 
import numpy as np
import matplotlib as mlt
import library as lib
import tkinter as tk
import tkinter.ttk as ttk

# class MenuTable(ttk.Frame(width=500, height=600)):

#     def __init__(self, df):
        

class Table(ttk.Frame):
 
    def __init__(self, parent, df):
        super().__init__(parent)
        self.df = df

        self.grid(column=0, row=0)

        frame = ttk.Frame(self)
        frame.grid(column=0, row=0, sticky="nsew")

        my_canvas = tk.Canvas(frame)
        my_canvas.pack(side=tk.LEFT, fill=tk.BOTH)

        my_scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))
        
        second_frame = ttk.Frame(my_canvas)
        my_canvas.create_window((0,0), window=second_frame, anchor="nw")

        menu = ttk.Frame(self, relief="ridge")
        menu.grid(column=1, row=0, sticky="nsew")

        for i, column in enumerate(self.df.columns):
            second_frame.grid_columnconfigure(i, weight=1)
            second_frame.grid_rowconfigure(i, weight=1)

            column_label = ttk.Label(second_frame, text=column)
            column_label.grid(row=0, column=i+1)
            for j in range(len(df.index)):
                
                if i == 0:
                    num = ttk.Label(second_frame, text=j)
                    num.grid(row=j+1, column=i)

                cell = ttk.Entry(second_frame)
                cell.insert(0,self.df[column][j])
                cell.grid(row=j+1, column=i+1)

        self.grid_columnconfigure(0, weight=1, uniform="group1")
        self.rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1, uniform="group1")
        # self.rowconfigure(1, weight=1)
        
        
def main():
    df_tracks = pd.read_excel("data/tracks.xlsx")
    df_albums = pd.read_excel("data/albums.xlsx")
    df_artists = pd.read_excel("data/artists.xlsx")
    df_genres = pd.read_excel("data/genres.xlsx")

    root = tk.Tk()
    root.geometry('1000x600+200+150')
    n = ttk.Notebook(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())

    tracks = Table(root, df_tracks)
    albums = Table(root, df_albums)
    artists = Table(root, df_artists)
    genres = Table(root, df_genres)


    n.add(tracks, text='Треки')
    n.add(albums, text='Альбомы')
    n.add(artists, text='Артисты')
    n.add(genres, text='Жанры')

    n.pack()
    root.mainloop()
 
 
if __name__ == '__main__':
    main()