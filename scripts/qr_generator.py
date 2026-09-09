import os
import qrcode

script_dir = os.path.dirname(os.path.abspath(__file__))

output_dir = os.path.abspath(
    os.path.join(
        script_dir,
        "..",
        "ros2_ws",
        "src",
        "puzzlebot_description",
        "materials",
        "textures"
    )
)

os.makedirs(output_dir, exist_ok=True)

clients = [
    "Emezon",
    "Wolmar",
    "Popsi"
]

for client in clients:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=20,
        border=4,
    )

    qr.add_data(client)
    qr.make(fit=True)

    img = qr.make_image(
        fill_color="black",
        back_color="white"
    ).convert("RGB")

    filename = f"qr_{client}.png"
    filepath = os.path.join(output_dir, filename)
    img.save(filepath)

    print(f"Generated {filename} with payload: {client}")