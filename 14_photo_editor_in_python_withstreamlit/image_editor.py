'''
streamlit: Web app framework for building UIs.

PIL (Pillow): Used for image loading, processing, filtering, drawing.

io: For converting images to bytes for downloading.


'''
import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont
import io


# Sets the page title and layout for the Streamlit app.
st.set_page_config(page_title="Photo Editor Pro", layout="centered")
st.title("🖼️ Image Manipulation App")

#Allows users to upload images and accepts JPG, JPEG, and PNG formats.
uploaded_file = st.file_uploader("📤 Upload an Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Loads the image and creates a copy to apply edits without changing the original. Converts the image to RGB mode.
    original_image = Image.open(uploaded_file).convert("RGB")
    image = original_image.copy()

    st.image(original_image, caption="📷 Original Image", use_container_width=True) # shows the orignal image which user uploaded 

    # === Filters Section ===
    with st.expander("🎛️ Filters"):
        grayscale = st.checkbox("Grayscale")
        blur_radius = st.slider("🌫️ Blur Radius", 0, 10, 0)
        brightness = st.slider("💡 Brightness", 0.5, 3.0, 1.0)
        contrast = st.slider("🌓 Contrast", 0.5, 3.0, 1.0)

    # === Rotation of image===
    with st.expander("🔄 Rotate Image"):
        angle = st.slider("Rotation Angle", -180, 180, 0)

    # === Crop Section ===
    with st.expander("✂️ Crop Image"):
        width, height = image.size
        left = st.number_input("Left", 0, width - 1, 0)
        top = st.number_input("Top", 0, height - 1, 0)
        right = st.number_input("Right", left + 1, width, width)
        bottom = st.number_input("Bottom", top + 1, height, height)

    # === Drawing Section ===
    with st.expander("✏️ Draw on Image"):
        draw_shape = st.selectbox("Draw shape", ["None", "Rectangle", "Ellipse"])
        shape_color = st.color_picker("Shape color", "#FF0000")
        shape_start = st.slider("Start (X, Y)", 0, min(width, height), (10, 10))
        shape_end = st.slider("End (X, Y)", 0, min(width, height), (100, 100))

        add_text = st.checkbox("Add Text")
        if add_text:
            text_content = st.text_input("Text")
            text_position = st.slider("Text Position (X, Y)", 0, min(width, height), (50, 50))
            text_color = st.color_picker("Text Color", "#000000")

    # === Apply Filters ===
    if grayscale:
        image = image.convert("L")
    if blur_radius > 0:
        image = image.filter(ImageFilter.GaussianBlur(blur_radius))
    if brightness != 1.0:
        image = ImageEnhance.Brightness(image).enhance(brightness)
    if contrast != 1.0:
        image = ImageEnhance.Contrast(image).enhance(contrast)
    if angle != 0:
        image = image.rotate(angle, expand=True)
    if right > left and bottom > top:
        image = image.crop((left, top, right, bottom))

    # Convert to RGB for drawing if needed
    if image.mode != "RGB":
        image = image.convert("RGB")

    draw = ImageDraw.Draw(image)

    # Draw shape
    if draw_shape != "None":
        coords = [shape_start, shape_end]
        if draw_shape == "Rectangle":
            draw.rectangle(coords, outline=shape_color, width=3)
        elif draw_shape == "Ellipse":
            draw.ellipse(coords, outline=shape_color, width=3)

    # Add text on image if needed
    if add_text and text_content:
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()
        draw.text(text_position, text_content, fill=text_color, font=font)

    # === Show result of filterations===
    st.markdown("## 🖼️ Modified Image Preview")
    st.image(image, use_container_width=True)

    # === Download options ===
    with st.expander("💾 Download Options"):
        format_option = st.selectbox("Download Format", ["PNG", "JPEG", "WEBP"])
        if format_option in ["JPEG", "WEBP"]:
            quality = st.slider("Image Quality", 10, 100, 90)
        else:
            quality = None

    buf = io.BytesIO()
    if format_option == "PNG":
        image.save(buf, format="PNG")
        ext = "png"
    elif format_option == "JPEG":
        image.save(buf, format="JPEG", quality=quality)
        ext = "jpg"
    elif format_option == "WEBP":
        image.save(buf, format="WEBP", quality=quality)
        ext = "webp"

    st.download_button(f"📥 Download as {ext.upper()}", data=buf.getvalue(),
                       file_name=f"edited_image.{ext}", mime=f"image/{ext}")

# Footer
st.markdown("---")
st.markdown("✨ Made with ❤️ using Python, Streamlit & Pillow.")
st.markdown("✨ Photo Manipulation Project. By: Zahida Raees")
