import cairo
from io import BytesIO

from utils import functions, cairo_functions


def format_large_number(number):
    return f"{number:,}"

def convert_to_discord(surface):
    image_stream = BytesIO()
    surface.write_to_png(image_stream)  # Write to the BytesIO object
    image_stream.seek(0)

    return image_stream

OPACITY = 200
LEFT_TEXT = 870
RIGHT_TEXT = 1410
RIGHT_Y_POSITION = 56

THIN = "Helvetica Neue Light"
BOLD = "Helvetica Neue"
REGULAR = "Helvetica Neue"

# cards
SIZE = (375, 188)
TOP_Y_POSITION = 251 #295
SPACING = int((840 - (2*SIZE[0]))/3)
LEFT = SPACING + SIZE[1]
RIGHT = (840 - SIZE[1]) - SPACING
LOGO_SIZE = (113,101)
PROFILE_PIC_SIZE = (192, 192)

def add_squad_text_element(text_info, context):
    font_path, text, position, color, font_size, alignment = text_info  # Unpack text information
    if isinstance(font_path, list):
        context.select_font_face(font_path[0], cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        context.set_font_size(font_size)
        context.set_source_rgba(*color)

        x_2, y = calculate_two_positions(context, text[0], position)


        context.move_to(position[0], y)
        context.show_text(str(text[0]))
        context.fill()

        context.select_font_face(font_path[1], cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        context.move_to(position[0] + x_2, y)
        context.show_text(str(text[1]))
        context.fill()
    else:
        context.select_font_face(font_path, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        context.set_font_size(font_size)

        context.set_source_rgba(*color)
        
        # check if first item of list or just tuple

        x, y = calculate_position(context, str(text), position, alignment)
        # Add the text
        context.move_to(x, y)
        context.show_text(str(text))
        context.fill()


def calculate_position(context, text, position, alignment):
    """
    Calculates position of text placement for
    different alignments.
    """
    extents = context.text_extents(text)
    text_width = extents.width
    text_height = extents.height
    
    x = position[0] - 1 # adjustment as it seemed to place it one pixel to the right (maybe should use -2?)
    if alignment[0] == 'm':
        x -= text_width / 2
    elif alignment[0] == 'r':
        x -= text_width

    y = position[1]
    if alignment[1] == 'm':
        y += text_height / 2
    elif alignment[1] == 'r':
        y += text_height

    return x, y


def calculate_two_positions(context, text, position):
    space_width = 15 # looks nice

    extents = context.text_extents(text)
    #print(f"\"{text}\"", extents.width)
    width = extents.width + space_width

    extents = context.text_extents(text)
    text_height = extents.height
    y = position[1]
    y += text_height / 2

    return width, y



# Function to add multiple pieces of text with Cairo
def text(text_elements):
    image_path = functions.get_random_background("utils/commands/squad/backgrounds")
    cairo_surface = cairo.ImageSurface.create_from_png(image_path)
    context = cairo.Context(cairo_surface)

    # Loop through each text element and add it to the context
    for text_info in text_elements:
        add_squad_text_element(text_info, context)

    return cairo_surface

def create_stat_card(stats):
    text_elements = [
        # NAME
        (THIN, stats['squad'], (1140, RIGHT_Y_POSITION + 225), (156/255, 156/255, 248/255), 60, "mm"),
        # ACTIVE MEMBERS
        ([BOLD, THIN], [str(stats['member_count']), f"({stats['active_players']} active this week)"], (LEFT_TEXT, RIGHT_Y_POSITION + 300 + 45), (1, 1, 1), 41, "lm"),
        # KDR
        (BOLD, str(round(float(stats['kdr']), 1)), (LEFT_TEXT, RIGHT_Y_POSITION + 401 + 45), (1, 1, 1), 41, "lm"),
        # KPM
        #(THIN, "Kills / Min", (LEFT_TEXT, RIGHT_Y_POSITION + 509), (1, 1, 1), 38, "lm"),
        (BOLD, str(round(float(stats['kpm']), 1)), (LEFT_TEXT, RIGHT_Y_POSITION + 500 + 45), (1, 1, 1), 41, "lm"),
        # LEVEL
        (BOLD, f"{stats['level']}", (LEFT_TEXT, RIGHT_Y_POSITION + 600 + 45), (1, 1, 1), 41, "lm"),
        (THIN, f"XP: {format_large_number(stats['xp'])}", (LEFT_TEXT, RIGHT_Y_POSITION + 615 + 75), (1, 1, 1), 38, "lm"),

        # KILLS
        #(THIN, "Kills:", (LEFT - (SIZE[0]/2) + 23, TOP_Y_POSITION - 45), (1, 1, 1), 41, "lm"),
        (BOLD, format_large_number(stats["kills"]), (LEFT - (SIZE[0]/2) + 23, TOP_Y_POSITION + 25), (1, 1, 1), 41, "lm"),
        # DEATHS
        #(THIN, "Deaths:", (RIGHT - (SIZE[0]/2) + 23, TOP_Y_POSITION - 45), (1, 1, 1), 41, "lm"),
        (BOLD, format_large_number(stats["deaths"]), (RIGHT - (SIZE[0]/2) + 23, TOP_Y_POSITION + 25), (1, 1, 1), 41, "lm"),
        # KILLS
        #(THIN, "Classic Wins:", (LEFT - (SIZE[0]/2) + 23, TOP_Y_POSITION + (SPACING + SIZE[1]) - 45), (1, 1, 1), 41, "lm"),
        (BOLD, format_large_number(stats["classic wins"]), (LEFT - (SIZE[0]/2) + 23, TOP_Y_POSITION + 25 + (SPACING + SIZE[1])), (1, 1, 1), 41, "lm"),
        # KILLS
        #(THIN, "BR Wins:", (RIGHT - (SIZE[0]/2) + 23, TOP_Y_POSITION + (SPACING + SIZE[1])- 45), (1, 1, 1), 41, "lm"),
        (BOLD, format_large_number(stats["br wins"]), (RIGHT - (SIZE[0]/2) + 23, TOP_Y_POSITION + 25 + (SPACING + SIZE[1])), (1, 1, 1), 41, "lm"),
        # KILLS
        #(THIN, "Kills ELO", (LEFT - (SIZE[0]/2) + 23, TOP_Y_POSITION + 2*(SPACING + SIZE[1]) - 45), (1, 1, 1), 41, "lm"),
        (BOLD, stats["kills_elo"], (LEFT - (SIZE[0]/2) + 23, TOP_Y_POSITION + 25 + 2*(SPACING + SIZE[1])), (1, 1, 1), 41, "lm"),
        # KILLS
        #(THIN, "Games ELO", (RIGHT - (SIZE[0]/2) + 23, TOP_Y_POSITION + 2*(SPACING + SIZE[1])- 45), (1, 1, 1), 41, "lm"),
        (BOLD, stats["games_elo"], (RIGHT - (SIZE[0]/2) + 23, TOP_Y_POSITION + 25 + 2*(SPACING + SIZE[1])), (1, 1, 1), 41, "lm"),
    ]

    surface = cairo_functions.squad_text(text_elements)

    return convert_to_discord(surface)