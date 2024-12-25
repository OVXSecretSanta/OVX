import os
from PIL import Image

def process_image(input_path, output_path, default_path, corner_radius=17):
    try:
        # Open the main image and the default image
        img = Image.open(input_path).convert("RGBA")
        default_img = Image.open(default_path).convert("RGBA")

        width, height = img.size
        pixels = img.load()  # Access pixel data
        default_pixels = default_img.load()  # Reference pixel data

        # Corner positions to check
        corner_positions = {
            "top_left": (0, 17),
            "top_right": (17, 0),
            "bottom_left": (16, 505),
            "bottom_right": (357, 505)
        }

        # Check if corner positions are within bounds
        for corner, (cx, cy) in corner_positions.items():
            if cx >= width or cy >= height:
                print(f"Skipping {input_path}: Corner position {corner} is out of bounds.")
                return  # Skip processing if any corner is out of bounds

        # Determine if black coating should be applied for each corner
        apply_black_coating = {}
        for corner, (cx, cy) in corner_positions.items():
            r, g, b, _ = pixels[cx, cy]
            apply_black_coating[corner] = (r == 0 and g == 0 and b == 0)

        # Create a new image for the output with an alpha channel
        new_img = Image.new("RGBA", (width, height))
        new_pixels = new_img.load()

        for y in range(height):
            for x in range(width):
                r, g, b, a = pixels[x, y]
                dr, dg, db, _ = default_pixels[x, y]

                # Calculate the grayscale brightness of the pixel
                brightness = (dr + dg + db) // 3  # Average of RGB values from default.png

                # Determine if the pixel is in one of the corners
                if x < corner_radius and y < corner_radius:
                    distance = max(x, y)  # Top-left corner
                    corner_key = "top_left"
                elif x >= width - corner_radius and y < corner_radius:
                    distance = max(width - x - 1, y)  # Top-right corner
                    corner_key = "top_right"
                elif x < corner_radius and y >= height - corner_radius:
                    distance = max(x, height - y - 1)  # Bottom-left corner
                    corner_key = "bottom_left"
                elif x >= width - corner_radius and y >= height - corner_radius:
                    distance = max(width - x - 1, height - y - 1)  # Bottom-right corner
                    corner_key = "bottom_right"
                else:
                    distance = None  # Pixel is not in a corner
                    corner_key = None

                if distance is not None and distance < corner_radius:
                    # Apply transparency based on brightness
                    transparency = int((brightness / 255) * 255)
                    if apply_black_coating.get(corner_key, False):
                        # Black with calculated transparency
                        new_pixels[x, y] = (0, 0, 0, 255 - transparency)
                    else:
                        # Retain original color with adjusted transparency
                        new_pixels[x, y] = (r, g, b, 255 - transparency)
                else:
                    # Preserve original pixel
                    new_pixels[x, y] = pixels[x, y]

        # Save the processed image
        new_img.save(output_path, "PNG")
    
    except Exception as e:
        print(f"Error processing {input_path}: {e}")

def batch_process_images(input_folder, output_folder, default_path, corner_radius=17):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    for file_name in os.listdir(input_folder):
        if file_name.endswith(".png") and file_name != "default.png":
            input_path = os.path.join(input_folder, file_name)
            output_path = os.path.join(output_folder, file_name)

            print(f"Processing {file_name}...")
            process_image(input_path, output_path, default_path, corner_radius)

    print("Batch processing complete.")
    
# Paths for input and output folders
input_folder = "C:/Users/Epid/Documents/GitHub/OVX/img/cards"
output_folder = "C:/Users/Epid/Documents/GitHub/OVX/img/cards-cropped"
default_path = os.path.join(input_folder, "default.png")

batch_process_images(input_folder, output_folder, default_path)