# \x1b[40m 	Black
# \x1b[41m 	Red
# \x1b[42m 	Green
# \x1b[43m 	Yellow
# \x1b[44m 	Blue
# \x1b[45m 	Magenta
# \x1b[46m 	Cyan
# \x1b[47m 	White
# \x1b[49m 	Default(background color at startup)
# \x1b[100m 	Light Gray
# \x1b[101m 	Light Red
# \x1b[102m 	Light Green
# \x1b[103m 	Light Yellow
# \x1b[104m 	Light Blue
# \x1b[105m 	Light Magenta
# \x1b[106m 	Light Cyan
# \x1b[107m 	Light White

black = "\x1b[40m"
red = "\x1b[41m"
green = "\x1b[42m"
yellow = "\x1b[43m"
blue = "\x1b[44m"
magenta = "\x1b[45m"
cyan = "\x1b[46m"
white = "\x1b[47m"
default = "\x1b[49m"
light_grey = "\x1b[100m"
light_red = "\x1b[101m"
light_green = "\x1b[102m"
light_yellow = "\x1b[103m"
light_blue = "\x1b[104m"
light_magenta = "\x1b[105m"
light_cyan = "\x1b[106m"
light_white = "\x1b[107m"

colors = {
    "black": black,
    "fire": red,
    "exit": green,
    "follower": yellow,
    "glass": blue,
    "stair": magenta,
    "wall": cyan,
    "empty": white,
    "reset": default,
    "object": light_grey,
    "light_red": light_red,
    "door": light_green,
    "nonfollower": light_yellow,
    "broken_glass": light_blue,
    "light_magenta": light_magenta,
    "exit_plan": light_cyan,
    "light_white": light_white
}

color_codes_html = {
    'w': '#0000ff',  # Blue
    'e': '#00ff00',  # Green
    'l': '#a9a9a9',  # Dark Gray
    'n': '#a9a9a9',  # Dark Gray
    'm': '#a9a9a9',  # Dark Gray
    's': '#ff69b4',  # Pink
    'g': '#0000cd',  # Medium Blue
    'd': '#32cd32',  # Lime Green
    ' ': '#ffffff',  # White
    '1': '#ffffff',  # White
    '2': '#ffffff',  # White
    'f': '#ff0000',  # Red
    'b': '#4682b4',  # Steel Blue
    'p': '#ffd700',  # Gold
    'fo': '#ffa500',  # Orange
    'nf': '#ffff00'  # Yellow
}
