import streamlit as st
from PIL import Image

# === 8 base colors ===
base_colors = [
    (0, 0, 0),       # 1 = black
    (255, 0, 0),     # 2 = red
    (0, 255, 0),     # 3 = green
    (0, 0, 255),     # 4 = blue
    (255, 255, 0),   # 5 = yellow
    (255, 0, 255),   # 6 = pink
    (0, 255, 255),   # 7 = teal
    (255, 255, 255)  # 8 = white
]

def color_distance(c1, c2):
    return (c1[0]-c2[0])**2 + (c1[1]-c2[1])**2 + (c1[2]-c2[2])**2

def find_closest_color(pixel):
    min_dist = float('inf')
    best_code = 1
    for i, color in enumerate(base_colors):
        d = color_distance(pixel, color)
        if d < min_dist:
            min_dist = d
            best_code = i + 1
    return best_code

def reduce_image(img, max_pixels=10000):
    width, height = img.size
    total_pixels = width * height
    if total_pixels <= max_pixels:
        return img
    ratio = (max_pixels / total_pixels) ** 0.5
    new_w = int(width * ratio)
    new_h = int(height * ratio)
    return img.resize((new_w, new_h), Image.LANCZOS)

def process_image(img):
    width, height = img.size
    total_pixels = width * height

    resized = None
    if total_pixels > 10000:
        resized = reduce_image(img)
        img = resized
        width, height = img.size
        total_pixels = width * height

    pixels = list(img.getdata())
    codes = [find_closest_color(p) for p in pixels]

    latex_codes = "\\left[" + ",".join(str(c) for c in codes) + "\\right]"
    return latex_codes, width, height, total_pixels, resized

# === STREAMLIT APP ===
st.set_page_config(page_title="Pixel Color Coder 🎨", layout="centered")

st.title("🎨 Pixel Color Coder")
st.write("Upload an image and I’ll turn it into an 8-color LaTeX-style pixel code array!")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, caption="Original Image", use_container_width=True)

    latex_codes, width, height, total_pixels, resized = process_image(image)

    st.subheader("🖼️ Image Info")
    st.write(f"**Width:** {width}")
    st.write(f"**Height:** {height}")
    st.write(f"**Total Pixels:** {total_pixels}")

    if resized:
        st.warning("Image was resized to stay under 10,000 pixels.")
        st.image(resized, caption="Resized Image", use_container_width=True)

    st.subheader("📜 Generated Code:")
    st.code(latex_codes, language="latex")

    st.download_button(
        label="💾 Download Code as .txt",
        data=latex_codes,
        file_name="pixel_codes.txt",
        mime="text/plain"
    )
else:
    st.info("👆 Upload an image to get started!")
