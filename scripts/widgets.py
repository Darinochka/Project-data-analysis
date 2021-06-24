import pandas as pd 
import numpy as np
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as mb
from tkinter import filedialog as fd
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib as mt
from datetime import datetime
import sys
sys.path.insert(1, 'D:/Google/University/data_analysis/work')

from library.db import *


class Table(ttk.Frame):

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

    def get_df(self):
        for i in range(self.hight):
            for j in range(len(self.df.columns)):
                self.df.iloc[i, j] = self.values_df[i, j].get()
        print(self.df)
        return self.df

class TableManage(DataBase):
    def __init__(self, root):
        super().__init__("data/tracks1.xlsx")

        self.manager = ttk.Frame(root)
        self.manager.grid(column=0, row=0)

        self.choice_data = tk.IntVar()
        self.choice_data.set(0)
        
        self.widgets_entry = np.empty(shape=(self.df.shape[0], self.df.shape[1]), dtype="O") 
        
        self.init_menu()
        self.init_table()

        self.manager.grid_columnconfigure(0, weight=1, uniform="group1")
        self.manager.rowconfigure(0, weight=1)
        self.manager.grid_columnconfigure(1, weight=1, uniform="group1")

    def init_table(self):
        temp = self.df_list[self.choice_data.get()].copy()
        self.table = Table(self.manager, temp)
        self.table.grid(column=0, row=0, sticky="nsew")

    def save_change(self):
        df = self.table.get_df()
        init_df = self.df_list[self.choice_data.get()]

        if self.check_types(df):
            for i in range(self.df.shape[0]):

                for x in range(init_df.shape[0]):
                    if self.df.loc[i][list(df.columns)].equals(other=init_df.loc[x]):
                        for column in init_df:
                            self.df.iloc[i, self.df.columns.get_loc(column)] = df[column][x]
                        break

            self.define_df()
            self.transform_type()
            self.init_table()

    def check_types(self, df):
        types = self.df_types_list[self.choice_data.get()]
        try:
            for i in range(df.shape[0]):
                for j in range(df.shape[1]):
                    entry = df.iloc[i, j]
                    if types[j] == np.dtype("int64"):
                        int(entry)

                    elif types[j] == np.dtype('float64'):
                        float(entry)

                    elif types[j] == np.dtype('datetime64[ns]'):
                        datetime.strptime(entry, "%Y-%m-%d") 
            return True
        except:
            mb.showerror(
                "Ошибка", 
                "Ты ввел данные не того типа!")
            return False

    def add_record(self):
        self.add()
        self.init_table()
        print(self.df)

    def delete_record(self):
        df = self.df_list[self.choice_data.get()]
        entry = int(self.delete_entry.get())
        if 0 <= entry and entry < df.shape[0]:
            self.delete(self.choice_data.get(), entry)
            self.init_table()
        else:
            mb.showerror(
                "Ошибка", 
                "Ты ввел неверные данные!")
        self.delete_entry.delete(0, 'end')

    def init_menu(self):
        menu = ttk.Frame(self.manager)
        menu.grid(column=1, row=0, sticky="nsew")

        label_choose = ttk.Label(menu, text="Выберите базу данных: ")
        label_choose.grid(column=0, row=0, padx=10, pady=10, sticky="nw")

        row_iter = 0

        for i in range(len(self.df_list)):
            radiobutton_choice = ttk.Radiobutton(menu, text=self.df_names[i], variable=self.choice_data, value=i, command=self.init_table)
            radiobutton_choice.grid(column=1, row=row_iter, padx=10, pady=10, sticky="nw")
            row_iter+=1

        add_button = ttk.Button(menu, text="Добавить", command=self.add_record, style='Kim.TButton')
        add_button.grid(column=0, row=row_iter, padx=10, pady=10, sticky="nw")

        delete_button = ttk.Button(menu, text="Удалить", command=self.delete_record)
        delete_button.grid(column=1, row=row_iter, padx=10, pady=10, sticky="nw")

        self.delete_entry = ttk.Entry(menu)
        self.delete_entry.grid(column=2, row=row_iter, padx=10, pady=10, sticky="nw")

        save_change = ttk.Button(menu, text="Применить изменения", command=self.save_change)
        save_change.grid(column=3, row=row_iter, padx=10, pady=10, sticky="nw")

        label_save_as = ttk.Label(menu, text="Сохранить как: ")
        label_save_as.grid(column=0, row=row_iter+1, padx=10, pady=10)

        button_save_csv = ttk.Button(menu, text=".csv", command=self.save_as_csv)
        button_save_csv.grid(column=1, row=row_iter+1, padx=10, pady=10, sticky="e")

        button_save_xlsx = ttk.Button(menu, text=".xlsx", command=self.save_as_xlsx)
        button_save_xlsx.grid(column=1, row=row_iter+2, padx=10, pady=10)

        button_save_pic = ttk.Button(menu, text=".pic", command=self.save_as_pic)
        button_save_pic.grid(column=1, row=row_iter+3, padx=10, pady=10)

    def get_frame(self):
        return self.manager

