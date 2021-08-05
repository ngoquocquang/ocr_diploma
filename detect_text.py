# Import required packages
import random

import cv2

def detect_text(img):
    # Read image from which text needs to be extracted
    # img = cv2.imread(img)

    # Preprocessing the image starts

    # Convert the image to gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Performing OTSU threshold
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    # Specify structure shape and kernel size.
    # Kernel size increases or decreases the area
    # of the rectangle to be detected.
    # A smaller value like (10, 10) will detect
    # each word instead of a sentence.
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (12, 12))

    # Appplying dilation on the threshold image
    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

    # Finding contours
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)

    # Creating a copy of image
    im2 = img.copy()


    # Looping through the identified contours
    # Then rectangular part is cropped and passed on
    # to pytesseract for extracting text from it
    # Extracted text is then written into the text file
    i=random.randint(0,1000)
    maxx = 0
    maxy = 0
    maxw = 0
    maxh = 0
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w *h >maxw * maxh:
            maxx=x
            maxy=y
            maxw=w
            maxh=h

        # Drawing a rectangle on copied image
    rect = cv2.rectangle(im2, (maxx, maxy), (maxx + maxw, maxy + maxh), (0, 255, 0), 2)

    # Cropping the text block for giving input to OCR
    cropped = im2[maxy:maxy + maxh, maxx:maxx + maxw]
    # cv2.imwrite("image\\" + str(i) + ".PNG", rect)
    # cv2.imwrite("image\\" + str(i) + "a.PNG", cropped)
    # cv2.imshow("a", dilation)
    # cv2.waitKey()
    return cropped
# detect_text("placeofbirth.PNG")