from flask import Flask, request, send_file, jsonify
from PIL import Image, ImageDraw, ImageFont
import io
import os
import requests

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG = {
    "DEFAULT_CANVAS_SIZE": (1280, 720),
    
    "THEMES": {
        "default": {
            "BG_IMAGE": os.path.join(BASE_DIR, "theme_bg/default.jpg"), 
            "CANVAS_SIZE": (1280, 720),
            "AVATAR": {
                "POSITION_XY": (297, 338), 
                "RADIUS": 236,  
            },
            "USERNAME": {
                "POSITION_XY": (858, 470), 
                "COLOR": (255, 255, 255),  
                "OUTLINE_COLOR": (0, 0, 0),
                "FONT_SIZE": 60,   
                "MAX_WIDTH": 500, 
            }
        },

"""        
        "orange": {
            "BG_IMAGE": os.path.join(BASE_DIR, "theme_bg/orange.jpg"), 
            "CANVAS_SIZE": (1280, 720),
            "AVATAR": {
                "POSITION_XY": (990, 362), 
                "RADIUS": 217, 
            },
            "USERNAME": {
                "POSITION_XY": (385, 345), 
                "COLOR": (255, 255, 255),  
                "OUTLINE_COLOR": (0, 0, 0),
                "FONT_SIZE": 65,   
                "MAX_WIDTH": 380, 
            }
        },
"""
    }
}

def get_font(size):
    return ImageFont.load_default().font_variant(size=size)

def generate_final_image(name, img_source, theme_name, is_file=False):
    theme_config = CONFIG["THEMES"].get(theme_name)
    if not theme_config:
        theme_config = CONFIG["THEMES"]["default"]
    
    try:
        bg = Image.open(theme_config["BG_IMAGE"]).convert("RGBA")
        bg = bg.resize(theme_config.get("CANVAS_SIZE", CONFIG["DEFAULT_CANVAS_SIZE"]))
    except FileNotFoundError:
        return None, f"Theme background image '{theme_config['BG_IMAGE']}' not found."

    if is_file:
        user_img = Image.open(img_source).convert("RGBA")
    else:
        try:
            response = requests.get(img_source, timeout=10)
            if response.status_code != 200:
                return None, "Failed to fetch image from URL"
            user_img = Image.open(io.BytesIO(response.content)).convert("RGBA")
        except Exception as e:
            return None, f"Error fetching URL: {str(e)}"

    avatar_conf = theme_config["AVATAR"]
    target_diameter = avatar_conf["RADIUS"] * 2
    user_img.thumbnail((target_diameter, target_diameter), Image.Resampling.LANCZOS)
    
    mask = Image.new("L", (target_diameter, target_diameter), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, target_diameter, target_diameter), fill=255)
    
    circular_avatar = Image.new("RGBA", (target_diameter, target_diameter), (0, 0, 0, 0))
    paste_offset = (target_diameter - user_img.size[0]) // 2
    circular_avatar.paste(user_img, (paste_offset, paste_offset), mask=user_img.split()[-1] if user_img.mode == 'RGBA' else None)
    circular_avatar.putalpha(mask)
    
    paste_x = avatar_conf["POSITION_XY"][0] - target_diameter // 2
    paste_y = avatar_conf["POSITION_XY"][1] - target_diameter // 2
    bg.paste(circular_avatar, (paste_x, paste_y), circular_avatar)

    uname_conf = theme_config["USERNAME"]
    draw = ImageDraw.Draw(bg)
    text = name.upper()
    
    font = get_font(uname_conf["FONT_SIZE"])
    
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    current_font_size = uname_conf["FONT_SIZE"]
    final_font = font
    while text_width > uname_conf["MAX_WIDTH"] and current_font_size > 20:
        current_font_size -= 2
        final_font = get_font(current_font_size)
        bbox = draw.textbbox((0, 0), text, font=final_font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

    centered_x = uname_conf["POSITION_XY"][0] - (text_width / 2)
    centered_y = uname_conf["POSITION_XY"][1] - (text_height / 2)
    
    if "OUTLINE_COLOR" in uname_conf:
        outline_color = uname_conf["OUTLINE_COLOR"]
        for off_x in [-2, 2]:
            for off_y in [-2, 2]:
                draw.text((centered_x + off_x, centered_y + off_y), text, fill=outline_color, font=final_font)
    
    draw.text((centered_x, centered_y), text, fill=uname_conf["COLOR"], font=final_font)

    output_buffer = io.BytesIO()
    bg.save(output_buffer, format="PNG")
    output_buffer.seek(0)
    return output_buffer, None

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "API Started", "status": "running"})

@app.route('/generate', methods=['GET'])
def generate_get():
    name = request.args.get('name')
    img_url = request.args.get('img_url')
    theme = request.args.get('theme', 'default')
    
    if not name or not img_url:
        return jsonify({"error": "Missing ?name=NAME&img_url=URL"}), 400
    
    result, error = generate_final_image(name, img_url, theme, is_file=False)
    return send_file(result, mimetype='image/png') if not error else (jsonify({"error": error}), 500)

@app.route('/generate', methods=['POST'])
def generate_post():
    name = request.form.get('name')
    img_file = request.files.get('img_file')
    theme = request.form.get('theme', 'default')
    
    if not name or not img_file:
        return jsonify({"error": "Missing 'name' or 'img_file'"}), 400
    
    result, error = generate_final_image(name, img_file, theme, is_file=True)
    return send_file(result, mimetype='image/png') if not error else (jsonify({"error": error}), 500)