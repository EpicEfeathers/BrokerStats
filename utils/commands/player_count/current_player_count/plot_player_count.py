import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for saving the figure without a GUI

import matplotlib.pyplot as plt
import matplotlib as mpl
from utils import functions

def return_image(data):
    '''
    Creates plot from image and overlays the player count bar chart.
    '''

    image = plt.imread('tests/blurred_images/space_station.png')  # Load the background image

    mpl.rcParams.update({ # various settings
        'xtick.color': "white",
        'ytick.color': "white",
        'axes.labelcolor': "white",
    }) 

    # Extract server names and player counts from the data
    server_names = [server["server_name"].replace("_", " ") for server in data]  # e.g., USA_4V4 -> USA 4V4
    player_count = [server["player_count"] for server in data]

    # Create a figure
    width = 8
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(width, width * image.shape[0] / image.shape[1]))
    ax.patch.set_alpha(0.7) # make plot background semi-transparent

    background_ax = plt.axes([0, 0, 1, 1])  # Cover the entire figure
    background_ax.set_zorder(-1)  # Make sure background goes behind plot
    background_ax.imshow(image, aspect='auto')  # Show the background image

    # Plot the bar chart data on top of the background image
    ax.barh(server_names, player_count, color=(1,0.235,0.016))

    max_value = max(player_count)
    ax.set_xlim(0, max_value + (max_value / 12.5))  # Adds padding so exact player count doesn't go off screen
    
    for index, value in enumerate(player_count): # Add player count numbers next to each bar
        ax.text(value + 0.5, index, str(value), color='black', fontsize=12, ha='left', va='center')

    # Set the title for the plot
    ax.set_title("Player Count By Server", color="white")

    plt.subplots_adjust(left=0.2, right=0.9, top=0.92, bottom=0.08)

    for spine in plt.gca().spines.values(): # removes annoying black outline around image
        spine.set_visible(False)


    image = functions.convert_plot_to_discord(plt)
    plt.close()

    return image