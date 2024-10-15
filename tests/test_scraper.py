import unittest
from unittest.mock import AsyncMock, patch, MagicMock
from telethon import TelegramClient
import os
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scrapers.telegram_scraper import scrape_telegram_channel

  # Import your scrape function

class TestTelegramScraper(unittest.TestCase):

    @patch('scraper.TelegramClient')  # Mock the TelegramClient to avoid real API calls
    def setUp(self, MockClient):
        # Set up mock client
        self.mock_client = MockClient.return_value
        self.mock_client.start = AsyncMock()  # Mock the start method
        self.mock_client.iter_messages = AsyncMock()

    @patch('os.makedirs')  # Mock os.makedirs to avoid real folder creation
    def test_folder_creation(self, mock_makedirs):
        # Simulate channel folder not existing
        channel_name = 'test_channel'
        scrape_telegram_channel(channel_name)
        
        # Check if os.makedirs was called to create the folder
        mock_makedirs.assert_called_once_with(channel_name)

    def test_message_processing(self):
        # Simulate messages returned by iter_messages
        message1 = MagicMock(id=1, message="Hello", media=None)
        message2 = MagicMock(id=2, message=None, media=MagicMock())
        self.mock_client.iter_messages.return_value = [message1, message2]

        # Run the scraping function
        with patch('builtins.open', new_callable=MagicMock()) as mock_open:
            scrape_telegram_channel('test_channel')

            # Check if the text file was created for the first message
            mock_open.assert_called_with('test_channel/1_text.txt', 'w', encoding='utf-8')

    def test_handle_telegram_error(self):
        # Simulate a TelegramError being raised
        self.mock_client.start.side_effect = Exception("Telegram error")

        # Run the scraping function and check if the error is logged
        with self.assertLogs('scraper', level='ERROR') as log:
            scrape_telegram_channel('test_channel')

            # Verify that the error was logged
            self.assertIn("ERROR", log.output[0])

    @patch('scraper.client.download_media', AsyncMock())  # Mock download_media method
    def test_media_download(self):
        # Simulate a media message
        media_message = MagicMock(id=3, media=MagicMock())
        self.mock_client.iter_messages.return_value = [media_message]

        # Run the scraping function
        scrape_telegram_channel('test_channel')

        # Verify that download_media was called once
        scraper.client.download_media.assert_called_once()

if __name__ == '__main__':
    unittest.main()
