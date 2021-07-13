from PIL import Image 
import numpy as np 
import matplotlib.pyplot as plt 
#I'm just making this edit so I can open a pull request and write comments. 
 
### The Quicksort Algorithm 
# This is a helpermethod for the quickSort Algorithm 
# We need to give the quickSort the parameters arr, low, high and comparator every time 
# arr = is the array we want to sort 
# low = the index of the first element in our array (NOT the value) 
# high = the index of the last element in our array (NOT the value) 
# comparator = a helpermethod which we use to decide how to compare stuff 
 
# Every time we want to sort a picture, we have to pass on the above mentioned 4 parameters. To avoid code duplication, 
# we created this helpermethod 
 
# This way we only need to manually pass on the array and the comparator method, the helpermethod does the rest for us 
 
def quickSortHelp(arr, comparator): 
    quickSort(arr, 0, len(arr) - 1, comparator) 
 
 
def quickSort(arr, low, high, comparator): 
    if len(arr) == 1: 
        return arr 
    if low < high: 
        # Pi is the index where the array gets divided in two (the place of our pivot element) 
        # arr[pi] is sorted 
        # what partition does will be explained below 
        pi = partition(arr, low, high, comparator) 
        # After you've divided the array, you repeat 
        quickSort(arr, low, pi - 1, comparator) 
        quickSort(arr, pi + 1, high, comparator) 
 
# Partition actually compares two values with each other 
def partition(arr, low, high, comparator): 
    # i : the index of the smallest elements minus 1, so suuuper on the left of the array 
    i = (low - 1) 
    # pivot : value of the pivot elements. We get it by using a comparator method. 
    pivot = comparator(arr[high]) 
 
    for j in range(low, high): 
        if comparator(arr[j]) <= pivot: 
            i = i + 1 
            arr[i], arr[j] = arr[j], arr[i].copy() 
    arr[i + 1], arr[high] = arr[high], arr[i + 1].copy() 
    return (i + 1) 
 
 
### Comparator = How we determine the value of a pixel 
# howBright just gives us the sum of the three RGB values 
def howBright(pixel): 
    return int(pixel[0]) + int(pixel[1]) + int(pixel[2]) 
 
# Sort by red 
def valueofRed(pixel): 
    return int(pixel[0]) 
 
# Oder yellow 
def valueofYellow(pixel): 
    return int(pixel[1]) 
 
# Oder blue 
def valueofBlue(pixel): 
    return int(pixel[2]) 
 
 
 
### Convert -> converting each row 
def convertRow(originalImage): 
    print(originalImage) 
    data_array = np.asarray(originalImage) 
    data_array_sortByRow = data_array.copy() 
    # .jpg and .png have different amounts of channels 
    # .jpg has three (RGB) and .png has four(RGBA) 
    # So that we won't get errors later, we use len() to find out how many channels we have, this way we can sort .jpg 
    # images and .png images without having to change the code 
    data_Format = len(data_array[0][0]) 
    width, height = originalImage.size 
    converted_data_array = np.zeros((height, width, data_Format), dtype=np.uint8) 
 
    for i in range(height): 
        sortedRow = data_array_sortByRow[i].copy() 
        quickSortHelp(sortedRow, howBright) 
        converted_data_array[i] = sortedRow 
 
    converted_image_row = Image.fromarray(converted_data_array, "RGBA"[:data_Format]) 
    return converted_image_row 
 
 
### Convert -> converting each column 
def convertColumn(originalImage): 
    print(originalImage) 
    # to Sort by columns, the easiest way was to just switch the axis of the picture. This way we don't have to create 
    # a separate quickSort Algorithm. What used to be the columns are now rows, what used to be rows are columns 
    data_array = switchAxis(np.asarray(originalImage)) 
    data_array_sortByColumn = data_array.copy() 
    data_Format = len(data_array[0][0]) 
    width, height = originalImage.size 
    converted_data_array = np.zeros((width, height, data_Format), dtype=np.uint8) 
 
    for i in range(width): 
        sortedColumn = data_array_sortByColumn[i].copy() 
        quickSortHelp(sortedColumn, howBright) 
        converted_data_array[i] = sortedColumn 
 
    # when converting the array into an image, we have to remember to switch the axis back the way they were 
    converted_image_column = Image.fromarray(switchAxis(converted_data_array), "RGBA"[:data_Format]) 
    return converted_image_column 
 
 
# a helpermethod for convertColumn 
def switchAxis(data_array): 
    switched_data_array = np.zeros((len(data_array[0]), len(data_array), len(data_array[0][0])), dtype=np.uint8) 
    for i in range(len(data_array)): 
        for j in range(len(data_array[i])): 
            switched_data_array[j][i] = data_array[i][j] 
    return switched_data_array 
 
 
### Convert -> Continuously 
def convertContinuously(originalImage): 
    print(originalImage) 
    data_array = np.asarray(originalImage) 
    data_Format = len(data_array[0][0]) 
    width, height = originalImage.size 
 
    # We change the array so that it has new dimensions 
    # -> before we had a 3d array, now we have a 2d array 
    # we use .reshape to achieve this 
    data_array_sortContinuously = data_array.reshape(width * height, data_Format).copy() 
    quickSortHelp(data_array_sortContinuously, howBright) 
    # after having sorted the array, we turn it back into a 3d array 
    converted_data_array = data_array_sortContinuously.reshape(height, width, data_Format) 
    converted_image_continously = Image.fromarray(converted_data_array, "RGBA"[:data_Format]) 
    return converted_image_continously 
 
#### Sorting by pixels 
original = Image.open('Bilder/Beispiel.PNG') 
 
# Make the image smaller while keeping the proportions 
factor = 0.25 
width, height = original.size 
width, height = int(width * factor), int(height * factor) 
original = original.resize((width, height)) 
 
def convert(originalImage): 
    original = originalImage 
    convertedImageRow = convertRow(originalImage) 
    print("Finished sorting each row") 
 
    convertedImageColumn = convertColumn(originalImage) 
    print("Finished sorting each colunmn") 
 
    convertedImageContinuously = convertContinuously(originalImage) 
    print("Finished sorting continuously") 
 
    # Displaying it in plotview 
    fig, axs = plt.subplots(2, 2) 
 
    axs[0][0].imshow(original) 
    axs[0][0].set_title("Orginal Image") 
    axs[0][0].axis('off') 
 
    axs[0][1].imshow(convertedImageRow) 
    axs[0][1].set_title("Sorted each Row") 
    axs[0][1].axis('off') 
 
    axs[1][0].imshow(convertedImageColumn) 
    axs[1][0].set_title("Sorted each Column") 
    axs[1][0].axis('off') 
 
    axs[1][1].imshow(convertedImageContinuously) 
    axs[1][1].set_title("Sorted Continuously") 
    axs[1][1].axis('off') 
 
    fig.tight_layout() 
    plt.show() 
 
convert(original) 
 
