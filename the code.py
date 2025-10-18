from flask import Flask, request, render_template_string
from PIL import Image

app = Flask(__name__)

# 🎨 Color codes
COLOR_MAP = {
    1: (0, 0, 0),       # black
    2: (255, 0, 0),     # red
    3: (0, 255, 0),     # green
    4: (0, 0, 255),     # blue
    5: (255, 255, 0),   # yellow
    6: (255, 105, 180), # pink
    7: (0, 255, 255),   # teal
    8: (255, 255, 255)  # white
}

def closest_color(r, g, b):
    best = None
    best_dist = float('inf')
    for code, (cr, cg, cb) in COLOR_MAP.items():
        dist = (r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2
        if dist < best_dist:
            best = code
            best_dist = dist
    return best

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['image']
        if not file:
            return "No file uploaded!"

        img = Image.open(file)
        width, height = img.size
        total_pixels = width * height

        # 🔽 Downscale until total pixels ≤ 10,000
        while total_pixels > 10000:
            img = img.resize((width // 2, height // 2))
            width, height = img.size
            total_pixels = width * height

        pixels = img.load()
        color_codes = []
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y][:3]
                color_codes.append(closest_color(r, g, b))

        # 🧾 Build LaTeX-style output
        result = f"<h3>Width: {width}<br>Total pixels: {total_pixels}</h3>"
        result += f"<p>\\left[{','.join(map(str, color_codes))}\\right]</p>"
        return result

    # 🖼 Upload form
    return render_template_string('''
        <h2>🎨 Image Color Analyzer</h2>
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="image" accept="image/*"><br><br>
            <input type="submit" value="Analyze">
        </form>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
