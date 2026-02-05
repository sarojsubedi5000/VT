from flask import Flask, render_template, redirect, url_for, request, session
import os
import base64
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io

app = Flask(__name__)
app.secret_key = "love_secret_key_2026"  # required for session

# Questions (answers use {name})
questions = [
    {
        "question": "💌 I want to ask you something… Do you think people meet by coincidence?",
        "answer": "✨ {name}, many believe it’s not coincidence. Destiny loves surprises."
    },
    {
        "question": "💖 Do you feel some people are meant to be in our lives?",
        "answer": "🌟 {name}, some souls are written into our story before we even meet them."
    },
    {
        "question": "🥰 Can a simple conversation change your life?",
        "answer": "💫 Yes {name}… sometimes destiny whispers instead of shouting."
    },
    {
        "question": "❤️ Do you want to be my Valentine?",
        "answer": ""
    }
]

# =========================
# Ask Name Page
# =========================
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        session["name"] = request.form.get("name", "Someone")
        return redirect(url_for("question", qid=0))
    return render_template("index.html")

# =========================
# Question Page
# =========================
@app.route("/question/<int:qid>")
def question(qid):
    if "name" not in session:
        return redirect(url_for("home"))

    if qid >= len(questions):
        return redirect(url_for("valentine"))

    q = questions[qid]
    name = session["name"]

    # Inject name into answer
    answer = q["answer"].format(name=name) if q["answer"] else ""

    return render_template(
        "question.html",
        question=q["question"],
        answer=answer,
        qid=qid,
        total=len(questions),
        name=name
    )

# =========================
# Valentine Page
# =========================
@app.route("/valentine")
def valentine():
    name = session.get("name", "")
    return render_template("valentine.html", name=name)

# =========================
# Save Photo
# =========================
@app.route("/save_photo", methods=["POST"])
def save_photo():
    data = request.get_json()
    if not data or "image" not in data:
        return "Camera Not Found", 400

    img_data = data["image"].split(",")[1]
    os.makedirs("static", exist_ok=True)

    user_img = Image.open(io.BytesIO(base64.b64decode(img_data))).convert("RGBA")
    width, height = user_img.size

    overlay = Image.new("RGBA", user_img.size, (255, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    try:
        font = ImageFont.truetype("arial.ttf", int(width * 0.07))
    except:
        font = ImageFont.load_default()

    name = session.get("name", "")

    draw.text(
        (width * 0.08, height * 0.1),
        f"Happy Valentine 2026 💖\n{name}, Will You Be Mine?",
        font=font,
        fill=(255, 0, 0, 255)
    )

    final = Image.alpha_composite(user_img, overlay)
    filename = f"static/valentine_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    final.convert("RGB").save(filename)

    return "Saved"

# =========================
if __name__ == "__main__":
    app.run(debug=True)
