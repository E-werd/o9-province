from PIL import Image
import numpy as np
from scipy.ndimage import measurements

def flood_fill(input_image_path, output_image_path, seed_point, new_color):
    # Open image and convert to RGB
    image = Image.open(input_image_path).convert("RGB")

    # Convert image data to numpy array
    img_array = np.array(image)

    # Get color at the seed_point
    seed_color = img_array[seed_point[1], seed_point[0]]

    # Generate a binary image (mask) where pixels with the seed color are white
    mask = np.all(img_array == seed_color, axis=-1)

    # Label all connected regions in the mask
    labeled_array, num_features = measurements.label(mask)

    # Get label of the region where seed_point is located
    seed_label = labeled_array[seed_point[1], seed_point[0]]

    # Create a new mask with only the selected region
    new_mask = (labeled_array == seed_label)

    # Generate a new image, replacing the selected region color
    new_img_array = img_array.copy()
    new_img_array[new_mask] = new_color

    # Convert array to image
    new_image = Image.fromarray(np.uint8(new_img_array))

    # Save the output image
    new_image.save(output_image_path)



# x = 900
# y = 200
# # Usage example
# flood_fill('image.png', 'colored_world_map.png', (x, y), (255, 0, 0))  # RGB for red