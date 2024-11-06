import cairo
import time
import math
from io import BytesIO

def calculate_kdr_changes(kills, deaths):
    kdr = kills/deaths
    rounded = round(kdr, 1)

    kills_needed = math.ceil(((rounded + 0.05) * deaths) - kills)

    deaths_avoid = math.floor((kills / (rounded - 0.05))) - deaths + 1

    return kills_needed, deaths_avoid

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

def add_text_element(text_info, context):
    font_path, text, position, color, font_size, alignment = text_info  # Unpack text information
    context.select_font_face(font_path, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    context.set_font_size(font_size)
    if not isinstance(text, list) or text[0] == "":
        if isinstance(text, list):
            text = text[1]
            context.set_source_rgba(*color[1])
        else:
            context.set_source_rgba(*color)
        
        # check if first item of list or just tuple
        '''if isinstance(color, list):
            context.set_source_rgba(*color[0])  # Set color in floats between 0-1
        else:
            context.set_source_rgba(*color)'''

        x, y = calculate_position(context, str(text), position, alignment)
        # Add the text
        context.move_to(x, y)
        context.show_text(str(text))
        context.fill()
    else:
        context.set_source_rgba(*color[0])  # Set color in floats between 0-1

        position1, position2 = calculate_two_positions(context, str(text[0]), str(text[1]), position)

        context.move_to(*position1)
        context.show_text(str(text[0]))

        context.set_source_rgb(*color[1])  # Set color in floats between 0-1


        context.move_to(*position2)
        context.show_text(str(text[1]))
        context.fill()

def calculate_position(context, text, position, alignment):
    extents = context.text_extents(text)
    text_width = extents.width
    text_height = extents.height
    
    x = position[0] - 1 # adjustment as it seemed to place it one pixel to the right (maybe should use -2)
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

def calculate_two_positions(context, text1, text2, position):
    space_width = 15 # looks nice

    text = f"{text1}{text2}"
    extents = context.text_extents(text)
    total_text_width = extents.width + space_width
    total_text_height = extents.height

    extents = context.text_extents(text1)
    text1_width = extents.width

    #space_width = 10.564 # calculated lol, only works for one size!!!!
    #center align
    middle_y = position[1]
    middle_y += total_text_height / 2

    return (position[0] - total_text_width/2, middle_y), (position[0] - total_text_width/2 + text1_width + space_width, middle_y)


# Function to add multiple pieces of text with Cairo
def text(text_elements):
    cairo_surface = cairo.ImageSurface.create_from_png("utils/commands/stats/3:4 size template.png")
    context = cairo.Context(cairo_surface)

    # Loop through each text element and add it to the context
    for text_info in text_elements:
        add_text_element(text_info, context)

    return cairo_surface

def create_stats_card(stats):
    start = time.time()
    kills_needed, deaths_to_avoid = calculate_kdr_changes(int(stats['kills'].replace(",","")), int(stats['deaths'].replace(",","")))
    # Define the text elements to add (text, position, color)
    if stats["steam"]:
        username_color = (245/255,179/255,62/255)
    else:
        username_color = (1,1,1)
    text_elements = [
        # NAME
        (BOLD, [stats["squad"], stats["nick"]], (1140, RIGHT_Y_POSITION + 225), [(156/255, 156/255, 248/255), username_color], 38, "mm"),
        (THIN, "Last seen 1 day ago", (1140, RIGHT_Y_POSITION + 263), (1, 1, 1), 38, "mm"),
        # KDR
        (BOLD, str(round(float(stats['kills / death']), 1)), (LEFT_TEXT, RIGHT_Y_POSITION + 323 + 45), (1, 1, 1), 41, "lm"),
        (THIN, "Top ??%", (RIGHT_TEXT, RIGHT_Y_POSITION + 323), (1, 1, 1), 30, "rm"),
        (THIN, f"{kills_needed} kills to advance", (LEFT_TEXT, RIGHT_Y_POSITION + 323 + 90), (1, 1, 1), 38, "lm"),
        (THIN, f"{deaths_to_avoid} deaths to avoid", (LEFT_TEXT, RIGHT_Y_POSITION + 323 + 128), (1, 1, 1), 38, "lm"),
        # KPM
        #(THIN, "Kills / Min", (LEFT_TEXT, RIGHT_Y_POSITION + 509), (1, 1, 1), 38, "lm"),
        (BOLD, str(round(float(stats['kills / min']), 1)), (LEFT_TEXT, RIGHT_Y_POSITION + 509 + 45), (1, 1, 1), 41, "lm"),
        (THIN, "Top ??%", (RIGHT_TEXT, RIGHT_Y_POSITION + 509), (1, 1, 1), 30, "rm"),
        # LEVEL
        (BOLD, f"Level {stats['level']}", (LEFT_TEXT, RIGHT_Y_POSITION + 615), (1, 1, 1), 41, "lm"),
        (THIN, f"Top {stats["xpPercentile"]}%", (RIGHT_TEXT, RIGHT_Y_POSITION + 615), (1, 1, 1), 30, "rm"),
        (THIN, f"{stats['progressPercentage']} to next level", (LEFT_TEXT, RIGHT_Y_POSITION + 615 + 38), (1, 1, 1), 38, "lm"),
        (THIN, f"XP: {format_large_number(stats['xp'])}", (LEFT_TEXT, RIGHT_Y_POSITION + 615 + 75), (1, 1, 1), 38, "lm"),

        # KILLS
        #(THIN, "Kills:", (LEFT - (SIZE[0]/2) + 23, TOP_Y_POSITION - 45), (1, 1, 1), 41, "lm"),
        (BOLD, stats["kills"], (LEFT - (SIZE[0]/2) + 23, TOP_Y_POSITION), (1, 1, 1), 41, "lm"),
        (THIN, "Top ??%", (LEFT - (SIZE[0]/2) + 23, TOP_Y_POSITION + 45), (1, 1, 1), 30, "lm"),
        # DEATHS
        #(THIN, "Deaths:", (RIGHT - (SIZE[0]/2) + 23, TOP_Y_POSITION - 45), (1, 1, 1), 41, "lm"),
        (BOLD, stats["deaths"], (RIGHT - (SIZE[0]/2) + 23, TOP_Y_POSITION), (1, 1, 1), 41, "lm"),
        (THIN, "Top ??%", (RIGHT - (SIZE[0]/2) + 23, TOP_Y_POSITION + 45), (1, 1, 1), 30, "lm"),
        # KILLS
        #(THIN, "Classic Wins:", (LEFT - (SIZE[0]/2) + 23, TOP_Y_POSITION + (SPACING + SIZE[1]) - 45), (1, 1, 1), 41, "lm"),
        (BOLD, stats["classic mode wins"], (LEFT - (SIZE[0]/2) + 23, TOP_Y_POSITION + (SPACING + SIZE[1])), (1, 1, 1), 41, "lm"),
        (THIN, "Top ??%", (LEFT - (SIZE[0]/2) + 23, TOP_Y_POSITION + (SPACING + SIZE[1]) + 45), (1, 1, 1), 30, "lm"),
        # KILLS
        #(THIN, "BR Wins:", (RIGHT - (SIZE[0]/2) + 23, TOP_Y_POSITION + (SPACING + SIZE[1])- 45), (1, 1, 1), 41, "lm"),
        (BOLD, stats["battle royale wins"], (RIGHT - (SIZE[0]/2) + 23, TOP_Y_POSITION + (SPACING + SIZE[1])), (1, 1, 1), 41, "lm"),
        (THIN, "Top ??%", (RIGHT - (SIZE[0]/2) + 23, TOP_Y_POSITION + (SPACING + SIZE[1]) + 45), (1, 1, 1), 30, "lm"),
        # KILLS
        #(THIN, "Kills ELO", (LEFT - (SIZE[0]/2) + 23, TOP_Y_POSITION + 2*(SPACING + SIZE[1]) - 45), (1, 1, 1), 41, "lm"),
        (BOLD, stats["killsELO"], (LEFT - (SIZE[0]/2) + 23, TOP_Y_POSITION + 2*(SPACING + SIZE[1])), (1, 1, 1), 41, "lm"),
        (THIN, "Top ??%", (LEFT - (SIZE[0]/2) + 23, TOP_Y_POSITION + 2*(SPACING + SIZE[1])+ 45), (1, 1, 1), 30, "lm"),
        # KILLS
        #(THIN, "Games ELO", (RIGHT - (SIZE[0]/2) + 23, TOP_Y_POSITION + 2*(SPACING + SIZE[1])- 45), (1, 1, 1), 41, "lm"),
        (BOLD, stats["gamesELO"], (RIGHT - (SIZE[0]/2) + 23, TOP_Y_POSITION + 2*(SPACING + SIZE[1])), (1, 1, 1), 41, "lm"),
        (THIN, "Top ??%", (RIGHT - (SIZE[0]/2) + 23, TOP_Y_POSITION + 2*(SPACING + SIZE[1])+ 45), (1, 1, 1), 30, "lm"),
    ]

    surface = text(text_elements)

    print(time.time() - start)

    return convert_to_discord(surface)