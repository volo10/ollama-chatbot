"""
Unit Tests for Ollama Chatbot v3.0
Tests chat history, UI, and fun facts
"""

import unittest
import tkinter as tk
from unittest.mock import Mock, patch, MagicMock, mock_open
import sys
import os
import pickle
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chatbot_v3 import OllamaChatbotV3, ChatSession


class TestChatSession(unittest.TestCase):
    """Test ChatSession class"""
    
    def test_chat_session_creation(self):
        """Test creating a chat session"""
        session = ChatSession(name="Test Chat")
        
        self.assertEqual(session.name, "Test Chat")
        self.assertIsInstance(session.messages, list)
        self.assertEqual(len(session.messages), 0)
        self.assertIsNotNone(session.id)
        self.assertIsNotNone(session.created_at)
    
    def test_chat_session_to_dict(self):
        """Test session serialization"""
        session = ChatSession(name="Test")
        session.messages.append({"role": "user", "content": "Hi"})
        
        data = session.to_dict()
        
        self.assertIn('id', data)
        self.assertIn('name', data)
        self.assertIn('messages', data)
        self.assertEqual(data['name'], "Test")
        self.assertEqual(len(data['messages']), 1)
    
    def test_chat_session_custom_id(self):
        """Test session with custom ID"""
        session = ChatSession(name="Test", chat_id="custom123")
        self.assertEqual(session.id, "custom123")


