import unittest
from unittest.mock import patch, MagicMock
from PIL import Image
import flashframe

class TestFlashFrame(unittest.TestCase):

    @patch('flashframe.ImageGrab.grab')
    def test_capture_screenshot(self, mock_grab):
        """Test capturing a screenshot."""
        # Mock the return value of ImageGrab.grab to simulate capturing a screenshot
        mock_grab.return_value = Image.new('RGB', (100, 100), 'white')
        result = flashframe.capture_screenshot(flashframe.SCREENSHOT_AREA)
        self.assertIsInstance(result, Image.Image)
        mock_grab.assert_called_once_with(bbox=(60, 110, 2270, 1350))

    def test_add_glow_effect(self):
        """Test adding a glowing gradient border."""
        input_image = Image.new('RGB', (100, 100), 'blue')
        border_size = 10
        solid_color = (255, 0, 0)
        fade_color = (255, 0, 0)
        result = flashframe.add_glow_effect(input_image, border_size, solid_color, fade_color)

        # Check if the result is an image and has the expected dimensions
        self.assertIsInstance(result, Image.Image)
        expected_size = (input_image.width + 2 * border_size, input_image.height + 2 * border_size)
        self.assertEqual(result.size, expected_size)

    @patch('flashframe.os.system')
    @patch('PIL.Image.new')
    def test_save_image_to_clipboard(self, mock_new, mock_system):
        """Test saving an image to the clipboard."""
        # Setup a mock Image object with a mock save method
        mock_image = MagicMock()
        mock_new.return_value = mock_image

        # Call your function that ends up calling `image.save()`
        flashframe.save_image_to_clipboard(mock_image)

        # Assert the mock save method was called on the mock Image object
        mock_image.save.assert_called_once_with('/tmp/temp_screenshot.png', format='PNG')

        # Assert the AppleScript command was executed
        mock_system.assert_called_once()
        args, _ = mock_system.call_args
        self.assertTrue('osascript' in args[0] and 'set the clipboard' in args[0])



if __name__ == '__main__':
    unittest.main()
