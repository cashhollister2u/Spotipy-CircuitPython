# adafruit
import displayio
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
from adafruit_display_shapes.triangle import Triangle
from adafruit_display_shapes.line import Line

# conventional libraries
import math 
import gc
import time

# custom components
from components.api_calls import getStockInstance, getStockDataGraph

# fonts
block_font = bitmap_font.load_font("fonts/IBMPlexMono-Medium-24_jep.bdf")
med_font = bitmap_font.load_font("fonts/MatrixChunky8.bdf")
small_font = bitmap_font.load_font("fonts/MatrixChunky6X.bdf")


    
def display_stock(bitmap, palette, display):
   
    # declared variables 
    stock_instanceJSON = None
    price_displayed = None
    text_color = 0x505050
    triangle = None
    bitmap_color = None

    
    # specified stock data
    stock_instanceJSON = getStockInstance() 
    price_displayed = round(float(stock_instanceJSON['close']), 2)
    percent_change = round(float(stock_instanceJSON['percent_change']), 2)
    price_change = round(float(stock_instanceJSON['change']), 2)

    # calculate graph parameters
    stock_graphJSON = getStockDataGraph(80)
    stock_graphJSON = stock_graphJSON['values'][:64][::-1]
    #filter out quotes from previous day
    for index, quote in enumerate(stock_graphJSON):
        if "09:30:00" in quote['datetime']:
            stock_graphJSON = stock_graphJSON[index:]
            break
       
    
    
    # deturmine x-axis height by ratio of day in red
    quote_in_red = 1
    for quote in stock_graphJSON:
        quote_in_red += 1 if (quote['close']) < (stock_instanceJSON['previous_close']) else 0
    x_axis_height = math.ceil(31 - 16*(quote_in_red / len(stock_graphJSON))) 

    # find the range of stock price for the day
    high_dif = x_axis_height - 15
    low_dif = 31 - x_axis_height
    try:
        high_unit_measurement = (float(stock_instanceJSON['high']) - float(stock_instanceJSON['previous_close'])) / high_dif
    except ZeroDivisionError:
        high_unit_measurement = None
    try:
         low_unit_measurement = (float(stock_instanceJSON['previous_close']) - float(stock_instanceJSON['low'])) / low_dif
    except ZeroDivisionError:
        low_unit_measurement = None
    
    # deturmine x value offset for text
    stock_ticker_len = len(stock_instanceJSON['symbol'])
    percent_change_len = len(str(percent_change))
    price_change_len = len(str(price_change))

    # deturmine x value offset for triangle
    triangle_x_offset = 2 + (stock_ticker_len*3) + stock_ticker_len
    for l in stock_instanceJSON['symbol']:
        triangle_x_offset += 1 if l == "N" or l == "H" else 0
        triangle_x_offset += 2 if l == "W" or l == "M" else 0

    # set values based on red or green market indicators
    if "-" in stock_instanceJSON['percent_change']:
        text_color = 0x120000
        bitmap_color = 1
        price = label.Label(small_font, text=f"{price_displayed:.2f}", color=0x121111)
        ticker = label.Label(small_font, text=stock_instanceJSON['symbol'], color=0x121111)
        triangle = Triangle(triangle_x_offset+2, 4, triangle_x_offset, 2, triangle_x_offset+4, 2, fill=text_color, outline=text_color) # xm, ym, xl, yl, xr, yr
        
    elif float(stock_instanceJSON['percent_change']) > 0:
        text_color = 0x001200
        bitmap_color = 4
        price = label.Label(small_font, text=f"{price_displayed:.2f}", color=0x121111)
        ticker = label.Label(small_font, text=stock_instanceJSON['symbol'], color=0x121111)
        triangle = Triangle(triangle_x_offset+2, 2, triangle_x_offset, 4, triangle_x_offset+4, 4, fill=text_color, outline=text_color) # xm, ym, xl, yl, xr, yr
        
    # Create text lines
    ticker.x = 1  
    ticker.y = 4  

    #price defined in the if condition above
    price.x = 2  

    # Manually set a closer y-position for the second line
    price.y = ticker.y + 7  

    price_difference = label.Label(small_font, text=f"{price_change:.2f}", color=text_color)
    price_difference.x = 52 - (((price_change_len - 1)*3) + (price_change_len - 4)) # account for dif len values
    price_difference.y = 4

    percent_difference = label.Label(small_font, text=f"{percent_change:.2f}", color=text_color)
    percent_difference.x = 52 - (((percent_change_len - 1)*3) + (percent_change_len - 4))
    percent_difference.y = price_difference.y + 7  

    # percent sign
    tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette) # init custom pixels
    bitmap[57, 9] = bitmap_color  # Light pixel @ x, y = color
    bitmap[61, 13] = bitmap_color
    slash = Line(61,9,57,13, color=text_color)

    # Create a group to hold both lines of text
    group = displayio.Group()
    group.append(tile_grid) # any kind of custom pixel config must be prioritized in the group

    # append the graph lines to the group
    step = 1
    for index, quote in enumerate(stock_graphJSON):
        if index % step == 0:
            # checks if negative line
            if (quote['close']) < (stock_instanceJSON['previous_close']):
                # assign line length based on ratio to day low, unit of measurement, and relative location of x axis 
                end_point = x_axis_height + (math.ceil((float(stock_instanceJSON['previous_close']) - float(quote['close'])) / low_unit_measurement))
                line_graph = Line(index,x_axis_height, index, end_point - 1, color=0x120000) # x1, y1, x2, y2
                group.append(line_graph)
                bitmap[index, end_point] = 6

            # checks if positive line
            elif (quote['close']) > (stock_instanceJSON['previous_close']):
                # assign line length based on ratio to day high, unit of measurement, and relative location of x axis 
                end_point = x_axis_height - (math.ceil((float(quote['close']) - float(stock_instanceJSON['previous_close'])) / high_unit_measurement))
                line_graph = Line(index,x_axis_height, index, end_point + 1, color=(0x001200)) # x1, y1, x2, y2
                group.append(line_graph)
                bitmap[index, end_point] = 3   

    
    #group.append(x_axis)
    group.append(slash)
    group.append(ticker)
    group.append(triangle)
    group.append(price)
    group.append(price_difference)
    group.append(percent_difference)
   
  
 
    # Assign the group to the display's root group
    display.root_group = group

    time.sleep(300)
    while len(group) > 0:
        group.pop()
    del group
    gc.collect()