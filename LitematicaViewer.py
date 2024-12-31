import tkinter as tk
from tkinter.constants import RAISED

import numpy as np
from tkinter import filedialog, ttk
from litemapy import Schematic, Region, BlockState
from PIL import Image, ImageTk
import importlib, webbrowser, json
your_module = importlib.import_module('litemapy')
YourClass = getattr(your_module, 'Region')


file_path = ""
Block = {}
images = {}
color_map = [
    '#3399ff',  # 主色 浅蓝
    '#0066cc',  # 副色 深蓝
    '#f8f9fa',  # 背景
    '#343a40',  # 文字
]

with open('zh_cn.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)

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

def cn_translate(id):
    for key, value in list(json_data.items()):  # 只打印前五个条目作为示例
        if key == id:
            return value
    return id

def start_analysis(simple_type=False):
    count_table.delete(*count_table.get_children())
    Block.clear()
    if not file_path:
        print("Please import a file first.")
        return

    try:
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
                            if block_id == "minecraft:piston_head" or block_id == "minecraft:bubble_column" or block_id == "minecraft:nether_portal" or block_id == "minecraft:moving_piston" or block_id == "minecraft:bedrock":
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
            if entry_times.get() == "":
                time = 1
            else:
                time = int(entry_times.get())
            label_bottom.config(text=f"Size体积: {size_x}x{size_y}x{size_z} | Number数量: {num} | Density密度: {num / (size_x * size_y * size_z) * 100:.2f}% | Times倍数: {time}")
    except Exception as e:
        print(f"Error during analysis: {e}")
        return
    sorted_block = sorted(Block.items(), key=lambda x: x[1], reverse=True)
    show_block_count(sorted_block, simple_type)

def show_block_count(sorted_block, simple_type):
    global images                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
    for index, (block_state, count) in enumerate(sorted_block):
        try:
            count = count * int(entry_times.get())
        except:
            count = count * 1
        block_name = str(block_state).split(":")[-1].split("[")[0]
        
        if str(block_state).split("/")[0]!="E":
            if simple_type:
                block_id = cn_translate(block_name)
                properties = block_name
            else:
                block_id = block_state._BlockState__block_id
                properties = str(block_state._BlockState__properties).replace("'", "")
            
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
                block_id = cn_translate(block_name)
                properties = block_name+"\tEntity实体"
            else:
                block_id = block_state
                properties = "Entity实体"
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
litem.title("Litematica Viewer投影查看器")
litem.geometry("1280x720")
litem.iconbitmap("icon.ico")
litem.configure(bg=color_map[2])
litem.attributes("-alpha", 0.9)
# MENU
menu = tk.Menu(litem)

menu_analysis = tk.Menu(menu, tearoff=0)
menu_analysis.add_command(label="IMPORT导入", command=import_file, font=("Arial", 10))
menu_analysis.add_command(label="SIMPLE简洁分析", command=start_analysis, font=("Arial", 10))
menu_analysis.add_command(label="FULL全面分析", command=lambda:start_analysis(True), font=("Arial", 10))
menu.add_cascade(label="Analysis分析", menu=menu_analysis, font=("Arial", 20))


litem.config(menu=menu, padx=10, pady=10)
# 上容器
frame_top = tk.Frame(litem)
frame_top.configure(bg=color_map[1], bd=5)
frame_top.pack(side=tk.TOP, fill=tk.X)

btn_import = tk.Button(frame_top, text="Import导入", command=import_file, font=("Arial", 10))
btn_import.configure(bg=color_map[0],fg=color_map[3],relief='ridge')
btn_import.pack(side=tk.LEFT, padx=5, pady=5)
btn_simstart = tk.Button(frame_top, text="SIMPLE Analysis简洁分析", command=lambda:start_analysis(True), font=("Arial", 10))
btn_simstart.configure(bg=color_map[0],fg=color_map[3],relief='ridge')
btn_simstart.pack(side=tk.LEFT, padx=5, pady=5)
btn_start = tk.Button(frame_top, text="FULL Analysis全面分析", command=start_analysis, font=("Arial", 10))
btn_start.configure(bg=color_map[0],fg=color_map[3],relief='ridge')
btn_start.pack(side=tk.LEFT, padx=5, pady=5)

btn_github = tk.Button(frame_top, text="GitHub", command=lambda:webbrowser.open("https://github.com/albertchen857/LitematicaViewer"), font=("Arial", 10))
btn_github.configure(bg="black",fg=color_map[2],relief='groove')
btn_github.pack(side=tk.RIGHT, padx=5, pady=5)
btn_bilibili = tk.Button(frame_top, text="Bilibili", command=lambda:webbrowser.open("https://space.bilibili.com/3494373232741268"), font=("Arial", 10))
btn_bilibili.configure(bg="#FF6699", fg=color_map[2],relief='groove')
btn_bilibili.pack(side=tk.RIGHT, padx=5, pady=5)
# STYLE
table_sty = ttk.Style()
table_sty.configure("Treeview", font=("Arial", 12), rowheight=25, background=color_map[1], foreground=color_map[2])
table_sty.configure("Treeview.Heading", font=("Helvetica", 14, "bold"), background=color_map[1], foreground=color_map[3])
table_sty.map('Treeview', background=[('selected', color_map[0])])
# 中容器
frame_middle = tk.Frame(litem, bg=color_map[0])
frame_middle.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
# - 中容器顶部
frame_middle_top = tk.Frame(frame_middle, bg=color_map[0])
frame_middle_top.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

label_middle = tk.Label(frame_middle_top, text="114514.litematica", font=("Helvetica", 30, 'bold'))
label_middle.configure(bg=color_map[0], fg=color_map[3], bd=5)
label_middle.pack(fill=tk.Y)

label_bottom = tk.Label(frame_middle_top, text="Size体积 | Number数量 | Density密度 | Times倍数", font=("Helvetica", 16, "bold"))
label_bottom.configure(bg=color_map[0], fg=color_map[2], bd=5)
label_bottom.pack(side=tk.LEFT, fill=tk.X, padx=40)

frame_right = tk.Frame(frame_middle_top, bg=color_map[0])
frame_right.pack(side=tk.RIGHT, fill=tk.Y, padx=40)

label_times = tk.Label(frame_right, text="Times倍数", font=("microsoft yahei ui", 16, "bold"))
label_times.configure(bg=color_map[0], fg=color_map[3])
label_times.pack(side=tk.LEFT, padx=5)

entry_times = tk.Entry(frame_right, width=10, bg=color_map[2], fg=color_map[1], font=("Helvetica", 10))
entry_times.pack(side=tk.RIGHT, padx=5)
# - 中容器DEC
#frame_middle_dec = tk.Frame(frame_middle)
#frame_middle_dec.pack()
underscore1 = tk.Frame(frame_middle, bg=color_map[2])
underscore1.pack( padx=40, pady=10)

# - 中容器表格
frame_chart = tk.Frame(frame_middle, bg=color_map[3])
frame_chart.configure(background=color_map[0])
frame_chart.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)

sroll = tk.Scrollbar(frame_chart, orient="vertical")
sroll.pack(side=tk.RIGHT, fill=tk.Y, padx=10)
count_table = ttk.Treeview(frame_chart, column=('blockID', 'num', 'unit', 'properties'), height=7, yscrollcommand=sroll.set)
count_table.heading('blockID', text='名字/ID', anchor="center")
count_table.heading('num', text='数量', anchor="center")
count_table.heading('unit', text='数量/单位', anchor="center")
count_table.heading('properties', text='属性', anchor="center")
count_table.column("#0", width=2, anchor="e")
count_table.column("blockID", width=2)
count_table.column("num", width=2)
count_table.column("unit", width=2)
count_table.column("properties", width=300)
count_table.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=10)



litem.mainloop()