class SampleData(DataBase):

    def __init__(self, parent):
        self.df = self.get_full_df()
        self.df_list, self.df_names = self.get_list_names_df()
        self.menu = ttk.Frame(parent)
        self.menu.grid(column=0, row=0)

        self.df_curr = self.df_list[0]
        self.df_change_curr = self.df_curr

        self.choice_data = tk.IntVar()
        self.choice_data.set(0)

        self.choice_attr = np.empty(shape=(self.df_curr.shape[1]), dtype="O")

        self.init_manager()

        self.menu.grid_columnconfigure(0, weight=1, uniform="group1")
        self.menu.rowconfigure(0, weight=1)
        self.menu.grid_columnconfigure(1, weight=1, uniform="group1")

    def init_table(self, df):
        table = Table(self.menu, df)
        table.grid(column=0, row=0, sticky="nsew")

    def change_main_base(self):
        self.df = self.get_full_df()
        self.df_list, self.df_names = self.get_list_names_df()
        self.df_curr = self.df_list[self.choice_data.get()]
        self.choice_attr = np.empty(shape=(self.df_curr.shape[1]), dtype="O")
        self.init_table(self.df_curr)
        self.init_manager()

    def init_manager(self):
        manager = ttk.Frame(self.menu)
        manager.grid(column=1, row=0, sticky="nsew")

        label_choose = ttk.Label(manager, text="Выберите базу данных: ")
        label_choose.grid(column=0, row=0, padx=10, pady=10, sticky="nw")

        len_df_list = len(self.df_list)
        row_iter = 1

        for i in range(len_df_list):
            radiobutton_choice = ttk.Radiobutton(manager, text=self.df_names[i], variable=self.choice_data, value=i, command=self.change_main_base)
            radiobutton_choice.grid(column=0, row=row_iter, padx=10, pady=10, sticky="nw")
            row_iter+=1

        label_choose_attr = ttk.Label(manager, text="Выберите атрибуты базы данных: ")
        label_choose_attr.grid(column=0, row=row_iter, padx=10, pady=10, sticky="nw")

        for i, column in enumerate(self.df_curr.columns):
            row_iter+=1
            self.choice_attr[i] = tk.BooleanVar()
            check_attr = ttk.Checkbutton(manager, text=column, onvalue=True, offvalue=False, variable=self.choice_attr[i])
            check_attr.grid(column=0, row=row_iter, padx=10, pady=10, sticky="nw")
        
        button_change = ttk.Button(manager, text="Применить", command=self.save_change)
        button_change.grid(column=0, row=row_iter+1, padx=10, pady=10, sticky="nw")

        label_save_as = ttk.Label(manager, text="Сохранить как: ")
        label_save_as.grid(column=0, row=row_iter+2, padx=10, pady=10, sticky="nw")

        button_save_csv = ttk.Button(manager, text=".csv", command=self.save_as_csv)
        button_save_csv.grid(column=1, row=row_iter+2, padx=10, pady=10, sticky="e")

        button_save_xlsx = ttk.Button(manager, text=".xlsx", command=self.save_as_xlsx)
        button_save_xlsx.grid(column=2, row=row_iter+2, padx=10, pady=10)

        button_save_pic = ttk.Button(manager, text=".pic", command=self.save_as_pic)
        button_save_pic.grid(column=3, row=row_iter+2, padx=10, pady=10)

    def save_change(self):
        values = [self.df_curr.columns[i] for i in range(len(self.choice_attr)) if self.choice_attr[i].get()]
        self.df_change_curr = self.df_curr[values]
        self.init_table(self.df_change_curr)

    def save_default(self, format):
        file_name_default = datetime.now().strftime("%Y%m%d-%H%M%S")
        f_default = open("output/"+file_name_default+format, 'w', encoding='utf-8')
        return f_default

    def save_as_csv(self):
        file_name = fd.asksaveasfilename(
        filetypes=(("CSV files", "*.csv"),
                   ("All files", "*.*")))
        f = open(file_name, 'w')
        self.df_change_curr.to_csv(file_name, sep = ",", index = False)
        f.close()

        self.df_change_curr.to_csv(self.save_default(".csv"), index = False)

    def save_as_xlsx(self):
        file_name = fd.asksaveasfilename(
        filetypes=(("Excel files", "*.xls"),
                   ("All files", "*.*")))
        f = open(file_name, 'w')
        writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
        self.df_change_curr.to_excel(writer, index = False, encoding='utf-8')
        writer.save()
        f.close()

        file_name_default = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.df_change_curr.to_excel("output/"+file_name_default+".xlsx", index = False)
    
    def save_as_pic(self):
        file_name = fd.asksaveasfilename(
        filetypes=(("Picle files", "*.pic"),
                   ("All files", "*.*")))
        f = open(file_name, 'w')
        self.df_change_curr.to_pickle(file_name)
        f.close()

        self.df_change_curr.to_pickle(self.save_default(".pic"), index=False)
    
    def get_frame(self):
        return self.menu

