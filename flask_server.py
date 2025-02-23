from flask import Flask, send_file, request
from PIL import Image
import os

app = Flask(__name__)

TEXTURE_FOLDER = "textures"

def pixelate_image(image_path, scale):
    """ Resize image to create a pixelated effect """
    img = Image.open(image_path)
    img = img.resize((scale, scale), Image.NEAREST)  # Downscale
    img = img.resize((16, 16), Image.NEAREST)  # Upscale back
    pixelated_path = f"temp/{os.path.basename(image_path).replace('.png', '')}_{scale}.png"
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
    os.makedirs("temp", exist_ok=True)
    app.run(debug=True)
