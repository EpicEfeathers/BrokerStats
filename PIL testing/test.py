from PIL import Image, ImageDraw, ImageFont

def create_rounded_rectangle_antialiased(image, size, corner_radius, color, position, scale_factor=3):
    width, height = size
    scaled_size = (width * scale_factor, height * scale_factor)
    scaled_radius = corner_radius * scale_factor
    
    # Create a scaled-up image
    rectangle = Image.new('RGBA', scaled_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(rectangle)
    
    # Draw the rounded rectangle on the scaled image
    draw.rounded_rectangle(
        [(0, 0), scaled_size],  # coordinates for the rectangle
        radius=scaled_radius,    # corner radius scaled
        fill=color               # fill color for the rectangle
    )
    
    # Downscale the image to the target size to apply anti-aliasing
    rounded_rectangle = rectangle.resize(size, Image.LANCZOS)
    
    image.paste(rounded_rectangle, position, rounded_rectangle)


im = Image.open("images/blurred_background.png")
width, height = im.size
middle_width = int((width - 1000)/2)


# Example usage:
size = (1000, 200)
corner_radius = 50
color = (0, 0, 0, 230)
position = (middle_width, 75) #centers horizontally

rounded_rectangle = create_rounded_rectangle_antialiased(im, size, corner_radius, color, position)

text = 'EpicEfeathers'

def centred_text(image, text, font_size, color, position):
    draw = ImageDraw.Draw(im)

    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", font_size)

    # drawing text size 
    bbox = draw.textbbox((0,0), text, font=font)

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = position[0] - text_width/2
    y = position[1] - text_height/2

    draw.text((x,y), text, fill=color, font_size=font_size, font=font)  

centred_text(im, text, 50, (255,255,255), (middle_width, 75))
im.show()