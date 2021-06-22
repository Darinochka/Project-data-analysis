from numpy.core.fromnumeric import size
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
import math
from datetime import datetime


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

class SampleData(ttk.Frame):

    def __init__(self, parent, df_list, df_names, file_path):
        super().__init__(parent)
        self.file_path = file_path
        self.df_names = df_names
        self.df_list = df_list
        self.df_curr = self.df_list[0]
        self.df_change_curr = self.df_curr

        self.choice_data = tk.IntVar()
        self.choice_data.set(0)

        self.choice_attr = np.empty(shape=(self.df_curr.shape[1]), dtype="O")

        self.grid(column=0, row=0)

        self.init_manager()

        self.grid_columnconfigure(0, weight=1, uniform="group1")
        self.rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1, uniform="group1")

    def init_table(self, df):
        table = Table(self, df)
        table.grid(column=0, row=0, sticky="nsew")

    def change_main_base(self):
        self.df_curr = self.df_list[self.choice_data.get()]
        self.choice_attr = np.empty(shape=(self.df_curr.shape[1]), dtype="O")
        self.init_table(self.df_curr)
        self.init_manager()

    def init_manager(self):
        manager = ttk.Frame(self)
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
        f_default = open(self.file_path+file_name_default+format, 'w', encoding='utf-8')
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
        self.df_change_curr.to_excel(self.file_path+file_name_default+".xlsx", index = False)
    
    def save_as_pic(self):
        file_name = fd.asksaveasfilename(
        filetypes=(("Picle files", "*.pic"),
                   ("All files", "*.*")))
        f = open(file_name, 'w')
        self.df_change_curr.to_pickle(file_name)
        f.close()

        self.df_change_curr.to_pickle(self.save_default(".pic"), index=False)

class TableManage(ttk.Frame):
 
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

        self.init_table()
        self.init_manager()

        self.grid_columnconfigure(0, weight=1, uniform="group1")
        self.rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1, uniform="group1")
 
    def init_table(self):

        table = Table(self, self.df)
        table.grid(column=0, row=0, sticky="nsew")

        self.widgets_entry = table.widgets_entry
        self.values_df = table.values_df
                
    def init_manager(self):
        #editor table
        menu = ttk.Frame(self)
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

            self.init_table()
            update_df()
        except (ValueError,KeyError):
            mb.showerror(
                "Ошибка", 
                "Ты ввел неверные данные!")
        self.entry_to_delete.delete(0, 'end')

    def clear(self, entries):
        for i in range(len(entries)):
            entries[i].delete(0, 'end')

    def transform_type(self, df, df_types):
        for i, column in enumerate(df.columns):
            df = df.astype({column:df_types[i]})
        return df

    def save_insert(self):
        self.hight = self.df.shape[0]
        self.width = self.df.shape[1]
        
        try:
            for j in range(self.width): #check empty entries
                entry = self.widgets_entry_insert[j].get()
                
                if not entry:
                    raise ValueError  

                elif self.df_types[j] == np.dtype('int64'):
                    int(entry)

                elif self.df_types[j] == np.dtype('float64'):
                    float(entry)

                elif self.df_types[j] == np.dtype('datetime64[ns]'):
                    datetime.strptime(entry, "%Y-%m-%d")       

            for j, column in enumerate(self.df.columns): 
                self.df.loc[self.hight, column] = self.widgets_entry_insert[j].get()

            self.df = self.transform_type(self.df, self.df_types)
            self.df = self.df.reset_index(drop=True)

            if self.df.duplicated().any():
                self.df = self.df.drop(index=[self.hight])
                raise Exception

            self.init_table()
            update_df()
        except ValueError:
            mb.showerror(
                "Ошибка", 
                "Ты ввел данные не того типа!")
        except Exception:
            mb.showerror(
                "Ошибка", 
                "Такая строка уже присутствует!")

        self.clear(self.widgets_entry_insert)

    def save_changes(self):
        self.hight = self.df.shape[0]
        self.width = self.df.shape[1]

        try:
            for i in range(self.hight): 
                for j in range(self.width): 
                    entry = self.widgets_entry[i, j].get()

                    if self.df_types[j] == np.dtype('int64'):
                        int(entry)

                    elif self.df_types[j] == np.dtype('float64'):
                        float(entry)

                    elif self.df_types[j] == np.dtype('datetime64[ns]'):
                        datetime.strptime(entry, "%Y-%m-%d") 

                    self.df.iloc[i, j] = entry

            self.df = self.transform_type(self.df, self.df_types)
            self.init_table()
            update_df()
        except ValueError:
            mb.showerror(
                "Ошибка", 
                "Ты ввел данные не того типа!")

    def get_upd_df(self):
        return self.df

