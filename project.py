# =========================================================
# FAST ULTIMATE IMAGE PROCESSING WEBSITE
# =========================================================

import streamlit as st
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Fast Image Processing Website",
    layout="wide"
)

st.title("⚡ Fast Ultimate Image Processing Website")

# =========================================================
# SIDEBAR MENU
# =========================================================

option = st.sidebar.selectbox(
    "Select Operation",
    [
        "Original Image",
        "Black & White",
        "Blur Filter",
        "Edge Detection",
        "Brightness & Contrast",
        "Rotate Image",
        "Resize Image",
        "Flip Image",
        "Histogram",
        "Fourier Transform",
        "Thresholding",
        "RGB Channel Split",
        "Negative Image",
        "Morphological Operations",
        "Add Text",
        "Face Detection",
        "Color Detection",
        "Crop Tool",
        "Watermark",
        "Oil Painting",
        "Image Information"
    ]
)

# =========================================================
# IMAGE SOURCE
# =========================================================

st.sidebar.subheader("📤 Image Source")

input_option = st.sidebar.radio(
    "Choose Input Method",
    [
        "Upload Image",
        "Laptop Camera"
    ]
)

image = None

# =========================================================
# UPLOAD IMAGE
# =========================================================

if input_option == "Upload Image":

    uploaded_file = st.file_uploader(
        "Upload Image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:

        pil_image = Image.open(uploaded_file)

        # FAST RESIZE
        pil_image.thumbnail((900, 900))

        image = np.array(pil_image)

# =========================================================
# LAPTOP CAMERA INPUT
# =========================================================

elif input_option == "Laptop Camera":

    st.info("📸 Take Photo From Laptop Camera")

    camera_image = st.camera_input("Take Photo")

    if camera_image is not None:

        pil_image = Image.open(camera_image)

        pil_image.thumbnail((900, 900))

        image = np.array(pil_image)

        st.success("✅ Photo Captured Successfully")

# =========================================================
# MAIN PROGRAM
# =========================================================

if image is not None:

    # RGB TO BGR
    if len(image.shape) == 3:

        image = cv2.cvtColor(
            image,
            cv2.COLOR_RGB2BGR
        )

    processed_img = image.copy()

    # =====================================================
    # ORIGINAL IMAGE
    # =====================================================

    if option == "Original Image":

        processed_img = image.copy()

    # =====================================================
    # BLACK & WHITE
    # =====================================================

    elif option == "Black & White":

        processed_img = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

    # =====================================================
    # BLUR FILTER
    # =====================================================

    elif option == "Blur Filter":

        blur_value = st.slider(
            "Blur Strength",
            1,
            15,
            5
        )

        processed_img = cv2.GaussianBlur(
            image,
            (blur_value * 2 + 1, blur_value * 2 + 1),
            0
        )

    # =====================================================
    # EDGE DETECTION
    # =====================================================

    elif option == "Edge Detection":

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        t1 = st.slider(
            "Threshold 1",
            0,
            255,
            100
        )

        t2 = st.slider(
            "Threshold 2",
            0,
            255,
            200
        )

        processed_img = cv2.Canny(
            gray,
            t1,
            t2
        )

    # =====================================================
    # BRIGHTNESS & CONTRAST
    # =====================================================

    elif option == "Brightness & Contrast":

        brightness = st.slider(
            "Brightness",
            -100,
            100,
            0
        )

        contrast = st.slider(
            "Contrast",
            0.5,
            3.0,
            1.0
        )

        processed_img = cv2.convertScaleAbs(
            image,
            alpha=contrast,
            beta=brightness
        )

    # =====================================================
    # ROTATE IMAGE
    # =====================================================

    elif option == "Rotate Image":

        angle = st.slider(
            "Angle",
            0,
            360,
            90
        )

        h, w = image.shape[:2]

        matrix = cv2.getRotationMatrix2D(
            (w // 2, h // 2),
            angle,
            1
        )

        processed_img = cv2.warpAffine(
            image,
            matrix,
            (w, h)
        )

    # =====================================================
    # RESIZE IMAGE
    # =====================================================

    elif option == "Resize Image":

        width = st.slider(
            "Width",
            100,
            1200,
            image.shape[1]
        )

        height = st.slider(
            "Height",
            100,
            1200,
            image.shape[0]
        )

        processed_img = cv2.resize(
            image,
            (width, height)
        )

    # =====================================================
    # FLIP IMAGE
    # =====================================================

    elif option == "Flip Image":

        flip_type = st.selectbox(
            "Flip Type",
            ["Horizontal", "Vertical"]
        )

        if flip_type == "Horizontal":

            processed_img = cv2.flip(
                image,
                1
            )

        else:

            processed_img = cv2.flip(
                image,
                0
            )

    # =====================================================
    # HISTOGRAM
    # =====================================================

    elif option == "Histogram":

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        hist = cv2.calcHist(
            [gray],
            [0],
            None,
            [256],
            [0, 256]
        )

        fig, ax = plt.subplots(figsize=(4, 2))

        ax.plot(hist)

        st.pyplot(fig)

        processed_img = gray

    # =====================================================
    # FOURIER TRANSFORM
    # =====================================================

    elif option == "Fourier Transform":

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        f = np.fft.fft2(gray)

        fshift = np.fft.fftshift(f)

        magnitude = 20 * np.log(
            np.abs(fshift) + 1
        )

        processed_img = cv2.normalize(
            magnitude,
            None,
            0,
            255,
            cv2.NORM_MINMAX
        ).astype(np.uint8)

    # =====================================================
    # THRESHOLDING
    # =====================================================

    elif option == "Thresholding":

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        threshold_value = st.slider(
            "Threshold Value",
            0,
            255,
            127
        )

        _, processed_img = cv2.threshold(
            gray,
            threshold_value,
            255,
            cv2.THRESH_BINARY
        )

    # =====================================================
    # RGB CHANNEL SPLIT
    # =====================================================

    elif option == "RGB Channel Split":

        b, g, r = cv2.split(image)

        channel = st.selectbox(
            "Select Channel",
            ["Red", "Green", "Blue"]
        )

        if channel == "Red":

            processed_img = r

        elif channel == "Green":

            processed_img = g

        else:

            processed_img = b

    # =====================================================
    # NEGATIVE IMAGE
    # =====================================================

    elif option == "Negative Image":

        processed_img = 255 - image

    # =====================================================
    # MORPHOLOGICAL OPERATIONS
    # =====================================================

    elif option == "Morphological Operations":

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        _, binary = cv2.threshold(
            gray,
            127,
            255,
            cv2.THRESH_BINARY
        )

        kernel = np.ones((3, 3), np.uint8)

        morph_type = st.selectbox(
            "Operation",
            ["Erosion", "Dilation"]
        )

        if morph_type == "Erosion":

            processed_img = cv2.erode(
                binary,
                kernel,
                iterations=1
            )

        else:

            processed_img = cv2.dilate(
                binary,
                kernel,
                iterations=1
            )

    # =====================================================
    # ADD TEXT
    # =====================================================

    elif option == "Add Text":

        text = st.text_input(
            "Enter Text",
            "Hello"
        )

        processed_img = image.copy()

        cv2.putText(
            processed_img,
            text,
            (50, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (0, 255, 0),
            3
        )

    # =====================================================
    # FACE DETECTION
    # =====================================================

    elif option == "Face Detection":

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades +
            'haarcascade_frontalface_default.xml'
        )

        faces = face_cascade.detectMultiScale(
            gray,
            1.1,
            4
        )

        processed_img = image.copy()

        for (x, y, w, h) in faces:

            cv2.rectangle(
                processed_img,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

    # =====================================================
    # COLOR DETECTION
    # =====================================================

    elif option == "Color Detection":

        hsv = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2HSV
        )

        lower = np.array([0, 120, 70])
        upper = np.array([10, 255, 255])

        mask = cv2.inRange(
            hsv,
            lower,
            upper
        )

        processed_img = cv2.bitwise_and(
            image,
            image,
            mask=mask
        )

    # =====================================================
    # CROP TOOL
    # =====================================================

    elif option == "Crop Tool":

        h, w = image.shape[:2]

        x1 = st.slider("Start X", 0, w - 1, 0)
        y1 = st.slider("Start Y", 0, h - 1, 0)

        x2 = st.slider("End X", x1 + 1, w, w)
        y2 = st.slider("End Y", y1 + 1, h, h)

        processed_img = image[
            y1:y2,
            x1:x2
        ]

    # =====================================================
    # WATERMARK
    # =====================================================

    elif option == "Watermark":

        watermark = st.text_input(
            "Watermark",
            "© My Website"
        )

        processed_img = image.copy()

        cv2.putText(
            processed_img,
            watermark,
            (30, image.shape[0] - 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2
        )

    # =====================================================
    # OIL PAINTING
    # =====================================================

    elif option == "Oil Painting":

        processed_img = cv2.stylization(
            image,
            sigma_s=40,
            sigma_r=0.4
        )

    # =====================================================
    # IMAGE INFORMATION
    # =====================================================

    elif option == "Image Information":

        st.subheader("📄 Image Details")

        st.write(f"Width: {image.shape[1]}")
        st.write(f"Height: {image.shape[0]}")
        st.write(f"Channels: {image.shape[2]}")
        st.write(f"Data Type: {image.dtype}")

        processed_img = image.copy()

    # =====================================================
    # BEFORE & AFTER
    # =====================================================

    st.subheader("📷 Before & After Comparison")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### Original Image")

        st.image(
            cv2.cvtColor(
                image,
                cv2.COLOR_BGR2RGB
            ),
            width=300
        )

    with col2:

        st.markdown("### Processed Image")

        if len(processed_img.shape) == 2:

            st.image(
                processed_img,
                width=300
            )

        else:

            st.image(
                cv2.cvtColor(
                    processed_img,
                    cv2.COLOR_BGR2RGB
                ),
                width=300
            )

    # =====================================================
    # DOWNLOAD BUTTON
    # =====================================================

    if processed_img is not None:

        if len(processed_img.shape) == 2:

            download_img = processed_img

        else:

            download_img = cv2.cvtColor(
                processed_img,
                cv2.COLOR_BGR2RGB
            )

        result = cv2.imencode(
            '.png',
            np.array(download_img)
        )[1].tobytes()

        st.download_button(
            label="⬇️ Download Processed Image",
            data=result,
            file_name="processed_image.png",
            mime="image/png"
        )

# =========================================================
# NO IMAGE
# =========================================================

else:

    st.info("📤 Please upload or capture an image")