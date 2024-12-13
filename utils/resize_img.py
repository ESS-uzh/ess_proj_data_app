from PIL import Image
import os
from glob import glob


INPUT_PATH = "/home/diego/work/projects/ess_proj_data_map/test"
OUTPUT_PATH = "../topics_resized"


# Function to downsize an image
def downsize_image(input_path, output_path, max_width, max_height):
    with Image.open(input_path) as img:
        # Maintain aspect ratio
        img.thumbnail((max_width, max_height), Image.LANCZOS)
        img.save(output_path, format="PNG", optimize=True)
        print(f"Image saved to {output_path}")


project_files = (
    glob(os.path.join(INPUT_PATH, "*.png"))
    + glob(os.path.join(INPUT_PATH, "*.jpeg"))
    + glob(os.path.join(INPUT_PATH, "*.jpg"))
)


for f in project_files:
    fname = os.path.basename(f).split(".")[0]
    downsize_image(f, os.path.join(OUTPUT_PATH, fname), max_width=242, max_height=152)
