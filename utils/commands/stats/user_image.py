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
        #(BOLD, [stats["squad"], f"{stats['nick']}"], (1140, RIGHT_Y_POSITION + 190), [(156/255, 156/255, 248/255), username_color], 38, "mm"),
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
        (BOLD, functions.format_large_number(stats["kills"]), (LEFT - (SIZE[0]/2) + 23, TOP_Y_POSITION), STAT_COLOR, STAT_SIZE, "lm"),
        (THIN, "Top ??%", (LEFT - (SIZE[0]/2) + 23, TOP_Y_POSITION + 45), PERCENTILE_COLOR, 30, "lm"),
        # DEATHS
        #(THIN, "Deaths:", (RIGHT - (SIZE[0]/2) + 23, TOP_Y_POSITION - 45), (1, 1, 1), STAT_SIZE, "lm"),
        (BOLD, functions.format_large_number(stats["deaths"]), (RIGHT - (SIZE[0]/2) + 23, TOP_Y_POSITION), STAT_COLOR, STAT_SIZE, "lm"),
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

    if stats["squad"] != "":
        text_elements.append((BOLD, [stats["squad"], f"{stats['nick']}"], (1140, RIGHT_Y_POSITION + 190), [(156/255, 156/255, 248/255), username_color], 38, "mm"))
    else:
        text_elements.append((BOLD, f"{stats['nick']}", (1140, RIGHT_Y_POSITION + 190), username_color, 38, "mm"))

    surface = cairo_functions.stats_text(text_elements)

    return functions.convert_to_discord(surface)