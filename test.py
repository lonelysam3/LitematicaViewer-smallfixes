import tkinter as tk
from tkinter import filedialog, ttk
from litemapy import Schematic, Region, BlockState
from PIL import Image, ImageTk


def func():
    global img
    table.insert('', 'end', image=img, value=("A's value", "B's value"))
    table.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

root=tk.Tk()
root.title("Litematica Viewer")
root.geometry("800x600")
img_path = "block/yellow_wool.png"  # Replace with actual image path
img = Image.open(img_path)
img = img.resize((32, 32), Image.LANCZOS)
img = ImageTk.PhotoImage(img)
lable = tk.Label(root, text="Litematica Viewer", image=img)
lable.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

table = ttk.Treeview(root, column=('A','B'), selectmode='none', height=7)
#table.grid(row=0, column=0, padx=10, pady=10)
#table.heading('#0', text=' Pic directory', anchor='center')
table.heading('#1', text=' A', anchor='center')
table.heading('#2', text=' B', anchor='center')
#table.insert('', 'end', image=img, value=("A's value", "B's value"))
table.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

btn = tk.Button(root, text="Add", command=func)
btn.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)




root.mainloop()