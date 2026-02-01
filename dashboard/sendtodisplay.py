import io
import logging
import os
import sys
from pathlib import Path

import cairosvg
from dotenv import load_dotenv
from PIL import Image

from dashboard.utils.utils import configure_logging

# Add the Waveshare e-Paper library to the path
WAVESHARE_LIB_PATH = "lib/e-Paper/RaspberryPi_JetsonNano/python/lib"
if os.path.exists(WAVESHARE_LIB_PATH):
    sys.path.insert(0, WAVESHARE_LIB_PATH)

SVG_FILE = "data/image.svg"


def main():
    load_dotenv()
    configure_logging()

    svg_path = Path(SVG_FILE)
    if not svg_path.exists():
        logging.error(f"SVG file not found: {SVG_FILE}")
        return

    # Convert SVG to 1-bit bitmap
    image = svg_to_bitmap(svg_path)

    # Send to e-ink display
    send_to_display(image)


def svg_to_bitmap(svg_path: Path) -> Image.Image:
    """
    Convert SVG to 1-bit black and white bitmap.
    Pipeline: SVG -> PNG (in memory) -> 1-bit bitmap
    """
    logging.info("Converting SVG to bitmap...")

    # Step 1: Convert SVG to PNG in memory
    png_data = cairosvg.svg2png(url=str(svg_path))

    # Step 2: Load PNG into PIL Image
    png_image = Image.open(io.BytesIO(png_data))

    # Step 3: Convert to 1-bit black and white bitmap
    # Mode '1' = 1-bit pixels, black and white
    bw_image = png_image.convert('1', dither=Image.Dither.FLOYDSTEINBERG)

    logging.info(f"Bitmap created: {bw_image.size} pixels, mode={bw_image.mode}")
    return bw_image


def send_to_display(image: Image.Image):
    try:
        from waveshare_epd import epd7in5_V2

        logging.info("Initializing e-Paper display...")
        epd = epd7in5_V2.EPD()
        epd.init()

        logging.info("Sending image to display...")
        epd.display(epd.getbuffer(image))

        logging.info("Putting display to sleep...")
        epd.sleep()

        logging.info("Display updated successfully")

    except (ImportError, OSError):
        # Expected when running on non-Raspberry Pi systems
        logging.warning(
            "Waveshare e-Paper library not available. "
            "This is expected when running outside of Raspberry Pi."
        )
        logging.info(f"Image ready to display: {image.size} pixels, mode={image.mode}")

    except Exception as e:
        logging.error(f"Error sending to display: {e}", exc_info=True)


if __name__ == "__main__":
    main()
