from flask import Flask, render_template, request
from PIL import Image
import numpy as np
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    original_data = None
    negative_data = None
    filename = None

    if request.method == 'POST':
        file = request.files.get('image')
        if not file or file.filename == '':
            return "No file selected"

        filename = file.filename

        # Open uploaded image in memory
        image = Image.open(file.stream).convert('RGB')
        img_array = np.array(image)

        # Create negative
        negative_array = 255 - img_array
        negative_image = Image.fromarray(negative_array)

        # Convert images to base64 for embedding
        def to_base64(img):
            buf = BytesIO()
            img.save(buf, format='PNG')
            buf.seek(0)
            return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode('utf-8')

        original_data = to_base64(image)
        negative_data = to_base64(negative_image)

    return render_template('index.html',
                           original=original_data,
                           negative=negative_data,
                           filename=filename)

if __name__ == '__main__':
    app.run(debug=True)
