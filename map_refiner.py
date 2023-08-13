# This works but it is not pretty
# It's also a little stupid
# I'm so sorry


import cv2
import numpy as np
from tkinter import Tk, Label, Entry, Button
from PIL import Image, ImageTk
import json
import os

# Assuming dark, mid, and lite are defined as:
dark = [0,76,0,255]
mid = [0, 127, 0, 255]
lite = [0, 178, 0, 255]

def blackout():
    """This takes the default map and turns it into black with gray lettering"""
    # Load the image in color
    image = cv2.imread('THC/map_original.png', cv2.IMREAD_COLOR)
    # Define the color range for green
    mid_green = np.array([0, 127, 0])  # use appropriate values
    lower_green = np.array([0, 76, 0])  # use appropriate values
    upper_green = np.array([0, 170, 0])  # use appropriate values
    upper_green2 = np.array([11, 182, 11])  # use appropriate values
    # Create a mask of green pixels
    mask = cv2.inRange(image, mid_green, mid_green)
    # Change all green (also near green) pixels to pink
    image[mask == 255] = [0, 0, 0]  # Note that OpenCV uses BGR, not RGB
    # Display the image
    # Create a mask of green pixels
    mask = cv2.inRange(image, upper_green, upper_green)
    # Change all green (also near green) pixels to pink
    image[mask == 255] = [0, 0, 0] # Note that OpenCV uses BGR, not RGB
    # Display the image
    # Create a mask of green pixels
    mask = cv2.inRange(image, lower_green, lower_green)
    # Change all green (also near green) pixels to pink
    image[mask == 255] = [0, 0, 0]  # Note that OpenCV uses BGR, not RGB
    # Create a mask of green pixels
    mask = cv2.inRange(image, upper_green, upper_green2)
    # Change all green (also near green) pixels to pink
    image[mask == 255] = [0, 0, 0]  # Note that OpenCV uses BGR, not RGB
    # Display the image
    # Save the images
    cv2.imwrite('Map_TMP_Blackout.jpg', image)
    return image

def pink_letters(image):
    # Define the color range for green
    dark_gray = np.array([20, 20, 20])  # use appropriate values
    dark_gray2 = np.array([50, 50, 50])  # use appropriate values

    # Create a mask of green pixels
    mask = cv2.inRange(image, dark_gray, dark_gray2)

    # Change all green (also near green) pixels to pink
    image[mask == 255] = [180, 105, 255]  # Note that OpenCV uses BGR, not RGB
    # image[mask == 255] = [0, 0, 0]  # Note that OpenCV uses BGR, not RGB

    # Create a mask of green pixels
    cv2.imwrite('Pink_Letters.jpg', image)

    return image



