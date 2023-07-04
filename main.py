from PIL import Image, ImageOps
import requests
from io import BytesIO
from flask import Flask, render_template, request
import random

app = Flask(__name__)

posterize_bits = 4
blank_rgb_list = [(0,0,0) for i in range(16)]

def get_top_16_colors(url):
    response = requests.get(url)
    img1 = Image.open(BytesIO(response.content)).convert("RGB")
    img2 = ImageOps.posterize(img1, posterize_bits).convert("RGB")
    color_list = sorted(img2.getcolors(img2.size[0]*img2.size[1]), reverse=True)
    top_16_colors = [color[1] for color in color_list[:16]]
    print(top_16_colors)
    return sort_colors(top_16_colors)

def sort_colors(rgb_list):
    rgb_list.sort(key = lambda x: (x[0] + x[1], x[1] + x[2], x[2] + x[0]))
    return sorted(rgb_list)

def get_random_colors(url):
    response = requests.get(url)
    img1 = Image.open(BytesIO(response.content)).convert("RGB")
    img2 = ImageOps.posterize(img1, 8).convert("RGB")
    color_list = [i[1] for i in img2.getcolors(img2.size[0]*img2.size[1])]
    random_colors = random.choices(color_list, k=16)
    return sort_colors(random_colors)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == 'POST' and request.form.get("image-url") != None:
        if request.form.get("search_type") == "random":
            colors = get_random_colors(request.form.get("image-url"))
        else:
            colors = get_top_16_colors(request.form.get("image-url"))
    else:
        colors = blank_rgb_list
    return render_template("index.html", colors=colors)

if __name__ == '__main__':
    app.run(debug=True)