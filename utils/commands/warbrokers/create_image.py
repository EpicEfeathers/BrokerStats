from utils import functions
import cairo
from utils import cairo_functions

THIN = "Helvetica Neue Light"
BOLD = "Helvetica Neue"
REGULAR = "Helvetica Neue"

SIZE = (1920, 1080)

class colours:
    white = (1,1,1)


def create_stats_card():
    text_elements = [ # Adding each individual piece of text
        # NAME
        (BOLD, "Total Users", (SIZE[0]/2, 100), colours.white, 60, "mm"),

    ]

    surface = cairo_functions.add_text_to_image(text_elements, "tests/blurred_images")

    return functions.convert_to_discord(surface)