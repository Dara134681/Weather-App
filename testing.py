"""
Weather App (Python console version)
Converted from: script.js / index.html / style.css

Teaching Tip: Explain 'requests.get()' using the waiter/restaurant analogy
(you place an order, wait for the kitchen, and get a response back).
"""

import tkinter as tk
from tkinter import font
import requests  # 3rd-party library for making HTTP calls, like fetch() in JS.
                 # Install it first with: pip install requests --break-system-packages


WEATHER_ICONS = {
    "Clear": "\u2600\ufe0f",
    "Clouds": "\u2601\ufe0f",
    "Rain": "\U0001F327\ufe0f",
    "Drizzle": "\U0001F326\ufe0f",
    "Thunderstorm": "\u26c8\ufe0f",
    "Snow": "\u2744\ufe0f",
    "Mist": "\U0001F32B\ufe0f",
    "Fog": "\U0001F32B\ufe0f",
    "Haze": "\U0001F32B\ufe0f",
}
DEFAULT_ICON = "\U0001F321\ufe0f"

# ------------------------------------------------------------------
# Feature: Background color shifts with the weather
# ------------------------------------------------------------------
WEATHER_BG_COLORS = {
    "Clear": "#ffd76e",
    "Clouds": "#b9c6d1",
    "Rain": "#7891a8",
    "Drizzle": "#9fb3c4",
    "Thunderstorm": "#5b6b82",
    "Snow": "#e8f1f8",
    "Mist": "#c8d2da",
    "Fog": "#c8d2da",
    "Haze": "#c8d2da",
}
DEFAULT_BG = "#8ec5ff"

# ------------------------------------------------------------------
# App state
# Teaching Concept: we store the last successful result and the
# current unit preference as module-level variables, so the °C/°F
# toggle can redraw the SAME data without making a new API call.
# ------------------------------------------------------------------
last_weather_data = None
use_fahrenheit = False


def celsius_to_fahrenheit(celsius):
    return celsius * 9 / 5 + 32                 


def get_weather():
    """
    Equivalent of the JS 'async function getWeather()'.
    Python doesn't need 'async' here because requests.get() is a normal,
    blocking call — it already waits for the response before moving on,
    so there's no separate 'await' keyword needed.
    """

    # 1. Get the city the student typed.
    #    JS: document.getElementById("city").value
    #    Python has no webpage/DOM, so we ask directly on the terminal instead.
    city = input("Enter city (e.g., London): ").strip()

    # instructor Checkpoint: This is where we verify the student typed something.
    # JS: if (!city) { showMessagePara(...); return; }
    if not city:
        show_message("Please type a city name.")
        return

    # Instructor setup: This is the free API Key.
    # (Same key from the JS file — in a real project, keep keys out of
    #  source code and load them from an environment variable instead.)
    api_key = "638ed8715b83a4ab1a9b255417142f33"

    # 2. Build the API 'order' (the URL).
    # JS: const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`;
    # Python f-strings work the same way as JS template literals (${...} -> {...}).
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    # Teaching Concept: 'try...except' is Python's version of JS's 'try...catch'.
    # It prevents the whole program from crashing if something goes wrong.
    try:
        # 3. 'Fetch' the data from the kitchen (OpenWeatherMap server).
        # JS: const response = await fetch(url);
        response = requests.get(url)

        # instructor checkpoint: Check if the waiter (response) brought back success.
        # JS: if (!response.ok) { throw new Error(...) }
        # requests doesn't raise automatically on 404, so we check the status code
        # ourselves, same as response.ok did in JS.
        if response.status_code != 200:
            # A 404 means the city wasn't found, so we raise a clean error.
            raise ValueError(f"We couldn't find '{city}'. Please check your spelling.")

        # 4. Open the JSON takeaway box (parse the response body).
        # JS: const data = await response.json();
        data = response.json()

        # 5. Print the data instead of updating the DOM.
        # Accessing nested JSON is identical in Python and JS:
        # JS:  data.sys.country          -> Python: data["sys"]["country"]
        # JS:  data.weather[0]           -> Python: data["weather"][0]
        name = data["name"]
        country = data["sys"]["country"]
        temp = round(data["main"]["temp"])
        description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]

        print(f"\n{name}, {country}")
        print(f"Temperature: {temp} °C")
        print(f"Weather: {description}")
        print(f"Humidity: {humidity}%\n")

    except ValueError as error:
        # instructor Checkpoint: Catches the "city not found" error we raised above.
        # JS: console.log("Calculations aren't working/screen is empty:", error);
        print("Calculations aren't working/screen is empty:", error)
        show_message(f"Error: {error}")

    except requests.exceptions.RequestException as error:
        # Extra case Python needs that JS's fetch() handles more loosely:
        # network failures (no internet, timeout, DNS error, etc.)
        show_message(f"Error: Network problem — {error}")


def show_message(text):
    """
    Simple helper function, same role as JS's showMessagePara().
    JS updated an HTML element; Python just prints to the console.
    """
    print(f"\n[Message] {text}\n")


# Optional UX bonus for classroom: the JS version listens for the 'Enter' key
# on a text input to re-trigger getWeather(). In a console app, every input()
# call already waits for Enter, so we recreate the "search again" experience
# with a simple loop instead.
if __name__ == "__main__":
    while True:
        get_weather()
        again = input("Check another city? (y/n): ").strip().lower()
        if again != "y":
            break