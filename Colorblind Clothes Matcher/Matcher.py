from rembg import remove
from PIL import Image
import cv2
import numpy as np
import heapq
global input_image
#Saves new image and strips background for easier handling
def saveClothing():
    # Path to the image file
    input_path = "Colorblind Clothes Matcher/decalShirt.jpg"
    tempClothing = "/Users/alexandermcgreevy/Documents/GitHub/Projects-Clone/Colorblind Clothes Matcher/Clothing.png"

    # Open and process the image
    with open(input_path, "rb+") as inp_file:
        input_image = inp_file.read()
        output_image = remove(input_image)
        out_file.write(output_image)

    # Save the output
    with open(tempClothing, "wb") as out_file:
        out_file.write(output_image)

    print("Background removed and saved to:", tempClothing)
    


# Function to get the top 3 intensity values
def get_top_colors(hist):
    # Flatten histogram and find the top 3 intensities found in the image
    top_values = heapq.nlargest(3, enumerate(hist.flatten()), key=lambda x: x[1])
    return [(index, int(value)) for index, value in top_values]


def clothingColor(top_blue, top_green, top_red):
    # Get the average of the top 3 intensity values for each channel
    blue = sum([top_blue[i][0] for i in range(3)]) // 3
    green = sum([top_green[i][0] for i in range(3)]) // 3
    red = sum([top_red[i][0] for i in range(3)]) // 3

    # Currently return the average color intensities(Fix it to ignore black and choose the next highest intensity)
    return red, green, blue

    
    

def findColor(red, green, blue):
    color_ranges = {
    'Red': [[50, 0, 0], [255, 75, 75]],
    'Red-orange': [[75, 25, 0], [255, 100, 75]],
    'Orange': [[100, 50, 0], [255, 165, 75]],
    'Yellow-orange': [[150, 100, 0], [255, 200, 75]],
    'Yellow': [[150, 150, 0], [255, 255, 75]],
    'Yellow-green': [[100, 150, 0], [200, 255, 75]],
    'Green': [[0, 100, 0], [75, 255, 75]],
    'Blue-green': [[0, 75, 50], [75, 255, 255]],
    'Blue': [[0, 0, 50], [75, 75, 255]],
    'Blue-violet': [[25, 0, 50], [100, 75, 255]],
    'Violet': [[50, 0, 100], [200, 75, 255]],
    'Red-violet': [[75, 0, 50], [200, 75, 100]]}

    for color_name, (lower, upper) in color_ranges.items():
        if lower[0] <= red <= upper[0] and lower[1] <= green <= upper[1] and lower[2] <= blue <= upper[2]:
            return color_name
    return "Unknown color"



def complementaryMatches(color):
    comp={'Red':'Green',
          'Red-orange':'Blue-Green',
          'Green':'Red',
          'Blue':'Orange',
          'Orange':'Blue',
          'Blue-Green':'Red-orange',
          'Red-violet':'Yellow-green',
          'Yellow-green':'Red-violet',
          'Yellow':'Violet',
          'Violet':'Yellow',
          'Blue-violet':'Yellow-orange',
          'Yellow-orange':'Blue-violet'}
    return comp[color]

def triadicMatches(color):
    triadic = {
        'Red': ['Yellow', 'Blue'],
        'Red-orange': ['Yellow-green', 'Blue-violet'],
        'Orange': ['Blue-green', 'Violet'],
        'Yellow-orange': ['Blue', 'Green'],
        'Yellow': ['Blue-violet', 'Red'],
        'Yellow-green': ['Red-orange', 'Blue'],
        'Green': ['Red-violet', 'Orange'],
        'Blue-green': ['Red-violet', 'Orange'],
        'Blue': ['Red-orange', 'Yellow-orange'],
        'Blue-violet': ['Yellow', 'Red'],
        'Violet': ['Green', 'Orange'],
        'Red-violet': ['Yellow-green', 'Blue']}
    return triadic[color]

def analogousMatches(color):
    analogous={
        'Red': ['Red-orange', 'Red-violet'],
        'Red-orange': ['Red', 'Orange'],
        'Orange': ['Red-orange', 'Yellow-orange'],
        'Yellow-orange': ['Orange', 'Yellow'],
        'Yellow': ['Yellow-orange', 'Yellow-green'],
        'Yellow-green': ['Yellow', 'Green'],
        'Green': ['Yellow-green', 'Blue-green'],
        'Blue-green': ['Green', 'Blue'],
        'Blue': ['Blue-green', 'Blue-violet'],
        'Blue-violet': ['Blue', 'Violet'],
        'Violet': ['Blue-violet', 'Red-violet'],
        'Red-violet': ['Violet', 'Red']}
    return analogous[color]
    
def splitComplementaryMatches(color):
    splitComplementary = {
        'Red': ['Blue-green', 'Yellow-green'], 
        'Red-orange': ['Blue', 'Green'],
        'Orange': ['Blue-violet', 'Blue-green'],
        'Yellow-orange': ['Blue', 'Violet'],
        'Yellow': ['Red-violet', 'Blue-violet'],
        'Yellow-green': ['Red', 'Violet'],
        'Green': ['Red-orange', 'Red-violet'],
        'Blue-green': ['Red', 'Orange'],
        'Blue': ['Yellow-orange', 'Red-orange'],
        'Blue-violet': ['Yellow', 'Orange'],
        'Violet': ['Yellow-orange', 'Yellow-green'],
        'Red-violet': ['Yellow', 'Green']
        }
    return splitComplementary[color]

def saveToFile():
    #Save the color information to a file
    file=open("Colorblind Clothes Matcher/ColorInfo.txt","w+")
    file.write(f"{inputImage} Color: {color_name}\n")




#TEMPORARY FUNCTION CALL
#saveClothing()
tempClothing="/Users/alexandermcgreevy/Documents/GitHub/Projects-Clone/Colorblind Clothes Matcher/Clothing.png"
# Read the image
img = cv2.imread(tempClothing)

# Calculate histograms for B, G, R channels
blueHist = cv2.calcHist([img], [0], None, [256], [0, 256])
greenHist = cv2.calcHist([img], [1], None, [256], [0, 256])
redHist = cv2.calcHist([img], [2], None, [256], [0, 256])
# Get top 3 colors for each channel
top_blue = get_top_colors(blueHist)
top_green = get_top_colors(greenHist)
top_red = get_top_colors(redHist)

#EXAMPLE OUTPUT
print("Top 3 Blue intensities and pixel counts:", top_blue)
print("Top 3 Green intensities and pixel counts:", top_green)
print("Top 3 Red intensities and pixel counts:", top_red)
red, green, blue = clothingColor(top_blue, top_green, top_red)
print(red,' ',green,' ',blue)
color_name = findColor(red, green, blue)
print(f"The color is: {color_name}")
print(f"The complementary color is: {complementaryMatches(color_name)}")
print(f"The triadic colors are: {triadicMatches(color_name)}")
print(f"The split complementary colors are: {splitComplementaryMatches(color_name)}")
print(f"The analogous colors are: {analogousMatches(color_name)}")
