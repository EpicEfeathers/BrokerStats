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

    #kills_needed, deaths_to_avoid = functions.calculate_kdr_changes(int(stats['kills'].replace(",","")), int(stats['deaths'].replace(",","")))
    kills_needed, deaths_to_avoid = functions.calculate_kdr_changes(stats['kills'], stats['deaths'])

    STAT_COLOR_WHITE = (1,1,1)
    PERCENTILE_COLOR = (0.75,0.75,0.75)

    username_color = (245/255,179/255,62/255) if stats.get("steam") else STAT_COLOR_WHITE

    STAT_SIZE = 41
    SUPPORTING_TEXT_SIZE = 34
    text_elements = [ # Adding each individual piece of text
        # CREATION DATE
        (BOLD, ["Created:", functions.uid_to_creation_date(stats["uid"])], (1140, RIGHT_Y_POSITION + 233), [PERCENTILE_COLOR, STAT_COLOR_WHITE], 30, "mm"),
        # KDR
        (BOLD, str(round(float(stats['kills / death']), 1)), (LEFT_TEXT, RIGHT_Y_POSITION + 323 + 45), STAT_COLOR_WHITE, STAT_SIZE, "lm"),
        (THIN, "Top ??%", (RIGHT_TEXT, RIGHT_Y_POSITION + 323), PERCENTILE_COLOR, 30, "rm"),
        (BOLD, [kills_needed, "kills to advance"], (LEFT_TEXT, RIGHT_Y_POSITION + 323 + 85), [(0,1,0), PERCENTILE_COLOR], SUPPORTING_TEXT_SIZE, "lm"),
        (BOLD, [deaths_to_avoid, "deaths to avoid"], (LEFT_TEXT, RIGHT_Y_POSITION + 323 + 118), [(1,60/250,60/250), PERCENTILE_COLOR], SUPPORTING_TEXT_SIZE, "lm"),
        # KPM
        (BOLD, str(round(float(stats['kills / min']), 1)), (LEFT_TEXT, RIGHT_Y_POSITION + 509 + 45), (1, 1, 1), STAT_SIZE, "lm"),
        (THIN, "Top ??%", (RIGHT_TEXT, RIGHT_Y_POSITION + 509), PERCENTILE_COLOR, 30, "rm"),
        # LEVEL
        (BOLD, f"Level {stats['level']}", (LEFT_TEXT, RIGHT_Y_POSITION + 615), (1, 1, 1), STAT_SIZE, "lm"),
        (THIN, f"Top {stats['xpPercentile']}%", (RIGHT_TEXT, RIGHT_Y_POSITION + 615), PERCENTILE_COLOR, 30, "rm"),
        (BOLD, ["Progress:", stats['progressPercentage']], (LEFT_TEXT, RIGHT_Y_POSITION + 615 + 39), [PERCENTILE_COLOR, STAT_COLOR_WHITE], SUPPORTING_TEXT_SIZE, "lm"),
        (BOLD, ["XP:", functions.format_large_number(stats['xp'])], (LEFT_TEXT, RIGHT_Y_POSITION + 615 + 80), [PERCENTILE_COLOR, STAT_COLOR_WHITE], SUPPORTING_TEXT_SIZE, "lm"),

        # KILLS
        (BOLD, functions.format_large_number(stats["kills"]), (LEFT - (SIZE[0]/2) + 23, TOP_Y_POSITION), STAT_COLOR_WHITE, STAT_SIZE, "lm"),
        (THIN, "Top ??%", (LEFT - (SIZE[0]/2) + 23, TOP_Y_POSITION + 45), PERCENTILE_COLOR, 30, "lm"),
        # DEATHS
        (BOLD, functions.format_large_number(stats["deaths"]), (RIGHT - (SIZE[0]/2) + 23, TOP_Y_POSITION), STAT_COLOR_WHITE, STAT_SIZE, "lm"),
        (THIN, "Top ??%", (RIGHT - (SIZE[0]/2) + 23, TOP_Y_POSITION + 45), PERCENTILE_COLOR, 30, "lm"),
        # CLASSIC WINS
        (BOLD, stats["classic mode wins"], (LEFT - (SIZE[0]/2) + 23, TOP_Y_POSITION + (SPACING + SIZE[1])), STAT_COLOR_WHITE, STAT_SIZE, "lm"),
        (THIN, "Top ??%", (LEFT - (SIZE[0]/2) + 23, TOP_Y_POSITION + (SPACING + SIZE[1]) + 45), PERCENTILE_COLOR, 30, "lm"),
        # BR WINS
        (BOLD, stats["battle royale wins"], (RIGHT - (SIZE[0]/2) + 23, TOP_Y_POSITION + (SPACING + SIZE[1])), STAT_COLOR_WHITE, STAT_SIZE, "lm"),
        (THIN, "Top ??%", (RIGHT - (SIZE[0]/2) + 23, TOP_Y_POSITION + (SPACING + SIZE[1]) + 45), PERCENTILE_COLOR, 30, "lm"),
        # KELO
        (BOLD, stats["killsELO"], (LEFT - (SIZE[0]/2) + 23, TOP_Y_POSITION + 2*(SPACING + SIZE[1])), STAT_COLOR_WHITE, STAT_SIZE, "lm"),
        (THIN, f"Top {stats['killsEloPercentile']}%", (LEFT - (SIZE[0]/2) + 23, TOP_Y_POSITION + 2*(SPACING + SIZE[1])+ 45), PERCENTILE_COLOR, 30, "lm"),
        # GELO
        (BOLD, stats["gamesELO"], (RIGHT - (SIZE[0]/2) + 23, TOP_Y_POSITION + 2*(SPACING + SIZE[1])), STAT_COLOR_WHITE, STAT_SIZE, "lm"),
        (THIN, f"Top {stats['gamesEloPercentile']}%", (RIGHT - (SIZE[0]/2) + 23, TOP_Y_POSITION + 2*(SPACING + SIZE[1])+ 45), PERCENTILE_COLOR, 30, "lm"),
    ]
    # add name
    if stats["squad"] != "": # if player part of squad
        cairo_functions.calculate_length(BOLD, 38, f"{stats['squad']} {stats['nick']}")
        text_elements.append((BOLD, [f"[{stats["squad"]}]", f"{stats['nick']}"], (1140, RIGHT_Y_POSITION + 190), [(156/255, 156/255, 248/255), username_color], 38, "mm"))
    else:
        text_elements.append((BOLD, f"{stats['nick']}", (1140, RIGHT_Y_POSITION + 190), username_color, 38, "mm"))

    time_since_last_seen = functions.time_since_last_seen(stats["time"])

    if time_since_last_seen != "Online now":
        text_elements.append((BOLD, ["Last seen", functions.time_since_last_seen(stats["time"])], (1140, RIGHT_Y_POSITION + 271), [PERCENTILE_COLOR, STAT_COLOR_WHITE], 38, "mm")), # old_y = 263)
    else:
        text_elements.append((BOLD, functions.time_since_last_seen(stats["time"]), (1140, RIGHT_Y_POSITION + 271), STAT_COLOR_WHITE, 38, "mm")), # old_y = 263

    surface = cairo_functions.add_text_to_image(text_elements, "utils/commands/stats/backgrounds")

    return functions.convert_to_discord(surface)