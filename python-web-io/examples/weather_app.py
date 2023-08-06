import codecs
import csv
import datetime
import json
import urllib.request

import pandas as pd

import python_web_io as io

"""
Datasets:
countries_cities_coords: https://simplemaps.com/data/world-cities
countries_continents: https://raw.githubusercontent.com/dbouquin/IS_608/master/NanosatDB_munging/Countries-Continents.csv
"""

@io.cache_to_file("cache.pickle")
def get_csv(url: str = None, filepath: str = None):
    """
    Load CSV file from filepath or URL.
    Loads from URL if specified, else from filepath if specified, else raises exception.

    Arguments:
        url (str): URL of CSV file.
        filepath (str): filepath of CSV file.

    Returns:
        df (pandas.Dataframe): Pandas DataFrame object.
    """

    if url:
        # fetch the source using urlopen
        response = urllib.request.urlopen(url)

        # parse the fetched data using csv.read
        # codecs allow us to decode the byte response into a string
        csvfile = csv.reader(codecs.iterdecode(response, "utf-8"))

        headers = next(csvfile, None)

        df = pd.DataFrame(list(csvfile), columns=headers)

    elif filepath:
        with open(filepath, "r") as file:
            csvfile = csv.reader(file, delimiter=",")

            headers = next(csvfile, None)

            df = pd.DataFrame(list(csvfile), columns=headers)

    else:
        raise Exception("URL or filepath must be specified.")

    return df


def get_weather(latitude: str, longitude: str):
    """
    Make POST request to https://open-meteo.com/ API to get weather information.

    Arguments:
        latitude (str): coordinate of target city.
        longitude (str): coordinate of target city.

    Returns:
        weather (dict): dictionary parsed from API JSON response.

    Example output:
        {
            "current_weather": {
                "time": "2022-01-01T15:00"
                "temperature": 2.4, "weathercode": 3,
                "windspeed": 11.9, "winddirection": 95.0,
            },
            "hourly": {
                "time": ["2022-07-01T00:00","2022-07-01T01:00", ...]
                "windspeed_10m": [3.16,3.02,3.3,3.14,3.2,2.95, ...],
                "temperature_2m": [13.7,13.3,12.8,12.3,11.8, ...],
                "relativehumidity_2m": [82,83,86,85,88,88,84,76, ...],
            }
        }
    """

    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true&hourly=temperature_2m,relativehumidity_2m,windspeed_10m"

    with urllib.request.urlopen(url) as response:
        weather = json.loads(response.read())

    return weather


def degrees_to_direction(degrees):
    dirs = [
        "North",
        "North-North-East",
        "North-East",
        "East-North-East",
        "East",
        "East-South-East",
        "South-East",
        "South-South-East",
        "South",
        "South-South-West",
        "South-West",
        "West-South-West",
        "West",
        "West-North-West",
        "North-West",
        "North-North-West",
    ]
    index = round(degrees / (360.0 / len(dirs))) % len(dirs)
    return dirs[index]


def main():
    print("#🗺️ Global weather webapp")
    print("<br>")

    # load countries -> continent mapping from URL
    countries_continents = get_csv(
        url="https://raw.githubusercontent.com/dbouquin/IS_608/master/NanosatDB_munging/Countries-Continents.csv"
    )

    # load cities + lat, lon coordinates -> countries mapping from file
    countries_cities_coords = get_csv(filepath="examples/worldcities.csv")

    continents = list(set(list(countries_continents["Continent"])))

    continent = input(
        "Select continent:",
        options=continents,
        type="button",
        _class="continents",
    )

    print("<small class='countries'>", continent, "</small>")

    # hide continent selection after input
    print("<style>.continents{display: none!important}</style>")

    countries = countries_continents.loc[
        countries_continents["Continent"] == continent, "Country"
    ]

    country = input(
        "Select country:",
        options=list(countries),
        type="button",
        _class="countries",
    )

    print(f"<small class='cities'>{continent}, {country}</small>")

    # hide country selection after input
    print("<style>.countries{display: none!important}</style>")

    cities = countries_cities_coords.loc[
        countries_cities_coords["country"] == country, ["city", "lat", "lng"]
    ]

    cities["Location"] = cities.apply(
        lambda row: f"{row['city']} ({row['lat']}, {row['lng']})", axis=1
    )
    
    options=cities["Location"].tolist()
    # if this case is true, the app will halt here till a reset
    if len(options) == 0:
        print(f"No cities with weather data available for {continent}, {country}.")
        raise io.RunPyInterrupt

    location = input(
        "Select city:",
        options=options,
        type="button",
        _class="cities",
    )

    print(f"<small>{continent}, {country}, {location}</small>")

    # hide city selection after input
    print("<style>.cities{display: none!important}</style>")

    row = cities.loc[cities["Location"] == location].iloc[0]

    city = row["city"]
    latitude = row["lat"]
    longitude = row["lng"]

    weather = get_weather(latitude, longitude)

    dt = datetime.datetime.fromisoformat(weather["current_weather"]["time"])
    day_of_week = dt.strftime("%A")
    date_time_str = dt.strftime("%B %d, %Y %I:%M %p")
    winddirection = weather["current_weather"]["winddirection"]

    print(
        f"###Current weather for {city}:<br>",
        f"Last updated ↻: {day_of_week}, {date_time_str}<br>",
        f"Temperature 🌡️: {weather['current_weather']['temperature']}°C<br>",
        f"Wind speed 💨: {weather['current_weather']['windspeed']} km/h, Wind direction 🧭: {winddirection}° ({degrees_to_direction(winddirection)})"
    )