#adafruit
import displayio
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
from adafruit_display_shapes.line import Line

# conventional 
from os import getenv

# custom components
from components.clock import JSON_clock

# enviromental variables
IS_CLOCK = getenv("IS_CLOCK")



#fonts
block_font = bitmap_font.load_font("fonts/IBMPlexMono-Medium-24_jep.bdf")
med_font = bitmap_font.load_font("fonts/MatrixChunky8.bdf")
small_font = bitmap_font.load_font("fonts/MatrixChunky6X.bdf")
white_color = 0x121212

if IS_CLOCK == 1:

    days_of_week = ['SUN', 'MON', 'TUES', 'WED', 'THURS', 'FRI', 'SAT']
    today = days_of_week[JSON_clock['day_of_week']]
    day_x_offset = 44
    if today == days_of_week[1]:
        day_x_offset -= 1
    elif today == days_of_week[2]:
        day_x_offset -= 2
    elif today == days_of_week[3]:
        day_x_offset -= 1
    elif today == days_of_week[4]:
        day_x_offset -= 4
    elif today == days_of_week[5]:
        day_x_offset += 1
    elif today == days_of_week[6]:
        day_x_offset += 1

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    month = months[JSON_clock['month'] + 1]
    month_x_offset = 39
    if month == months[2]:
        month_x_offset -= 1
    elif month == months[4]:
        month_x_offset -= 1


def display_clock(display):
    # Create display objects 
    time = label.Label(
        med_font, 
        text=f"{JSON_clock['hour']:02}:{JSON_clock['minute']:02}:{JSON_clock['second']:02}", 
        color=white_color)
    time.x = 4  
    time.y = 5  

    current_day = label.Label(
        med_font, 
        text=today, 
        color=0x171501)
    current_day.x = day_x_offset  
    current_day.y = 28  

    divide_cal = Line(37,9,62,9, color=0x120607)

    current_month = label.Label(
        med_font, 
        text=f"{month.upper()} {JSON_clock['day']:02}", 
        color=white_color)
    current_month.x = month_x_offset  
    current_month.y = 5  

    divide_main = Line(35,1,35,30, color=white_color)

    # Create a group to hold both lines of text
    group = displayio.Group()

    # Add both lines to the group
    group.append(time)
    group.append(current_day)
    group.append(current_month)
    group.append(divide_main)
    group.append(divide_cal)


    # Assign the group to the display's root group
    display.root_group = group