import tkinter as tk
from tkinter import colorchooser, Scale, Button, HORIZONTAL, Label, Canvas, Tk, filedialog
import os

class DrawingApp:
    def __init__(self, master):
        self.master = master
        master.title("Drawing Application")

        self.width = 400  # Modified width
        self.height = 400 # Modified height
        self.brush_color = "black"
        self.eraser_color = "white"  #Default Eraser color
        self.brush_radius = 5
        self.opacity = 1.0
        self.sharpness = 0.5  # Not directly implemented, see comments
        self.tool = "brush"  #or "eraser"

        # --- Main Frame for Layout ---
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Canvas ---
        self.canvas = Canvas(self.main_frame, width=self.width, height=self.height, bg="white")
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)  # Left side, padding

        # --- Controls Frame ---
        self.controls_frame = tk.Frame(self.main_frame)
        self.controls_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.Y)  # Right side, padding

        # --- Sliders ---
        self.radius_slider = Scale(self.controls_frame, from_=1, to=50, orient=HORIZONTAL, label="Radius", command=self.update_radius)
        self.radius_slider.set(self.brush_radius)  # Set initial value
        self.radius_slider.pack()


        self.opacity_slider = Scale(self.controls_frame, from_=0.01, to=1.0, resolution=0.01, orient=HORIZONTAL, label="Opacity", command=self.update_opacity) #Added resolution to avoid errors.
        self.opacity_slider.set(self.opacity)  # Set initial value
        self.opacity_slider.pack()

        # Sharpness slider (not directly implemented)
        self.sharpness_slider = Scale(self.controls_frame, from_=0.0, to=1.0, resolution=0.01, orient=HORIZONTAL, label="Sharpness", command=self.update_sharpness)
        self.sharpness_slider.set(self.sharpness)
        self.sharpness_slider.pack()


        # --- Color Chooser ---
        self.color_button = Button(self.controls_frame, text="Choose Color", command=self.choose_color)
        self.color_button.pack()


        # --- Buttons ---
        self.erase_button = Button(self.controls_frame, text="Eraser", command=self.set_eraser) #Added button to use eraser.
        self.erase_button.pack()

        self.brush_button = Button(self.controls_frame, text="Brush", command=self.set_brush) #Added button to use brush.
        self.brush_button.pack()

        self.save_button = Button(self.controls_frame, text="Save", command=self.save_image)
        self.save_button.pack()



        # --- Bindings ---
        self.canvas.bind("<B1-Motion>", self.paint)  # Mouse drag
        self.canvas.bind("<ButtonRelease-1>", self.reset) #On mouse release

        master.bind("b", self.set_brush) #Hotkey for brush
        master.bind("e", self.set_eraser) #Hotkey for eraser
        master.bind("s", self.save_image) #Hotkey for save

        self.last_x = None
        self.last_y = None
        self.drawing = False #Flag if drawing or not.

    def paint(self, event):
      if self.tool == "brush":
            paint_color = self.brush_color
      elif self.tool == "eraser":
            paint_color = self.eraser_color  # Use eraser color

      if self.last_x and self.last_y:
        self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                               width=2 * self.brush_radius, fill=paint_color,
                               capstyle=tk.ROUND, smooth=True, splinesteps=36,
                               stipple="") # Removed opacity from here to fix the way opacity behaves
      self.last_x = event.x
      self.last_y = event.y
      self.drawing = True #Set the drawing flag true

    def reset(self, event): #Resets the coordinates to prevent lines being drawn across canvas.
        self.last_x = None
        self.last_y = None
        self.drawing = False

    def update_radius(self, value):
        self.brush_radius = int(value)

    def update_opacity(self, value):
        self.opacity = float(value)


    def update_sharpness(self, value):
      # In a real image processing program, you would use this value to
      # control blurring, sharpening, or other edge-enhancing filters.
      # This example provides the slider but doesn't actually implement the
      # image processing functionality.  You'd typically need libraries
      # like PIL (Pillow) and NumPy for that.
      self.sharpness = float(value)
      print(f"Sharpness set to: {self.sharpness}")  #Just prints to console.

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Choose Brush Color")
        if color_code:
            self.brush_color = color_code[1] # color_code is a tuple; [1] is the hex color string

    def set_eraser(self, event=None): # Added event so that the hotkey also works
        self.tool = "eraser"

    def set_brush(self, event=None): # Added event so that the hotkey also works
        self.tool = "brush"

    def save_image(self, event=None): # Added event so that the hotkey also works
        try:
            from PIL import ImageGrab  # Pillow library (PIL)
        except ImportError:
            print("Please install Pillow (PIL) to save images: pip install pillow")
            return

        x = self.master.winfo_rootx() + self.canvas.winfo_x()
        y = self.master.winfo_rooty() + self.canvas.winfo_y()
        x1 = x + self.width
        y1 = y + self.height

        # Use ImageGrab to capture the canvas area
        try:
            image = ImageGrab.grab().crop((x, y, x1, y1))  # Capture the canvas
        except Exception as e:
            print(f"Error during screen capture: {e}")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                               filetypes=[("PNG files", "*.png"), ("All files", "*.*")])

        if file_path:
            try:
                image.save(file_path)
                print(f"Image saved to {file_path}")
            except Exception as e:
                print(f"Error saving image: {e}")

root = Tk()
app = DrawingApp(root)
root.mainloop()