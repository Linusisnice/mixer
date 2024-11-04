import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from PIL import ImageEnhance
import time
import math
import serial

# Function to resize the background image
def resize_background(event):
    global background_photo_resized, background_image_width, background_image_height, slider_photos_resized
    canvas_width = event.width
    canvas_height = event.height

    # Calculate the new dimensions while maintaining the aspect ratio
    aspect_ratio = background_image_width / background_image_height
    if canvas_width / canvas_height > aspect_ratio:
        new_height = canvas_height
        new_width = int(new_height * aspect_ratio)
    else:
        new_width = canvas_width
        new_height = int(new_width / aspect_ratio)

    # Ensure new dimensions are greater than zero
    if new_width > 0 and new_height > 0:
        resized_image = background_image.resize((new_width, new_height), Image.LANCZOS)
        background_photo_resized = ImageTk.PhotoImage(resized_image)
        canvas.itemconfig(background_image_id, image=background_photo_resized)
        canvas.config(width=new_width, height=new_height)
        canvas.background_photo_resized = background_photo_resized  # Keep a reference to avoid garbage collection
        background_image_width = new_width
        background_image_height = new_height

        # Resize slider images to be 19% of the height of the background image
        slider_height = int(new_height * 0.19)
        if slider_height > 0:
            slider_photos_resized = []
            for i, slider_image_path in enumerate(slider_images):
                slider_image = Image.open(slider_image_path)
                aspect_ratio_slider = slider_image.width / slider_image.height
                slider_width = int(slider_height * aspect_ratio_slider)
                if slider_width > 0:
                    slider_image_resized = slider_image.resize((slider_width, slider_height), Image.LANCZOS)
                    slider_photo_resized = ImageTk.PhotoImage(slider_image_resized)
                    slider_photos_resized.append(slider_photo_resized)
                    canvas.itemconfig(sliders[i], image=slider_photo_resized)
                    canvas.coords(sliders[i], update_image_position_side(i+1), update_image_position(i+1))
                    canvas.slider_photos_resized = slider_photos_resized  # Keep a reference to avoid garbage collection

        # Adjust the window size to fit the resized background image dimensions
        root.geometry(f"{new_width}x{new_height}")

# Initialize the main window
root = tk.Tk()
root.title("Background with Clickable Transparent PNG Overlay")
root.iconbitmap("pythonicon.ico")  # Set the window icon

# Remove the window transparency and decorations settings
# root.attributes('-transparentcolor', 'white')
# root.overrideredirect(True)

# Add a frame to handle window dragging and resizing
frame = tk.Frame(root, bg='white')
frame.pack(fill=tk.BOTH, expand=True)

# Function to allow window dragging
def start_move(event):
    root.x = event.x
    root.y = event.y

def stop_move(event):
    root.x = None
    root.y = None

def on_motion(event):
    deltax = event.x - root.x
    deltay = event.y - root.y
    x = root.winfo_x() + deltax
    y = root.winfo_y() + deltay
    root.geometry(f"+{x}+{y}")

frame.bind("<ButtonPress-1>", start_move)
frame.bind("<ButtonRelease-1>", stop_move)
frame.bind("<B1-Motion>", on_motion)

# Load and display the background image
background_image_path = "back.png"  # Replace with the path to your background image
background_image = Image.open(background_image_path)
background_photo = ImageTk.PhotoImage(background_image)
background_image_width, background_image_height = background_image.size

# Create a canvas to display images
canvas = tk.Canvas(frame, highlightthickness=0, bg='white')
canvas.pack(fill=tk.BOTH, expand=True)

# Place the background image
background_image_id = canvas.create_image(0, 0, image=background_photo, anchor="nw")

# Debounce resize event handling to reduce lag
resize_timer = None

def on_resize(event):
    global resize_timer
    if resize_timer is not None:
        root.after_cancel(resize_timer)
    resize_timer = root.after(200, resize_background, event)

# Bind the debounced resize event to the resize_background function
root.bind("<Configure>", on_resize)

def open_master_window():
    # Create secondary (or popup) window.
    secondary_window = tk.Toplevel()
    secondary_window.title("Secondary Window")
    secondary_window.config(width=300, height=200)
    # Create a button to close (destroy) this window.
    button_close = tk.Button(
        secondary_window,
        text="Close window",
        command=secondary_window.destroy
    )
    button_close.place(x=75, y=75)

def open_display_window():
    # Create secondary (or popup) window.
    secondary_window = tk.Toplevel()
    secondary_window.title("Secondary Window")
    secondary_window.config(width=300, height=200)
    # Create a button to close (destroy) this window.
    button_close = tk.Button(
        secondary_window,
        text="Close window",
        command=secondary_window.destroy
    )
    button_close.place(x=75, y=75)

def update_image_position(slidernm):
    balls = read_serial(str(slidernm))
    ball = (balls * 0.53) + 0.3
    y = background_image_height * ball
    return y

def update_image_position_side(slidernm):
    balls = read_serial(str(slidernm))
    angles = [-1.42, -0.49, 1, 1.92, 3.02]
    permdivs = [2.4, 1.86, 1.517, 1.285, 1.115]
    angle = angles[slidernm - 1]
    permdiv = permdivs[slidernm - 1]
    ball = (balls * 0.53) + 0.3
    y = background_image_height * ball
    angle_radians = math.radians(angle)
    x = y * math.tan(angle_radians)
    x = (background_image_width / permdiv) + x
    return x
    c
def read_serial(whatthing):
    data = "70,80,100,90,10,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1"
    values = data.split(',')
    if len(values) == 22:  # Ensure there are exactly 22 values
        alldata = [int(values[i]) for i in range(len(values))]
        return (alldata[int(whatthing) - 1]) / 100

def update_sliders():
    for i in range(1, 6):
        canvas.coords(sliders[i-1], update_image_position_side(i), update_image_position(i))
    root.after(100, update_sliders)

# Load slider images
slider_images = ["slider1.png", "slider2.png", "slider3.png", "slider4.png", "slider5.png"]
sliders = []
slider_photos = []  # Keep a reference to avoid garbage collection

for i, slider_image_path in enumerate(slider_images):
    slider_image = Image.open(slider_image_path)
    slider_photo = ImageTk.PhotoImage(slider_image)
    slider_photos.append(slider_photo)  # Keep a reference to avoid garbage collection
    slider = canvas.create_image(update_image_position_side(i+1), update_image_position(i+1), image=slider_photo, anchor="center", tags=f"clickable_slider{i+1}")
    sliders.append(slider)
    canvas.tag_bind(f"clickable_slider{i+1}", "<Button-1>", lambda event, i=i: print(f"Slider {i+1} clicked!"))

# Load and place other images (buttons, pots, etc.)
# ...existing code for loading and placing other images...

# Start the loop to update sliders
root.after(100, update_sliders)
root.mainloop()