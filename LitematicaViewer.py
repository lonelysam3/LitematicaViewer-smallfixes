import tkinter as tk
import numpy as np
from tkinter import filedialog, ttk
from litemapy import Schematic, Region, BlockState
from PIL import Image, ImageTk

file_path = ""
Block = {}
images = {}  # Dictionary to hold image references

def convert_units(number):
    units = {'箱': 54 * 27 * 64, '盒': 27 * 64, '组': 64, '个': 1}
    result = ""
    for unit, value in units.items():
        result += str(number // value) + unit
        number %= value
    return result

def import_file():
    global file_path
    file_path = filedialog.askopenfilename()
    file_path = file_path.replace("\\", "/")
    print(f"Imported file: {file_path}")
    file_name = file_path.split("/")[-1]
    label_bottom.config(text=f"{file_name}")

def start_analysis(simple_type=False):
    count_table.delete(*count_table.get_children())
    Block.clear()
    if not file_path:
        print("Please import a file first.")
        return

    print(f"Analyzing file: {file_path}")
    try:
        schematic = Schematic.load(file_path)
        print(f"Schematic loaded: {schematic}")
        for region_index, region in enumerate(schematic.regions.values()):
            print(f"Analyzing region {region_index + 1}")
            size_x = region.maxx() - region.minx()
            size_y = region.maxy() - region.miny()
            size_z = region.maxz() - region.minz()
            label_bottom2.config(text=f"{size_x}x{size_y}x{size_z}")
            # Analyze blocks
            for x in range(size_x + 1):
                for y in range(size_y + 1):
                    for z in range(size_z + 1):
                        block_id = region._Region__blocks[x, y, z]
                        block_state = region._Region__palette[block_id]
                        if simple_type:
                            block_state = str(block_state).split(":")[-1].split("[")[0]
                        if block_id == 0:
                            continue
                        if block_state not in Block:
                            Block[block_state] = 1
                        else:
                            Block[block_state] += 1
    except Exception as e:
        print(f"Error during analysis: {e}")
        return
    sorted_block = sorted(Block.items(), key=lambda x: x[1], reverse=True)
    show_block_count(sorted_block, simple_type)

def show_block_count(sorted_block, simple_type):
    global images
    for index, (block_state, count) in enumerate(sorted_block):
        block_name = str(block_state).split(":")[-1].split("[")[0]
        if simple_type:
            properties = ""
            block_id = block_name
        else:
            properties = str(block_state._BlockState__properties)
            properties = properties.replace("{", "").replace("}", "").replace("'", "")
            block_id = block_state._BlockState__block_id
        #print(block_name)
        try:
            img_path = f"block/{str(block_name)}.png"
            img2 = Image.open(img_path)
            img2 = img2.resize((20, 20), Image.LANCZOS)
            img2 = ImageTk.PhotoImage(img2)
            images[index] = img2
            count_table.insert('', 'end', image=img2, values=(str(block_id), str(count), convert_units(count), properties))
        except:
            count_table.insert('', 'end', text="Unknown Block", values=(str(block_id), str(count), convert_units(count), properties))
        count_table.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Tkinter Setting
litem = tk.Tk()
litem.title("Litematica Viewer")
litem.geometry("720x720")
litem.iconbitmap("block/crafting_table2.png")

# 上容器
frame_top = tk.Frame(litem)
frame_top.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

btn_import = tk.Button(frame_top, text="Import", command=import_file)
btn_import.pack(side=tk.LEFT, padx=5, pady=5)

btn_start = tk.Button(frame_top, text="Start Analysis(id & properties)", command=start_analysis)
btn_start.pack(side=tk.LEFT, padx=5, pady=5)

btn_simstart = tk.Button(frame_top, text="Simple Analysis(block name)", command=lambda:start_analysis(True))
btn_simstart.pack(side=tk.LEFT, padx=5, pady=5)

icon = tk.PhotoImage(file="block/crafting_table2.png")
icon_image = tk.Label(frame_top, image=icon)
icon_image.pack(side=tk.RIGHT, padx=5, pady=5)

# 中容器
frame_middle = tk.Frame(litem, bg="white", height=400)
frame_middle.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
label_middle = tk.Label(frame_middle, text="Block Count List", font=("Helvetica", 24, "bold"))
label_middle.pack()

count_table = ttk.Treeview(frame_middle, column=('blockID',  '数量', '数量（组）', '属性'), height=7)
count_table.heading('blockID', text='blockID', anchor="center")
count_table.heading('数量', text='数量', anchor="center")
count_table.heading('数量（组）', text='数量（组）', anchor="center")
count_table.heading('属性', text='属性', anchor="center")
count_table.column("#0", width=10, anchor="e")
count_table.column("blockID", width=50)
count_table.column("数量" , width=2)
count_table.column("数量（组）", width=20)
count_table.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=50, pady=20)

# 下容器
frame_bottom = tk.Frame(litem)
frame_bottom.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
label_bottom = tk.Label(frame_bottom, text="114514.litematica", font=("Helvetica", 12, "italic"))
label_bottom.pack()
label_bottom2 = tk.Label(frame_bottom, text="Size", font=("Helvetica", 10))
label_bottom2.pack()

litem.mainloop()
