from PIL import ImageGrab, Image, ImageDraw
from pynput import keyboard
import os

# Define the screenshot area (left, top, width, height)
SCREENSHOT_AREA = (60, 110, 2210, 1240)


# Function to capture a screenshot of the predefined area
def capture_screenshot(area):
    x, y, w, h = area
    return ImageGrab.grab(bbox=(x, y, x + w, y + h))


# Function to add a glowing gradient border to an image
def add_glow_effect(img, border_size, solid_color, fade_color):
    original_size = img.size
    new_size = (
        original_size[0] + border_size * 2,
        original_size[1] + border_size * 2,
    )

    # Create a new image with a transparent background
    new_img = Image.new("RGBA", new_size, (0, 0, 0, 0))

    # Paste the original image onto the center of the new image
    new_img.paste(img, (border_size, border_size))

    for i in range(border_size):
        # The alpha value should decrease to create the fade-out effect
        alpha = int(255 - (255 * i / border_size))

        # Generate the color for this iteration, including the alpha for the fade-out effect
        color = (
            int(
                solid_color[0] * (1 - i / border_size)
                + fade_color[0] * (i / border_size)
            ),
            int(
                solid_color[1] * (1 - i / border_size)
                + fade_color[1] * (i / border_size)
            ),
            int(
                solid_color[2] * (1 - i / border_size)
                + fade_color[2] * (i / border_size)
            ),
            alpha,
        )

        # Expand the border with the current color and alpha
        ImageDraw.Draw(new_img).rectangle(
            [(i, i), (new_size[0] - i - 1, new_size[1] - i - 1)], outline=color
        )
    return new_img


# macOS-specific function to save an image to the clipboard using AppleScript
def save_image_to_clipboard(image):
    # Save the image to a temporary file
    temp_path = "/tmp/temp_screenshot.png"
    image.save(temp_path, format="PNG")

    # Construct the AppleScript command to load the image from the temp file to the clipboard
    applescript_command = f"""
    set the clipboard to (the clipboard as record)
    set png_data to (read (POSIX file "{temp_path}") as picture)
    set the clipboard to ({{«class PNGf»:png_data}})
    """

    # Execute the AppleScript command
    os.system(f"osascript -e '{applescript_command}'")


# Main function to handle the screenshot process
def handle_screenshot():
    screenshot = SCREENSHOT_AREA
    # Adjust solid_color and fade_color for your desired glow effect
    solid_color = (
        0,
        191,
        255,
    )  # Solid color for the part of the glow closest to the photo
    fade_color = (
        0,
        191,
        255,
    )  # Same color for the fading part, alpha will be adjusted
    bordered_screenshot = add_glow_effect(
        screenshot, 30, solid_color, fade_color
    )
    save_image_to_clipboard(bordered_screenshot)
    print("Screenshot taken and saved to clipboard.")


# Hotkey listener callback
def on_press(key):
    if key == keyboard.Key.f12:  # Customize the hotkey
        handle_screenshot()


def start_listener():
    # Listen for the hotkey
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == "__main__":
    start_listener()
