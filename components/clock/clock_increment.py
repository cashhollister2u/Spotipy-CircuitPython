from components.clock.clock import sync_time
import time
from os import getenv

IS_CLOCK = getenv("IS_CLOCK")

json_time = sync_time()

# Convert JSON string to a dictionary
JSON_clock = json_time

# Helper function to convert dictionary to a time tuple
def dict_to_tuple(t_dict):
    return (t_dict['year'], t_dict['month'], t_dict['day'], t_dict['hour'], t_dict['minute'], t_dict['second'], -1, -1, -1)

# Function to increment the time object by one second
def increment_time(t_dict):
    t = time.struct_time(dict_to_tuple(t_dict))
    # Increment by one second using time.mktime and time.localtime
    new_t = time.localtime(time.mktime(t) + 1)

    # Update dictionary with new values
    t_dict.update({
        'year': new_t.tm_year,
        'month': new_t.tm_mon,
        'day': new_t.tm_mday,
        'hour': new_t.tm_hour,
        'minute': new_t.tm_min,
        'second': new_t.tm_sec,
    })

    convert_to_12hr(t_dict)

def convert_to_12hr(t_dict):
    hour = t_dict['hour']
    if hour == 0:
        # Midnight case, set to 12 AM
        t_dict['hour'] = 12
        t_dict['period'] = 'AM'
    elif hour < 12:
        # Morning hours, just add AM
        t_dict['period'] = 'AM'
    elif hour == 12:
        # Noon case, set to 12 PM
        t_dict['period'] = 'PM'
    else:
        # Afternoon and evening hours, convert and set to PM
        t_dict['hour'] = hour - 12
        t_dict['period'] = 'PM'