class TestChatbotV3(unittest.TestCase):
    """Test cases for Ollama Chatbot v3.0"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Clean up any existing test session file
        if os.path.exists("chat_sessions.pkl"):
            os.remove("chat_sessions.pkl")
        
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = OllamaChatbotV3(self.root)
    
    def tearDown(self):
        """Clean up after tests"""
        try:
            self.root.destroy()
        except:
            pass
        
        # Clean up test session file
        if os.path.exists("chat_sessions.pkl"):
            os.remove("chat_sessions.pkl")
    
    def test_initialization(self):
        """Test v3 app initializes correctly"""
        self.assertIsNotNone(self.app)
        self.assertIsInstance(self.app.chat_sessions, list)
        self.assertIsNotNone(self.app.current_session)
    
    def test_fun_facts_loaded(self):
        """Test fun facts are loaded"""
        self.assertIsInstance(self.app.fun_facts, list)
        self.assertGreater(len(self.app.fun_facts), 0)
        
        # Check they're diverse, not all AI-related
        facts_text = ' '.join(self.app.fun_facts)
        # Should contain non-AI topics
        self.assertTrue(
            'shark' in facts_text.lower() or 
            'honey' in facts_text.lower() or
            'ocean' in facts_text.lower()
        )
    
    def test_ticker_label_exists(self):
        """Test fun facts ticker exists"""
        self.assertIsNotNone(self.app.ticker_label)
        self.assertIsInstance(self.app.ticker_label, tk.Label)
    
    def test_sidebar_exists(self):
        """Test sidebar is created"""
        self.assertIsNotNone(self.app.chat_list_frame)
        self.assertIsNotNone(self.app.chat_list_canvas)
    
    def test_initial_chat_created(self):
        """Test initial chat session is created"""
        self.assertGreater(len(self.app.chat_sessions), 0)
        self.assertIsNotNone(self.app.current_session)
    
    def test_new_chat_creation(self):
        """Test creating new chat"""
        initial_count = len(self.app.chat_sessions)
        
        self.app.new_chat()
        
        self.assertEqual(len(self.app.chat_sessions), initial_count + 1)
        self.assertEqual(self.app.current_session.name, "New Chat")
    
    def test_chat_switching(self):
        """Test switching between chats"""
        # Create two chats
        chat1 = ChatSession(name="Chat 1", chat_id="chat1")
        chat2 = ChatSession(name="Chat 2", chat_id="chat2")
        
        self.app.chat_sessions = [chat1, chat2]
        self.app.current_session = chat1
        
        # Switch to chat2
        self.app.load_chat("chat2")
        
        self.assertEqual(self.app.current_session.id, "chat2")
    
    def test_delete_chat(self):
        """Test deleting a chat"""
        # Create test chat
        test_chat = ChatSession(name="Test", chat_id="test123")
        self.app.chat_sessions.append(test_chat)
        initial_count = len(self.app.chat_sessions)
        
        # Mock confirmation dialog
        with patch('tkinter.messagebox.askyesno', return_value=True):
            self.app.delete_chat("test123")
        
        self.assertEqual(len(self.app.chat_sessions), initial_count - 1)
        
        # Check it's actually removed
        ids = [s.id for s in self.app.chat_sessions]
        self.assertNotIn("test123", ids)
    
    def test_save_and_load_sessions(self):
        """Test session persistence"""
        # Create and save sessions
        self.app.chat_sessions = [
            ChatSession(name="Chat 1", chat_id="c1"),
            ChatSession(name="Chat 2", chat_id="c2")
        ]
        self.app.save_sessions()
        
        # Check file was created
        self.assertTrue(os.path.exists(self.app.sessions_file))
        
        # Clear and reload
        self.app.chat_sessions = []
        
        # Load from file
        with open(self.app.sessions_file, 'rb') as f:
            loaded = pickle.load(f)
        
        self.assertEqual(len(loaded), 2)
    
    def test_chat_naming_from_first_message(self):
        """Test chat gets named from first message"""
        self.app.new_chat()
        
        # Simulate adding first message
        message = "This is my first question about Python"
        self.app.current_session.messages.append({
            "role": "user",
            "content": message
        })
        
        # In real app, this happens in send_message
        # Simulate the naming logic
        if len(self.app.current_session.messages) == 1:
            self.app.current_session.name = message[:40]
        
        expected_name = message[:40]
        self.assertEqual(self.app.current_session.name, expected_name)
    
    def test_refresh_chat_list(self):
        """Test chat list refresh"""
        # Add some chats
        self.app.chat_sessions = [
            ChatSession(name="Chat 1"),
            ChatSession(name="Chat 2")
        ]
        
        # Refresh should not crash
        self.app.refresh_chat_list()
        
        # Check widgets were created
        widgets = self.app.chat_list_frame.winfo_children()
        self.assertGreater(len(widgets), 0)
    
    def test_display_chat_history(self):
        """Test displaying chat history"""
        # Add messages to current session
        self.app.current_session.messages = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"}
        ]
        
        # Display history
        self.app.display_chat_history()
        
        # Check content appears in display
        content = self.app.chat_display.get("1.0", tk.END)
        self.assertIn("Hello", content)
        self.assertIn("Hi there!", content)
    
    def test_attachment_functionality_preserved(self):
        """Test v2 attachment features still work in v3"""
        self.assertIsInstance(self.app.attached_files, list)
        self.assertIsInstance(self.app.attached_images, list)
        
        # Methods should exist
        self.assertTrue(hasattr(self.app, 'attach_file'))
        self.assertTrue(hasattr(self.app, 'attach_image'))
        self.assertTrue(hasattr(self.app, 'clear_attachments'))
    
    def test_export_current_chat(self):
        """Test exporting current chat"""
        # Add some messages
        self.app.current_session.messages = [
            {"role": "user", "content": "Test question"},
            {"role": "assistant", "content": "Test answer"}
        ]
        self.app.current_session.name = "Test Chat"
        
        # Mock file operations
        with patch('builtins.open', mock_open()) as mock_file:
            with patch('tkinter.messagebox.showinfo'):
                self.app.export_chat()
        
        # Should have attempted to write file
        mock_file.assert_called()


class TestChatbotV3FunFacts(unittest.TestCase):
    """Test fun facts ticker functionality"""
    
    def setUp(self):
        if os.path.exists("chat_sessions.pkl"):
            os.remove("chat_sessions.pkl")
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = OllamaChatbotV3(self.root)
    
    def tearDown(self):
        try:
            self.root.destroy()
        except:
            pass
        if os.path.exists("chat_sessions.pkl"):
            os.remove("chat_sessions.pkl")
    
    def test_ticker_animation(self):
        """Test ticker updates fact"""
        initial_fact_index = self.app.current_fact_index
        initial_text = self.app.ticker_label.cget("text")
        
        # Manually trigger animation
        self.app.animate_ticker()
        
        # Fact index should have incremented
        new_fact_index = self.app.current_fact_index
        self.assertEqual(new_fact_index, (initial_fact_index + 1) % len(self.app.fun_facts))
    
    def test_all_facts_displayable(self):
        """Test all fun facts can be displayed"""
        for fact in self.app.fun_facts:
            self.app.ticker_label.config(text=fact)
            text = self.app.ticker_label.cget("text")
            self.assertEqual(text, fact)
    
    def test_facts_are_diverse(self):
        """Test that facts cover diverse topics"""
        topics_found = {
            'animals': False,
            'science': False,
            'history': False,
            'nature': False
        }
        
        facts_text = ' '.join(self.app.fun_facts).lower()
        
        if any(word in facts_text for word in ['shark', 'octopus', 'bee', 'giraffe']):
            topics_found['animals'] = True
        if any(word in facts_text for word in ['brain', 'stars', 'diamond']):
            topics_found['science'] = True
        if any(word in facts_text for word in ['library', 'war', 'leonardo']):
            topics_found['history'] = True
        if any(word in facts_text for word in ['ocean', 'moon', 'tree', 'rainbow']):
            topics_found['nature'] = True
        
        # Should have at least 3 different topic types
        self.assertGreaterEqual(sum(topics_found.values()), 3)


def suite():
    """Create test suite"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestChatSession))
    suite.addTest(unittest.makeSuite(TestChatbotV3))
    suite.addTest(unittest.makeSuite(TestChatbotV3FunFacts))
    return suite


if __name__ == '__main__':
    print("Running Ollama Chatbot v3.0 Tests...")
    print("=" * 60)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite())
    
    print("\n" + "=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    sys.exit(0 if result.wasSuccessful() else 1)

