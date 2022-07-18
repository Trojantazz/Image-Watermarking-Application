from PIL import Image, ImageTk, ImageDraw, ImageFont
import PIL.Image

from tkinter import *
from tkinter import filedialog, simpledialog, messagebox

# -----------------------CONSTANTS ---------------------------#
WHITE = (255, 255, 255, 128)
BLACK = (0, 0, 0, 128)
filename = None


# ------------------------------------------------------------#


def watermark(image_path, text_color):
    """
    Places a watermark on the selected image.
    """

    # Ask the user for watermark text
    text = simpledialog.askstring(title="Watermark Text",
                                  prompt="Enter text")

    # Add watermark to the image if text was entered
    if text:
        with PIL.Image.open(image_path).convert("RGBA") as im:
            # Get the dimensions of the imported image
            [width, height] = im.size

            # make a blank image for the text, initialized to transparent text color
            txt = PIL.Image.new("RGBA", im.size, (255, 255, 255, 0))

            # get a font
            fnt = ImageFont.truetype("arial.ttf", 40, encoding="UTF-8")
            # get a drawing context
            d = ImageDraw.Draw(txt)
            # draw text at centre of the image
            d.text((width / 2, height / 2), text, font=fnt, fill=text_color)

            result = PIL.Image.alpha_composite(im, txt)

            result = result.convert("RGB")

            """ Create a directory 'watermarked_imgs'"""
            # Save the watermarked image to the watermarked_imgs folder
            result.save(f"watermarked_imgs/{image_path.split('/')[-1]}")

        # Tell the user that image has been saved
        messagebox.showinfo(title="Image Saved", message="Your image has been saved.")


def select_image():
    """
    Opens a dialog box for the user to select an image.
    """
    global filename
    filename = filedialog.askopenfilename(title='Select Image', filetypes=[
        ("image", ".jpeg"),
        ("image", ".png"),
        ("image", ".jpg"),
    ])

    with PIL.Image.open(filename).convert("RGBA") as im:
        # Get the dimensions of the imported image
        [width, height] = im.size

        # If the image is too large, halve the width and height
        if height >= 1000:
            im = im.resize((int(width / 2), int(height / 2)))

        # Place the imported image on the panel(label)
        image = ImageTk.PhotoImage(im)
        panel.configure(image=image)
        panel.image = image


def on_option_change():
    # Changes the add_watermark parameters when listbox value is changed.

    if variable.get() == "White Text":
        add_watermark_button.config(command=lambda: watermark(filename, WHITE))
    else:
        add_watermark_button.config(command=lambda: watermark(filename, BLACK))


# -----------------------UI SETUP ---------------------------#
ui = Tk()
ui.title("Image Watermarking App")
ui.config(padx=20, pady=20)

# Buttons
select_image_button = Button(text="Select Image", command=select_image)
select_image_button.grid(row=1, column=0)

add_watermark_button = Button(text="Add Watermark", command=lambda: watermark(filename, WHITE))
add_watermark_button.grid(row=1, column=1)

# Panel(Labels)
panel = Label(ui, text=" ")
panel.grid(row=0, column=0, columnspan=3)

# Listbox
variable = StringVar(ui)
variable.set("White Text")  # default
options = OptionMenu(ui, variable, "White Text", "Black Text", command=on_option_change)
options.grid(row=1, column=2)

ui.mainloop()
