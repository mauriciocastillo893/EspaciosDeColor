import tkinter as tk
from tkinter import ttk
import cv2
import numpy as np
from PIL import Image, ImageTk

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.canvas_width = 800
        self.canvas_height = 600
        self.image = np.ones((self.canvas_height, self.canvas_width, 3), dtype=np.uint8) * 255
        self.drawn_image = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)))
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.create_image(0, 0, image=self.drawn_image, anchor="nw")
        self.colors = ["Black", "Red", "Green", "Blue", "Yellow", "Orange", "Purple"]
        self.setup_tools()
        self.setup_events()
        self.prev_x = None
        self.prev_y = None
        self.drawing = False
        self.img_temp = None

    def setup_tools(self):
        self.selected_tool = "pen"
        self.color_map = {
            "Black": (0, 0, 0),
            "Red": (0, 0, 255),
            "Green": (0, 255, 0),
            "Blue": (255, 0, 0),
            "Yellow": (0, 255, 255),
            "Orange": (0, 165, 255),
            "Purple": (255, 0, 255)
        }
        self.selected_color = self.colors[0]
        self.brush_size = 4

        self.tool_frame = ttk.LabelFrame(self.root, text="Tools")
        self.tool_frame.pack(side=tk.RIGHT, padx=5, pady=5, fill=tk.Y)

        self.pen_button = ttk.Button(self.tool_frame, text="Lapiz", command=self.select_pen_tool)
        self.pen_button.pack(side=tk.TOP, padx=5, pady=5)
        
        self.line_button = ttk.Button(self.tool_frame, text="Linea", command=self.select_line_tool)
        self.line_button.pack(side=tk.TOP, padx=5, pady=5)
        
        self.rectangle_button = ttk.Button(self.tool_frame, text="Rectangulo", command=self.select_rectangle_tool)
        self.rectangle_button.pack(side=tk.TOP, padx=5, pady=5)
        
        self.circle_button = ttk.Button(self.tool_frame, text="Circulo", command=self.select_circle_tool)
        self.circle_button.pack(side=tk.TOP, padx=5, pady=5)

        self.eraser_button = ttk.Button(self.tool_frame, text="Borrador", command=self.select_eraser_tool)
        self.eraser_button.pack(side=tk.TOP, padx=5, pady=5)

        self.color_label = ttk.Label(self.tool_frame, text="Color:")
        self.color_label.pack(side=tk.TOP, padx=5, pady=5)

        self.color_combobox = ttk.Combobox(self.tool_frame, values=self.colors, state="readonly")
        self.color_combobox.current(0)
        self.color_combobox.pack(side=tk.TOP, padx=5, pady=5)
        self.color_combobox.bind("<<ComboboxSelected>>", lambda event: self.select_color(self.color_combobox.get()))

        self.clear_button = ttk.Button(self.tool_frame, text="Limpiar", command=self.clear_canvas)
        self.clear_button.pack(side=tk.TOP, padx=5, pady=5)
    
    def release(self, event):
        self.prev_x = None
        self.prev_y = None
        
    def setup_events(self):
        self.canvas.bind("<Button-1>", self.start_draw) 
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.finalize_draw)

    def select_pen_tool(self):
        self.selected_tool = "pen"

    def select_eraser_tool(self):
        self.selected_tool = "eraser"
    
    def select_line_tool(self):
        self.selected_tool = "line"
    
    def select_rectangle_tool(self):
        self.selected_tool = "rectangle"
    
    def select_circle_tool(self):
        self.selected_tool = "circle"

    def select_color(self, color):
        self.selected_color = color


    def start_draw(self, event):
        self.prev_x = event.x
        self.prev_y = event.y
        self.temp_image = self.image.copy()

    def draw(self, event):
        color = self.color_map[self.selected_color]
        if self.selected_tool == "pen":
            cv2.line(self.image, (self.prev_x, self.prev_y), (event.x, event.y), color, self.brush_size)
            self.prev_x = event.x
            self.prev_y = event.y
            self.redraw()
        elif self.selected_tool == "eraser":
            color = (255, 255, 255)
            cv2.line(self.image, (self.prev_x, self.prev_y), (event.x, event.y), color, self.brush_size)
            self.prev_x = event.x
            self.prev_y = event.y
            self.redraw()
        elif self.selected_tool in ["line", "rectangle", "circle"]:
            self.temp_image = self.image.copy()
            if self.selected_tool == "line":
                cv2.line(self.temp_image, (self.prev_x, self.prev_y), (event.x, event.y), color, self.brush_size)
            elif self.selected_tool == "rectangle":
                cv2.rectangle(self.temp_image, (self.prev_x, self.prev_y), (event.x, event.y), color, self.brush_size)
            elif self.selected_tool == "circle":
                center = ((self.prev_x + event.x) // 2, (self.prev_y + event.y) // 2)
                radius = int(np.sqrt((event.x - self.prev_x) ** 2 + (event.y - self.prev_y) ** 2) / 2)
                cv2.circle(self.temp_image, center, radius, color, self.brush_size)
            self.redraw(temp_image=True)

    def finalize_draw(self, event):
        if self.selected_tool in ["line", "rectangle", "circle"]:
            self.image = self.temp_image.copy()
        self.prev_x = None
        self.prev_y = None
        self.redraw()

    def redraw(self, temp_image=False):
        if temp_image:
            image = self.temp_image
        else:
            image = self.image
        self.drawn_image = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)))
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.drawn_image, anchor="nw")
    
    def clear_canvas(self):
        self.image = np.ones((self.canvas_height, self.canvas_width, 3), dtype=np.uint8) * 255
        self.redraw()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Tkinter_OpenCV GUI")
    app = PaintApp(root)
    root.mainloop()