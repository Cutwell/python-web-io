import urllib.request
import csv
import codecs
import math
import python_web_io as io


def load_csv(url):
    # fetch the source using urlopen
    response = urllib.request.urlopen(url)

    # parse the fetched data using csv.read
    # codecs allow us to decode the byte response into a string
    csvfile = csv.reader(codecs.iterdecode(response, "utf-8"))

    # skip header
    next(csvfile, None)

    return csvfile


@io.cache_to_file("cache.pickle")
def load_colors(url):
    csvfile = load_csv(url)

    colors = [(name, hexcode, hex_to_rgb(hexcode)) for name, hexcode in csvfile]

    return colors


def hex_to_rgb(hexcode):
    hexcode = hexcode.lstrip("#")
    return tuple(int(hexcode[i : i + 2], 16) for i in (0, 2, 4))


def get_col(arr, col):
    return map(lambda x: x[col], arr)


@io.cache_to_file("cache.pickle")
def get_nearest_color_name(hex_color):
    colors = load_colors("https://unpkg.com/color-name-list/dist/colornames.bestof.csv")

    hex_3d_point = hex_to_rgb(hex_color)

    closest_point = min(
        get_col(colors, 2),
        key=lambda point: math.hypot(
            hex_3d_point[2] - point[2],
            hex_3d_point[1] - point[1],
            hex_3d_point[0] - point[0],
        ),
    )

    closest_hex = (
        f"#{closest_point[0] << 16 | closest_point[1] << 8 | closest_point[2]:06x}"
    )

    for name, hexcode, rgb in colors:
        if hexcode == closest_hex:
            return name


def main():
    print("<style>#logo{height: 32px; width: 32px;}#title{font-size:2em}</style>")

    print(
        "<img id='logo' src='https://cdn2.iconfinder.com/data/icons/activity-5/50/1F3A8-artist-palette-1024.png'>",
        "<span id='title'>Color palette!</span>",
        "<br>"
    )

    hex_color = input("What's your favourite color?", type="color")    
    print(f"Nice! That colour looks like {get_nearest_color_name(hex_color)}!")

if __name__ == "__main__":
    main()
