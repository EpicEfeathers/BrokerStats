import cairo

from utils import functions, cairo_functions


THIN = "Helvetica Neue Light"
BOLD = "Helvetica Neue"
REGULAR = "Helvetica Neue"

# cards
IMAGE_SIZE = (600, 810)

SIZE = (508, 57) # (820, 57)
STEP = SIZE[1] + 5
TOP_Y_POSITION = SIZE[1]/2 + 180

def daily_leaderboard_text(text_elements, img_path):
    image_path = functions.get_random_background(img_path)
    cairo_surface = cairo.ImageSurface.create_from_png(image_path)
    context = cairo.Context(cairo_surface)

    # Loop through each text element and add it to the context
    for text_info in text_elements:
        add_stats_text_element(text_info, context)

    return cairo_surface

def add_stats_text_element(text_info, context):
    """
    Adds text element to image (way too complicated).
    Can handle adding a single color, or multiple colors.
    """

    font_path, text, position, color, font_size, alignment = text_info  # Unpack text information
    context.select_font_face(font_path, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    context.set_font_size(font_size)

    if not isinstance(text, list) or text[0] == "": # for single colors

        x, y = calculate_position(context, str(text), position, alignment) # calculates proper position based on alignment
        context.set_source_rgba(*color)
        context.move_to(x, y)
        context.show_text(str(text))

        context.set_source_rgba(1, 0, 0)  # Red pixel
        context.rectangle(position[0], position[1], 1, 1)  # Define a 1x1 rectangle at (x, y)
        context.fill()

def calculate_position(context, text, position, alignment):
    """
    Calculates position of text placement for
    different alignments.
    """
    extents = context.text_extents(text)
    scaled_font = context.get_scaled_font()
    font_extents = scaled_font.extents()
    ascent = font_extents[0]

    text_width = extents.width
    text_height = extents.height
    x_bearing = extents.x_bearing  # Account for horizontal offset

    x = position[0] - x_bearing  # Adjust by the bearing
    if alignment[0] == 'm':
        x -= text_width / 2
    elif alignment[0] == 'r':
        x -= text_width

    y = position[1]
    if alignment[1] == 'm':
        y += ascent / 2

    #print(str(text), text_width, x)

    return x, y


def create_stats_card(data, category, img_path):
    """
    Main function to write info to stats card
    """

    if category == "Classic Mode Wins": # makes it fit on the screen
        category = "Classic Wins"

    text_elements = [ # Adding each individual piece of text
        (BOLD, category, (IMAGE_SIZE[0]/2, 130), (255, 255, 255), 32, "mm"),
    ]

    old_rank = None
    rank = 1
    skipped_ranks = 0

    for height in range(10 if len(data) >= 10 else len(data)):
        if data[height][1] != old_rank:
            rank += skipped_ranks  # Add skipped ranks when moving to a new value
            skipped_ranks = 0      # Reset skipped ranks for the next rank group

        old_rank = data[height][1]
        skipped_ranks += 1

        text_elements.append((BOLD, f"{rank}", (41, TOP_Y_POSITION - 4 + height*(STEP)), (200,200,200), 36, "mm")) # rank
        text_elements.append((REGULAR, data[height][0], (100, TOP_Y_POSITION - 3 + height*(STEP)), (200,200,200), 30, "lm")) # username
        text_elements.append((REGULAR, data[height][1], (IMAGE_SIZE[0]-30, TOP_Y_POSITION - 4 + height*(STEP)), (200,200,200), 36, "rm")) # value

    surface = daily_leaderboard_text(text_elements, img_path)

    return functions.convert_to_discord(surface)