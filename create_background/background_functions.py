from PIL import Image, ImageDraw, ImageFont

FONT_PATH = "HelveticaNeue.ttc"

def draw_text(im, text, color, position, font_size, index, anchor):
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(FONT_PATH, font_size, index=index)
    draw.text(position, str(text), font=font, fill=color,anchor=anchor)

def text_bold(im, text, color, position, font_size, anchor):
    draw_text(im, text, color, position, font_size, 10, anchor=anchor)

def text(im, text, color, position, font_size, anchor):
    draw_text(im, text, color, position, font_size, 0, anchor=anchor)

def text_narrow(im, text, color, position, font_size, anchor):
    draw_text(im, text, color, position, font_size, 7, anchor=anchor)

def create_rounded_rectangle(image, size, corner_radius, color, position, scale_factor=3):
    width, height = size
    scaled_size = (width * scale_factor, height * scale_factor)
    scaled_radius = corner_radius * scale_factor

    # centre on position, rather than top left
    position = int(position[0] - width/2), int(position[1] - height/2)

    # Create a scaled-up image
    rectangle = Image.new('RGBA', scaled_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(rectangle)

    # Draw the rounded rectangle on the scaled image
    draw.rounded_rectangle(
        [(0, 0), scaled_size],
        radius=scaled_radius,
        fill=color
    )

    # Downscale the image to the target size to apply anti-aliasing
    rounded_rectangle = rectangle.resize(size, Image.LANCZOS)
    image.paste(rounded_rectangle, position, rounded_rectangle)