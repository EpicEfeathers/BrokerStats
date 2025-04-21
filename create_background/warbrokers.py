import sys, os
import cairo

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import cairo_functions

THIN = "Helvetica Neue Light"
BOLD = "Helvetica Neue Bold"
REGULAR = "Helvetica Neue"

SIZE = (1920, 1080)

class colours:
    white = (1,1,1)

def create_stats_card():
    cairo_surface = cairo.ImageSurface.create_from_png("tests/blurred_images/space_station.png")

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
        (BOLD, "Total Players", (middle_w, 106), colours.white, 65, "mt"),
        #(REGULAR, "146,844,720", (middle_w, 180), colours.white, 50, "mt"),
        
        # Online Players
        (BOLD, "Online Players", (middle_w, 284), colours.white, 65, "mt"),
        #(REGULAR, "193", (middle_w, 371), colours.white, 50, "mt"),

        # Total Maps
        (BOLD, "Total Maps", (middle_w, 477), colours.white, 65, "mt"),
        #(REGULAR, "39", (middle_w, 563), colours.white, 50, "mt"),

        # Total Weapons
        (BOLD, "Total Weapons", (middle_w, 666), colours.white, 65, "mt"),
        #(REGULAR, "39", (middle_w, 752), colours.white, 50, "mt"),

        # Total Cosmetics
        (BOLD, "Total Cosmetics", (middle_w, 851), colours.white, 65, "mt"),
        #(REGULAR, "5107", (middle_w, 937), colours.white, 50, "mt"),
    ]

    surface = cairo_functions.add_text_to_surface(cairo_surface, text_elements)

    surface.write_to_png("test.png")

def draw_rounded_rectangle(ctx, x, y, width, height, radius):
    """Draws a rounded rectangle on the given cairo context."""
    ctx.set_source_rgba(0, 0, 0, 0.5)  # 50% opaque black

    ctx.new_sub_path()
    ctx.arc(x + width - radius, y + radius, radius, -90 * (3.14/180), 0)
    ctx.arc(x + width - radius, y + height - radius, radius, 0, 90 * (3.14/180))
    ctx.arc(x + radius, y + height - radius, radius, 90 * (3.14/180), 180 * (3.14/180))
    ctx.arc(x + radius, y + radius, radius, 180 * (3.14/180), 270 * (3.14/180))
    ctx.close_path()

create_stats_card()
