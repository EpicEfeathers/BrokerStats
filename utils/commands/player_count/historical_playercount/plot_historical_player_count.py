import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for saving the figure without a GUI

import matplotlib.pyplot as plt
import matplotlib as mpl
from utils import functions

# plot settings
mpl.rcParams.update({ # various settings
        'xtick.color': "white",
        'ytick.color': "white",
        'axes.labelcolor': "white",
    }) 

def return_image(region, playercount, timestamps, title):
    '''
    Creates plot from historical data, overlaying it on a background image.
    '''

    image = plt.imread('tests/blurred_images/space_station.png')  # Load the background image


    # Create a figure
    width = 8
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(width, width * image.shape[0] / image.shape[1]))
    ax.patch.set_alpha(0.7) # make plot background semi-transparent

    background_ax = plt.axes([0, 0, 1, 1])  # Cover the entire figure
    background_ax.set_zorder(-1)  # Make sure background goes behind plot
    background_ax.imshow(image, aspect='auto')  # Show the background image

    # Plot the bar chart data on top of the background image
    ax.plot(playercount, linestyle="-", marker="o", markersize=4) 

    tick_positions = list(range(0, 49, 4))  # Every 4th step in a 48-point dataset aligns with every 2-hour step. 49 so there is one extra (for the "now" datapoint)

    # Apply x-ticks
    ax.set_xticks(ticks=tick_positions, labels=timestamps, rotation=30, ha="right")

    ax.grid(axis='y', linestyle='--', alpha=0.3, color="black")
    #ax.barh(server_names, player_count, color=(1,0.235,0.016))

    #ax.set_xlabel("Time")
    #ax.set_ylabel(f"{region.capitalize()} playercount")

    ax.set_title(f"{title} playercount - Last 24 Hours", color="white")


    plt.subplots_adjust(top=0.9, bottom=0.15)

    for spine in plt.gca().spines.values(): # removes annoying black outline around image
        spine.set_visible(False)

    image = functions.convert_plot_to_discord(plt)
    plt.close()

    return image