'''
QR code encoder / decoder Python
I'll install it:
pip install streamlit qrcode[pil] opencv-python

streamlit: Used to create the web app interface.

qrcode: Generates QR codes from text.

cv2 (OpenCV): Detects and decodes QR codes from images.

numpy: Converts image data for OpenCV processing.

PIL.Image: Handles image reading/writing.

io: Used to create in-memory file objects (for downloading images).
'''


import streamlit as st  #Used to create the web app interface.
import qrcode           #Generates QR codes from text.
import cv2              #images.cv2 (OpenCV): Detects and decodes QR codes from images.
import numpy as np      #numpy: Converts image data for OpenCV processing.
from PIL import Image   #PIL.Image: Handles image reading/writing.
import io               #io: Used to create in-memory file objects (for downloading images).

# streamlit Page configuration Sets the Streamlit web page title and layout. and Adds a title to the top of the page.
st.set_page_config(page_title="QR Code Encoder & Decoder", layout="centered")
st.title("🔐 QR Code Encoder & Decoder")

# Tabs for Encode and Decode
tab1, tab2 = st.tabs(["📤 Encode", "📥 Decode"])

# ==========================
#        QR ENCODER
# ==========================
with tab1:
    st.header("QR Code Encoder")
    text_to_encode = st.text_input("Enter text to encode:", "")

    if st.button("Generate QR Code") and text_to_encode:
        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(text_to_encode)
        qr.make(fit=True)

        # Generate image and convert to RGB
        img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

        # Save to buffer for display and download
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()

        # Show and download QR code
        st.image(img, caption="Generated QR Code", use_container_width=False)
        st.download_button(
            label="📥 Download QR Code",
            data=byte_im,
            file_name="qr_code.png",
            mime="image/png"
        )

# ==========================
#        QR DECODER
# ==========================
with tab2:
    st.header("QR Code Decoder")
    uploaded_file = st.file_uploader("Upload a QR Code image", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        # Load and display image
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded QR Code", use_container_width=False)

        # Convert to array for OpenCV
        img_array = np.array(image)
        detector = cv2.QRCodeDetector()

        # Try to detect and decode
        data, bbox, _ = detector.detectAndDecode(img_array)

        if bbox is not None:
            st.info("🔍 QR code was detected in the image.")
        else:
            st.warning("⚠️ No QR code was detected. Try a clearer or uncropped image.")

        if data:
            st.success(f"✅ Decoded Data: `{data}`")
        else:
            st.error("❌ QR code detected but failed to decode. Ensure the image is sharp and well lit.")
