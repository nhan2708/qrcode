from PIL import Image, ImageDraw, ImageFont
import qrcode

# Yêu cầu người dùng nhập link
data = input("Nhập link bạn muốn tạo mã QR: ")

# Yêu cầu người dùng nhập tên muốn hiển thị
name = input("Nhập tên bạn muốn hiển thị: ")

# Bước 1: Tạo mã QR
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(data)
qr.make(fit=True)
qr_img = qr.make_image(fill_color="black", back_color="white")

# Chuyển mã QR sang chế độ RGB để tránh lỗi khi thêm viền
qr_img = qr_img.convert("RGB")

# Bước 2: Tùy chỉnh viền màu hồng
border_color = "pink"
border_width = 20
qr_width, qr_height = qr_img.size
new_width = qr_width + 2 * border_width
new_height = qr_height + 2 * border_width

bordered_img = Image.new("RGB", (new_width, new_height), border_color)
bordered_img.paste(qr_img, (border_width, border_width))

# Bước 3: Thêm phần dưới cùng
footer_height = 100
final_img = Image.new("RGB", (new_width, new_height + footer_height), border_color)

final_img.paste(bordered_img, (0, 0))

draw = ImageDraw.Draw(final_img)

# Thêm nền cho phần footer
draw.rectangle(
    [(0, new_height), (new_width, new_height + footer_height)],
    fill=border_color,
)

# Thêm văn bản
font_path = "arial.ttf"  # Thay đường dẫn này bằng font chữ có sẵn trên máy của bạn
try:
    font = ImageFont.truetype(font_path, 40)
except OSError:
    font = ImageFont.load_default()  # Dùng font mặc định nếu không tìm thấy font

# Sử dụng tên đã nhập để hiển thị trên ảnh
text = name
text_bbox = draw.textbbox((0, 0), text, font=font)
text_width = text_bbox[2] - text_bbox[0]
text_height = text_bbox[3] - text_bbox[1]
text_x = (new_width - text_width) // 2
text_y = new_height + (footer_height - text_height) // 2
draw.text((text_x, text_y), text, fill="white", font=font)

# Lưu hình ảnh cuối cùng
final_img.save("custom_qr.png")
print("Mã QR được tạo và lưu thành công dưới tên 'custom_qr.png'.")

