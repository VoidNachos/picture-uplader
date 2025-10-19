from flask import Flask, request, render_template_string
from PIL import Image

app = Flask(__name__)

COLOR_MAP = {
    1: (0, 0, 0),
    2: (255, 0, 0),
    3: (0, 255, 0),
    4: (0, 0, 255),
    5: (255, 255, 0),
    6: (255, 105, 180),
    7: (0, 255, 255),
    8: (255, 255, 255)
}

def closest_color(r, g, b):
    best = None
    best_dist = float('inf')
    for code, (cr, cg, cb) in COLOR_MAP.items():
        dist = (r - cr)**2 + (g - cg)**2 + (b - cb)**2
        if dist < best_dist:
            best = code
            best_dist = dist
    return best

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('image')
        if not file:
            return "No file uploaded!"

        img = Image.open(file.stream)
        width, height = img.size
        total_pixels = width * height

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

        result = f"<h3>Width: {width}<br>Total pixels: {total_pixels}</h3>"
        result += f"<p>\\left[{','.join(map(str, color_codes))}\\right]</p>"
        return result

    return render_template_string('''
        <h2>🎨 Image Color Analyzer</h2>
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="image" accept="image/*"><br><br>
            <input type="submit" value="Analyze">
        </form>
    ''')

if __name__ == "__main__":
    # use port from Render’s environment variable
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