class QualityData(DataBase):
    def __init__(self, parent, file_path):
        self.df_list, self.df_names = self.get_list_names_df()
        self.file_path = file_path

        self.frame = ttk.Frame(parent)

        self.df_curr = self.df_list[0] #current dataframe
        self.df_stat_curr = pd.DataFrame() #current statistic dataframe
        self.df_types = [[col_type for col_type in df.dtypes] for df in self.df_list] #list of the types every dataframe
        self.df_curr_types = self.df_types[0]   #current types of the current dataframe

        self.choice_data = tk.IntVar()  #choice of dataframe
        self.choice_data.set(-1)

        self.choice_attr = tk.StringVar()   #choice of the attribute
        self.choice_attr.set("")

        self.attr = []
        self.define_quality_attr()

        self.init_manager()

        self.frame.grid_rowconfigure(0, weight=1, uniform="group1")
        self.frame.columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1, uniform="group1")

    def init_table(self, df):
        table = Table(self.frame, df)
        table.grid(column=0, row=1, sticky="nsew")

    def change_main_base(self):
        self.df_list, self.df_names = self.get_list_names_df()
        self.df_curr = self.df_list[self.choice_data.get()]
        self.df_curr_types = self.df_types[self.choice_data.get()]
        self.define_quality_attr()
        self.init_manager()

    def build_statistic(self):
        df = self.df_curr.groupby(self.df_curr[self.choice_attr.get()]).size().reset_index(name="Количество")
        df["Частотность"] = pd.Series((round(df["Количество"]/self.df_curr.shape[0], 3))*100, index=df.index)
        self.df_stat_curr = df
        self.init_table(df)

    def define_quality_attr(self):
        self.attr = []
        for i in range(len(self.df_curr.columns)):
            if self.df_curr_types[i] == "O":
               self.attr.append(self.df_curr.columns[i]) 

    def init_manager(self):
        manager = ttk.Frame(self.frame)
        manager.grid(column=0, row=0, sticky="nsew")

        label_attr = ttk.Label(manager, text="Качественные атрибуты")
        label_attr.grid(column=0, row=0, padx=10, pady=10, sticky="nw")

        label_choose = ttk.Label(manager, text="Выберите базу данных: ")
        label_choose.grid(column=0, row=1, padx=10, pady=10, sticky="nw")

        len_df_list = len(self.df_list)
        column_iter = 0

        for i in range(len_df_list):
            radiobutton_choice = ttk.Radiobutton(manager, 
                                                text=self.df_names[i], 
                                                variable=self.choice_data, 
                                                value=i, 
                                                command=self.change_main_base)
            radiobutton_choice.grid(column=column_iter, row=2, padx=5, pady=5, sticky="ne")
            column_iter+=1

        label_choose_attr = ttk.Label(manager, text="Выберите атрибуты базы данных: ")
        label_choose_attr.grid(column=0, row=3, padx=10, pady=10, sticky="nw")

        self.define_quality_attr()

        column_iter = 0
        for i in range(len(self.attr)):
            if self.attr[i]:
                radiobutton_choice = ttk.Radiobutton(manager, 
                                                    text=self.attr[i], 
                                                    variable=self.choice_attr, 
                                                    value=self.attr[i], 
                                                    command=self.build_statistic)
                radiobutton_choice.grid(column=column_iter, row=4, padx=5, pady=5, sticky="ne")
                column_iter+=1

        label_save_as = ttk.Label(manager, text="Сохранить как: ")
        label_save_as.grid(column=0, row=5, padx=10, pady=10)

        button_save_csv = ttk.Button(manager, text=".csv", command=self.save_as_csv)
        button_save_csv.grid(column=1, row=5, padx=10, pady=10, sticky="e")

        button_save_xlsx = ttk.Button(manager, text=".xlsx", command=self.save_as_xlsx)
        button_save_xlsx.grid(column=2, row=5, padx=10, pady=10)

        button_save_pic = ttk.Button(manager, text=".pic", command=self.save_as_pic)
        button_save_pic.grid(column=3, row=5, padx=10, pady=10)

    def save_default(self, format):
        file_name_default = datetime.now().strftime("%Y%m%d-%H%M%S")
        f_default = open(self.file_path+file_name_default+format, 'w', encoding='utf-8')
        return f_default

    def save_as_csv(self):
        file_name = fd.asksaveasfilename(
        filetypes=(("CSV files", "*.csv"),
                   ("All files", "*.*")))
        f = open(file_name, 'w')
        self.df_stat_curr.to_csv(file_name, sep = ",", index = False)
        f.close()

        self.df_stat_curr.to_csv(self.save_default(".csv"), index = False)

    def save_as_xlsx(self):
        file_name = fd.asksaveasfilename(
        filetypes=(("Excel files", "*.xls"),
                   ("All files", "*.*")))
        f = open(file_name, 'w')
        writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
        self.df_stat_curr.to_excel(writer, index = False, encoding='utf-8')
        writer.save()
        f.close()

        file_name_default = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.df_stat_curr.to_excel(self.file_path+file_name_default+".xlsx", index = False)
    
    def save_as_pic(self):
        file_name = fd.asksaveasfilename(
        filetypes=(("Picle files", "*.pic"),
                   ("All files", "*.*")))
        f = open(file_name, 'w')
        self.df_stat_curr.to_pickle(file_name)
        f.close()

        self.df_stat_curr.to_pickle(self.save_default(".pic"), index=False)
    def get_frame(self):
        return self.frame

