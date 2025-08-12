from PIL import Image
import numpy as np

# --- SETTINGS ---
input_image = "image_0.jpg"
output_image = "output.jpg"
mask_output = "mask.png"        # mask output file (image)
mask_array_output = "mask.npy"  # mask array file
ratios = (0, 0.33, 0.33, 0.66)  # start_h, end_h, start_w, end_w
icon_path = "637.png"           # leave as None if no overlay
icon_scale = 0.2                # size of icon relative to cropped width
# ----------------

# Load image
img = Image.open(input_image)

# Crop
w, h = img.size
sh, eh, sw, ew = ratios
top = int(h * sh)
bottom = int(h * eh)
left = int(w * sw)
right = int(w * ew)
cropped = img.crop((left, top, right, bottom))

# Prepare mask (same size as cropped area, all black)
mask_array = np.zeros((cropped.height, cropped.width), dtype=np.uint8)

# Overlay icon in center
if icon_path:
    icon = Image.open(icon_path).convert("RGBA")
    icon_w = int(cropped.width * icon_scale)
    icon_h = int(icon.height * (icon_w / icon.width))
    icon = icon.resize((icon_w, icon_h), Image.LANCZOS)

    pos_x = (cropped.width - icon_w) // 2
    pos_y = (cropped.height - icon_h) // 2

    # Extract alpha channel from icon
    alpha = np.array(icon.split()[-1])  # last channel is alpha

    # Where alpha > 0, set mask to 1 (binary)
    mask_array[pos_y:pos_y+icon_h, pos_x:pos_x+icon_w][alpha > 0] = 1

    cropped = cropped.convert("RGBA")
    cropped.paste(icon, (pos_x, pos_y), icon)

# Save mask as binary image (255 for visible, 0 for background)
mask_img = Image.fromarray((mask_array * 255).astype(np.uint8), mode="L")
mask_img.save(mask_output)

# Save mask as NumPy array (0/1 values)
np.save(mask_array_output, mask_array)

# If saving as JPEG, must be RGB
if output_image.lower().endswith((".jpg", ".jpeg")) and cropped.mode == "RGBA":
    cropped = cropped.convert("RGB")

# Save output image
cropped.save(output_image)

print(f"Saved image to {output_image}")
print(f"Saved mask image to {mask_output}")
print(f"Saved mask array to {mask_array_output}")
