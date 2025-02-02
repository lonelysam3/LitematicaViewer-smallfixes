import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# 创建Tkinter窗口
root = tk.Tk()
root.title("Tkinter with Matplotlib Pie Chart")
root.geometry("600x400")

# 创建matplotlib的Figure对象
fig, ax = plt.subplots()
sizes = [15, 30, 45, 10]  # 饼图每一块的大小
labels = ['A', 'B', 'C', 'D']  # 饼图每一块的标签
colors = ['#d5695d', '#5d8ca8', '#65a479', '#a564c9']  # 颜色
explode = (0, 0.1, 0, 0)  # 突出显示第二个扇区

# 绘制饼图
ax.pie(sizes,  labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # 使饼图为圆形

# 将matplotlib图表嵌入到Tkinter窗口中
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# 运行Tkinter主循环
root.mainloop()