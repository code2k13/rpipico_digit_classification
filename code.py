import gc
import sys
from time import sleep

import bitmaptools
import board
import busio
import digitalio
import displayio
import svm_min
import terminalio
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
from adafruit_ov7670 import OV7670
from adafruit_st7735r import ST7735R


# Function to convert RGB565_SWAPPED to grayscale
def rgb565_to_1bit(pixel_val):
    pixel_val = ((pixel_val & 0x00FF)<<8) | ((25889 & 0xFF00) >> 8)
    r = (pixel_val & 0xF800)>>11
    g = (pixel_val & 0x7E0)>>5
    b = pixel_val & 0x1F
    return (r+g+b)/128


#Setting up the TFT LCD display
mosi_pin = board.GP11
clk_pin = board.GP10
reset_pin = board.GP17
cs_pin = board.GP18
dc_pin = board.GP16

displayio.release_displays()
spi = busio.SPI(clock=clk_pin, MOSI=mosi_pin)
display_bus = displayio.FourWire(
    spi, command=dc_pin, chip_select=cs_pin, reset=reset_pin
)

display = ST7735R(display_bus, width=128, height=160, bgr=True)
group = displayio.Group( scale=1)
display.show(group)

font = bitmap_font.load_font("./Helvetica-Bold-16.bdf")
color = 0xffffff
text_area = label.Label(font, text='', color=color)
text_area.x = 10
text_area.y = 140
group.append(text_area)

cam_width = 80
cam_height = 60
cam_size = 3 #80x60 resolution

camera_image = displayio.Bitmap(cam_width, cam_height, 65536)
camera_image_tile = displayio.TileGrid(
    camera_image ,
    pixel_shader=displayio.ColorConverter(
        input_colorspace=displayio.Colorspace.RGB565_SWAPPED
    ),
    x=30,
    y=30,
)
group.append(camera_image_tile)
camera_image_tile.transpose_xy=True

inference_image = displayio.Bitmap(12,12, 65536)

#Setting up the camera
cam_bus = busio.I2C(board.GP21, board.GP20)

cam = OV7670(
    cam_bus,
    data_pins=[
        board.GP0,
        board.GP1,
        board.GP2,
        board.GP3,
        board.GP4,
        board.GP5,
        board.GP6,
        board.GP7,
    ],
    clock=board.GP8,
    vsync=board.GP13,
    href=board.GP12,
    mclk=board.GP9,
    shutdown=board.GP15,
    reset=board.GP14,
)
cam.size =  cam_size
cam.flip_y = True

ctr = 0
while True:
    cam.capture(camera_image)
    sleep(0.1)
    temp_bmp = displayio.Bitmap(cam_height, cam_height, 65536)
    for i in range(0,cam_height):
        for j in range(0,cam_height):
            temp_bmp[i,j] =  camera_image[i,j]
    bitmaptools.rotozoom(inference_image,temp_bmp,scale=12/cam_height,ox=0,oy=0,px=0,py=0)
    del(temp_bmp)

    input_data = []
    for i in range(0,12):
        for j in range(0,12):
            gray_pixel = 1 -rgb565_to_1bit(inference_image[i,j])
            if gray_pixel < 0.5:
                gray_pixel = 0
            input_data.append(gray_pixel)

    camera_image.dirty()
    display.refresh(minimum_frames_per_second=0)
    prediction = svm_min.score(input_data)
    #Uncomment these lines for debugging
    ctr = ctr + 1
    if ctr%50 == 0:
        print(input_data)
        print("------")
    res = prediction.index(max(prediction))
    #print(res)
    text_area.text = "Prediction : " +str(res)
    sleep(0.01)

