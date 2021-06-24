import tkinter as tk
import tkinter.ttk as ttk
import tkinter as tk
from widgets import *

def build_app(root, graph_path, text_path):

    n = ttk.Notebook(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())

    manager = TableManage(root).get_frame()
    select_data = SampleData(root).get_frame()
    static_data = StaticData(root, text_path)
    pivot_table = PivotTable(root, text_path).get_frame()
    graph_bar = BarPlot(root, graph_path).get_frame()
    graph_hist = HistPlot(root, graph_path).get_frame()
    graph_box = BoxVisk(root, graph_path).get_frame()
    graph_scatter = Scatter(root, graph_path).get_frame()

    widgets = {manager : "Данные", 
                select_data : "Выборка данных", 
                static_data : "Статистический отчет", 
                pivot_table : "Сводная таблица", 
                graph_bar : "Столбчатая диаграмма", 
                graph_hist : "Гистограмма", 
                graph_box : "Диаграмма Бокса-Уискера", 
                graph_scatter : "Диаграмма рассеяния"}
                
    for widget in widgets:
        n.add(widget, text=widgets[widget])

    n.pack()

def main():
    root = tk.Tk()
    root.geometry('1200x600+200+150')
    root.title("Менеджер")
    build_app(root, "graphics/", "output/")
    root.mainloop()

if __name__ == "__main__":
    main()