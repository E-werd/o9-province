import cv2
import numpy as np

def blackout():

    # Load the image in color
    image = cv2.imread('sample/image.png', cv2.IMREAD_COLOR)

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
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Create a mask of green pixels
    mask = cv2.inRange(image, upper_green, upper_green)

    # Change all green (also near green) pixels to pink
    image[mask == 255] = [0, 0, 0] # Note that OpenCV uses BGR, not RGB
    # Display the image
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Create a mask of green pixels
    mask = cv2.inRange(image, lower_green, lower_green)

    # Change all green (also near green) pixels to pink
    image[mask == 255] = [0, 0, 0]  # Note that OpenCV uses BGR, not RGB


    # Create a mask of green pixels
    mask = cv2.inRange(image, upper_green, upper_green2)

    # Change all green (also near green) pixels to pink
    image[mask == 255] = [0, 0, 0]  # Note that OpenCV uses BGR, not RGB


    # Display the image
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Save the images
    cv2.imwrite('blackout.jpg', image)

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
    cv2.imwrite('No_Labels.jpg', image)
def remove_letters(image):
    # Define the color range for green
    dark_gray = np.array([20, 20, 20])  # use appropriate values
    dark_gray2 = np.array([40, 40, 40])  # use appropriate values

    # Create a mask of green pixels
    mask = cv2.inRange(image, dark_gray, dark_gray2)

    # Change all green (also near green) pixels to pink
    # image[mask == 255] = [180, 105, 255]  # Note that OpenCV uses BGR, not RGB
    image[mask == 255] = [0, 0, 0]  # Note that OpenCV uses BGR, not RGB

    # Create a mask of green pixels
    cv2.imwrite('No_Labels.jpg', image)


image = blackout()
remove_letters(image)