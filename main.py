import sys
import qrcode
from dotenv import load_dotenv
import logging.config
from pathlib import Path
import os
import argparse
from datetime import datetime
import validators  # Import the validators package

# Load environment variables
load_dotenv()

# Environment Variables for Configuration
QR_DIRECTORY = os.getenv('QR_CODE_DIR', 'qr_codes')  # Directory for saving QR code
FILL_COLOR = os.getenv('FILL_COLOR', 'red')  # Fill color for the QR code
BACK_COLOR = os.getenv('BACK_COLOR', 'white')  # Background color for the QR code

def setup_logging():
    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create a console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    # Create a file handler
    file_handler = logging.FileHandler('qr_code_generator.log')
    file_handler.setLevel(logging.DEBUG)  # Change this to whatever level you want for the file

    # Create a formatter and set it for both handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add both handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logging.info("Logging configured successfully.")


def create_directory(path: Path):
    try:
        path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logging.error(f"Failed to create directory {path}: {e}")
        exit(1)

def is_valid_url(url):
    if validators.url(url):
        return True
    else:
        logging.error(f"Invalid URL provided: {url}")
        return False

def generate_qr_code(data, path, fill_color='red', back_color='white'):
    if not is_valid_url(data):
        return  # Exit the function if the URL is not valid

    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color=fill_color, back_color=back_color)

        with path.open('wb') as qr_file:
            img.save(qr_file)
        logging.info(f"QR code successfully saved to {path}")

    except Exception as e:
        logging.error(f"An error occurred while generating or saving the QR code: {e}")

def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Generate a QR code.')
    parser.add_argument('--url', help='The URL to encode in the QR code', default='https://github.com/Livia-1212/improved-qr-docker-2024.git')
    args = parser.parse_args()

    # Initial logging setup
    setup_logging()
    
    # Generate a timestamped filename for the QR code
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    qr_filename = f"QRCode_{timestamp}.png"

    # Create the full path for the QR code file
    qr_code_full_path = Path.cwd() / QR_DIRECTORY / qr_filename
    
    # Ensure the QR code directory exists
    create_directory(Path.cwd() / QR_DIRECTORY)
    
    # Generate and save the QR code
    generate_qr_code(args.url, qr_code_full_path, FILL_COLOR, BACK_COLOR)

if __name__ == "__main__":
    main()
