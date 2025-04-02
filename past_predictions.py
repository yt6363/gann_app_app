import streamlit as st
import os
import base64

def past_predictions():
    # Remove st.set_page_config from here
    st.markdown(
        """
        <style>
        .main {
            padding: 0 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("Past Predictions")
    st.write("Explore past predictions and their outcomes.")

    # Media directory
    media_dir = "Media"

    # Verify directory exists
    if not os.path.exists(media_dir):
        st.error("The 'Media' directory does not exist. Please add it to your project.")
        return

    # Filter valid media files
    media_files = [
        file for file in os.listdir(media_dir)
        if file.lower().endswith(("jpg", "jpeg", "png", "mp4", "mov", "avi"))
    ]
    if not media_files:
        st.warning("No valid media files found in the 'Media' directory.")
        return

    # Prepare Streamlit-compatible paths
    def get_encoded_file(file_path):
        """Encode media files to base64 for embedding in HTML."""
        with open(file_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
        return encoded

    # Generate HTML slideshow
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {
                margin: 0;
                padding: 0;
                overflow: hidden; /* Hide scrollbars for a clean full-screen look */
            }
            .slideshow-container {
                width: 100vw; /* Full viewport width */
                height: 100vh; /* Full viewport height */
                margin: 0;
                position: fixed; /* Ensure it fills the entire screen */
                top: 0;
                left: 0;
                background-color: #000; /* Black background for better visibility */
                overflow: hidden;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .slides {
                display: none;
            }
            .slides img, .slides video {
                max-width: 100%;
                max-height: 100%;
                width: auto;
                height: auto;
            }
            .prev, .next {
                cursor: pointer;
                position: absolute;
                top: 50%;
                width: auto;
                padding: 16px;
                color: white;
                font-weight: bold;
                font-size: 24px;
                transition: 0.6s ease;
                border-radius: 3px;
                background-color: rgba(0,0,0,0.5);
                user-select: none;
            }
            .prev {
                left: 10px;
                transform: translateY(-50%);
            }
            .next {
                right: 10px;
                transform: translateY(-50%);
            }
            .prev:hover, .next:hover {
                background-color: rgba(0,0,0,0.8);
            }
        </style>
    </head>
    <body>
        <div class="slideshow-container">
    """

    for i, file in enumerate(media_files):
        file_path = os.path.join(media_dir, file)
        if file.lower().endswith(("jpg", "jpeg", "png")):
            encoded_file = get_encoded_file(file_path)
            html_content += f"""
            <div class="slides">
                <img src="data:image/jpeg;base64,{encoded_file}" alt="Slide {i+1}">
            </div>
            """
        elif file.lower().endswith(("mp4", "mov", "avi")):
            encoded_file = get_encoded_file(file_path)
            html_content += f"""
            <div class="slides">
                <video controls>
                    <source src="data:video/mp4;base64,{encoded_file}" type="video/mp4">
                </video>
            </div>
            """

    html_content += """
        <a class="prev" onclick="plusSlides(-1)">&#10094;</a>
        <a class="next" onclick="plusSlides(1)">&#10095;</a>
        <script>
            let slideIndex = 0;

            function showSlides(n) {
                let slides = document.getElementsByClassName("slides");
                if (n > slides.length) { slideIndex = 1; }
                if (n < 1) { slideIndex = slides.length; }
                for (let i = 0; i < slides.length; i++) {
                    slides[i].style.display = "none";
                }
                slides[slideIndex - 1].style.display = "block";
            }

            function plusSlides(n) {
                slideIndex += n;
                showSlides(slideIndex);
            }

            document.addEventListener("DOMContentLoaded", function () {
                slideIndex = 1;
                showSlides(slideIndex);
            });
        </script>
    </div>
    </body>
    </html>
    """

    # Embed HTML
    st.components.v1.html(html_content, height=800, scrolling=False)
