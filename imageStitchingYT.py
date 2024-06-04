import numpy as np  # Import the numpy library and assign it the alias 'np'
import cv2  # Import the OpenCV library and assign it the alias 'cv2'
import glob  # Import the glob library for file path manipulation
import imutils  # Import the imutils library for image processing utilities

# Initialize an empty list to store the image paths
image_paths = glob.glob('images/*.jpg')  

# Initialize an empty list to store the images
images = []  

# Iterate over each image path
for image in image_paths:
    # Read the image using OpenCV
    img = cv2.imread(image)
    
    # Append the image to the list of images
    images.append(img)
    
    # Display the image using OpenCV
    cv2.imshow("Image", img)
    
    # Wait for a keyboard input
    cv2.waitKey(0)

# Create a Stitcher object to stitch the images together
imageStitcher = cv2.Stitcher_create()  

# Stitch the images together
error, stitched_img = imageStitcher.stitch(images)  

# Check if there was an error during stitching
if not error:
    # Save the stitched image to a file
    cv2.imwrite("stitchedOutput.png", stitched_img)
    
    # Display the stitched image
    cv2.imshow("Stitched Img", stitched_img)
    
    # Wait for a keyboard input
    cv2.waitKey(0)

    # Add a 10-pixel border to the stitched image
    stitched_img = cv2.copyMakeBorder(stitched_img, 10, 10, 10, 10, cv2.BORDER_CONSTANT, (0,0,0))

    # Convert the stitched image to grayscale
    gray = cv2.cvtColor(stitched_img, cv2.COLOR_BGR2GRAY)
    
    # Apply binary thresholding to the grayscale image
    thresh_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]

    # Display the thresholded image
    cv2.imshow("Threshold Image", thresh_img)
    
    # Wait for a keyboard input
    cv2.waitKey(0)

    # Find contours in the thresholded image
    contours = cv2.findContours(thresh_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Extract the contours from the result
    contours = imutils.grab_contours(contours)

    # Find the contour with the maximum area
    areaOI = max(contours, key=cv2.contourArea)

    # Create a mask with the same shape as the thresholded image
    mask = np.zeros(thresh_img.shape, dtype="uint8")
    
    # Get the bounding rectangle of the contour
    x, y, w, h = cv2.boundingRect(areaOI)
    
    # Draw the bounding rectangle on the mask
    cv2.rectangle(mask, (x,y), (x + w, y + h), 255, -1)

    # Initialize the minimum rectangle and subtraction images
    minRectangle = mask.copy()
    sub = mask.copy()

    # Erode the minimum rectangle until it disappears
    while cv2.countNonZero(sub) > 0:
        minRectangle = cv2.erode(minRectangle, None)
        sub = cv2.subtract(minRectangle, thresh_img)

    # Find contours in the minimum rectangle
    contours = cv2.findContours(minRectangle.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Extract the contours from the result
    contours = imutils.grab_contours(contours)

    # Find the contour with the maximum area
    areaOI = max(contours, key=cv2.contourArea)

    # Display the minimum rectangle
    cv2.imshow("minRectangle Image", minRectangle)
    
    # Wait for a keyboard input
    cv2.waitKey(0)

    # Get the bounding rectangle of the contour
    x, y, w, h = cv2.boundingRect(areaOI)

    # Crop the stitched image to the bounding rectangle
    stitched_img = stitched_img[y:y + h, x:x + w]

    # Save the cropped image to a file
    cv2.imwrite("stitchedOutputProcessed.png", stitched_img)

    # Display the cropped image
    cv2.imshow("Stitched Image Processed", stitched_img)

    # Wait for a keyboard input
    cv2.waitKey(0)

# If there was an error during stitching, print an error message
else:
    print("Images could not be stitched!")
    print("Likely not enough keypoints being detected!")