import tkinter as tk
import numpy as np
from tkinter import filedialog, ttk
from litemapy import Schematic, Region, BlockState

file_path = ""
Block = {}

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

def start_analysis():
    count_table.delete(*count_table.get_children())
    Block.clear()
    if not file_path:
        print("Please import a file first.")
        return

    print(f"Analyzing file: {file_path}")
    
    schem = Schematic.load(file_path)
    print(f"Schematic loaded: {schem}")
    
    if not schem.regions:
        print("No regions found in the schematic.")
        return

    for region_index, region in enumerate(schem.regions.values()):
        print(f"Analyzing region {region_index + 1}")
        size_x=region.maxx()-region.minx()
        size_y=region.maxy()-region.miny()
        size_z=region.maxz()-region.minz()
        label_bottom2.config(text=f"{size_x}x{size_y}x{size_z}")
        # Analyze blocks
        for x in range(size_x+1):
            for y in range(size_y+1):
                for z in range(size_z+1):
                    block_id = region._Region__blocks[x, y, z]
                    block_state = region._Region__palette[block_id]
                    if block_id == 0: 
                        continue
                    if block_state not in Block:
                        Block[block_state] = 1
                    else:
                        Block[block_state] += 1
    sorted_block = sorted(Block.items(), key=lambda x: x[1], reverse=True)
    show_block_count(sorted_block)

def show_block_count(list):
    for block_state, count in list:
        print(f"{block_state}: {count}")
        properties = str(block_state._BlockState__properties)
        properties = properties.replace("{", "")
        properties = properties.replace("}", "")
        properties = properties.replace("'", "")
        count_table.insert('', 'end', values=(str(block_state._BlockState__block_id), properties, str(count), convert_units(count)))
    count_table.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)



# Tkinter Setting
litem = tk.Tk()
litem.title("Litematica Viewer")
litem.geometry("1090x720")  

# 上容器
frame_top = tk.Frame(litem)
frame_top.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

btn_import = tk.Button(frame_top, text="Import", command=import_file)
btn_import.pack(side=tk.LEFT, padx=5, pady=5)

btn_start = tk.Button(frame_top, text="Start Analysis", command=start_analysis)
btn_start.pack(side=tk.RIGHT, padx=5, pady=5)

# 中容器
frame_middle = tk.Frame(litem, bg="white", height=400)
frame_middle.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
label_middle = tk.Label(frame_middle, text="Block Count List" ,font=("Helvetica", 24, "bold"))
label_middle.pack()
count_table = ttk.Treeview(frame_middle, columns=('blockID', '属性' , '数量', '数量（组）'), show='headings')
count_table.heading('blockID', text='blockID')
count_table.heading('属性', text='属性')
count_table.heading('数量', text='数量')
count_table.heading('数量（组）', text='数量（组）')
count_table.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)



# 下容器
frame_bottom = tk.Frame(litem)
frame_bottom.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

label_bottom = tk.Label(frame_bottom, text="114514.litematica", font=("Helvetica", 12, "italic"))
label_bottom.pack()
label_bottom2 = tk.Label(frame_bottom, text="Size", font=("Helvetica", 10))
label_bottom2.pack()

litem.mainloop()