class QualityData(ttk.Frame):
    def __init__(self, parent, df_list, df_names, file_path):
        super().__init__(parent)
        self.df_list = df_list
        self.file_path = file_path
        self.df_names = df_names

        self.df_curr = self.df_list[0] #current dataframe
        self.df_stat_curr = pd.DataFrame() #current statistic dataframe
        self.df_types = [[col_type for col_type in df.dtypes] for df in df_list] #list of the types every dataframe
        self.df_curr_types = self.df_types[0]   #current types of the current dataframe

        self.choice_data = tk.IntVar()  #choice of dataframe
        self.choice_data.set(-1)

        self.choice_attr = tk.StringVar()   #choice of the attribute
        self.choice_attr.set("")

        self.attr = []
        self.define_quality_attr()

        self.init_manager()

        self.grid_rowconfigure(0, weight=1, uniform="group1")
        self.columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1, uniform="group1")

    def init_table(self, df):
        table = Table(self, df)
        table.grid(column=0, row=1, sticky="nsew")

    def change_main_base(self):
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
        manager = ttk.Frame(self)
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

class QuantityData(ttk.Frame):
    def __init__(self, parent, df_list, df_names, file_path):
        super().__init__(parent)
        self.df_list = df_list
        self.file_path = file_path
        self.df_names = df_names

        self.df_curr = self.df_list[0] #current dataframe
        self.df_stat_curr = pd.DataFrame()
        self.df_types = [[col_type for col_type in df.dtypes] for df in df_list] #list of the types every dataframe
        self.df_curr_types = self.df_types[0]   #current types of the current dataframe

        self.choice_data = tk.IntVar()  #choice of dataframe
        self.choice_data.set(-1)

        self.choice_attr = tk.StringVar()   #choice of the attribute
        self.choice_attr.set("")

        self.define_quantity_attr()

        self.init_manager()

        self.grid_rowconfigure(0, weight=1, uniform="group1")
        self.columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1, uniform="group1")

    def init_table(self, df):
        table = Table(self, df)
        table.grid(column=0, row=1, sticky="nsew")

    def change_main_base(self):
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
        manager = ttk.Frame(self)
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

class StaticData(ttk.Frame):
    def __init__(self, parent, df_list, df_names, file_path):
        super().__init__(parent)
        self.grid(column=0, row=0)

        quality = QualityData(self, df_list, df_names, file_path)
        quality.grid(column=0, row=0, sticky="nsew")
        quantity = QuantityData(self, df_list, df_names, file_path)
        quantity.grid(column=1, row=0, sticky="nsew")

        self.grid_columnconfigure(0, weight=1, uniform="group1")
        self.rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1, uniform="group1")

class PivotTable(ttk.Frame):
    def __init__(self, parent, df_list, df_names, file_path):
        super().__init__(parent)
        self.grid(column=0, row=0)
        
        self.df_names = df_names
        self.df_list = df_list
        self.df_curr = df_list[0]
        self.df_types = [[col_type for col_type in df.dtypes] for df in df_list] #list of the types every dataframe
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

        self.grid_columnconfigure(0, weight=1, uniform="group1")
        self.rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1, uniform="group1")

    def change_main_base(self):
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
        table = Table(self, df)
        table.grid(column=0, row=0, sticky="nsew")

    def change_table(self):
        try:
            index = [self.first_attr.get(), self.second_attr.get()]

            if self.aggfunc.get() == "Среднее":
                df_update = pd.pivot_table(self.df_curr, index=index, aggfunc=np.mean, margins=True)
            elif self.aggfunc.get() == "Сумма":
                df_update = pd.pivot_table(self.df_curr, index=index, aggfunc=np.sum, margins=True)
            elif self.aggfunc.get() == "Максимум":
                df_update = pd.pivot_table(self.df_curr, index=index, aggfunc=np.max, margins=True)
            elif self.aggfunc.get() == "Минимум":
                df_update = pd.pivot_table(self.df_curr, index=index, aggfunc=np.min, margins=True)

            self.df_update = df_update.reset_index()
            self.init_table(self.df_update)
        except:
            mb.showerror(
                "Ошибка", 
                "Ты ввел неверные данные!")

    def init_manager(self):
        manager = ttk.Frame(self)
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

