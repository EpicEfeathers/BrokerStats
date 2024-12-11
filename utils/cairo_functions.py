import cairo

from utils import functions

def add_text_element(text_info, context):
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
    else: # for multiple colors
        positions = calculate_multiple_positions(context, text, position, alignment) # calculated proper positions of different segments based on alignment

        for i, position in enumerate(positions):
            context.set_source_rgb(*color[i])
            context.move_to(*position)
            context.show_text(str(text[i]))

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

# Function to add multiple pieces of text with Cairo
def text(text_elements):
    image_path = functions.get_random_background("utils/commands/stats/backgrounds")
    cairo_surface = cairo.ImageSurface.create_from_png(image_path)
    context = cairo.Context(cairo_surface)

    # Loop through each text element and add it to the context
    for text_info in text_elements:
        add_text_element(text_info, context)

    return cairo_surface