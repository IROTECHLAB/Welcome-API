# 🎨 WELCOME API - Welcome Image Generator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-3.0.3-green.svg)](https://flask.palletsprojects.com/)

<p align="center">
  <img src="https://iili.io/CcIFJpa.jpg" alt="Welcome API Banner" width="100%">
</p>

A powerful Flask-based API that generates customized welcome images with user avatars and names. Perfect for Discord, Telegram, WhatsApp bots, or any platform that needs personalized welcome messages.

## ✨ Features

- **🎯 Dynamic Welcome Images**: Generate personalized welcome images with user avatars and names
- **🖼️ Theme System**: Easy-to-configure templates with customizable positions and styles
- **📸 Avatar Support**: Accepts both URL and file upload for profile pictures
- **🎨 Circular Avatars**: Automatically crops avatars into clean circular shapes
- **📝 Auto-scaled Text**: Smart font sizing to fit names perfectly within the template
- **🌐 RESTful API**: Simple GET and POST endpoints for easy integration
- **⚡ Lightweight**: Built with Flask and PIL for fast processing
- **🚀 Vercel Ready**: One-click deployment to Vercel

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Local Installation

```bash
# Clone the repository
git clone https://github.com/IROTECHLAB/welcome-api.git
cd welcome-api

# Install dependencies
pip install -r requirements.txt

# Run the API
python app.py
```

The API will start on `http://localhost:5000`

## ☁️ Deploy to Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/IROTECHLAB/welcome-api)

### Manual Vercel Deployment

1. **Install Vercel CLI**
```bash
npm install -g vercel
```

2. **Deploy**
```bash
vercel
```

3. **Follow the prompts** to complete deployment

### Vercel Configuration

The `vercel.json` file handles the deployment configuration:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

## 📡 API Endpoints

### GET `/generate`
Generate a welcome image using a profile picture URL.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | ✅ | User's name to display |
| `img_url` | string | ✅ | URL of the user's profile picture |
| `theme` | string | ❌ | Theme name (default: "default") |

**Example:**
```bash
curl "http://localhost:5000/generate?name=JohnDoe&img_url=https://example.com/avatar.jpg&theme=default"
```

### POST `/generate`
Generate a welcome image using a file upload.

**Form Data:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | ✅ | User's name to display |
| `img_file` | file | ✅ | Profile picture file |
| `theme` | string | ❌ | Theme name (default: "default") |

**Example:**
```bash
curl -X POST "http://localhost:5000/generate" \
  -F "name=JohnDoe" \
  -F "img_file=@avatar.jpg" \
  -F "theme=default"
```

### GET `/`
Check if API is running.

**Response:**
```json
{
  "message": "API Started",
  "status": "running"
}
```

## 🎨 Theme Customization

### Adding Your Own Theme

The `orange` theme is commented out as an example. You can create your own themes in the `CONFIG["THEMES"]` dictionary:

```python
"your_theme": {
    "BG_IMAGE": os.path.join(BASE_DIR, "theme_bg/your_bg.jpg"),
    "CANVAS_SIZE": (1280, 720),  # (width, height)
    "AVATAR": {
        "POSITION_XY": (297, 338),  # (x, y) center position
        "RADIUS": 236,  # Avatar size in pixels
    },
    "USERNAME": {
        "POSITION_XY": (858, 470),  # (x, y) center position
        "COLOR": (255, 255, 255),  # RGB values
        "OUTLINE_COLOR": (0, 0, 0),  # For text readability
        "FONT_SIZE": 60,  # Starting font size (auto-scaled)
        "MAX_WIDTH": 500,  # Maximum width in pixels
    }
}
```

### Theme Configuration Tips

1. **Positioning** - Use image editing software to find exact pixel positions
2. **Avatar Size** - Ensure `RADIUS` matches your template design
3. **Text Max Width** - Prevents text from overflowing outside designated area
4. **Background Images** - Place JPG/PNG files in `/theme_bg/` folder

## 🎯 Integration Examples

### Discord Bot Integration
```python
import discord
import requests

@bot.event
async def on_member_join(member):
    avatar_url = member.display_avatar.url
    name = member.name
    
    response = requests.get(
        f"https://your-vercel-app.vercel.app/generate",
        params={"name": name, "img_url": avatar_url, "theme": "default"}
    )
    
    if response.status_code == 200:
        with open("welcome.png", "wb") as f:
            f.write(response.content)
        await member.guild.system_channel.send(file=discord.File("welcome.png"))
```

### Telegram Bot Integration
```python
from telegram import Bot
import requests

def generate_welcome(name, avatar_url):
    response = requests.get(
        f"https://your-vercel-app.vercel.app/generate",
        params={"name": name, "img_url": avatar_url}
    )
    return response.content if response.status_code == 200 else None
```

### WhatsApp Bot Integration
```python
import requests

def generate_welcome_whatsapp(name, avatar_url):
    response = requests.get(
        f"https://your-vercel-app.vercel.app/generate",
        params={"name": name, "img_url": avatar_url}
    )
    if response.status_code == 200:
        # Send image via WhatsApp API
        send_whatsapp_image(response.content)
```

## 📁 Project Structure

```
welcome-api/
├── app.py              # Main application
├── vercel.json         # Vercel deployment configuration
├── theme_bg/           # Background images folder
│   ├── default.jpg
│   └── your_theme.jpg
├── requirements.txt    # Python dependencies
├── README.md          # Documentation
└── LICENSE            # MIT License
```

## 🛠️ Dependencies

```txt
Flask==3.0.3
Pillow==10.3.0
requests==2.31.0
```

## 🔧 Error Handling

The API returns appropriate error messages for:
- Invalid or missing parameters
- Failed image URL fetches
- Missing background images
- File upload issues

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**IROTECHLAB**
- GitHub: [@IROTECHLAB](https://github.com/IROTECHLAB)

## 🙏 Acknowledgments

- Flask for the web framework
- Pillow for image processing
- Vercel for easy deployment
- All contributors and users of this API

## 💬 Support

For issues, questions, or contributions:
- Open an [issue](https://github.com/IROTECHLAB/welcome-api/issues)
- Star ⭐ the repository to show support

---

<p align="center">Made with ❤️ by IROTECHLAB</p>
