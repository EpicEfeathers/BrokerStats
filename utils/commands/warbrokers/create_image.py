from utils import functions
import requests
from utils import cairo_functions

THIN = "Helvetica Neue Light"
BOLD = "Helvetica Neue"
REGULAR = "Helvetica Neue"

SIZE = (1920, 1080)

class colours:
    white = (1,1,1)


def create_stats_card(total_playercount, playercount):
    maps = 39
    weapons = 39
    cosmetics = 5107

    middle_w = SIZE[0] / 2
    text_elements = [ # Adding each individual piece of text
        # Total Players
        (REGULAR, functions.format_large_number(total_playercount), (middle_w, 180), colours.white, 50, "mt"),
        
        # Online Players
        (REGULAR, playercount, (middle_w, 371), colours.white, 50, "mt"),

        # Total Maps
        (REGULAR, maps, (middle_w, 563), colours.white, 50, "mt"),

        # Total Weapons
        (REGULAR, weapons, (middle_w, 752), colours.white, 50, "mt"),

        # Total Cosmetics
        (REGULAR, cosmetics, (middle_w, 937), colours.white, 50, "mt"),
    ]
    surface = cairo_functions.add_text_to_image(text_elements, "utils/commands/warbrokers/backgrounds")

    return functions.convert_to_discord(surface)