class QuantityData(DataBase):
    def __init__(self, parent, file_path):
        self.df_list, self.df_names = self.get_list_names_df()
        self.file_path = file_path
        
        self.frame = ttk.Frame(parent)

        self.df_curr = self.df_list[0] #current dataframe
        self.df_stat_curr = pd.DataFrame()
        self.df_types = [[col_type for col_type in df.dtypes] for df in self.df_list] #list of the types every dataframe
        self.df_curr_types = self.df_types[0]   #current types of the current dataframe

        self.choice_data = tk.IntVar()  #choice of dataframe
        self.choice_data.set(-1)

        self.choice_attr = tk.StringVar()   #choice of the attribute
        self.choice_attr.set("")

        self.define_quantity_attr()

        self.init_manager()

        self.frame.grid_rowconfigure(0, weight=1, uniform="group1")
        self.frame.columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1, uniform="group1")

    def init_table(self, df):
        table = Table(self.frame, df)
        table.grid(column=0, row=1, sticky="nsew")

    def change_main_base(self):
        self.df_list, self.df_names = self.get_list_names_df()
        self.df_curr = self.df_list[self.choice_data.get()]
        self.df_curr_types = self.df_types[self.choice_data.get()]
        self.transform_type()
        self.build_statistic()

    def transform_type(self):
        for i, column in enumerate(self.df_curr.columns):
            self.df_curr = self.df_curr.astype({column:self.df_curr_types[i]})

    def build_statistic(self):
        self.define_quantity_attr()
        df = pd.DataFrame(index=self.df_curr.columns)
        df["Переменные"] = self.df_curr.columns
        df["Среднее"] = self.df_curr.mean().round(3)
        df["Максимальное"] = self.df_curr.max().round(3)
        df["Минимальное"] = self.df_curr.min().round(3)
        df["Выборочная дисперсия"] = self.df_curr.var(ddof=1).round(3)
        df["Стадартное отклонение"] = self.df_curr.std().round(3)
        self.df_stat_curr = df
        self.init_table(df)

    def define_quantity_attr(self):
        attr = []
        for i in range(len(self.df_curr.columns)):
            if self.df_curr_types[i] == "int64" or self.df_curr_types[i] == "float64":
               attr.append(self.df_curr.columns[i]) 
        self.df_curr = self.df_curr[attr]
        
    def init_manager(self):
        manager = ttk.Frame(self.frame)
        manager.grid(column=0, row=0, sticky="nsew")

        label_attr = ttk.Label(manager, text="Количественные атрибуты")
        label_attr.grid(column=0, row=0, padx=10, pady=10, sticky="nw")

        label_choose = ttk.Label(manager, text="Выберите базу данных: ")
        label_choose.grid(column=0, row=1, padx=10, pady=10, sticky="nw")

        len_df_list = len(self.df_list)
        column_iter = 0

        for i in range(len_df_list):
            radiobutton_choice = ttk.Radiobutton(manager, text=self.df_names[i], variable=self.choice_data, value=i, command=self.change_main_base)
            radiobutton_choice.grid(column=column_iter, row=2, padx=5, pady=5, sticky="ne")
            column_iter+=1

        label_save_as = ttk.Label(manager, text="Сохранить как: ")
        label_save_as.grid(column=0, row=5, padx=10, pady=10)

        button_save_csv = ttk.Button(manager, text=".csv", command=self.save_as_csv)
        button_save_csv.grid(column=1, row=5, padx=10, pady=10, sticky="e")

        button_save_xlsx = ttk.Button(manager, text=".xlsx", command=self.save_as_xlsx)
        button_save_xlsx.grid(column=2, row=5, padx=10, pady=10)

        button_save_pic = ttk.Button(manager, text=".pic", command=self.save_as_pic)
        button_save_pic.grid(column=3, row=5, padx=10, pady=10)

    def save_default(self, format):
        file_name_default = datetime.now().strftime("%Y%m%d-%H%M%S")
        f_default = open(self.file_path+file_name_default+format, 'w', encoding='utf-8')
        return f_default

    def save_as_csv(self):
        file_name = fd.asksaveasfilename(
        filetypes=(("CSV files", "*.csv"),
                   ("All files", "*.*")))
        f = open(file_name, 'w')
        self.df_stat_curr.to_csv(file_name, sep = ",", index = False)
        f.close()

        self.df_stat_curr.to_csv(self.save_default(".csv"), index = False)

    def save_as_xlsx(self):
        file_name = fd.asksaveasfilename(
        filetypes=(("Excel files", "*.xls"),
                   ("All files", "*.*")))
        f = open(file_name, 'w')
        writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
        self.df_stat_curr.to_excel(writer, index = False, encoding='utf-8')
        writer.save()
        f.close()

        file_name_default = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.df_stat_curr.to_excel(self.file_path+file_name_default+".xlsx", index = False)
    
    def save_as_pic(self):
        file_name = fd.asksaveasfilename(
        filetypes=(("Picle files", "*.pic"),
                   ("All files", "*.*")))
        f = open(file_name, 'w')
        self.df_stat_curr.to_pickle(file_name)
        f.close()

        self.df_stat_curr.to_pickle(self.save_default(".pic"), index=False)
    def get_frame(self):
        return self.frame

class StaticData(ttk.Frame):
    def __init__(self, parent, file_path):
        super().__init__(parent)
        self.grid(column=0, row=0)

        quality = QualityData(self, file_path).get_frame()
        quality.grid(column=0, row=0, sticky="nsew")
        quantity = QuantityData(self, file_path).get_frame()
        quantity.grid(column=1, row=0, sticky="nsew")

        self.grid_columnconfigure(0, weight=1, uniform="group1")
        self.rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1, uniform="group1")

