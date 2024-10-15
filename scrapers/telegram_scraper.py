import os  # For environment variables and file operations
import logging  # For logging events
from dotenv import load_dotenv  # To load environment variables from .env
from telethon import TelegramClient, errors
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
import asyncio

# Step 2: Configure logging
logging.basicConfig(
    filename='telegram_scraper.log',  # Log file name
    level=logging.INFO,  # Log everything (INFO and above)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
)

# Step 3: Load environment variables from .env
load_dotenv()

# Retrieve values from the .env file
api_id = os.getenv('API_ID')  # Get the API ID
api_hash = os.getenv('API_HASH')  # Get the API hash
phone_number = os.getenv('PHONE_NUMBER')  # Get the phone number

# Debugging output to verify loaded values
logging.info(f"API_ID: {api_id}, API_HASH: {api_hash}, PHONE_NUMBER: {phone_number}")

# Ensure API_ID is not None
if api_id is None or api_hash is None or phone_number is None:
    logging.error("One or more environment variables are not set. Please check your .env file.")
    raise ValueError("Missing environment variables.")

# Initialize the Telegram client
client = TelegramClient('session_name', int(api_id), api_hash)

async def scrape_telegram_channel(channel_username):
    try:
        await client.start(phone_number)
        logging.info(f"Started client for channel: {channel_username}")

        if not os.path.exists(channel_username):
            os.makedirs(channel_username)
            logging.info(f"Created folder: {channel_username}")

        async for message in client.iter_messages(channel_username, limit=100):
            try:
                if message.message:
                    text_file = os.path.join(channel_username, f"{message.id}_text.txt")
                    with open(text_file, 'w', encoding='utf-8') as f:
                        f.write(message.message)
                    logging.info(f"Saved text message: {text_file}")

                if isinstance(message.media, MessageMediaPhoto):
                    image_path = os.path.join(channel_username, f"{message.id}_image.jpg")
                    await client.download_media(message.media, file=image_path)
                    logging.info(f"Saved image: {image_path}")

                elif isinstance(message.media, MessageMediaDocument):
                    if message.media.document.mime_type.startswith('image/'):
                        image_path = os.path.join(channel_username, f"{message.id}_image.jpg")
                        await client.download_media(message.media, file=image_path)
                        logging.info(f"Saved image document: {image_path}")
                    else:
                        logging.warning(f"Skipping non-image document (ID: {message.id})")
            except Exception as e:
                logging.error(f"Failed to process message (ID: {message.id}): {e}")

        logging.info(f"Scraping of {channel_username} completed!")

    except errors.TelegramError as e:
        logging.error(f"Telegram error occurred: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

# Run the scraper
if __name__ == "__main__":
    logging.info("Starting the Telegram scraper...")
    with client:
        channel_username = 'your_channel_username_here'  # Replace with the actual channel username
        logging.info(f"Scraping channel: {channel_username}")
        client.loop.run_until_complete(scrape_telegram_channel(channel_username))
