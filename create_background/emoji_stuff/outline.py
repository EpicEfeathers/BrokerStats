from PIL import Image, ImageFilter, ImageOps

def add_outline(image_path, outline_color=(255, 255, 255, 255), outline_size=3):
    # Open image and convert to RGBA
    img = Image.open(image_path).convert("RGBA")
    
    # Create an alpha mask (grayscale version of the transparency)
    alpha = img.split()[3]  # Get the alpha channel

    # Find edges in the alpha channel
    outline = alpha.filter(ImageFilter.FIND_EDGES)
    
    # Expand the outline by applying a dilation effect
    outline = outline.filter(ImageFilter.MaxFilter(outline_size))

    # Convert outline to solid color
    colored_outline = ImageOps.colorize(outline.convert("L"), black="black", white=outline_color[:3])
    colored_outline.putalpha(outline)  # Apply transparency

    # Create a new image with the outline
    outlined_img = Image.alpha_composite(colored_outline, img)

    return outlined_img

# Example usage
image_path = "/Users/elingrell/Documents/Useful/Coding/python/discord/Broker-Stats/create_background/emoji_stuff/old_emojis/shotgun.png"
outlined_img = add_outline(image_path, outline_color=(255, 255, 255, 255), outline_size=10)
outlined_img.save("/Users/elingrell/Documents/Useful/Coding/python/discord/Broker-Stats/create_background/emoji_stuff/outlined_emojis/shotgun.png")
outlined_img.show()