class PivotTable(DataBase):
    def __init__(self, parent, file_path):
        self.df_list, self.df_names = self.get_list_names_df()

        self.frame = ttk.Frame(parent)
        self.frame.grid(column=0, row=0)
 
        self.df_curr = self.df_list[0]
        self.df_types = [[col_type for col_type in df.dtypes] for df in self.df_list] #list of the types every dataframe
        self.df_curr_types = self.df_types[0]
        self.file_path = file_path

        self.df_update = pd.DataFrame()
        self.choice_data = tk.IntVar()  #choice of dataframe
        self.choice_data.set(-1)

        self.aggfunc = tk.StringVar()  #choice of datafram

        self.first_attr = tk.StringVar()
        self.second_attr = tk.StringVar()

        self.attr = []
        self.define_quality_attr()

        self.init_manager()

        self.frame.grid_columnconfigure(0, weight=1, uniform="group1")
        self.frame.rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1, uniform="group1")

    def change_main_base(self):
        self.df_list, self.df_names = self.get_list_names_df()
        self.df_curr = self.df_list[self.choice_data.get()]
        self.df_curr_types = self.df_types[self.choice_data.get()]
        self.define_quality_attr()
        self.clear_combobox()
        self.init_manager()
    
    def clear_combobox(self):
        self.first_attr.set("")
        self.second_attr.set("")
        self.aggfunc.set("")

    def define_quality_attr(self):
        self.attr = []
        for i in range(len(self.df_curr.columns)):
            if self.df_curr_types[i] == "O":
               self.attr.append(self.df_curr.columns[i]) 

    def init_table(self, df):
        table = Table(self.frame, df)
        table.grid(column=0, row=0, sticky="nsew")

    def change_table(self):
        try:
            index = [self.first_attr.get(), self.second_attr.get()]

            if self.aggfunc.get() == "Среднее":
                df_update = pd.pivot_table(self.df_curr, index=index, aggfunc=np.mean)
            elif self.aggfunc.get() == "Сумма":
                df_update = pd.pivot_table(self.df_curr, index=index, aggfunc=np.sum)
            elif self.aggfunc.get() == "Максимум":
                df_update = pd.pivot_table(self.df_curr, index=index, aggfunc=np.max)
            elif self.aggfunc.get() == "Минимум":
                df_update = pd.pivot_table(self.df_curr, index=index, aggfunc=np.min)

            self.df_update = df_update.reset_index()
            self.init_table(self.df_update)
        except:
            mb.showerror(
                "Ошибка", 
                "Ты ввел неверные данные!")

    def init_manager(self):
        manager = ttk.Frame(self.frame)
        manager.grid(column=1, row=0, sticky="nsew")

        choice_dataframe = ttk.Label(manager, text="Выберите базу данных: ")
        choice_dataframe.grid(column=0, row=0, padx=10, pady=10, sticky="nw")
        
        len_df_list = len(self.df_list)
        row_iter = 0

        for i in range(len_df_list):
            radiobutton_choice = ttk.Radiobutton(manager, 
                                                text=self.df_names[i], 
                                                variable=self.choice_data, 
                                                value=i, 
                                                command=self.change_main_base)
            radiobutton_choice.grid(column=1, row=row_iter, padx=10, pady=10, sticky="nw")
            row_iter+=1

        choice_quality_attr = ttk.Label(manager, text="Выберите пару качественных\n атрибутов: ")
        choice_quality_attr.grid(column=0, row=row_iter+1, padx=10, pady=10, sticky="nw")

        first_attr_choice = ttk.Combobox(manager, textvariable=self.first_attr, state="readonly", values=self.attr)
        first_attr_choice.grid(column=1, row=row_iter+1, padx=10, pady=10)

        second_attr_choice = ttk.Combobox(manager, textvariable=self.second_attr, state="readonly", values=self.attr)
        second_attr_choice.grid(column=2, row=row_iter+1, padx=10, pady=10)

        label_сhoice_afffunc = ttk.Label(manager, text="Выберите метод агрегации: ")
        label_сhoice_afffunc.grid(column=0, row=row_iter+2, padx=10, pady=10, sticky="nw")

        agg_funcs = ["Среднее", "Сумма", "Максимум", "Минимум"]

        choice_agg_func = ttk.Combobox(manager, textvariable=self.aggfunc, state="readonly", values=agg_funcs)
        choice_agg_func.grid(column=1, row=row_iter+2, padx=10, pady=10)

        apply_button = ttk.Button(manager, text="Применить", command=self.change_table)
        apply_button.grid(column=2, row=row_iter+2, padx=10, pady=10, sticky="ne")

        label_save_as = ttk.Label(manager, text="Сохранить как: ")
        label_save_as.grid(column=0, row=row_iter+4, padx=10, pady=10, sticky="nw")

        button_save_csv = ttk.Button(manager, text=".csv", command=self.save_as_csv)
        button_save_csv.grid(column=1, row=row_iter+4, padx=10, pady=10, sticky="e")

        button_save_xlsx = ttk.Button(manager, text=".xlsx", command=self.save_as_xlsx)
        button_save_xlsx.grid(column=1, row=row_iter+5, padx=10, pady=10, sticky="e")

        button_save_pic = ttk.Button(manager, text=".pic", command=self.save_as_pic)
        button_save_pic.grid(column=1, row=row_iter+6, padx=10, pady=10, sticky="e")

    def save_default(self, format):
        file_name_default = datetime.now().strftime("%Y%m%d-%H%M%S")
        f_default = open(self.file_path+file_name_default+format, 'w', encoding='utf-8')
        return f_default

    def save_as_csv(self):
        file_name = fd.asksaveasfilename(
        filetypes=(("CSV files", "*.csv"),
                   ("All files", "*.*")))
        f = open(file_name, 'w')
        self.df_update.to_csv(file_name, sep = ",", index = False)
        f.close()

        self.df_update.to_csv(self.save_default(".csv"), index = False)

    def save_as_xlsx(self):
        file_name = fd.asksaveasfilename(
        filetypes=(("Excel files", "*.xls"),
                   ("All files", "*.*")))
        f = open(file_name, 'w')
        writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
        self.df_update.to_excel(writer, index = False, encoding='utf-8')
        writer.save()
        f.close()

        file_name_default = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.df_update.to_excel(self.file_path+file_name_default+".xlsx", index = False)
    
    def save_as_pic(self):
        file_name = fd.asksaveasfilename(
        filetypes=(("Picle files", "*.pic"),
                   ("All files", "*.*")))
        f = open(file_name, 'w')
        self.df_update.to_pickle(file_name)
        f.close()

        self.df_update.to_pickle(self.save_default(".pic"), index=False)

    def get_frame(self):
        return self.frame

