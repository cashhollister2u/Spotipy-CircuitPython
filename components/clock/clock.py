# conventional 
from os import getenv
from components.network_connect import requests

# time
TIME_ZONE = getenv("TIME_ZONE")
COUNTRY = getenv("COUNTRY")
IS_CLOCK = getenv("IS_CLOCK")


#retrieves current time
def sync_time():
    TIME_ZONE_URL = f"http://worldtimeapi.org/api/timezone/{COUNTRY}/{TIME_ZONE}"
    if IS_CLOCK == 1:
        try:
            #get the current time data
            with requests.get(TIME_ZONE_URL) as response:
                response_json = response.json()  # Parse as JSON
                # Extract the ISO datetime string
                datetime_str = response_json["datetime"]

                # Split date and time components
                date_part, time_part = datetime_str.split("T")
                year, month, day = map(int, date_part.split("-"))
                day_of_week = response_json['day_of_week']

                # Further split and parse time components
                time_parts = time_part.split(":")
                hour, minute, second = map(lambda x: int(x.split(".")[0]), time_parts[0:3])
                time_JSON = {
                    'year':year,
                    'month':month,
                    'day':day,
                    'hour':hour,
                    'minute':minute,
                    'second':second,
                    'day_of_week': day_of_week
                }
                print(time_JSON)
                return time_JSON
        
        except Exception as e:
            print("Error:", e)
            return "Time Error"