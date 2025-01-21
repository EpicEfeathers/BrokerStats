import cairo

from utils import functions

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
    else: # for multiple colors
        positions = calculate_multiple_positions(context, text, position, alignment) # calculated proper positions of different segments based on alignment

        for i, position in enumerate(positions):
            context.set_source_rgb(*color[i])
            context.move_to(*position)
            context.show_text(str(text[i]))

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

    #print(str(text), text_width, x)

    return x, y

def calculate_multiple_positions(context, text, position, alignment):
    """
    Calculated the proper positions for each piece of text
    if there are multiple different pieces.
    """

    space_width = 15 # looks nice

    extents = [context.text_extents(str(i)) for i in text]
    widths = [i.width for i in extents]
    total_text_width = sum(widths) + space_width

    #center align
    middle_y = position[1] + extents[0].height / 2

    x = []
    if alignment[0] == 'm':
        for i in range(len(text)):
            x.append(position[0] - total_text_width/2 + i*(widths[0] + space_width))
    elif alignment[0] == 'l':
        for i in range(len(text)):
            x.append(position[0] + i*(widths[0] + space_width))
    
    return [(xi, middle_y) for xi in x]

def calculate_two_positions(context, text, position):
    space_width = 15 # looks nice

    extents = context.text_extents(text)
    width = extents.width + space_width

    extents = context.text_extents(text)
    text_height = extents.height
    y = position[1]
    y += text_height / 2

    return width, y

# Function to add multiple pieces of text with Cairo
def stats_text(text_elements):
    image_path = functions.get_random_background("utils/commands/stats/backgrounds")
    cairo_surface = cairo.ImageSurface.create_from_png(image_path)
    context = cairo.Context(cairo_surface)

    # Loop through each text element and add it to the context
    for text_info in text_elements:
        add_stats_text_element(text_info, context)

    return cairo_surface

def daily_leaderboard_text(text_elements):
    image_path = functions.get_random_background("utils/commands/leaderboards/daily_weapon_kills/backgrounds")
    cairo_surface = cairo.ImageSurface.create_from_png(image_path)
    context = cairo.Context(cairo_surface)

    # Loop through each text element and add it to the context
    for text_info in text_elements:
        add_stats_text_element(text_info, context)

    return cairo_surface

# Function to add multiple pieces of text with Cairo
def squad_text(text_elements):
    image_path = functions.get_random_background("utils/commands/squad/backgrounds")
    cairo_surface = cairo.ImageSurface.create_from_png(image_path)
    context = cairo.Context(cairo_surface)

    # Loop through each text element and add it to the context
    for text_info in text_elements:
        add_squad_text_element(text_info, context)

    return cairo_surface