class BarPlot(DataBase):
    def __init__(self, parent, file_path):
        self.df = self.get_full_df()

        self.frame = ttk.Frame(parent)
        self.frame.grid(column=0, row=0)

        self.file_path = file_path
        
        self.df_types = self.get_df_types()

        self.qual_attr = tk.StringVar()
        self.quan_attr = tk.StringVar()

        self.define_quality_attr()
        self.define_quantity_attr()
        self.init_manager()
        mt.use('TkAgg')

    def transform_type(self):
        for i, column in enumerate(self.df.columns):
            self.df = self.df.astype({column:self.df_types[i]})

    def define_quality_attr(self):
        self.quality_attributes = []
        for i in range(len(self.df.columns)):
            if self.df_types[i] == "O":
               self.quality_attributes.append(self.df.columns[i])

    def define_quantity_attr(self):
        self.quantity_attributes = []
        for i in range(len(self.df.columns)):
            if self.df_types[i] == "int64" or self.df_types[i] == "float64":
               self.quantity_attributes.append(self.df.columns[i]) 

    def init_graph(self):
        self.df = self.get_full_df()
        self.transform_type()

        try:
            plt.style.use('ggplot')
            plt.rcParams['font.size'] = '7'

            fig = plt.figure(figsize=(10, 4.4), dpi=100)

            canvas = FigureCanvasTkAgg(fig, master=self.frame)
            plot_widget = canvas.get_tk_widget()
            plot_widget.grid(column=0, row=1, padx=20, sticky="e")

            df = pd.pivot_table(self.df, index=[self.qual_attr.get()], values=[self.quan_attr.get()])
            ax = fig.add_subplot()  
            df.plot(kind='barh', legend=True, ax=ax)
            plt.tight_layout()
        except:
            mb.showerror(
                "Ошибка", 
                "Ты ввел неверные данные!")
        
    def init_manager(self):
        manager = ttk.Frame(self.frame)
        manager.grid(column=0, row=0)

        label_choice = ttk.Label(manager, text="Выберите качественный атрибут: ")
        label_choice.grid(column=0, row=0, padx=10, pady=10)

        first_choice_rad = ttk.Combobox(manager, textvariable=self.qual_attr, state="readonly", values=self.quality_attributes)
        first_choice_rad.grid(column=1, row=0, padx=10, pady=10)

        label_choice = ttk.Label(manager, text="Выберите количественный атрибут: ")
        label_choice.grid(column=2, row=0, padx=10, pady=10)

        second_choice_rad = ttk.Combobox(manager, textvariable=self.quan_attr, state="readonly", values=self.quantity_attributes)
        second_choice_rad.grid(column=3, row=0, padx=10, pady=10)

        button_apply = ttk.Button(manager, text="Применить", command=self.init_graph)
        button_apply.grid(column=4, row=0, padx=10, pady=10)

        button_save_csv = ttk.Button(manager, text="Сохранить", command=self.save)
        button_save_csv.grid(column=5, row=0, padx=10, pady=10, sticky="e")

    def save_default(self):
        file_name_default = datetime.now().strftime("%Y%m%d-%H%M%S")
        f_default = self.file_path+file_name_default+".png"
        plt.savefig(f_default)

    def save(self):
        file_name = fd.asksaveasfilename(
            filetypes=(("PNG files", "*.png"),
                    ("All files", "*.*")))
        plt.savefig(file_name)

        self.save_default()

    def get_frame(self):
        return self.frame

