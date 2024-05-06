import board
import busio
from digitalio import DigitalInOut
import adafruit_connection_manager
import adafruit_requests
from adafruit_esp32spi import adafruit_esp32spi

# conventional 
from os import getenv

# ---------------------------------- user inputs ----------------------------------

# stocks
STOCK = getenv("STOCK")
TWELVE_API_KEY = getenv("TWELVE_API_KEY")

# time
TIME_ZONE = getenv("TIME_ZONE")
COUNTRY = getenv("COUNTRY")
IS_CLOCK = getenv("IS_CLOCK")




# ---------------------------------------------------------------------------------

# ---------------------------------- wifi connect ---------------------------------

# Get wifi details and more from a settings.toml file
# tokens used by this Demo: CIRCUITPY_WIFI_SSID, CIRCUITPY_WIFI_PASSWORD
secrets = {
    "ssid": getenv("CIRCUITPY_WIFI_SSID"),
    "password": getenv("CIRCUITPY_WIFI_PASSWORD"),
}
if secrets == {"ssid": None, "password": None}:
    try:
        # Fallback on secrets.py until depreciation is over and option is removed
        from secrets import secrets
    except ImportError:
        print("WiFi secrets are kept in settings.toml, please add them there!")
        raise

print("ESP32 SPI webclient test")

# If you are using a board with pre-defined ESP32 Pins:
esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)


# Secondary (SCK1) SPI used to connect to WiFi board on Arduino Nano Connect RP2040
if "SCK1" in dir(board):
    spi = busio.SPI(board.SCK1, board.MOSI1, board.MISO1)
else:
    spi = busio.SPI(board.SCK, board.MOSI, board.MISO)

esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

pool = adafruit_connection_manager.get_radio_socketpool(esp)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(esp)
requests = adafruit_requests.Session(pool, ssl_context)

if esp.status == adafruit_esp32spi.WL_IDLE_STATUS:
    print("ESP32 found and in idle mode")
print("Firmware vers.", esp.firmware_version.decode("utf-8"))
print("MAC addr:", ":".join("%02X" % byte for byte in esp.MAC_address))

for ap in esp.scan_networks():
    print("\t%-23s RSSI: %d" % (str(ap["ssid"], "utf-8"), ap["rssi"]))

print("Connecting to AP...")
while not esp.is_connected:
    try:
        esp.connect_AP(secrets["ssid"], secrets["password"])
    except OSError as e:
        print("could not connect to AP, retrying: ", e)
        continue
print("Connected to", str(esp.ssid, "utf-8"), "\tRSSI:", esp.rssi)
print("My IP address is", esp.pretty_ip(esp.ip_address))
print(
    "IP lookup adafruit.com: %s" % esp.pretty_ip(esp.get_host_by_name("adafruit.com"))
)

# ---------------------------------------------------------------------------------


# ---------------------------------- API Calls ----------------------------------

#collects financial data from twelve data api

def getStockInstance(): 
    STOCK_URL = f"https://api.twelvedata.com/quote?symbol={STOCK}&apikey={TWELVE_API_KEY}"

    try:
        print("Loading...")
        with requests.get(STOCK_URL) as response:
            print("---Done---")
            return response.json()
    
    except Exception as e:
        print("Error instance stock data :", e)

def getStockDataGraph(output_size): 
    STOCK_URL = f"https://api.twelvedata.com/time_series?symbol={STOCK}&interval=5min&outputsize={output_size}&apikey={TWELVE_API_KEY}"

    try:
        print("Loading...")
        with requests.get(STOCK_URL) as response:
            print("---Done---")
            return response.json()
    
    except Exception as e:
        print("Error stock graph data:", e)

#returns current time on start-up
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



# ---------------------------------------------------------------------------------
