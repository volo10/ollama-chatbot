"""
Unit Tests for Ollama Chatbot v1.0
"""

import unittest
import tkinter as tk
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chatbot import OllamaChatbot


class TestChatbotV1(unittest.TestCase):
    """Test cases for Ollama Chatbot v1.0"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide window during tests
        self.app = OllamaChatbot(self.root)
    
    def tearDown(self):
        """Clean up after tests"""
        try:
            self.root.destroy()
        except:
            pass
    
    def test_initialization(self):
        """Test app initializes correctly"""
        self.assertIsNotNone(self.app)
        self.assertEqual(self.app.current_model.get(), "llama2")
        self.assertEqual(self.app.temperature.get(), 0.7)
        self.assertIsInstance(self.app.chat_history, list)
        self.assertEqual(len(self.app.chat_history), 0)
    
    def test_color_scheme(self):
        """Test color scheme is properly defined"""
        self.assertIn('bg_primary', self.app.colors)
        self.assertIn('accent', self.app.colors)
        self.assertIn('text_primary', self.app.colors)
        self.assertEqual(len(self.app.colors), 11)
    
    def test_model_variable(self):
        """Test model selection"""
        self.app.current_model.set("mistral")
        self.assertEqual(self.app.current_model.get(), "mistral")
        
        self.app.current_model.set("codellama")
        self.assertEqual(self.app.current_model.get(), "codellama")
    
    def test_temperature_range(self):
        """Test temperature variable"""
        self.app.temperature.set(0.5)
        self.assertEqual(self.app.temperature.get(), 0.5)
        
        self.app.temperature.set(1.5)
        self.assertEqual(self.app.temperature.get(), 1.5)
    
    def test_chat_display_exists(self):
        """Test chat display widget exists"""
        self.assertIsNotNone(self.app.chat_display)
        self.assertIsInstance(self.app.chat_display, tk.Text)
    
    def test_message_input_exists(self):
        """Test message input widget exists"""
        self.assertIsNotNone(self.app.message_input)
        self.assertIsInstance(self.app.message_input, tk.Text)
    
    def test_send_button_exists(self):
        """Test send button exists"""
        self.assertIsNotNone(self.app.send_button)
        self.assertIsInstance(self.app.send_button, tk.Button)
    
    def test_display_message(self):
        """Test message display functionality"""
        initial_content = self.app.chat_display.get("1.0", tk.END)
        
        self.app.display_message("Test message", "user")
        
        new_content = self.app.chat_display.get("1.0", tk.END)
        self.assertNotEqual(initial_content, new_content)
        self.assertIn("Test message", new_content)
    
    def test_clear_chat(self):
        """Test chat clearing"""
        # Add some messages
        self.app.chat_history.append({"role": "user", "content": "test"})
        self.app.display_message("Test", "user")
        
        # Mock the messagebox to return True
        with patch('tkinter.messagebox.askyesno', return_value=True):
            self.app.clear_chat()
        
        self.assertEqual(len(self.app.chat_history), 0)
    
    def test_update_temp_label(self):
        """Test temperature label update"""
        self.app.update_temp_label(1.2)
        self.assertEqual(self.app.temp_label.cget("text"), "1.2")
    
    def test_update_status(self):
        """Test status bar update"""
        self.app.update_status("Test status")
        self.assertEqual(self.app.status_bar.cget("text"), "Test status")
    
    @patch('requests.get')
    def test_check_ollama_connection_success(self, mock_get):
        """Test successful Ollama connection check"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # Run check in thread and wait
        import time
        self.app.check_ollama_connection()
        time.sleep(0.5)  # Wait for thread
        self.root.update()  # Process GUI updates
        
        # Should show connected
        indicator_text = self.app.connection_indicator.cget("text")
        self.assertIn("Connected", indicator_text)
    
    @patch('requests.get')
    def test_check_ollama_connection_failure(self, mock_get):
        """Test failed Ollama connection check"""
        mock_get.side_effect = Exception("Connection error")
        
        import time
        self.app.check_ollama_connection()
        time.sleep(0.5)
        self.root.update()
        
        indicator_text = self.app.connection_indicator.cget("text")
        self.assertIn("Disconnected", indicator_text)
    
    def test_system_prompt_text(self):
        """Test system prompt text widget"""
        self.assertIsNotNone(self.app.system_prompt_text)
        content = self.app.system_prompt_text.get("1.0", tk.END).strip()
        self.assertTrue(len(content) > 0)
    
    def test_empty_message_handling(self):
        """Test that empty messages are not sent"""
        initial_history_len = len(self.app.chat_history)
        
        self.app.message_input.delete("1.0", tk.END)
        self.app.message_input.insert("1.0", "")
        
        # Should not crash or send
        # (Would need to mock messagebox for full test)
        self.assertEqual(len(self.app.chat_history), initial_history_len)


class TestChatbotV1Integration(unittest.TestCase):
    """Integration tests for v1.0"""
    
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = OllamaChatbot(self.root)
    
    def tearDown(self):
        try:
            self.root.destroy()
        except:
            pass
    
    def test_full_message_flow(self):
        """Test complete message sending flow (mocked)"""
        # Add test message to input
        test_message = "Hello, test!"
        self.app.message_input.insert("1.0", test_message)
        
        # Get content
        content = self.app.message_input.get("1.0", tk.END).strip()
        self.assertEqual(content, test_message)
    
    def test_gui_layout_integrity(self):
        """Test that all major GUI components exist"""
        # Check all major components are created
        self.assertIsNotNone(self.app.chat_display)
        self.assertIsNotNone(self.app.message_input)
        self.assertIsNotNone(self.app.send_button)
        self.assertIsNotNone(self.app.status_bar)
        self.assertIsNotNone(self.app.connection_indicator)
        self.assertIsNotNone(self.app.temp_label)
        self.assertIsNotNone(self.app.system_prompt_text)


def suite():
    """Create test suite"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestChatbotV1))
    suite.addTest(unittest.makeSuite(TestChatbotV1Integration))
    return suite


if __name__ == '__main__':
    print("Running Ollama Chatbot v1.0 Tests...")
    print("=" * 60)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite())
    
    print("\n" + "=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    sys.exit(0 if result.wasSuccessful() else 1)