class HistPlot(DataBase):
    def __init__(self, parent, file_path):
        self.df = self.get_full_df()

        self.frame = ttk.Frame(parent)

        self.file_path = file_path
        
        self.df_types = self.get_df_types()

        self.qual_attr = tk.StringVar()
        self.quan_attr = tk.StringVar()

        self.define_quality_attr()
        self.define_quantity_attr()
        self.init_manager()
        mt.use('TkAgg')

    def transform_type(self):
        for i, column in enumerate(self.df.columns):
            self.df = self.df.astype({column:self.df_types[i]})

    def define_quality_attr(self):
        self.quality_attributes = []
        for i in range(len(self.df.columns)):
            if self.df_types[i] == "O":
               self.quality_attributes.append(self.df.columns[i])

    def define_quantity_attr(self):
        self.quantity_attributes = []
        for i in range(len(self.df.columns)):
            if self.df_types[i] == "int64" or self.df_types[i] == "float64":
               self.quantity_attributes.append(self.df.columns[i]) 

    def init_graph(self):
        self.df = self.get_full_df()
        self.transform_type()
        #try:
        plt.style.use('ggplot')
        plt.rcParams['font.size'] = '7'

        fig = plt.figure(figsize=(10, 4.4), dpi=100)

        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        plot_widget = canvas.get_tk_widget()
        plot_widget.grid(column=0, row=1, padx=20, sticky="e")

        names = list(self.df[self.qual_attr.get()].unique())
        values = []
        for x in names:
            values_x = list(self.df[self.df[self.qual_attr.get()] == x][self.quan_attr.get()])
            values.append(values_x)
        plt.hist(values, bins=int(180/15), label=names, density=True)
        plt.legend()
        plt.tight_layout()
        # except:
        #     mb.showerror(
        #         "Ошибка", 
        #         "Ты ввел неверные данные!")
        
    def init_manager(self):
        manager = ttk.Frame(self.frame)
        manager.grid(column=0, row=0)

        label_choice = ttk.Label(manager, text="Выберите качественный атрибут: ")
        label_choice.grid(column=0, row=0, padx=10, pady=10)

        first_choice_rad = ttk.Combobox(manager, textvariable=self.qual_attr, state="readonly", values=self.quality_attributes)
        first_choice_rad.grid(column=1, row=0, padx=10, pady=10)

        label_choice = ttk.Label(manager, text="Выберите количественный атрибут: ")
        label_choice.grid(column=2, row=0, padx=10, pady=10)

        second_choice_rad = ttk.Combobox(manager, textvariable=self.quan_attr, state="readonly", values=self.quantity_attributes)
        second_choice_rad.grid(column=3, row=0, padx=10, pady=10)

        button_apply = ttk.Button(manager, text="Применить", command=self.init_graph)
        button_apply.grid(column=4, row=0, padx=10, pady=10)

        button_save_csv = ttk.Button(manager, text="Сохранить", command=self.save)
        button_save_csv.grid(column=5, row=0, padx=10, pady=10, sticky="e")

    def save_default(self):
        file_name_default = datetime.now().strftime("%Y%m%d-%H%M%S")
        f_default = self.file_path+file_name_default+".png"
        plt.savefig(f_default)

    def save(self):
        file_name = fd.asksaveasfilename(
            filetypes=(("PNG files", "*.png"),
                    ("All files", "*.*")))
        f = open(file_name, 'w')
        plt.savefig(file_name)

        self.save_default()

    def get_frame(self):
        return self.frame

class BoxVisk(DataBase):
    def __init__(self, parent, file_path):
        self.df = self.get_full_df()

        self.frame = ttk.Frame(parent)

        self.file_path = file_path
        
        self.df_types = self.get_df_types()

        self.qual_attr = tk.StringVar()
        self.quan_attr = tk.StringVar()

        self.define_quality_attr()
        self.define_quantity_attr()
        self.init_manager()
        mt.use('TkAgg')

    def transform_type(self):
        for i, column in enumerate(self.df.columns):
            self.df = self.df.astype({column:self.df_types[i]})

    def define_quality_attr(self):
        self.quality_attributes = []
        for i in range(len(self.df.columns)):
            if self.df_types[i] == "O":
               self.quality_attributes.append(self.df.columns[i])

    def define_quantity_attr(self):
        self.quantity_attributes = []
        for i in range(len(self.df.columns)):
            if self.df_types[i] == "int64" or self.df_types[i] == "float64":
               self.quantity_attributes.append(self.df.columns[i]) 

    def init_graph(self):
        self.df = self.get_full_df()
        self.transform_type()
        try:
            plt.style.use('ggplot')
            plt.rcParams['font.size'] = '7'

            fig = plt.figure(figsize=(10, 4.4), dpi=100)

            canvas = FigureCanvasTkAgg(fig, master=self.frame)
            plot_widget = canvas.get_tk_widget()
            plot_widget.grid(column=0, row=1, padx=20, sticky="e")

            names = list(self.df[self.qual_attr.get()].unique())
            values = []
            for x in names:
                values_x = list(self.df[self.df[self.qual_attr.get()] == x][self.quan_attr.get()])
                values.append(values_x)
            plt.boxplot(values, vert=True, labels=names)
            plt.tight_layout()
        except:
            mb.showerror(
                "Ошибка", 
                "Ты ввел неверные данные!")
        
    def init_manager(self):
        manager = ttk.Frame(self.frame)
        manager.grid(column=0, row=0)

        label_choice = ttk.Label(manager, text="Выберите качественный атрибут: ")
        label_choice.grid(column=0, row=0, padx=10, pady=10)

        first_choice_rad = ttk.Combobox(manager, textvariable=self.qual_attr, state="readonly", values=self.quality_attributes)
        first_choice_rad.grid(column=1, row=0, padx=10, pady=10)

        label_choice = ttk.Label(manager, text="Выберите количественный атрибут: ")
        label_choice.grid(column=2, row=0, padx=10, pady=10)

        second_choice_rad = ttk.Combobox(manager, textvariable=self.quan_attr, state="readonly", values=self.quantity_attributes)
        second_choice_rad.grid(column=3, row=0, padx=10, pady=10)

        button_apply = ttk.Button(manager, text="Применить", command=self.init_graph)
        button_apply.grid(column=4, row=0, padx=10, pady=10)

        button_save_csv = ttk.Button(manager, text="Сохранить", command=self.save)
        button_save_csv.grid(column=5, row=0, padx=10, pady=10, sticky="e")

    def save_default(self):
        file_name_default = datetime.now().strftime("%Y%m%d-%H%M%S")
        f_default = self.file_path+file_name_default+".png"
        plt.savefig(f_default)

    def save(self):
        file_name = fd.asksaveasfilename(
            filetypes=(("PNG files", "*.png"),
                    ("All files", "*.*")))
        f = open(file_name, 'w')
        plt.savefig(file_name)

        self.save_default()

    def get_frame(self):
        return self.frame

