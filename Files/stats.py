# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# -*- coding: utf-8 -*-

import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789

import os

file_path = os.path.dirname(os.path.realpath(__file__))

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=240,
    height=240,
    x_offset=0,
    y_offset=80
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 180

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
fontvbig = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
fontbig = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
fontlbig = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
fontsmall = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
fontvsmall = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True


disk_size = 65
disk1_none = Image.open(file_path + "/icons/disk1_none.png")
disk1_none = disk1_none.resize((disk_size, disk_size), Image.Resampling.BICUBIC).convert('RGBA')
disk2_none = Image.open(file_path + "/icons/disk2_none.png")
disk2_none = disk2_none.resize((disk_size, disk_size), Image.Resampling.BICUBIC).convert('RGBA')
disk1_good = Image.open(file_path + "/icons/disk1_good.png")
disk1_good = disk1_good.resize((disk_size, disk_size), Image.Resampling.BICUBIC).convert('RGBA')
disk2_good = Image.open(file_path + "/icons/disk2_good.png")
disk2_good = disk2_good.resize((disk_size, disk_size), Image.Resampling.BICUBIC).convert('RGBA')
disk1_bad = Image.open(file_path + "/icons/disk1_bad.png")
disk1_bad = disk1_bad.resize((disk_size, disk_size), Image.Resampling.BICUBIC).convert('RGBA')
disk2_bad = Image.open(file_path + "/icons/disk2_bad.png")
disk2_bad = disk2_bad.resize((disk_size, disk_size), Image.Resampling.BICUBIC).convert('RGBA')

def checkDiskStatus(disk_number):
    disk_status_files = [file_path + "/diskstatus/disk1.txt", file_path + "/diskstatus/disk2.txt"]
    disk_images = [[disk1_none, disk1_good, disk1_bad], [disk2_none, disk2_good, disk2_bad]]

    cmd = "cat " + disk_status_files[disk_number-1]
    status = subprocess.check_output(cmd, shell=True).decode("utf-8")
    if status == "1\n":
        disk_image = disk_images[disk_number-1][1] #good
    elif status == "2\n":
        disk_image = disk_images[disk_number-1][2] #bad
    else:
        disk_image = disk_images[disk_number-1][0] #no data
    return disk_image


while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Shell scripts for system monitoring from here:
    # https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    


    #Partie IP
    cmd = "hostname -I | cut -d' ' -f1"
    IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
    draw.text((15, top+10), IP, font=fontbig, fill="#FFFFFF")
    lineY = font.getbbox(IP)[3] + 25
    draw.line([(width, lineY), (0, lineY)], width=3, fill="#FFFFFF")

    draw.line([(width/2, lineY), (width/2, 157)], width=3, fill="#FFFFFF")
    
    #Partie CPU
    draw.text((width/4 - 30, lineY+2), "CPU", font=fontbig, fill="#FFFFFF")
    cmd = "top -bn1 | grep load | awk '{printf \"%.0f%%\", $(NF-2)*100}'"
    CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "cat /sys/class/thermal/thermal_zone0/temp |  awk '{printf \"%.0f°C\", $(NF-0) / 1000}'"  # pylint: disable=line-too-long
    Temp = subprocess.check_output(cmd, shell=True).decode("utf-8")
    draw.text((width/4 - 30, 85), CPU, font=fontlbig, fill="#FFFFFF")
    draw.text((width/4 - 33, 120), Temp, font=fontlbig, fill="#FFFFFF")

    #Partie RAM
    draw.text((3*width/4 - 30, lineY+2), "RAM", font=fontbig, fill="#FFFFFF")
    cmd_pourcent = "free -m | awk 'NR==2{printf \"%.0f%%\", $3*100/$2 }'"
    pourcent = subprocess.check_output(cmd_pourcent, shell=True).decode("utf-8")
    draw.text((3*width/4 - 30, 96), pourcent, font=fontbig, fill="#FFFFFF")

    #Partie Disque
    draw.line([(width, 157), (0, 157)], width=3, fill="#FFFFFF")
    
    cmd = 'df -h --block-size=1073741824 | awk \'/md0/ {printf "%s",$5}\''
    pourcent = subprocess.check_output(cmd, shell=True).decode("utf-8")
    draw.text((140, 190), pourcent, font=fontvbig, fill="#FFFFFF")
    draw.text((140, 165), "DISQUES", font=font, fill="#FFFFFF")

    # Display image.
    disp.image(image, rotation)

    
    disp.image(checkDiskStatus(1), rotation, 175, 0)
    disp.image(checkDiskStatus(2), rotation, 115, 0)

    subprocess.run(file_path + "/diskstatus/checkDisks.sh", shell=True)

    time.sleep(1)
