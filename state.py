order_items = []
boxes = "left"

def read_colors_config():
    with open("colors.txt", "r") as f:
        data = f.readlines()

    colors = {}
    for i in range(0, len(data), 7):
        color_name = data[i].strip()
        colors[color_name] = {}

        colors[color_name]['low'] = tuple(map(int, data[i + 1:i + 4]))
        colors[color_name]['high'] = tuple(map(int, data[i + 4:i + 7]))

    return colors
        

colors = read_colors_config()