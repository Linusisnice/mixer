import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from PIL import ImageEnhance
import time
import math
# Initialize the main window
root = tk.Tk()
root.title("Background with Clickable Transparent PNG Overlay")
root.iconbitmap("pythonicon.ico")  # Set the window icon

# Load and display the background image
background_image_path = "back.png"  # Replace with the path to your background image
background_image = Image.open(background_image_path)
background_photo = ImageTk.PhotoImage(background_image)

# Create a canvas to display images
canvas = tk.Canvas(root, width=background_image.width, height=background_image.height, highlightthickness=0)
canvas.pack()
x=0
# Place the background image
canvas.create_image(0, 0, image=background_photo, anchor="nw")
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
    

    if slidernm==1:
        balls=0.3
    elif slidernm==2: 
        balls=0.4
    elif slidernm==3:  
        balls=0.5
    elif slidernm==4:
        balls=0.6
    elif slidernm==5:
        balls=0.9
    ball=(balls*0.53)+0.3

    y = background_image.height * ball
    print (y)
    return y

def update_image_position_side(slidernm):
    

    if slidernm==1:
        balls=0.3
    elif slidernm==2: 
        balls=0.4
    elif slidernm==3:  
        balls=0.5
    elif slidernm==4:
        balls=0.6
    elif slidernm==5:
        balls=0.9
        angle=3.02
        permdiv=1.115
    ball=(balls*0.53)+0.3
    

    y = background_image.height * ball
    # Convert angle from degrees to radians
    angle_radians = math.radians(angle)
    print("angle radian= "+ str(angle_radians))
    # Calculate x using the tangent function
    x = y * math.tan(angle_radians)
    print("x balls= "+str(x))
    x=(background_image.width/permdiv)+x
    return x
# Run the application
while True:
    time.sleep(0.001)
        # Start
    slider1_image_path = "slider1.png" 
    slider1_image = Image.open(slider1_image_path)
    slider1_photo = ImageTk.PhotoImage(slider1_image)

    parent = tk.Tk()  # Create the object
    parent.overrideredirect(1)  # Avoid it appearing and then disappearing quickly
    parent.iconbitmap("pythonicon.ico")  # Set an icon (this is optional - must be in a .ico format)
    parent.withdraw()  # Hide the window as we do not want to see this one
