import os
import sys
import pandas as pd 
import numpy as np
import matplotlib as mlt
import library as lib
import tkinter as tk
import tkinter.ttk as ttk


class Table(ttk.Frame):
 
    def __init__(self, df):
        super().__init__()
        self.df = df

        self.grid(column=0, row=0)

        v = ttk.Scrollbar(self, orient=tk.VERTICAL)
        canvas = tk.Canvas(self, scrollregion=(0, 0, 1000, 1000), yscrollcommand=v.set, width=400, height=500)
        v['command'] = canvas.yview
        canvas.yview_moveto(0)

        self.interior = interior = ttk.Frame(canvas)
        interior.grid(column=0, row=0)
 
        v.grid(column=1, row=0, sticky=(tk.N,tk.S))

        menu = ttk.Frame(self, width=400, height=200, relief="ridge")
        menu.grid(column=2, row=0)

        for i, column in enumerate(self.df.columns):
            column_label = ttk.Label(interior, text=column)
            column_label.grid(row=0, column=i)

        for i, column in enumerate(self.df.columns):
            for j in range(len(df.index)):
                
                cell = ttk.Entry(interior)
                cell.insert(0,self.df[column][j])
                cell.grid(row=j+1, column=i)
        
        canvas.grid_columnconfigure(0, weight=1)
        canvas.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)


 
 
def main():
    df_tracks = pd.read_excel("data/tracks.xlsx")
    df_albums = pd.read_excel("data/albums.xlsx")
    df_artists = pd.read_excel("data/artists.xlsx")
    df_genres = pd.read_excel("data/genres.xlsx")

    root = tk.Tk()
    root.geometry('800x600+300+300')
    n = ttk.Notebook(root)

    tracks = Table(df_tracks)
    albums = Table(df_albums)
    artists = Table(df_artists)
    genres = Table(df_genres)


    n.add(tracks, text='Треки')
    n.add(albums, text='Альбомы')
    n.add(artists, text='Артисты')
    n.add(genres, text='Жанры')

    n.grid_columnconfigure(0, weight=1)
    n.grid_rowconfigure(0, weight=1)
    n.pack()
    root.mainloop()
 
 
if __name__ == '__main__':
    main()