class Scatter(DataBase):
    def __init__(self, parent, file_path):
        self.df = self.get_full_df()

        self.frame = ttk.Frame(parent)

        self.file_path = file_path
        
        self.df_types = self.get_df_types()

        self.qual_attr = tk.StringVar()
        self.quan_first_attr = tk.StringVar()
        self.quan_second_attr = tk.StringVar()

        self.define_quality_attr()
        self.define_quantity_attr()
        self.init_manager()
        mt.use('TkAgg')

    def transform_type(self):
        for i, column in enumerate(self.df.columns):
            self.df = self.df.astype({column:self.df_types[i]})

    def define_quality_attr(self):
        self.quality_attributes = []
        for i in range(len(self.df.columns)):
            if self.df_types[i] == "O":
               self.quality_attributes.append(self.df.columns[i])

    def define_quantity_attr(self):
        self.quantity_attributes = []
        for i in range(len(self.df.columns)):
            if self.df_types[i] == "int64" or self.df_types[i] == "float64":
               self.quantity_attributes.append(self.df.columns[i]) 

    def init_graph(self):
        self.df = self.get_full_df()
        self.transform_type()
        try:
            plt.style.use('ggplot')
            plt.rcParams['font.size'] = '7'

            fig = plt.figure(figsize=(10, 4.4), dpi=100)

            canvas = FigureCanvasTkAgg(fig, master=self.frame)
            plot_widget = canvas.get_tk_widget()
            plot_widget.grid(column=0, row=1, padx=20, sticky="e")

            names = list(self.df[self.qual_attr.get()].unique())
            for x in names:
                values_x = list(self.df[self.df[self.qual_attr.get()] == x][self.quan_first_attr.get()])
                values_y = list(self.df[self.df[self.qual_attr.get()] == x][self.quan_second_attr.get()])
                plt.scatter(x=values_x, y=values_y, label=x)

            plt.xlabel(self.quan_first_attr.get())
            plt.ylabel(self.quan_second_attr.get())
            plt.legend()
            plt.tight_layout()
        except:
            mb.showerror(
                "Ошибка", 
                "Ты ввел неверные данные!")
        
    def init_manager(self):
        manager = ttk.Frame(self.frame)
        manager.grid(column=0, row=0)

        label_choice = ttk.Label(manager, text="Выберите качественный атрибут: ")
        label_choice.grid(column=0, row=0, padx=10, pady=10)

        first_choice_rad = ttk.Combobox(manager, textvariable=self.qual_attr, state="readonly", values=self.quality_attributes)
        first_choice_rad.grid(column=1, row=0, padx=10, pady=10)

        label_choice = ttk.Label(manager, text="Выберите количественные атрибуты: ")
        label_choice.grid(column=2, row=0, padx=10, pady=10)

        second_choice_rad = ttk.Combobox(manager, textvariable=self.quan_first_attr, state="readonly", values=self.quantity_attributes)
        second_choice_rad.grid(column=3, row=0, padx=10, pady=10)

        third_choice_rad = ttk.Combobox(manager, textvariable=self.quan_second_attr, state="readonly", values=self.quantity_attributes)
        third_choice_rad.grid(column=4, row=0, padx=10, pady=10)

        button_apply = ttk.Button(manager, text="Применить", command=self.init_graph)
        button_apply.grid(column=5, row=0, padx=10, pady=10)

        button_save_csv = ttk.Button(manager, text="Сохранить", command=self.save)
        button_save_csv.grid(column=6, row=0, padx=10, pady=10, sticky="e")

    def save_default(self):
        file_name_default = datetime.now().strftime("%Y%m%d-%H%M%S")
        f_default = self.file_path+file_name_default+".png"
        plt.savefig(f_default)

    def save(self):
        file_name = fd.asksaveasfilename(
            filetypes=(("PNG files", "*.png"),
                    ("All files", "*.*")))
        f = open(file_name, 'w')
        plt.savefig(file_name)

        self.save_default()

    def get_frame(self):
        return self.frame
