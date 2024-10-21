import tkinter as tk
import numpy as np
from tkinter import filedialog, ttk
from litemapy import Schematic, Region, BlockState
from PIL import Image, ImageTk
import importlib, webbrowser
your_module = importlib.import_module('litemapy')
YourClass = getattr(your_module, 'Region')


file_path = ""
Block = {}
images = {}

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
    label_middle.config(text=f"{file_name}")

def start_analysis(simple_type=False):
    count_table.delete(*count_table.get_children())
    Block.clear()
    if not file_path:
        print("Please import a file first.")
        return

    #try:
    schematic = Schematic.load(file_path)
    print(f"Schematic loaded: {schematic}")
    for region_index, region in enumerate(schematic.regions.values()):
        print(f"Analyzing region {region_index + 1}")
        size_x = region.maxx() - region.minx() + 1
        size_y = region.maxy() - region.miny() + 1
        size_z = region.maxz() - region.minz() + 1
        num = 0
        for x in range(size_x):
            for y in range(size_y):
                for z in range(size_z):
                    block_state = region._Region__palette[region._Region__blocks[x, y, z]]
                    block_id = block_state._BlockState__block_id
                    output = block_state
                    if block_id != "minecraft:air" and block_id != "minecraft:cave_air" and block_id != "minecraft:void_air":
                        num += 1
                        if block_id == "minecraft:piston_head" or block_id == "minecraft:bubble_column" or block_id == "minecraft:nether_portal" or block_id == "minecraft:moving_piston":
                            continue
                        if simple_type:
                            output = block_id
                        if output not in Block:
                            Block[output] = 1
                        else:
                            Block[output] += 1
        
        for entity in region._Region__entities:
            entity_type = "E/"+str(entity.id)
            if entity_type == "E/minecraft:item" or entity_type == "E/minecraft:bat" or entity_type == "E/minecraft:experience_orb" or entity_type == "E/minecraft:shulker_bullet":
                continue
            if entity_type not in Block:
                Block[entity_type] = 1
            else:
                Block[entity_type] += 1
        label_bottom.config(text=f"Size体积: {size_x}x{size_y}x{size_z} | Number数量: {num} | Density密度: {num / (size_x * size_y * size_z) * 100:.2f}%")
    '''except Exception as e:
        print(f"Error during analysis: {e}")
        return'''
    sorted_block = sorted(Block.items(), key=lambda x: x[1], reverse=True)
    show_block_count(sorted_block, simple_type)


def show_block_count(sorted_block, simple_type):
    global images
    for index, (block_state, count) in enumerate(sorted_block):
        block_name = str(block_state).split(":")[-1].split("[")[0]
        
        if str(block_state).split("/")[0]!="E":
            if simple_type:
                block_id = block_name
                properties = ""
            else:
                block_id = block_state._BlockState__block_id
                properties = str(block_state._BlockState__properties)
                properties = properties.replace("'", "")
            
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
        else:
            if simple_type:
                block_id = block_name
            else:
                block_id = block_state
            
            try:
                img_path = f"block/{str(block_name)}.png"
                img2 = Image.open(img_path)
                img2 = img2.resize((20, 20), Image.LANCZOS)
                img2 = ImageTk.PhotoImage(img2)
                images[index] = img2
                count_table.insert('', 'end', image=img2, values=(str(block_id), str(count), convert_units(count), "Entity实体"))
            except:
                count_table.insert('', 'end', text="Unknown Block", values=(str(block_id), str(count), convert_units(count), "Entity实体"))
            count_table.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Tkinter Setting
litem = tk.Tk()
litem.title("Litematica Viewer投影查看器")
litem.geometry("720x720")
litem.iconbitmap("icon.ico")
litem.configure(bg="#3E3E3E")

# 上容器
frame_top = tk.Frame(litem)
frame_top.configure(bg="#3E3E3E")
frame_top.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

btn_import = tk.Button(frame_top, text="Import导入", command=import_file)
btn_import.pack(side=tk.LEFT, padx=5, pady=5)

btn_start = tk.Button(frame_top, text="Start Analysis(id & properties)分析", command=start_analysis)
btn_start.pack(side=tk.LEFT, padx=5, pady=5)

btn_simstart = tk.Button(frame_top, text="Simple Analysis(block name)简洁分析", command=lambda:start_analysis(True))
btn_simstart.pack(side=tk.LEFT, padx=5, pady=5)

btn_github = tk.Button(frame_top, text="GitHub", command=lambda:webbrowser.open("https://github.com/albertchen857/LitematicaViewer"), font=("Arial", 10))
btn_github.configure(bg="black",fg="white")
btn_github.pack(side=tk.RIGHT, padx=5, pady=5)

btn_bilibili = tk.Button(frame_top, text="Bilibili", command=lambda:webbrowser.open("https://space.bilibili.com/3494373232741268"), font=("Arial", 10))
btn_bilibili.configure(bg="#fb7299", fg="white")
btn_bilibili.pack(side=tk.RIGHT, padx=5, pady=5)

table_sty = ttk.Style()
table_sty.configure("Treeview", font=("Helvetica", 10), rowheight=25, background="#1F1F1F", foreground="white")
table_sty.configure("Treeview.Heading", font=("Minecraft", 12, "bold"))
table_sty.map('Treeview', background=[('selected', 'blue')])
# 中容器
frame_middle = tk.Frame(litem, bg="white", height=400)
frame_middle.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
frame_middle.configure(background="#2F2F2F")
label_middle = tk.Label(frame_middle, text="114514.litematica", font=("Helvetica", 18))
label_middle.configure(bg="#3E3E3E", fg="white")
label_middle.pack(padx=5, pady=20)

count_table = ttk.Treeview(frame_middle, column=('blockID',  'num', 'unit', 'properties'), height=7)
count_table.heading('blockID', text='blockID', anchor="center")
count_table.heading('num', text='数量', anchor="center")
count_table.heading('unit', text='数量/单位', anchor="center")
count_table.heading('properties', text='属性', anchor="center")
count_table.column("#0", width=10, anchor="e")
count_table.column("blockID", width=50)
count_table.column("num" , width=2)
count_table.column("unit", width=30)
count_table.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=50, pady=10)

# 下容器
frame_bottom = tk.Frame(litem)
frame_bottom.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
frame_bottom.configure(bg="#3E3E3E")
label_bottom = tk.Label(frame_bottom, text="Size体积 | Number数量 | Density密度", font=("Helvetica", 14))
label_bottom.configure(bg="#3E3E3E", fg="white")
label_bottom.pack()

litem.mainloop()
