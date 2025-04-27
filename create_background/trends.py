import sys, os, io
import cairo
from PIL import Image, ImageFilter

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import cairo_functions

THIN = "Helvetica Neue Light"
BOLD = "Helvetica Neue Bold"
REGULAR = "Helvetica Neue"

SIZE = (1920, 1080)

class colours:
    white = (1,1,1)
    green = (0, 1, 0)
    red = (1, 0, 0)

def create_stats_card(file_path, file_name):
    # PIL: Open and blur the image
    pil_image = Image.open(file_path)
    blurred_pil = pil_image.filter(ImageFilter.GaussianBlur(radius=5.0))

    # Convert the blurred PIL image into a format Cairo can use
    with io.BytesIO() as output:
        blurred_pil.save(output, format="PNG")
        output.seek(0)
        cairo_surface = cairo.ImageSurface.create_from_png(output)

        ctx = cairo.Context(cairo_surface)

    background_size = (SIZE[0]-100, SIZE[1]-100)
    ctx.set_source_rgba(0, 0, 0, 1)  # Fully opaque black
    draw_rounded_rectangle(ctx, (SIZE[0]-background_size[0])/2, (SIZE[1]-background_size[1])/2, background_size[0], background_size[1], 25)
    ctx.fill()


    # paste image
    ctx.save()

    ctx.translate(102, 100) # moves the paper under the pen, that's why we use save / restore
    ctx.scale(2/5, 2/5)

    image_surface = cairo.ImageSurface.create_from_png("create_background/images/wb_logo.png")
    ctx.set_source_surface(image_surface, 0, 0)
    ctx.paint()

    ctx.restore()



    middle_w = SIZE[0] / 2
    text_elements = [ # Adding each individual piece of text
        # Total Players
        (BOLD, "Daily Trends", (middle_w, 145), colours.white, 90, "mt"),
        
        # Online Players
        (BOLD, "Total Players", (middle_w, 394), colours.white, 80, "mt"),
        #(REGULAR, ["156,768,987  ", "(+47,356)"], (middle_w, 526), [colours.white, colours.green], 65, "mt", 30),

        # Total Maps
        (BOLD, "Average Playercount", (middle_w, 651), colours.white, 80, "mt"),
        #(REGULAR, ["195", "(-15)"], (middle_w, 785), [colours.white, colours.red], 65, "mt", 30),
    ]

    surface = cairo_functions.add_text_to_surface(cairo_surface, text_elements)

    surface.write_to_png(f"create_background/outputted_backgrounds/{file_name}")

def draw_rounded_rectangle(ctx, x, y, width, height, radius):
    """Draws a rounded rectangle on the given cairo context."""
    ctx.set_source_rgba(0, 0, 0, 0.5)  # 50% opaque black

    ctx.new_sub_path()
    ctx.arc(x + width - radius, y + radius, radius, -90 * (3.14/180), 0)
    ctx.arc(x + width - radius, y + height - radius, radius, 0, 90 * (3.14/180))
    ctx.arc(x + radius, y + height - radius, radius, 90 * (3.14/180), 180 * (3.14/180))
    ctx.arc(x + radius, y + radius, radius, 180 * (3.14/180), 270 * (3.14/180))
    ctx.close_path()

folder_path = "create_background/backgrounds"
for filename in os.listdir(folder_path):
    if filename != ".DS_Store":
        file_path = os.path.join(folder_path, filename)
        create_stats_card(file_path, filename)
