from flask import Flask, request, jsonify, render_template
from CLIP import CLIP

app = Flask(__name__)
clip = CLIP()

# Mock function to handle text input and return image links
def process_embedding(embedding):
    # Here, you would have your logic to process the text and generate image links
    # For simplicity, we're returning a static list of image links
    return [
        "https://example.com/image1.jpg",
        "https://example.com/image2.jpg",
        "https://example.com/image3.jpg"
    ]

@app.route('/')
def index():
    # Render the index.html template from the templates folder
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_input():
    if request.content_type == 'application/json':
        if 'text' in request.json:
            text = request.json['text']
            embedding = clip.extract_text_embedding(text)
        else:
            return jsonify({'error': 'No valid JSON data provided'}), 400
    elif 'image' in request.files:
        image_file = request.files['image']
        if image_file and allowed_file(image_file.filename):
            embedding = clip.extract_image_embedding(image_file)
        else:
            return jsonify({'error': 'No valid image file provided'}), 400
    else:
        return jsonify({'error': 'No valid input provided'}), 400

    image_links = process_embedding(embedding)
    return jsonify({'image_links': image_links, 'embedding': embedding.cpu().tolist()})

def allowed_file(filename):
    # Check if the file is an allowed type (e.g., .jpg, .png)
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png'}

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad Request'}), 400

if __name__ == '__main__':
    app.run(debug=True)