from flask import Flask, request
from flask_cors import CORS
from rembg import remove
import base64
from io import BytesIO

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5503", "https://artistacademyphilippines.github.io"])

#always use 'GET' AND 'POST' even if you're only doing post back to frontend
@app.route('/', methods=['GET','POST'])

def index():

    #Get the base64 string from the request
    data = request.data.decode('utf-8')

    # Decode the base64 string to image
    new_img = base64.b64decode(data.split(',')[1])
    
    # Process the image with rembg to remove the background
    removed_background = remove(new_img, post_process_mask=True)  # Processed image with background removed
    
    # Convert the result into a binary format
    new_data = BytesIO(removed_background)
    new_data.seek(0)

    # Convert binary to base64 format and decode again to text format
    new_base64 = base64.b64encode(new_data.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{new_base64}"
        
if __name__ == '__main__':
    app.run(timeout=2400)