# Post-Co: Image Search & Generation Web Service for "Poster-Copyright"

![Title](app\static\images\main.png)

<div align="center">
    <a href="README.md"><img src="https://img.shields.io/badge/lang-한국어-red.svg" alt="한국어"></a>
    <a href="README_en.md"><img src="https://img.shields.io/badge/lang-English-blue.svg" alt="English"></a>
</div>

## Project Overview
**Post-Co** is a web service designed to prevent copyright infringement in performance posters while fostering creative content creation. This service allows users to upload images or text to search for related posters and provides tools to generate or modify images based on those results. **Post-Co** is tailored to help creators avoid copyright issues while producing original and high-quality content.

### Subtitle
"Image Search & Generation Web Service for 'Poster-Copyright'"

## Team Information
- **Team Name:** This-is-That
- **Competition:** 2024 4th KOPIS Big Data Contest - Service Development Division
- **Team Members:**
  - **Jihwan Lee:** Client & Application Development
  - **Jaeyong Eom:** Database Construction

## Key Features
### 1. Image Search
- **Main Interface:** Users can upload an image or text to receive search results of posters that are similar to the input.

### 2. Image Generation and Editing
- **Cart Interface:** 
  - Users can save their favorite posters to a cart.
  - They can generate new images using selected posters and text, and further refine the generated images.

## Tech Stack
- **Client:** HTML, CSS, JavaScript
- **Application:** Flask, PyTorch, CLIP, OpenCV, HuggingFace (VisionGPT-2)
- **Database:** MySQL, FAISS
- **Advanced Prompting:** GPT-4o-mini
- **Translation API:** NAVER PAPAGO API
- **Image Generation:** DALL-E 3

## Differentiators
- **Purpose-Driven Image Search:** 
  - Traditional services often return images with uncertain sources when searching for specific keywords (e.g., "winter"). 
  - **Post-Co** focuses on providing poster examples directly related to the search keyword, ensuring more relevant and usable results.
  
- **Effective Image Generation:** 
  - Non-designers and those unfamiliar with AI tools may find it challenging to generate detailed images using simple text input on traditional platforms.
  - **Post-Co** assists users by crafting more specific prompts based on a predefined template, enabling the creation of detailed images.

## Future Enhancements
### 1. Improved Prompt Customization
- **Current (As-Is):** Users rely on AI to craft detailed prompts, which may limit the accuracy of the generated images.
- **Future (To-Be):** We plan to provide example keywords that users can utilize to fine-tune their prompts, allowing for more precise image generation.

### 2. Enhanced Text Rendering in Images
- **Current (As-Is):** The DALL-E 3 model has limitations in rendering text within images.
- **Future (To-Be):** We aim to integrate Ideogram 2.0, which will offer improved text filtering and color palette features (currently, the Ideogram API is in beta).

## Installation & Setup
1. Clone the repository:
    ```bash
    git clone https://github.com/username/Post-Co.git
    ```
2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the Flask application:
    ```bash
    python app/app.py
    ```
4. Open your web browser and go to `http://127.0.0.1:5000/` to start using the service.

## License
This project is licensed under the [MIT License](LICENSE).