# Check the distance between two points
def distance(pt1, pt2):
    return int(((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)**0.5)


def filter_coords(coords):
    # Filter out the coordinates that are duplicates or super close
    filtered_coords = []
    dead = []
    for pt in coords:
        close = False
        for fpt in filtered_coords:
            # Check if the point is a duplicate or within the threshold
            if pt == fpt or distance(pt, fpt) <= 22:
                close = True
                break
        if not close:
            filtered_coords.append(pt)
        else:
            dead.append(pt)
    return filtered_coords


def get_letter_coordinates(image):
    """
    Reads the blackout map and gets the location of all the words
    This might need the pink map...
    """
    # Needs a black and white map
    # img_path2 = 'THC/Map_TMP_Blackout.jpg'
    # image = cv2.imread(img_path2)
    # Convert image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        # Define range for pink color in HSV
    lower_pink = np.array([150, 50, 50])  # These values may need adjustments
    upper_pink = np.array([170, 255, 255])  # These values may need adjustments
    # Threshold the HSV image to get only pink colors
    mask = cv2.inRange(hsv, lower_pink, upper_pink)
    # Morphological operations to remove noise and join parts of the letters
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    centroids = []
        # For each contour, find the centroid
    for contour in contours:
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
        else:
            cx, cy = 0, 0
        centroids.append((cx, cy))
    log = []

    for center in centroids:
        # cv2.circle(image, center, 3, (0, 255, 0), -1)
        log.append(center)

    clean_coords = filter_coords(log)

    with open('THC/territory_coords.json', 'w') as file:
        data = json.dumps(clean_coords)
        file.write(data)
    return log



def find_nearest_color(coord, image_data, width, height):
    for y_offset in range(-2, 3):
        for x_offset in range(-2, 3):
            x, y = coord[0] + x_offset, coord[1] + y_offset
            if x < 0 or y < 0 or x >= width or y >= height:
                continue
            tmplst = list(image_data[x, y])
            print(tmplst)

            if tmplst == dark:
                return "3"
            elif tmplst == mid:
                return "2"
            elif tmplst == lite:
                return "1"
            # Add conditions for 'lite' or any other colors here

def get_territory_colors(all_coordinates):
    img_path = 'sample_data/image.png'
    image = Image.open(img_path)
    width, height = image.size
    image_data = image.load()
    all_data = {}
    for entry in all_coordinates:
        coord = all_coordinates[entry]
        all_data[entry] = {
            'coordinates': coord
        }
        newColor = find_nearest_color(coord, image_data, width, height)
        all_data[entry]['value'] = newColor

    with open('map_data_master.json', 'w') as file:
        data = json.dumps(all_data)
        file.write(data)


def remove_black_text(image_path, output_path):
    # Read the image
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)

    # Define the target color
    target = [28, 28, 28]

    # Create a binary mask where black pixels are set to 255 and all other pixels to 0
    mask = np.all(img == target, axis=-1).astype(np.uint8) * 255

    # Use the inpainting function
    inpainted = cv2.inpaint(img, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)

    # Save the inpainted image
    cv2.imwrite(output_path, inpainted)


def show_point(image_path, points):
    root = Tk()
    image = Image.open(image_path)
    photo = ImageTk.PhotoImage(image)
    label = Label(root, image=photo)
    label.pack()
    entry = Entry(root)
    def on_submit(event=None):  # The event parameter is optional, to handle both button and Enter key presses
        root.quit()
    button = Button(root, text="Submit", command=root.quit)
    def ask_name(point):
        x, y = point
        crop_size = 50
        left = x - crop_size
        right = x + crop_size
        top = y - crop_size
        bottom = y + crop_size
        cropped = image.crop((left, top, right, bottom))
        cropped_photo = ImageTk.PhotoImage(cropped)
        label.config(image=cropped_photo)
        entry.pack()
        button.pack()
        entry.bind('<Return>', on_submit)
        root.mainloop()
        name = entry.get()
        entry.delete(0, 'end')
        label.config(image=photo)
        entry.pack_forget()
        button.pack_forget()
        return name
    names = {}
    for point in points:
        name = ask_name(point)
        names[name] = point
        print(names)
    root.destroy()
    return names


def labeler(filtered_coords):
    image_path = "sample_data/image.png"
    result = show_point(image_path, filtered_coords)

    # Write the names of the countries and their coordinates to a file
    with open('territory_names.json', 'w') as file:
        data = json.dumps(result)
        file.write(data)
        file.close()

    return result



# Make everything the same color, not sure if this is necessery
img = blackout()

# Make the letters pink for some reason, ditto on necesseryness, I was hammered I'm sorry
img = pink_letters(img)

# Get all the coordinates where Python can see pink text, AKA get the center of each territory
all_coordinates = get_letter_coordinates(img)

# Extremely tedious manual process of typing the names in for each province, but this makes it a little less painful
if os.path.exists('THC/names.json'):
    with open('THC/names.json','r') as file:
        data = file.read()
        names_and_coords = json.loads(data)
else:
    names_and_coords = labeler(all_coordinates)

print(names_and_coords)
# Grabs the color of each territory and associates it with the coordinates
get_territory_colors(names_and_coords)

# Removes the labels from the map so that the territories are completely green
remove_black_text('sample_data/image.png', 'image_no_names.png')
