import pandas as pd 
from tkinter import filedialog as fd
from datetime import datetime

class DataBase:
    df = pd.DataFrame()
    df_list = []
    df_names = []
    df_types = []
    
    def __init__(self, path):
        self.df = pd.read_excel(path)
        self.define_df()
        self.df_types_list = [[col_type for col_type in df.dtypes] for df in self.df_list]
        self.df_types = [x for x in self.df.dtypes]
        DataBase.df_types = self.df_types

    def add(self):
        record = pd.Series(["", 0, 0, 0, "", 0, 0, 0, "", ""], index=self.df.columns)
        self.df = self.df.append(record, ignore_index=True)
        self.define_df()

    def delete(self, index_df, row):
        temp_df = self.df_list[index_df]
        if index_df == 0:
            self.df = self.df.loc[self.df["Трек ID"] != temp_df.iloc[row]["Трек ID"]]
        elif index_df == 1:
            self.df = self.df.loc[self.df["Альбом ID"] != temp_df.iloc[row]["Альбом ID"]]
        elif index_df == 2:
            self.df = self.df.loc[self.df["Артист ID"] != temp_df.iloc[row]["Артист ID"]]
        else:
            self.df = self.df.loc[self.df["Жанр ID"] != temp_df.iloc[row]["Жанр ID"]]
        self.define_df()

    def define_df(self):
        self.df_tracks = self.df[["Трек ID", "Название", "Альбом ID", "Прослушиваний"]].drop_duplicates().reset_index(drop=True)
        self.df_albums = self.df[["Название альбома", "Альбом ID", "Жанр ID", "Артист ID","Стоимость", "Место создания"]].drop_duplicates().reset_index(drop=True)
        self.df_artists = self.df[["Имя артиста", "Артист ID", "Рейтинг"]].drop_duplicates().reset_index(drop=True)
        self.df_genres = self.df[["Название жанра", "Жанр ID"]].drop_duplicates().reset_index(drop=True)
        self.df_list = [self.df_tracks, self.df_albums, self.df_artists, self.df_genres]
        self.df_names = ["Треки", "Альбомы", "Артисты", "Жанры"]
        DataBase.df = self.df
        DataBase.df_list = self.df_list
        DataBase.df_names = self.df_names

    def transform_type(self):
        for i, column in enumerate(self.df.columns):
            self.df = self.df.astype({column:self.df_types[i]})

    def save_default(self, format):
        file_name_default = datetime.now().strftime("%Y%m%d-%H%M%S")
        f_default = open("output/"+file_name_default+format, 'w', encoding='utf-8')
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
        self.df.to_excel("output/"+file_name_default+".xlsx", index = False)
    
    def save_as_pic(self):
        file_name = fd.asksaveasfilename(
        filetypes=(("Picle files", "*.pic"),
                   ("All files", "*.*")))
        f = open(file_name, 'w')
        self.df.to_pickle(file_name)
        f.close()

        self.df.to_pickle(self.save_default(".pic"), index=False)

    @classmethod
    def get_full_df(cls):
        return cls.df
    
    @classmethod
    def get_list_names_df(cls):
        return cls.df_list, cls.df_names

    @classmethod
    def get_df_types(cls):
        return cls.df_types
