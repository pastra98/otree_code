import sys
from PIL import Image, ImageDraw

def create_checkerboard_pattern(image, level):
    """
    Creates a checkerboard pattern on the image based on the level.
    """
    width, height = image.size
    tile_size = width // 12
    draw = ImageDraw.Draw(image)
    
    for i in range(0, width, tile_size):
        for j in range(0, height, tile_size):
            if level == 1 or level == 5:
                draw.rectangle([i, j, i + tile_size, j + tile_size], fill='black')
            elif level == 2:
                if (i // tile_size + j // tile_size) % 2 == 0 or (i // tile_size) % 2 == 0:
                    draw.rectangle([i, j, i + tile_size, j + tile_size], fill='black')
            elif level == 3:
                if (i // tile_size + j // tile_size) % 2 == 0:
                    draw.rectangle([i, j, i + tile_size, j + tile_size], fill='black')
            elif level == 4:
                if (i // tile_size + j // tile_size) % 2 != 0 and (i // tile_size) % 2 != 0:
                    draw.rectangle([i, j, i + tile_size, j + tile_size], fill='black')

    return image

def process_image(image_path):
    """
    Processes the image at the given path and creates 5 new images with different checkerboard patterns.
    """
    try:
        original = Image.open(image_path)
    except IOError:
        print("Error: Unable to open image file.")
        return

    if original.width != original.height:
        print("Error: Image is not square.")
        return

    for level in range(1, 6):
        if level == 1:
            # Create a completely black image
            img = Image.new('RGB', original.size, 'black')
        elif level == 5:
            # Level 5: Original image without any overlay
            img = original.copy()
        else:
            img = original.copy()
            img = create_checkerboard_pattern(img, level)

        base_name = image_path.rsplit('.', 1)[0]
        new_image_name = f"{base_name}{level}.jpg"
        img.save(new_image_name, 'JPEG')
        print(f"Image saved as {new_image_name}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_image>")
    else:
        process_image(sys.argv[1])
