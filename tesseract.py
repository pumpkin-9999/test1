import cv2
import numpy as np
from PIL import Image
from pytesseract import pytesseract

camera = cv2.VideoCapture(0)

while True:
    _, image = camera.read()
    cv2.imshow('Text detection', image)
    if cv2.waitKey(1) & 0xFF==ord('s'):
        cv2.imwrite("C:/Users/sieun/2-2/embedded software/image/test1.jpg", image)
        break
camera.release()
cv2.destroyAllWindows()

hsvFrame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

blue_lower = np.array([94, 80, 2], np.uint8) #blue
blue_upper = np.array([120, 255, 255], np.uint8)
blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)

red_lower = cv2.inRange(hsvFrame, (0, 100, 100), (5, 255, 255)) #red
red_upper = cv2.inRange(hsvFrame, (175, 100, 100), (255, 255, 255))
red_mask = cv2.addWeighted(red_lower, 1.0, red_upper, 1.0, 0,0)

black_lower = np.array([0, 0, 0], np.uint8) #black
black_upper = np.array([360, 255, 50], np.uint8)
black_mask = cv2.inRange(hsvFrame, black_lower, black_upper)
black_mask = 255 - black_mask

kernel = np.ones((5, 5), "uint8")

blue_mask = cv2.dilate(blue_mask, kernel) #blue
res_blue = cv2.bitwise_and(image, image, mask = blue_mask)
#res_blue = cv2.cvtColor(res_blue, cv2.COLOR_HSV2BGR)
gray_blue = cv2.cvtColor(res_blue, cv2.COLOR_BGR2GRAY)
ret_blue, dst_blue = cv2.threshold(gray_blue, 50, 255, cv2.THRESH_BINARY)
dst_blue = cv2.bitwise_not(dst_blue)


red_mask = cv2.dilate(red_mask, kernel) #red
res_red = cv2.bitwise_and(image, image, mask = red_mask)
#res_red = cv2.cvtColor(res_red, cv2.COLOR_HSV2BGR)
gray_red = cv2.cvtColor(res_red, cv2.COLOR_BGR2GRAY)
ret_red, dst_red = cv2.threshold(gray_red, 50, 255, cv2.THRESH_BINARY)
dst_red = cv2.bitwise_not(dst_red)

black_mask = cv2.dilate(black_mask, kernel, iterations=300) #black ???????
res_black = cv2.bitwise_and(image, image, mask = black_mask)
#res_black = cv2.cvtColor(res_black, cv2.COLOR_HSV2BGR)
gray_black = cv2.cvtColor(res_black, cv2.COLOR_BGR2GRAY)
ret_black, dst_black = cv2.threshold(gray_black, 50, 255, cv2.THRESH_BINARY)
dst_black = cv2.bitwise_not(dst_black)
dst_black = 255 - dst_black


cv2.imwrite("C:/Users/sieun/2-2/embedded software/image/test_blue.jpg", dst_blue)
cv2.imwrite("C:/Users/sieun/2-2/embedded software/image/test_red.jpg", dst_red)
cv2.imwrite("C:/Users/sieun/2-2/embedded software/image/test_black.jpg", dst_black)



def tesseract_blue():
    path_to_tesseract = R"C:\Program Files\Tesseract-OCR\tesseract"
    Imagepath_blue="C:/Users/sieun/2-2/embedded software/image/test_blue.jpg"
    pytesseract.tesseract_cmd = path_to_tesseract
    text_blue=pytesseract.image_to_string(Image.open(Imagepath_blue))
    if text_blue == "":
        pass
    else:
        print(text_blue[:-1])
tesseract_blue()

def tesseract_red():
    path_to_tesseract = R"C:\Program Files\Tesseract-OCR\tesseract"
    Imagepath_red="C:/Users/sieun/2-2/embedded software/image/test_red.jpg"
    pytesseract.tesseract_cmd = path_to_tesseract
    text_red=pytesseract.image_to_string(Image.open(Imagepath_red))
    if text_red == "":
        pass
    else:
        print(text_red[:-1])
tesseract_red()

def tesseract_black():
    path_to_tesseract = R"C:\Program Files\Tesseract-OCR\tesseract"
    Imagepath_black="C:/Users/sieun/2-2/embedded software/image/test_black.jpg"
    pytesseract.tesseract_cmd = path_to_tesseract
    text_black=pytesseract.image_to_string(Image.open(Imagepath_black))
    if text_black == "":
        pass
    else:
        print(text_black[:-1])
        if text_black[:-1] == "E":
            print("동쪽 동쪽")
        elif text_black[:-1] == "W":
            print("서쪽 서쪽")
        elif text_black[:-1] == "S":
            print("남쪽 남쪽")
        elif text_black[:-1] == "N":
            print("북쪽 북쪽")
        
tesseract_black()

