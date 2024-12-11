import cairo

from utils import functions, cairo_functions

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

'''def add_text_element(text_info, context):
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

    return cairo_surface'''

def create_stats_card(stats):
    """
    Main function to write info to stats card
    """

    kills_needed, deaths_to_avoid = functions.calculate_kdr_changes(int(stats['kills'].replace(",","")), int(stats['deaths'].replace(",","")))

    username_color = (245/255,179/255,62/255) if stats.get("steam") else (1,1,1)

    STAT_COLOR = (1,1,1)
    PERCENTILE_COLOR = (0.75,0.75,0.75)

    STAT_SIZE = 41
    SUPPORTING_TEXT_SIZE = 34
    text_elements = [ # Adding each individual piece of text
        # NAME
        #(BOLD, [stats["squad"], f"{stats["nick"]}"], (1140, RIGHT_Y_POSITION + 225), [(156/255, 156/255, 248/255), username_color], 38, "mm"),
        (BOLD, [stats["squad"], f"{stats['nick']}"], (1140, RIGHT_Y_POSITION + 190), [(156/255, 156/255, 248/255), username_color], 38, "mm"),
        (THIN, ["Created:", functions.uid_to_creation_date(stats["uid"])], (1140, RIGHT_Y_POSITION + 228), [PERCENTILE_COLOR, (1,1,1)], 30, "mm"),
        (THIN, functions.time_since_last_seen(stats["time"]), (1140, RIGHT_Y_POSITION + 260), STAT_COLOR, 38, "mm"), # old_y = 263
        # KDR
        (BOLD, str(round(float(stats['kills / death']), 1)), (LEFT_TEXT, RIGHT_Y_POSITION + 323 + 45), STAT_COLOR, STAT_SIZE, "lm"),
        (THIN, "Top ??%", (RIGHT_TEXT, RIGHT_Y_POSITION + 323), PERCENTILE_COLOR, 30, "rm"),
        #(THIN, f"{kills_needed} kills to advance", (LEFT_TEXT, RIGHT_Y_POSITION + 323 + 85), PERCENTILE_COLOR, SUPPORTING_TEXT_SIZE, "lm"),
        (THIN, [kills_needed, "kills to advance"], (LEFT_TEXT, RIGHT_Y_POSITION + 323 + 85), [(0,1,0), PERCENTILE_COLOR], SUPPORTING_TEXT_SIZE, "lm"),
        (THIN, [deaths_to_avoid, "deaths to avoid"], (LEFT_TEXT, RIGHT_Y_POSITION + 323 + 118), [(1,60/250,60/250), PERCENTILE_COLOR], SUPPORTING_TEXT_SIZE, "lm"),
        #(THIN, f"{deaths_to_avoid} deaths to avoid", (LEFT_TEXT, RIGHT_Y_POSITION + 323 + 118), PERCENTILE_COLOR, SUPPORTING_TEXT_SIZE, "lm"),
        # KPM
        #(THIN, "Kills / Min", (LEFT_TEXT, RIGHT_Y_POSITION + 509), (1, 1, 1), 38, "lm"),
        (BOLD, str(round(float(stats['kills / min']), 1)), (LEFT_TEXT, RIGHT_Y_POSITION + 509 + 45), (1, 1, 1), STAT_SIZE, "lm"),
        (THIN, "Top ??%", (RIGHT_TEXT, RIGHT_Y_POSITION + 509), PERCENTILE_COLOR, 30, "rm"),
        # LEVEL
        (BOLD, f"Level {stats['level']}", (LEFT_TEXT, RIGHT_Y_POSITION + 615), (1, 1, 1), STAT_SIZE, "lm"),
        (THIN, f"Top {stats['xpPercentile']}%", (RIGHT_TEXT, RIGHT_Y_POSITION + 615), PERCENTILE_COLOR, 30, "rm"),
        #(THIN, f"{stats['progressPercentage']} to next level", (LEFT_TEXT, RIGHT_Y_POSITION + 615 + 39), PERCENTILE_COLOR, SUPPORTING_TEXT_SIZE, "lm"),
        (THIN, [stats['progressPercentage'], "to next level"], (LEFT_TEXT, RIGHT_Y_POSITION + 615 + 39), [(1,1,1), PERCENTILE_COLOR], SUPPORTING_TEXT_SIZE, "lm"),
        (THIN, ["XP:", functions.format_large_number(stats['xp'])], (LEFT_TEXT, RIGHT_Y_POSITION + 615 + 75), [PERCENTILE_COLOR, (1,1,1)], SUPPORTING_TEXT_SIZE, "lm"),

        # KILLS
        #(THIN, "Kills:", (LEFT - (SIZE[0]/2) + 23, TOP_Y_POSITION - 45), (1, 1, 1), STAT_SIZE, "lm"),
        (BOLD, stats["kills"], (LEFT - (SIZE[0]/2) + 23, TOP_Y_POSITION), STAT_COLOR, STAT_SIZE, "lm"),
        (THIN, "Top ??%", (LEFT - (SIZE[0]/2) + 23, TOP_Y_POSITION + 45), PERCENTILE_COLOR, 30, "lm"),
        # DEATHS
        #(THIN, "Deaths:", (RIGHT - (SIZE[0]/2) + 23, TOP_Y_POSITION - 45), (1, 1, 1), STAT_SIZE, "lm"),
        (BOLD, stats["deaths"], (RIGHT - (SIZE[0]/2) + 23, TOP_Y_POSITION), STAT_COLOR, STAT_SIZE, "lm"),
        (THIN, "Top ??%", (RIGHT - (SIZE[0]/2) + 23, TOP_Y_POSITION + 45), PERCENTILE_COLOR, 30, "lm"),
        # KILLS
        #(THIN, "Classic Wins:", (LEFT - (SIZE[0]/2) + 23, TOP_Y_POSITION + (SPACING + SIZE[1]) - 45), (1, 1, 1), STAT_SIZE, "lm"),
        (BOLD, stats["classic mode wins"], (LEFT - (SIZE[0]/2) + 23, TOP_Y_POSITION + (SPACING + SIZE[1])), STAT_COLOR, STAT_SIZE, "lm"),
        (THIN, "Top ??%", (LEFT - (SIZE[0]/2) + 23, TOP_Y_POSITION + (SPACING + SIZE[1]) + 45), PERCENTILE_COLOR, 30, "lm"),
        # KILLS
        #(THIN, "BR Wins:", (RIGHT - (SIZE[0]/2) + 23, TOP_Y_POSITION + (SPACING + SIZE[1])- 45), (1, 1, 1), STAT_SIZE, "lm"),
        (BOLD, stats["battle royale wins"], (RIGHT - (SIZE[0]/2) + 23, TOP_Y_POSITION + (SPACING + SIZE[1])), STAT_COLOR, STAT_SIZE, "lm"),
        (THIN, "Top ??%", (RIGHT - (SIZE[0]/2) + 23, TOP_Y_POSITION + (SPACING + SIZE[1]) + 45), PERCENTILE_COLOR, 30, "lm"),
        # KILLS
        #(THIN, "Kills ELO", (LEFT - (SIZE[0]/2) + 23, TOP_Y_POSITION + 2*(SPACING + SIZE[1]) - 45), (1, 1, 1), STAT_SIZE, "lm"),
        (BOLD, stats["killsELO"], (LEFT - (SIZE[0]/2) + 23, TOP_Y_POSITION + 2*(SPACING + SIZE[1])), STAT_COLOR, STAT_SIZE, "lm"),
        (THIN, f"Top {stats['killsEloPercentile']}%", (LEFT - (SIZE[0]/2) + 23, TOP_Y_POSITION + 2*(SPACING + SIZE[1])+ 45), PERCENTILE_COLOR, 30, "lm"),
        # KILLS
        #(THIN, "Games ELO", (RIGHT - (SIZE[0]/2) + 23, TOP_Y_POSITION + 2*(SPACING + SIZE[1])- 45), (1, 1, 1), STAT_SIZE, "lm"),
        (BOLD, stats["gamesELO"], (RIGHT - (SIZE[0]/2) + 23, TOP_Y_POSITION + 2*(SPACING + SIZE[1])), STAT_COLOR, STAT_SIZE, "lm"),
        (THIN, f"Top {stats['gamesEloPercentile']}%", (RIGHT - (SIZE[0]/2) + 23, TOP_Y_POSITION + 2*(SPACING + SIZE[1])+ 45), PERCENTILE_COLOR, 30, "lm"),
    ]

    surface = cairo_functions.text(text_elements)

    return functions.convert_to_discord(surface)