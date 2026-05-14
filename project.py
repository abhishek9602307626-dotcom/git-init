import streamlit as st
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from io import BytesIO

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Digital Image Processing Website",
    layout="wide"
)

st.title("📷 Digital Image Processing Website")
st.write("Built using Python, OpenCV and Streamlit")

# ---------------- SIDEBAR ----------------

st.sidebar.title("Image Processing Menu")

option = st.sidebar.selectbox(
    "Choose Operation",
    [
        "Original",
        "Black & White",
        "Blur Filter",
        "Edge Detection",
        "Brightness & Contrast",
        "Rotate Image",
        "Resize Image",
        "Histogram",
        "Fourier Transform",
        "Draw Shapes",
        "Add Text",
        "Image Information",
        "Real-Time Webcam Filter"
    ]
)

# ---------------- IMAGE UPLOAD ----------------

uploaded_file = st.file_uploader(
    "Upload an Image",
    type=["jpg", "png", "jpeg"]
)

# ---------------- MAIN PROCESSING ----------------

if uploaded_file is not None:

    image = Image.open(uploaded_file)

    img = np.array(image)

    original = img.copy()

    # Convert RGBA to RGB if needed
    if len(img.shape) == 3 and img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)

    # ---------------- BEFORE / AFTER ----------------

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original Image")
        st.image(original, use_container_width=True)

    processed_img = img.copy()

    # ---------------- BLACK & WHITE ----------------

    if option == "Black & White":

        processed_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # ---------------- BLUR FILTER ----------------

    elif option == "Blur Filter":

        k = st.sidebar.slider("Kernel Size", 1, 31, 15)

        if k % 2 == 0:
            k += 1

        processed_img = cv2.GaussianBlur(img, (k, k), 0)

    # ---------------- EDGE DETECTION ----------------

    elif option == "Edge Detection":

        low = st.sidebar.slider("Lower Threshold", 0, 255, 100)

        high = st.sidebar.slider("Upper Threshold", 0, 255, 200)

        processed_img = cv2.Canny(img, low, high)

    # ---------------- BRIGHTNESS & CONTRAST ----------------

    elif option == "Brightness & Contrast":

        brightness = st.sidebar.slider("Brightness", -100, 100, 0)

        contrast = st.sidebar.slider("Contrast", 1.0, 3.0, 1.0)

        processed_img = cv2.convertScaleAbs(
            img,
            alpha=contrast,
            beta=brightness
        )

    # ---------------- ROTATE IMAGE ----------------

    elif option == "Rotate Image":

        rotate_option = st.sidebar.selectbox(
            "Rotation",
            [
                "90 Clockwise",
                "90 CounterClockwise",
                "180"
            ]
        )

        if rotate_option == "90 Clockwise":
            processed_img = cv2.rotate(
                img,
                cv2.ROTATE_90_CLOCKWISE
            )

        elif rotate_option == "90 CounterClockwise":
            processed_img = cv2.rotate(
                img,
                cv2.ROTATE_90_COUNTERCLOCKWISE
            )

        elif rotate_option == "180":
            processed_img = cv2.rotate(
                img,
                cv2.ROTATE_180
            )

    # ---------------- RESIZE IMAGE ----------------

    elif option == "Resize Image":

        width = st.sidebar.slider("Width", 100, 1000, 300)

        height = st.sidebar.slider("Height", 100, 1000, 300)

        processed_img = cv2.resize(img, (width, height))

    # ---------------- HISTOGRAM ----------------

    elif option == "Histogram":

        fig, ax = plt.subplots()

        if len(img.shape) == 3:

            colors = ('b', 'g', 'r')

            for i, color in enumerate(colors):

                hist = cv2.calcHist(
                    [img],
                    [i],
                    None,
                    [256],
                    [0, 256]
                )

                ax.plot(hist, color=color)

        else:

            hist = cv2.calcHist(
                [img],
                [0],
                None,
                [256],
                [0, 256]
            )

            ax.plot(hist)

        ax.set_title("Histogram")

        st.pyplot(fig)

        processed_img = img

    # ---------------- FOURIER TRANSFORM ----------------

    elif option == "Fourier Transform":

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        f = np.fft.fft2(gray)

        fshift = np.fft.fftshift(f)

        magnitude = 20 * np.log(np.abs(fshift) + 1)

        processed_img = magnitude

    # ---------------- DRAW SHAPES ----------------

    elif option == "Draw Shapes":

        shape = st.sidebar.selectbox(
            "Select Shape",
            [
                "Rectangle",
                "Circle",
                "Line"
            ]
        )

        processed_img = img.copy()

        if shape == "Rectangle":

            cv2.rectangle(
                processed_img,
                (50, 50),
                (300, 300),
                (0, 255, 0),
                3
            )

        elif shape == "Circle":

            cv2.circle(
                processed_img,
                (250, 250),
                100,
                (255, 0, 0),
                3
            )

        elif shape == "Line":

            cv2.line(
                processed_img,
                (50, 50),
                (400, 400),
                (0, 0, 255),
                3
            )

    # ---------------- ADD TEXT ----------------

    elif option == "Add Text":

        text = st.sidebar.text_input(
            "Enter Text",
            "OpenCV Project"
        )

        processed_img = img.copy()

        cv2.putText(
            processed_img,
            text,
            (50, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (255, 0, 0),
            3
        )

    # ---------------- IMAGE INFORMATION ----------------

    elif option == "Image Information":

        st.subheader("Image Information")

        st.write(f"Width : {img.shape[1]}")

        st.write(f"Height : {img.shape[0]}")

        st.write(f"Channels : {img.shape[2]}")

        st.write(f"Image Shape : {img.shape}")

        processed_img = img

    # ---------------- REAL-TIME WEBCAM ----------------

    elif option == "Real-Time Webcam Filter":

        run = st.checkbox("Start Webcam")

        FRAME_WINDOW = st.image([])

        camera = cv2.VideoCapture(0)

        while run:

            ret, frame = camera.read()

            if not ret:
                st.write("Camera Not Working")
                break

            gray = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2GRAY
            )

            FRAME_WINDOW.image(gray)

        camera.release()

        processed_img = img

    # ---------------- SHOW OUTPUT ----------------

    with col2:

        st.subheader("Processed Image")

        st.image(
            processed_img,
            use_container_width=True
        )

    # ---------------- DOWNLOAD BUTTON ----------------

    st.subheader("Download Processed Image")

    if len(processed_img.shape) == 2:

        save_img = Image.fromarray(processed_img)

    else:

        save_img = Image.fromarray(
            cv2.cvtColor(
                processed_img,
                cv2.COLOR_BGR2RGB
            )
        )

    buf = BytesIO()

    save_img.save(buf, format="PNG")

    byte_im = buf.getvalue()

    st.download_button(
        label="Download Image",
        data=byte_im,
        file_name="processed_image.png",
        mime="image/png"
    )

else:

    st.info("Please upload an image to begin.")