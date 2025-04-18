import cairo

from utils import functions

def calculate_length(font_path, font_size, text):
    temp_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1000, 100)  # Temporary surface
    context = cairo.Context(temp_surface)

    context.select_font_face(font_path, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    context.set_font_size(font_size)

    extents = context.text_extents(text)
    text_width = extents.width

    #print(text_width)


'''def add_stats_text_element(text_info, context):
    """
    Adds text element to image (way too complicated).
    Can handle adding a single color, or multiple colors.
    """

    font_path, text, position, color, font_size, alignment = text_info  # Unpack text information
    context.select_font_face(font_path, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    context.set_font_size(font_size)

    if not isinstance(text, list) or text[0] == "": # for single colors

        positions = calculate_position(context, str(text), position, alignment) # calculates proper position based on alignment

        # as these are returned as strings or tuples, and not lists of strings or tuples,
        # convert them to the proper format so they can be used below
        text = [text]
        color = [color]
        positions = [positions]
    else: # for multiple colors
        positions = calculate_multiple_positions(context, text, position, alignment) # calculated proper positions of different segments based on alignment

    for i, position in enumerate(positions):
        context.set_source_rgb(*color[i])
        context.move_to(*position)
        context.show_text(str(text[i]))'''


def add_text_element(text_info, context):
    font_path, text, position, color, font_size, alignment = text_info  # Unpack text information
    context.set_font_size(font_size)

    if not isinstance(font_path, list) and not isinstance(text, list) or text[0] == "": # if font path is not a list (just one font)
        positions = calculate_position(context, str(text), position, alignment)
        font_path = [font_path]
        text = [text]
        color = [color]
        positions = [positions]
    elif isinstance(font_path, list): # if multiple fonts
        x_diff, y = calculate_two_positions(context, text[0], position)
        positions = [(position[0], y), (position[0] + x_diff, y)]
        color = [color for position in positions]
    else: # if multiple pieces of text, same font
        positions = calculate_multiple_positions(context, text, position, alignment) # calculated proper positions of different segments based on alignment
        font_path = [font_path]

    for i, position in enumerate(positions):
        context.move_to(*position)


        if i < len(font_path):
            context.select_font_face(font_path[i], cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        else:
            context.select_font_face(font_path[-1], cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)


        context.set_source_rgb(*color[i])
        context.show_text(str(text[i]))

    


def calculate_position(context, text, position, alignment):
    """
    Calculates position of text placement for
    different alignments.
    """
    extents = context.text_extents(text)
    text_width = extents.width
    text_height = extents.height

    text_height_without_below_line, descent, height, max_x_advance, max_y_advance = context.font_extents()
    
    x = position[0] - 1 # adjustment as it seemed to place it one pixel to the right (maybe should use -2?)
    if alignment[0] == 'm':
        x -= text_width / 2
    elif alignment[0] == 'r':
        x -= text_width

    y = position[1]
    if alignment[1] == 'm':
        y += text_height / 2
    elif alignment[1] == 't':
        y += text_height_without_below_line

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
'''def stats_text(text_elements):
    image_path = functions.get_random_background("utils/commands/stats/backgrounds")
    cairo_surface = cairo.ImageSurface.create_from_png(image_path)
    context = cairo.Context(cairo_surface)

    # Loop through each text element and add it to the context
    for text_info in text_elements:
        add_stats_text_element(text_info, context)

    return cairo_surface'''

def daily_leaderboard_text(text_elements):
    image_path = functions.get_random_background("utils/commands/leaderboards/daily_weapon_kills/backgrounds")
    cairo_surface = cairo.ImageSurface.create_from_png(image_path)
    context = cairo.Context(cairo_surface)

    # Loop through each text element and add it to the context
    for text_info in text_elements:
        add_text_element(text_info, context)

    return cairo_surface

# add text to imag
def add_text_to_image(text_elements, image_folder_path):
    image_path = functions.get_random_background(image_folder_path)
    cairo_surface = cairo.ImageSurface.create_from_png(image_path)
    context = cairo.Context(cairo_surface)

    # Loop through each text element and add it to the context
    for text_info in text_elements:
        add_text_element(text_info, context)

    return cairo_surface

def add_text_to_surface(cairo_surface, text_elements):
    """
    Used when already have a surface (not creating a new one)
    """
    context = cairo.Context(cairo_surface)

    for text_info in text_elements:
        add_text_element(text_info, context)

    return cairo_surface