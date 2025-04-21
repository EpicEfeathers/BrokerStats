from utils import cairo_functions, functions

THIN = "Helvetica Neue Light"
BOLD = "Helvetica Neue Bold"
REGULAR = "Helvetica Neue"

SIZE = (1920, 1080)

class colours:
    white = (1,1,1)
    green = (0, 1, 0)
    red = (1, 0, 0)

def create_image(daily_average, daily_average_diff, total_playercount, total_playercount_diff):
    middle_w = SIZE[0] / 2

    text_elements = [ # Adding each individual piece of text
        # Online Players

        (REGULAR, [f"{functions.format_large_number(total_playercount[0])}  ", f"({"+" if total_playercount_diff >= 0 else ""}{functions.format_large_number(total_playercount_diff)})"], (middle_w, 526), [colours.white, (colours.green if total_playercount_diff >= 0 else colours.red)], 65, "mt", 30),
        (REGULAR, [f"{daily_average[0]}  ", f"({"+" if daily_average_diff >= 0 else ""}{daily_average_diff})"], (middle_w, 785), [colours.white, (colours.green if daily_average_diff >= 0 else colours.red)], 65, "mt", 30),
    ]   

    surface = cairo_functions.add_text_to_image(text_elements, "utils/commands/trends/backgrounds")

    return functions.convert_to_discord(surface)