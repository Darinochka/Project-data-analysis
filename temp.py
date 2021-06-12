import tkinter as tk
import tkinter.ttk as ttk

def appear():
    global i
    label = ttk.Label(root, text=sorry[i])
    label.pack()
    i += 1

root = tk.Tk()
root.geometry("500x500")
root.title("Привет...")

sorry = list("не обижайся, Алишервандус!")
i = 0
butt = ttk.Button(root, text="Нажми!", command=appear)
butt.pack()

root.mainloop()