class BarPlot(ttk.Frame):
    def __init__(self, parent, df, file_path):
        super().__init__(parent)

        self.file_path = file_path
        
        self.df = df
        self.df_types = [col_type for col_type in df.dtypes] 

        self.qual_attr = tk.StringVar()
        self.quan_attr = tk.StringVar()

        self.define_quality_attr()
        self.define_quantity_attr()
        self.init_manager()
        mt.use('TkAgg')

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
        try:
            plt.style.use('ggplot')
            plt.rcParams['font.size'] = '7'

            fig = plt.figure(figsize=(10, 4.4), dpi=100)

            canvas = FigureCanvasTkAgg(fig, master=self)
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
        manager = ttk.Frame(self)
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

class HistPlot(ttk.Frame):
    def __init__(self, parent, df, file_path):
        super().__init__(parent)

        self.file_path = file_path
        
        self.df = df
        self.df_types = [col_type for col_type in df.dtypes] 

        self.qual_attr = tk.StringVar()
        self.quan_attr = tk.StringVar()

        self.define_quality_attr()
        self.define_quantity_attr()
        self.init_manager()
        mt.use('TkAgg')

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
        try:
            plt.style.use('ggplot')
            plt.rcParams['font.size'] = '7'

            fig = plt.figure(figsize=(10, 4.4), dpi=100)

            canvas = FigureCanvasTkAgg(fig, master=self)
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
        except:
            mb.showerror(
                "Ошибка", 
                "Ты ввел неверные данные!")
        
    def init_manager(self):
        manager = ttk.Frame(self)
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

def update_df():
    df_list = [tracks.get_upd_df(), albums.get_upd_df(), artists.get_upd_df(), genres.get_upd_df()]
    select_data.df_list = df_list
    static_data.df_list = df_list
    pivot_table.df_list = df_list

file_path = "output/"
df_tracks = pd.read_excel("data/tracks.xlsx")
df_albums = pd.read_excel("data/albums.xlsx")
df_artists = pd.read_excel("data/artists.xlsx")
df_genres = pd.read_excel("data/genres.xlsx")
df = pd.read_excel("data/tracks1.xlsx")

df_list = [df_tracks, df_albums, df_artists, df_genres]
df_names = ["Треки", "Альбомы", "Артисты", "Жанры"]

root = tk.Tk()
root.geometry('1200x600+200+150')
root.title("Менеджер")
n = ttk.Notebook(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())

tracks = TableManage(root, df_tracks, file_path)
albums = TableManage(root, df_albums, file_path)
artists = TableManage(root, df_artists, file_path)
genres = TableManage(root, df_genres, file_path)

select_data = SampleData(root, df_list, df_names, file_path)
static_data = StaticData(root, df_list, df_names, file_path)
pivot_table = PivotTable(root, df_list, df_names, file_path)
graph_bar = BarPlot(root, df, "graphics/")
graph_hist = HistPlot(root, df, "graphics/")

n.add(tracks, text='Треки')
n.add(albums, text='Альбомы')
n.add(artists, text='Артисты')
n.add(genres, text='Жанры')
n.add(select_data, text='Выборка данных')
n.add(static_data, text='Статистический отчет')
n.add(pivot_table, text="Сводная таблица")
n.add(graph_bar, text="Столбчатая диаграмма")
n.add(graph_hist, text="Гистограмма")

n.pack()
root.mainloop()