#min 0.3 max  0.83
    slider1 = canvas.create_image(background_image.width/2.5, update_image_position(1), image=slider1_photo, anchor="center", tags="clickable_slider1")

    def on_slider1_click(event):
        print("Overlay image clicked!")

    canvas.tag_bind("clickable_slider1", "<Button-1>", on_slider1_click)
    # Finish
    # Start
    slider2_image_path = "slider2.png" 
    slider2_image = Image.open(slider2_image_path)
    slider2_photo = ImageTk.PhotoImage(slider2_image)

    slider2 = canvas.create_image(background_image.width // 1.875, update_image_position(2), image=slider2_photo, anchor="center", tags="clickable_slider2")

    def on_slider2_click(event):
        print("Overlay image clicked! nigga")

    canvas.tag_bind("clickable_slider2", "<Button-1>", on_slider2_click)
    # Finish
    # Start
    slider3_image_path = "slider3.png" 
    slider3_image = Image.open(slider3_image_path)
    slider3_photo = ImageTk.PhotoImage(slider3_image)

    slider3 = canvas.create_image(background_image.width // 1.517, update_image_position(3), image=slider3_photo, anchor="center", tags="clickable_slider3")

    def on_slider3_click(event):
        print("Overlay image clicked!")

    canvas.tag_bind("clickable_slider3", "<Button-1>", on_slider3_click)
    # Finish
    # Start
    slider4_image_path = "slider4.png" 
    slider4_image = Image.open(slider4_image_path)
    slider4_photo = ImageTk.PhotoImage(slider4_image)

    slider4 = canvas.create_image(background_image.width // 1.27, update_image_position(4), image=slider4_photo, anchor="center", tags="clickable_slider4")

    def on_slider4_click(event):
        print("Overlay image clicked!")

    canvas.tag_bind("clickable_slider4", "<Button-1>", on_slider4_click)
    # Finish
    # Start
    slider5_image_path = "slider5.png" 
    slider5_image = Image.open(slider5_image_path)
    slider5_photo = ImageTk.PhotoImage(slider5_image)

    slider5 = canvas.create_image(update_image_position_side(5), update_image_position(5), image=slider5_photo, anchor="center", tags="clickable_slider5")

    def on_slider5_click(event):
        print("Overlay image clicked!")

    canvas.tag_bind("clickable_slider5", "<Button-1>", on_slider5_click)
    # Finish
    # Start
    b1_image_path = "b1.png" 
    b1_image = Image.open(b1_image_path)
    b1_photo = ImageTk.PhotoImage(b1_image)

    b1 = canvas.create_image(background_image.width // 17.5, background_image.height // 2.7, image=b1_photo, anchor="center", tags="clickable_b1")

    def on_b1_click(event):
        print("Overlay image clicked!")

    canvas.tag_bind("clickable_b1", "<Button-1>", on_b1_click)
    # Finish
    # Start
    b2_image_path = "b2.png" 
    b2_image = Image.open(b2_image_path)
    b2_photo = ImageTk.PhotoImage(b2_image)

    b2 = canvas.create_image(background_image.width // 9, background_image.height // 2.7, image=b2_photo, anchor="center", tags="clickable_b2")

    def on_b2_click(event):
        print("Overlay image clicked!")

    canvas.tag_bind("clickable_b2", "<Button-1>", on_b2_click)
    # Finish
    # Start
    b3_image_path = "b3.png" 
    b3_image = Image.open(b3_image_path)
    b3_photo = ImageTk.PhotoImage(b3_image)

    b3 = canvas.create_image(background_image.width // 6.1, background_image.height // 2.7, image=b3_photo, anchor="center", tags="clickable_b3")

    def on_b3_click(event):
        print("Overlay image clicked!")

    canvas.tag_bind("clickable_b3", "<Button-1>", on_b3_click)
    # Finish
    # Start
    b4_image_path = "b4.png" 
    b4_image = Image.open(b4_image_path)
    b4_photo = ImageTk.PhotoImage(b4_image)

    b4 = canvas.create_image(background_image.width // 4.6, background_image.height // 2.7, image=b4_photo, anchor="center", tags="clickable_b4")

    def on_b4_click(event):
        print("Overlay image clicked!")

    canvas.tag_bind("clickable_b4", "<Button-1>", on_b4_click)
    # Finish
    # Start
    b5_image_path = "b5.png" 
    b5_image = Image.open(b5_image_path)
    b5_photo = ImageTk.PhotoImage(b5_image)

    b5 = canvas.create_image(background_image.width // 17.5, background_image.height // 2.2, image=b5_photo, anchor="center", tags="clickable_b5")

    def on_b5_click(event):
        print("Overlay image clicked!")

    canvas.tag_bind("clickable_b5", "<Button-1>", on_b5_click)
    # Finish
    # Start
    b6_image_path = "b6.png" 
    b6_image = Image.open(b6_image_path)
    b6_photo = ImageTk.PhotoImage(b6_image)

    b6 = canvas.create_image(background_image.width // 9, background_image.height // 2.2, image=b6_photo, anchor="center", tags="clickable_b6")

    def on_b6_click(event):
        print("Overlay image clicked!")

    canvas.tag_bind("clickable_b6", "<Button-1>", on_b6_click)
    # Finish
    # Start
    b7_image_path = "b7.png" 
    b7_image = Image.open(b7_image_path)
    b7_photo = ImageTk.PhotoImage(b7_image)

    b7 = canvas.create_image(background_image.width // 6.1, background_image.height // 2.2, image=b7_photo, anchor="center", tags="clickable_b7")

    def on_b7_click(event):
        print("Overlay image clicked!")

    canvas.tag_bind("clickable_b7", "<Button-1>", on_b7_click)
    # Finish
    # Start
    b8_image_path = "b8.png" 
    b8_image = Image.open(b8_image_path)
    b8_photo = ImageTk.PhotoImage(b8_image)

    b8 = canvas.create_image(background_image.width // 4.6, background_image.height // 2.2, image=b8_photo, anchor="center", tags="clickable_b8")

    def on_b8_click(event):
        print("Overlay image clicked!")

    canvas.tag_bind("clickable_b8", "<Button-1>", on_b8_click)
    # Finish
    # Start
    b9_image_path = "b9.png" 
    b9_image = Image.open(b9_image_path)
    b9_photo = ImageTk.PhotoImage(b9_image)

    b9 = canvas.create_image(background_image.width // 17.5, background_image.height // 1.87, image=b9_photo, anchor="center", tags="clickable_b9")

    def on_b9_click(event):
        print("Overlay image clicked!")

    canvas.tag_bind("clickable_b9", "<Button-1>", on_b9_click)
    # Finish
    # Start
    b10_image_path = "b10.png" 
    b10_image = Image.open(b10_image_path)
    b10_photo = ImageTk.PhotoImage(b10_image)

    b10 = canvas.create_image(background_image.width // 9, background_image.height // 1.87, image=b10_photo, anchor="center", tags="clickable_b10")

    def on_b10_click(event):
        print("Overlay image clicked!")

    canvas.tag_bind("clickable_b10", "<Button-1>", on_b10_click)
    # Finish
    # Start
    b11_image_path = "b11.png" 
    b11_image = Image.open(b11_image_path)
    b11_photo = ImageTk.PhotoImage(b11_image)

    b11 = canvas.create_image(background_image.width // 6.1, background_image.height // 1.87, image=b11_photo, anchor="center", tags="clickable_b11")

    def on_b11_click(event):
        print("Overlay image clicked!")

    canvas.tag_bind("clickable_b11", "<Button-1>", on_b11_click)
    # Finish
    # Start
    b12_image_path = "b12.png" 
    b12_image = Image.open(b12_image_path)
    b12_photo = ImageTk.PhotoImage(b12_image)

    b12 = canvas.create_image(background_image.width // 4.6, background_image.height // 1.87, image=b12_photo, anchor="center", tags="clickable_b12")

    def on_b12_click(event):
        print("Overlay image clicked!")

    canvas.tag_bind("clickable_b12", "<Button-1>", on_b12_click)
    # Finish
    # Start
    b13_image_path = "b13.png" 
    b13_image = Image.open(b13_image_path)
    b13_photo = ImageTk.PhotoImage(b13_image)

    b13 = canvas.create_image(background_image.width // 17.5, background_image.height // 1.63, image=b13_photo, anchor="center", tags="clickable_b13")

    def on_b13_click(event):
        print("Overlay image clicked!")

    canvas.tag_bind("clickable_b13", "<Button-1>", on_b13_click)
    # Finish
    # Start
    b14_image_path = "b14.png" 
    b14_image = Image.open(b14_image_path)
    b14_photo = ImageTk.PhotoImage(b14_image)

    b14 = canvas.create_image(background_image.width // 9, background_image.height // 1.63, image=b14_photo, anchor="center", tags="clickable_b14")

    def on_b14_click(event):
        print("Overlay image clicked!")

    canvas.tag_bind("clickable_b14", "<Button-1>", on_b14_click)
    # Finish
    # Start
    b15_image_path = "b15.png" 
    b15_image = Image.open(b15_image_path)
    b15_photo = ImageTk.PhotoImage(b15_image)

    b15 = canvas.create_image(background_image.width // 6.1, background_image.height // 1.63, image=b15_photo, anchor="center", tags="clickable_b15")

    def on_b15_click(event):
        print("Overlay image clicked!")

    canvas.tag_bind("clickable_b15", "<Button-1>", on_b15_click)
    # Finish
    # Start
    b16_image_path = "b16.png" 
    b16_image = Image.open(b16_image_path)
    b16_photo = ImageTk.PhotoImage(b16_image)

    # Reduce the brightness of the image
    enhancer = ImageEnhance.Brightness(b16_image)
    b16_image = enhancer.enhance(0.3)  # Reduce brightness by 50%

    b16_photo = ImageTk.PhotoImage(b16_image)
    b16 = canvas.create_image(background_image.width // 4.6, background_image.height // 1.63, image=b16_photo, anchor="center", tags="clickable_b16")

    def on_b16_click(event):
        ()
    canvas.tag_bind("clickable_b16", "<Button-1>", on_b16_click)
    # Finish
    # Start
    master_image_path = "master.png" 
    master_image = Image.open(master_image_path)
    master_photo = ImageTk.PhotoImage(master_image)

    master = canvas.create_image(background_image.width // 12, background_image.height // 14, image=master_photo, anchor="center", tags="clickable_master")

    def on_master_click(event):
        open_master_window()

    canvas.tag_bind("clickable_master", "<Button-1>", on_master_click)
    # Finish
    # Start
    display_image_path = "display.png" 
    display_image = Image.open(display_image_path)
    display_photo = ImageTk.PhotoImage(display_image)

    display = canvas.create_image(background_image.width // 7.50, background_image.height // 5, image=display_photo, anchor="center", tags="clickable_display")

    def on_display_click(event):
        open_display_window()

    canvas.tag_bind("clickable_display", "<Button-1>", on_display_click)
    # Finish
    root.mainloop()