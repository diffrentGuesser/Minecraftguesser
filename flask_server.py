from flask import Flask, send_file, request
from PIL import Image
import os

app = Flask(__name__)

TEXTURE_FOLDER = "textures"
TEMP_FOLDER = "temp"

# Ensure temp folder exists
os.makedirs(TEMP_FOLDER, exist_ok=True)

def pixelate_image(image_path, scale):
    """ Resizes the image to simulate pixelation. """
    img = Image.open(image_path)
    img = img.resize((scale, scale), Image.NEAREST)  # Downscale
    img = img.resize((16, 16), Image.NEAREST)  # Upscale back to 16x16
    pixelated_path = os.path.join(TEMP_FOLDER, f"{os.path.basename(image_path)}_{scale}.png")
    img.save(pixelated_path)
    return pixelated_path

@app.route("/get_texture")
def get_texture():
    texture_name = request.args.get("name", "stone.png")
    scale = int(request.args.get("scale", 16))

    texture_path = os.path.join(TEXTURE_FOLDER, texture_name)
    if not os.path.exists(texture_path):
        return "Texture not found", 404

    pixelated_path = pixelate_image(texture_path, scale)
    return send_file(pixelated_path, mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)
