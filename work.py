import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scipy.interpolate import make_interp_spline
from PIL import Image
import io

# 更新输入框值的函数，支持整型和浮点型
def update_entry_value(entry, delta, is_integer=False):
    try:
        value = float(entry.get()) + delta
        if is_integer:
            value = int(round(value))  # 确保为整数
        entry.delete(0, tk.END)
        entry.insert(0, str(value))
    except ValueError:
        pass

def generate_and_display_shape():
    try:
        min_vertices = int(min_entry.get())
        max_vertices = int(max_entry.get())
        line_width = float(line_width_entry.get())
        scatter = float(scatter_entry.get())

        if min_vertices < 3 or max_vertices < 3 or min_vertices > max_vertices:
            messagebox.showerror("无效输入", "最小和最大顶点数必须至少为3，并且最小值不应超过最大值。")
            return

        ax.clear()

        num_vertices = np.random.randint(min_vertices, max_vertices + 1)
        angles = np.sort(np.random.rand(num_vertices) * 2 * np.pi)
        angles += np.random.normal(0, scatter, num_vertices)
        angles = np.sort(angles % (2 * np.pi))

        x = np.cos(angles)
        y = np.sin(angles)

        x = np.append(x, x[0])
        y = np.append(y, y[0])

        t = np.linspace(0, 1, num_vertices + 1)
        t_smooth = np.linspace(0, 1, 300)

        spl_x = make_interp_spline(t, x, k=3)
        spl_y = make_interp_spline(t, y, k=3)

        x_smooth = spl_x(t_smooth)
        y_smooth = spl_y(t_smooth)

        global current_line
        if current_line:
            current_line.remove()
        current_line, = ax.plot(x_smooth, y_smooth, linestyle='-', color='gray', linewidth=line_width)
        ax.axis('equal')
        ax.axis('off')
        canvas.draw()
    except ValueError:
        messagebox.showerror("无效输入", "请输入有效的整数作为最小和最大顶点数，以及浮点数作为线的粗细和散布。")

def adjust_line_width():
    try:
        line_width = float(line_width_entry.get())
        if current_line:
            current_line.set_linewidth(line_width)
            canvas.draw()
    except ValueError:
        messagebox.showerror("无效输入", "请输入有效的浮点数作为线的粗细。")

def save_shape():
    buf = io.BytesIO()
    plt.savefig(buf, format='png', transparent=True)
    buf.seek(0)
    image = Image.open(buf).convert("RGBA")
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG 文件", "*.png"), ("所有文件", "*.*")])
    if file_path:
        image.save(file_path)
        messagebox.showinfo("保存成功", f"图像已保存到 {file_path}")

# 创建主窗口
root = tk.Tk()
root.title("随机封闭形状生成器-醉流ab")
root.geometry("800x700")

# 创建Matplotlib图形
fig, ax = plt.subplots(figsize=(5, 5), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# 创建输入框和按钮的框架
input_frame = tk.Frame(root)
input_frame.pack(side=tk.TOP, padx=30, pady=30)

# 线的粗细控制
line_width_label = tk.Label(input_frame, text="线的粗细:")
line_width_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
line_width_entry = tk.Entry(input_frame, width=8)
line_width_entry.insert(0, "1.0")
line_width_entry.grid(row=0, column=1, padx=10, pady=10)

# 线的粗细 +/- 按钮（只调整线宽）
tk.Button(input_frame, text="-", width=3,
          command=lambda: [update_entry_value(line_width_entry, -0.1), adjust_line_width()]
          ).grid(row=0, column=0, sticky="w")
tk.Button(input_frame, text="+", width=3,
          command=lambda: [update_entry_value(line_width_entry, 0.1), adjust_line_width()]
          ).grid(row=0, column=1, sticky="e")

# 散布控制
scatter_label = tk.Label(input_frame, text="散布:")
scatter_label.grid(row=0, column=2, padx=10, pady=10, sticky="e")
scatter_entry = tk.Entry(input_frame, width=8)
scatter_entry.insert(0, "0.1")
scatter_entry.grid(row=0, column=3, padx=10, pady=10)

# 散布 +/- 按钮（刷新图形）
tk.Button(input_frame, text="-", width=3,
          command=lambda: [update_entry_value(scatter_entry, -0.01), generate_and_display_shape()]
          ).grid(row=0, column=2, sticky="w")
tk.Button(input_frame, text="+", width=3,
          command=lambda: [update_entry_value(scatter_entry, 0.01), generate_and_display_shape()]
          ).grid(row=0, column=3, sticky="e")

# 调整按钮
adjust_button = tk.Button(input_frame, text="调整", command=adjust_line_width, width=10, height=2)
adjust_button.grid(row=0, column=4, padx=10, pady=10)

# 最小顶点数控制
min_label = tk.Label(input_frame, text="      最小顶点数 (>3):")
min_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
min_entry = tk.Entry(input_frame, width=8)
min_entry.insert(0, "10")
min_entry.grid(row=1, column=1, padx=10, pady=10)

# 最小顶点数 +/- 按钮（刷新图形）
tk.Button(input_frame, text="-", width=3,
          command=lambda: [update_entry_value(min_entry, -1, is_integer=True), generate_and_display_shape()]
          ).grid(row=1, column=0, sticky="w")
tk.Button(input_frame, text="+", width=3,
          command=lambda: [update_entry_value(min_entry, 1, is_integer=True), generate_and_display_shape()]
          ).grid(row=1, column=1, sticky="e")

# 最大顶点数控制
max_label = tk.Label(input_frame, text="      最大顶点数:")
max_label.grid(row=1, column=2, padx=10, pady=10, sticky="e")
max_entry = tk.Entry(input_frame, width=8)
max_entry.insert(0, "15")
max_entry.grid(row=1, column=3, padx=10, pady=10)

# 最大顶点数 +/- 按钮（刷新图形）
tk.Button(input_frame, text="-", width=3,
          command=lambda: [update_entry_value(max_entry, -1, is_integer=True), generate_and_display_shape()]
          ).grid(row=1, column=2, sticky="w")
tk.Button(input_frame, text="+", width=3,
          command=lambda: [update_entry_value(max_entry, 1, is_integer=True), generate_and_display_shape()]
          ).grid(row=1, column=3, sticky="e")

# 刷新按钮
refresh_button = tk.Button(input_frame, text="刷新", command=generate_and_display_shape, width=10, height=2)
refresh_button.grid(row=1, column=4, padx=10, pady=10)

# 保存按钮
save_button = tk.Button(input_frame, text="保存", command=save_shape, width=10, height=2)
save_button.grid(row=1, column=5, padx=10, pady=10)

# 初始化图形
current_line = None
generate_and_display_shape()

# 运行主循环
root.mainloop()
