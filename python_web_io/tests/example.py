import time

# custom CSS
print("#logo{height: 32px; width: 32px}#title{font-size:2em}", magic="style")

print(
    magic="img",
    magic_args={
        "id": "logo",
        "src": "https://cdn2.iconfinder.com/data/icons/activity-5/50/1F3A8-artist-palette-1024.png",
    },
)

print("Color palette!", magic="span", magic_args={'id': 'title'})

print(magic="br")

class colorNames:
    def __init__(self):
        pass

    def hex_to_rgb(self, hexcode):
        hexcode = hexcode.lstrip("#")
        return tuple(int(hexcode[i : i + 2], 16) for i in (0, 2, 4))

    def get_col(self, arr, col):
        return map(lambda x: x[col], arr)

    def get_nearest_color_name(self, hex_color):
        import urllib.request
        import csv
        import codecs
        import math

        # load color names from url
        url = "https://unpkg.com/color-name-list/dist/colornames.bestof.csv"
        # fetch the source using urlopen

        response = urllib.request.urlopen(url)
        # parse the fetched data using csv.read
        # codecs allow us to decode the byte response into a string
        csvfile = csv.reader(codecs.iterdecode(response, "utf-8"))

        # skip header
        next(csvfile, None)

        colors = [
            (name, hexcode, self.hex_to_rgb(hexcode)) for name, hexcode in csvfile
        ]

        hex_3d_point = self.hex_to_rgb(hex_color)

        closest_point = min(
            self.get_col(colors, 2),
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
                closest_hex_name = name
                break

        return closest_hex_name

seconds = time.time()
local_time = time.ctime(seconds)
print(f"Local time: {local_time}", magic="small")

input("Click me to start!", magic="button")

hex_color = input("What's your favourite color?", magic="color")
col = colorNames()
print(f"Nice! That colour reminds me of {col.get_nearest_color_name(hex_color)}!")
