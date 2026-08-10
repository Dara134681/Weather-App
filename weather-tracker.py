"""
Weather App — Python Edition (v2 — with extra features)
CodeSmart Academy

This is a Python (tkinter) port of the original HTML / CSS / JavaScript
Weather App, now extended with a few classroom-friendly features:

    - A weather emoji/icon based on current conditions
    - A Celsius / Fahrenheit toggle
    - Extra data: "feels like" temperature, wind speed, and pressure
    - A background color that shifts to match the weather
    - A "Loading..." message while waiting on the network

Run it with:  python weather_app.py
(Requires the 'requests' library — install with: pip install requests)
"""

import tkinter as tk
from tkinter import font
import requests

# ------------------------------------------------------------------
# Instructor setup: your free OpenWeatherMap API key.
# Teaching tip: in a real production app, this would live in an
# environment variable, not directly in the code — but for a
# classroom demo, keeping it visible here makes it easy to explain.
# ------------------------------------------------------------------
API_KEY = "638ed8715b83a4ab1a9b255417142f33"
PLACEHOLDER_TEXT = "Enter city (e.g., London)"

# ------------------------------------------------------------------
# Feature: Weather icons
# Teaching Concept: a dictionary is a perfect tool here — we're
# looking up one value (an emoji) using another value (the weather's
# "main" category) as the key. Same idea as a JS object lookup.
# ------------------------------------------------------------------
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
    Teaching Tip: Explain this the same way as the JS version —
    like ordering food at a restaurant.
      1. We tell the waiter (requests) what we want (the URL).
      2. The waiter walks to the kitchen (OpenWeatherMap's server).
      3. The waiter comes back with a box of food (the response).
      4. We open the box (response.json()) to see what's inside.
    """
    city = city_entry.get().strip()

    if not city or city == PLACEHOLDER_TEXT:
        show_message("Please type a city name.")
        return

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    # Feature: Loading state.
    # Teaching Concept: root.update_idletasks() forces tkinter to redraw
    # the window RIGHT NOW, before the (blocking) network call below.
    # Without this line, "Loading..." would never actually appear on
    # screen — the window wouldn't repaint until get_weather() finishes.
    show_loading()
    root.update_idletasks()

    try:
        response = requests.get(url)

        if response.status_code != 200:
            raise ValueError(f"We couldn't find '{city}'. Please check your spelling.")

        data = response.json()

        global last_weather_data
        last_weather_data = data
        render_result(data)

    except requests.exceptions.RequestException:
        show_message("Error: Could not connect to the weather service.")
    except ValueError as error:
        show_message(f"Error: {error}")
    except (KeyError, IndexError):
        show_message("Error: Something went wrong reading the weather data.")


def render_result(data):
    """
    Draws the result panel from a stored weather data dictionary.
    Separated from get_weather() so the °C/°F toggle can call this
    again WITHOUT re-fetching from the internet.
    """
    name = data["name"]
    country = data["sys"]["country"]
    condition_main = data["weather"][0]["main"]
    description = data["weather"][0]["description"]
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    wind_speed = data["wind"]["speed"]

    temp_c = data["main"]["temp"]
    feels_like_c = data["main"]["feels_like"]

    if use_fahrenheit:
        temp_display = f"{round(celsius_to_fahrenheit(temp_c))}\u00b0F"
        feels_display = f"{round(celsius_to_fahrenheit(feels_like_c))}\u00b0F"
    else:
        temp_display = f"{round(temp_c)}\u00b0C"
        feels_display = f"{round(feels_like_c)}\u00b0C"

    icon = WEATHER_ICONS.get(condition_main, DEFAULT_ICON)

    weather_icon_label.config(text=icon)
    result_title.config(text=f"{name}, {country}")
    result_body.config(
        text=(
            f"Temperature: {temp_display}   (feels like {feels_display})\n"
            f"Weather: {description}\n"
            f"Humidity: {humidity}%   Wind: {wind_speed} m/s   Pressure: {pressure} hPa"
        ),
        fg="#4c5a71",
    )
    result_frame.pack(pady=(15, 0))

    bg_color = WEATHER_BG_COLORS.get(condition_main, DEFAULT_BG)
    root.configure(bg=bg_color)


def show_loading():
    weather_icon_label.config(text="\u23f3")
    result_title.config(text="")
    result_body.config(text="Loading weather data...", fg="#4c5a71")
    result_frame.pack(pady=(15, 0))


def show_message(text):
    weather_icon_label.config(text="\u26a0\ufe0f")
    result_title.config(text="")
    result_body.config(text=text, fg="#e74c3c")
    result_frame.pack(pady=(15, 0))
    root.configure(bg=DEFAULT_BG)


def toggle_units():
    """
    Feature: °C / °F toggle.
    Teaching Concept: flips a boolean, then re-renders the SAME stored
    data — a good example of why saving data in a variable is useful,
    instead of only ever using it once and throwing it away.
    """
    global use_fahrenheit
    use_fahrenheit = not use_fahrenheit
    unit_button.config(text="Switch to \u00b0C" if use_fahrenheit else "Switch to \u00b0F")
    if last_weather_data is not None:
        render_result(last_weather_data)


def on_enter_key(event):
    get_weather()


def clear_placeholder(event):
    if city_entry.get() == PLACEHOLDER_TEXT:
        city_entry.delete(0, tk.END)
        city_entry.config(fg="#4c5a71")


def restore_placeholder(event):
    if not city_entry.get():
        city_entry.insert(0, PLACEHOLDER_TEXT)
        city_entry.config(fg="#a0a7b4")


# ====================================================================
# Build the window — this replaces index.html + style.css
# ====================================================================
root = tk.Tk()
root.title("DAR-A WEATHER APP")
root.geometry("440x520")
root.configure(bg=DEFAULT_BG)
root.resizable(False, False)

title_font = font.Font(family="Segoe UI", size=20, weight="bold")
label_font = font.Font(family="Segoe UI", size=12)
result_title_font = font.Font(family="Segoe UI", size=18, weight="bold")
icon_font = font.Font(family="Segoe UI Emoji", size=36)

card = tk.Frame(root, bg="white", padx=30, pady=30)
card.place(relx=0.5, rely=0.5, anchor="center", width=380)

title_label = tk.Label(card, text="DAR-A Weather App", font=title_font, fg="#4c5a71", bg="white")
title_label.pack(pady=(0, 20))

city_entry = tk.Entry(
    card, font=label_font, fg="#a0a7b4", bg="#f7f9fc",
    relief="flat", justify="center", insertbackground="#4c5a71"
)
city_entry.insert(0, PLACEHOLDER_TEXT)
city_entry.pack(fill="x", ipady=10, pady=(0, 15))
city_entry.bind("<FocusIn>", clear_placeholder)
city_entry.bind("<FocusOut>", restore_placeholder)

check_button = tk.Button(
    card, text="Check Weather", font=("Segoe UI", 11, "bold"),
    bg="#3498db", fg="white", relief="flat", cursor="hand2",
    activebackground="#74b9ff", activeforeground="white",
    command=get_weather,
)
check_button.pack(fill="x", ipady=10)

unit_button = tk.Button(
    card, text="Switch to \u00b0F", font=("Segoe UI", 10),
    bg="#eef2f7", fg="#4c5a71", relief="flat", cursor="hand2",
    activebackground="#dbe4ee",
    command=toggle_units,
)
unit_button.pack(fill="x", ipady=6, pady=(8, 0))

result_frame = tk.Frame(card, bg="white")
weather_icon_label = tk.Label(result_frame, font=icon_font, bg="white")
weather_icon_label.pack()
result_title = tk.Label(result_frame, font=result_title_font, fg="#4c5a71", bg="white")
result_title.pack()
result_body = tk.Label(result_frame, font=label_font, bg="white", justify="center")
result_body.pack(pady=(5, 0))

root.bind("<Return>", on_enter_key)

if __name__ == "__main__":
    root.mainloop()