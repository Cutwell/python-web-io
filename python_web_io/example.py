import time

seconds = time.time()
local_time = time.ctime(seconds)
print(f"Local time: {local_time}", magic="small")

input("Click me to start!", magic="button")

year = int(input("What year were you born?", magic="number"))
age = 2023 - year
print(f"So you must be {age} years old!")

name = input("What's your name?")
print(f"Hello {name}! Nice to meet you!")

color = input("What's your favourite color?", magic="color")
print(color)