from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
import qrcode
from io import BytesIO
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Nhận dữ liệu từ form HTML
        data = request.form.get("data")
        name = request.form.get("name")
        border_color = request.form.get("border_color")
        text_color = request.form.get("text_color")

        # Tạo mã QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

        # Tùy chỉnh viền
        border_width = 20
        qr_width, qr_height = qr_img.size
        new_width = qr_width + 2 * border_width
        new_height = qr_height + 2 * border_width

        bordered_img = Image.new("RGB", (new_width, new_height), border_color)
        bordered_img.paste(qr_img, (border_width, border_width))

        # Thêm phần footer (tăng đủ cao để chữ lớn không bị cắt)
        footer_height = 200
        final_img = Image.new("RGB", (new_width, new_height + footer_height), border_color)
        final_img.paste(bordered_img, (0, 0))

        draw = ImageDraw.Draw(final_img)

        # Load font
        font_path = "fonts/arial.ttf"
        font_size = 120
        if os.path.exists(font_path):
            font = ImageFont.truetype(font_path, font_size)
        else:
            font = ImageFont.load_default()

        # Tính toán vị trí chữ
        text_bbox = draw.textbbox((0, 0), name, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_x = (new_width - text_width) // 2
        text_y = new_height + (footer_height - text_height) // 2

        # Vẽ chữ
        draw.text((text_x, text_y), name, fill=text_color, font=font)

        # Xuất ảnh
        buffer = BytesIO()
        final_img.save(buffer, format="PNG")
        buffer.seek(0)
        return send_file(buffer, mimetype="image/png", as_attachment=True, download_name="custom_qr.png")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
