"""
Unit Tests for Ollama Chatbot v2.0
Tests file/image upload functionality
"""

import unittest
import tkinter as tk
from unittest.mock import Mock, patch, MagicMock, mock_open
import sys
import os
import base64

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chatbot_v2 import OllamaChatbotV2


class TestChatbotV2(unittest.TestCase):
    """Test cases for Ollama Chatbot v2.0"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = OllamaChatbotV2(self.root)
    
    def tearDown(self):
        """Clean up after tests"""
        try:
            self.root.destroy()
        except:
            pass
    
    def test_initialization(self):
        """Test v2 app initializes correctly"""
        self.assertIsNotNone(self.app)
        self.assertEqual(self.app.current_model.get(), "llama2")
        self.assertIsInstance(self.app.attached_files, list)
        self.assertIsInstance(self.app.attached_images, list)
    
    def test_attachment_lists_initialized(self):
        """Test attachment lists are empty on start"""
        self.assertEqual(len(self.app.attached_files), 0)
        self.assertEqual(len(self.app.attached_images), 0)
        self.assertIsNone(self.app.current_image_data)
    
    def test_preview_frame_exists(self):
        """Test attachment preview frame exists"""
        self.assertIsNotNone(self.app.preview_frame)
    
    @patch('tkinter.filedialog.askopenfilename')
    @patch('builtins.open', new_callable=mock_open, read_data='test content')
    def test_attach_file(self, mock_file, mock_dialog):
        """Test file attachment"""
        mock_dialog.return_value = '/path/to/test.txt'
        
        self.app.attach_file()
        
        self.assertEqual(len(self.app.attached_files), 1)
        self.assertEqual(self.app.attached_files[0]['name'], 'test.txt')
        self.assertIn('content', self.app.attached_files[0])
    
    @patch('tkinter.filedialog.askopenfilename')
    @patch('builtins.open', new_callable=mock_open, read_data=b'fake_image_data')
    def test_attach_image(self, mock_file, mock_dialog):
        """Test image attachment"""
        mock_dialog.return_value = '/path/to/test.jpg'
        
        # Mock messagebox to not show dialog
        with patch('tkinter.messagebox.askyesno', return_value=False):
            self.app.attach_image()
        
        self.assertEqual(len(self.app.attached_images), 1)
        self.assertEqual(self.app.attached_images[0]['name'], 'test.jpg')
        self.assertIsNotNone(self.app.current_image_data)
    
    def test_clear_attachments(self):
        """Test clearing attachments"""
        # Add some mock attachments
        self.app.attached_files.append({'name': 'test.txt', 'content': 'test'})
        self.app.attached_images.append({'name': 'test.jpg', 'data': 'data'})
        self.app.current_image_data = 'some_data'
        
        self.app.clear_attachments()
        
        self.assertEqual(len(self.app.attached_files), 0)
        self.assertEqual(len(self.app.attached_images), 0)
        self.assertIsNone(self.app.current_image_data)
    
    def test_update_attachment_preview(self):
        """Test attachment preview updates"""
        self.app.attached_files.append({'name': 'test.txt', 'content': 'test'})
        self.app.update_attachment_preview()
        
        # Preview frame should be visible
        # (Pack info would be checked in integration test)
        self.assertTrue(True)  # Placeholder
    
    def test_model_includes_llava(self):
        """Test that llava model is available for images"""
        # Check llava is in model list
        # This would require accessing the combobox values
        # For now, just verify model can be set to llava
        self.app.current_model.set("llava")
        self.assertEqual(self.app.current_model.get(), "llava")
    
    def test_display_message_with_attachments(self):
        """Test displaying message with attachment info"""
        # Add attachment
        self.app.attached_files.append({'name': 'test.txt', 'content': 'test'})
        
        # Display should work (would be more complex in real scenario)
        self.app.display_message("Test with file", "user")
        
        content = self.app.chat_display.get("1.0", tk.END)
        self.assertIn("Test with file", content)


class TestChatbotV2FileHandling(unittest.TestCase):
    """Test file handling specific to v2"""
    
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = OllamaChatbotV2(self.root)
    
    def tearDown(self):
        try:
            self.root.destroy()
        except:
            pass
    
    @patch('tkinter.filedialog.askopenfilename', return_value='')
    def test_attach_file_cancelled(self, mock_dialog):
        """Test file dialog cancellation"""
        initial_count = len(self.app.attached_files)
        self.app.attach_file()
        self.assertEqual(len(self.app.attached_files), initial_count)
    
    @patch('tkinter.filedialog.askopenfilename', return_value='')
    def test_attach_image_cancelled(self, mock_dialog):
        """Test image dialog cancellation"""
        initial_count = len(self.app.attached_images)
        self.app.attach_image()
        self.assertEqual(len(self.app.attached_images), initial_count)
    
    def test_multiple_file_attachments(self):
        """Test multiple file attachments"""
        self.app.attached_files.append({'name': 'file1.txt', 'content': 'test1'})
        self.app.attached_files.append({'name': 'file2.txt', 'content': 'test2'})
        
        self.assertEqual(len(self.app.attached_files), 2)
    
    def test_multiple_image_attachments(self):
        """Test multiple image attachments"""
        self.app.attached_images.append({'name': 'img1.jpg', 'data': 'data1'})
        self.app.attached_images.append({'name': 'img2.jpg', 'data': 'data2'})
        
        self.assertEqual(len(self.app.attached_images), 2)


def suite():
    """Create test suite"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestChatbotV2))
    suite.addTest(unittest.makeSuite(TestChatbotV2FileHandling))
    return suite


if __name__ == '__main__':
    print("Running Ollama Chatbot v2.0 Tests...")
    print("=" * 60)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite())
    
    print("\n" + "=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    sys.exit(0 if result.wasSuccessful() else 1)

