"""
Ollama Chatbot v3.0 - ChatGPT-Inspired Interface
Professional chatbot with modern UI, chat history, and fun facts ticker
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
import json
import threading
from datetime import datetime
import os
import base64
from PIL import Image, ImageTk
import pickle
import random

class ChatSession:
    """Represents a single chat conversation"""
    def __init__(self, name="New Chat", chat_id=None):
        self.id = chat_id or datetime.now().strftime("%Y%m%d_%H%M%S")
        self.name = name
        self.messages = []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'messages': self.messages,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class OllamaChatbotV3:
    def __init__(self, root):
        self.root = root
        self.root.title("Ollama AI Assistant v3.0")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        # Modern color scheme (ChatGPT-inspired)
        self.colors = {
            'bg_primary': '#ffffff',
            'bg_secondary': '#f7f7f8',
            'bg_tertiary': '#ececf1',
            'sidebar': '#202123',
            'sidebar_hover': '#2a2b32',
            'accent': '#10a37f',
            'accent_hover': '#1a7f64',
            'text_primary': '#353740',
            'text_secondary': '#6e6e80',
            'text_white': '#ffffff',
            'border': '#d9d9e3',
            'user_msg': '#f7f7f8',
            'bot_msg': '#ffffff',
            'ticker_bg': '#10a37f',
            'ticker_text': '#ffffff',
        }
        
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Configuration
        self.ollama_url = "http://localhost:11434/api/chat"
        self.current_model = tk.StringVar(value="llama2")
        self.temperature = tk.DoubleVar(value=0.7)
        self.system_prompt = "You are a helpful AI assistant that can analyze files and images."
        self.is_generating = False
        
        # Chat history management
        self.chat_sessions = []
        self.current_session = None
        self.sessions_file = "chat_sessions.pkl"
        
        # File/Image handling
        self.attached_files = []
        self.attached_images = []
        self.current_image_data = None
        
        # Fun facts - diverse and interesting!
        self.fun_facts = [
            "🦈 Sharks have been around longer than trees - about 400 million years!",
            "🍯 Honey never spoils - archaeologists found 3,000 year old honey that's still edible!",
            "🌍 There are more stars in the universe than grains of sand on all Earth's beaches!",
            "🐙 Octopuses have three hearts and blue blood!",
            "🎵 Music can make plants grow faster according to studies!",
            "🧠 Your brain uses 20% of your body's energy while being only 2% of your weight!",
            "🌙 The Moon is moving away from Earth at about 1.5 inches per year!",
            "💎 Diamonds can be made from peanut butter under extreme pressure!",
            "🐝 A single bee produces only 1/12 of a teaspoon of honey in its lifetime!",
            "📚 The world's oldest known library is in Morocco, founded in 859 AD!",
            "🎨 Leonardo da Vinci could write with one hand and draw with the other simultaneously!",
            "🌊 Ocean waves can travel thousands of miles without losing energy!",
            "🦎 Some lizards can detach their tails and grow new ones!",
            "☕ Coffee is the world's second most traded commodity after oil!",
            "🎯 Bananas are berries, but strawberries aren't!",
            "🌈 A rainbow can only be seen if the sun is behind you!",
            "🦒 Giraffes only need 5-30 minutes of sleep per day!",
            "📖 The shortest war in history lasted only 38 minutes!",
            "🎪 The Eiffel Tower can grow up to 6 inches taller in summer due to heat!",
            "🐌 Snails can sleep for up to 3 years!",
        ]
        self.current_fact_index = 0
        
        # Setup GUI
        self.setup_gui()
        
        # Load sessions after GUI is ready
        self.load_sessions()
        
        # Start fun facts ticker
        self.animate_ticker()
        
        # Check Ollama connection
        self.root.after(100, self.check_ollama_connection)
    
    def setup_gui(self):
        """Setup the main GUI layout"""
        # Fun facts ticker at the top
        self.create_ticker()
        
        # Main container with sidebar
        main_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left sidebar
        self.create_sidebar(main_frame)
        
        # Right main area
        right_container = tk.Frame(main_frame, bg=self.colors['bg_primary'])
        right_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Chat display
        self.create_chat_display(right_container)
        
        # Input area
        self.create_input_area(right_container)
        
        # Settings panel (collapsible)
        self.create_compact_settings(right_container)
    
    def create_ticker(self):
        """Create animated fun facts ticker"""
        ticker_frame = tk.Frame(
            self.root,
            bg=self.colors['ticker_bg'],
            height=35
        )
        ticker_frame.pack(fill=tk.X, side=tk.TOP)
        ticker_frame.pack_propagate(False)
        
        self.ticker_label = tk.Label(
            ticker_frame,
            text="",
            font=("Arial", 10),
            bg=self.colors['ticker_bg'],
            fg=self.colors['ticker_text'],
            anchor=tk.W
        )
        self.ticker_label.pack(fill=tk.BOTH, expand=True, padx=20)
    
    def animate_ticker(self):
        """Animate the fun facts ticker"""
        fact = self.fun_facts[self.current_fact_index]
        self.ticker_label.config(text=fact)
        
        # Fade effect by changing to next fact
        self.current_fact_index = (self.current_fact_index + 1) % len(self.fun_facts)
        
        # Update every 5 seconds
        self.root.after(5000, self.animate_ticker)
    
    def create_sidebar(self, parent):
        """Create left sidebar with chat history"""
        sidebar = tk.Frame(
            parent,
            bg=self.colors['sidebar'],
            width=280
        )
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        # Header
        header_frame = tk.Frame(sidebar, bg=self.colors['sidebar'])
        header_frame.pack(fill=tk.X, pady=15, padx=10)
        
        # New Chat button
        new_chat_btn = tk.Button(
            header_frame,
            text="+ New Chat",
            command=self.new_chat,
            bg=self.colors['sidebar'],
            fg=self.colors['text_white'],
            font=("Arial", 11, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            borderwidth=1,
            highlightthickness=1,
            highlightbackground=self.colors['border'],
            padx=15,
            pady=10
        )
        new_chat_btn.pack(fill=tk.X)
        new_chat_btn.bind("<Enter>", lambda e: new_chat_btn.configure(bg=self.colors['sidebar_hover']))
        new_chat_btn.bind("<Leave>", lambda e: new_chat_btn.configure(bg=self.colors['sidebar']))
        
        # Separator
        sep = tk.Frame(sidebar, height=1, bg=self.colors['border'])
        sep.pack(fill=tk.X, pady=10)
        
        # Chat history label
        tk.Label(
            sidebar,
            text="Recent Chats",
            font=("Arial", 10, "bold"),
            bg=self.colors['sidebar'],
            fg=self.colors['text_secondary'],
            anchor=tk.W
        ).pack(fill=tk.X, padx=15, pady=(5, 10))
        
        # Scrollable chat list
        canvas_frame = tk.Frame(sidebar, bg=self.colors['sidebar'])
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5)
        
        scrollbar = tk.Scrollbar(canvas_frame, bg=self.colors['sidebar'])
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.chat_list_canvas = tk.Canvas(
            canvas_frame,
            bg=self.colors['sidebar'],
            highlightthickness=0,
            yscrollcommand=scrollbar.set
        )
        self.chat_list_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.chat_list_canvas.yview)
        
        self.chat_list_frame = tk.Frame(self.chat_list_canvas, bg=self.colors['sidebar'])
        self.chat_list_canvas.create_window((0, 0), window=self.chat_list_frame, anchor=tk.NW)
        
        self.chat_list_frame.bind("<Configure>", lambda e: self.chat_list_canvas.configure(
            scrollregion=self.chat_list_canvas.bbox("all")
        ))
        
        # Footer with version
        footer = tk.Label(
            sidebar,
            text="v3.0 | Ollama AI",
            font=("Arial", 8),
            bg=self.colors['sidebar'],
            fg=self.colors['text_secondary']
        )
        footer.pack(side=tk.BOTTOM, pady=10)
        
        # Populate chat list
        self.refresh_chat_list()
    
    def refresh_chat_list(self):
        """Refresh the chat list in sidebar"""
        # Clear existing
        for widget in self.chat_list_frame.winfo_children():
            widget.destroy()
        
        # Add chat buttons
        for session in reversed(self.chat_sessions):  # Most recent first
            self.create_chat_button(session)
    
    def create_chat_button(self, session):
        """Create a button for a chat session"""
        is_active = self.current_session and session.id == self.current_session.id
        
        btn_frame = tk.Frame(
            self.chat_list_frame,
            bg=self.colors['sidebar_hover'] if is_active else self.colors['sidebar']
        )
        btn_frame.pack(fill=tk.X, padx=5, pady=2)
        
        btn = tk.Button(
            btn_frame,
            text=session.name[:30] + "..." if len(session.name) > 30 else session.name,
            command=lambda: self.load_chat(session.id),
            bg=self.colors['sidebar_hover'] if is_active else self.colors['sidebar'],
            fg=self.colors['text_white'],
            font=("Arial", 10),
            relief=tk.FLAT,
            cursor="hand2",
            anchor=tk.W,
            padx=10,
            pady=8
        )
        btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        if not is_active:
            btn.bind("<Enter>", lambda e: btn.configure(bg=self.colors['sidebar_hover']))
            btn.bind("<Leave>", lambda e: btn.configure(bg=self.colors['sidebar']))
        
        # Delete button
        del_btn = tk.Button(
            btn_frame,
            text="🗑",
            command=lambda: self.delete_chat(session.id),
            bg=self.colors['sidebar_hover'] if is_active else self.colors['sidebar'],
            fg=self.colors['text_secondary'],
            font=("Arial", 10),
            relief=tk.FLAT,
            cursor="hand2",
            width=3
        )
        del_btn.pack(side=tk.RIGHT)
        del_btn.bind("<Enter>", lambda e: del_btn.configure(fg="#ff4444"))
        del_btn.bind("<Leave>", lambda e: del_btn.configure(fg=self.colors['text_secondary']))
    
    def create_chat_display(self, parent):
        """Create the chat display area"""
        chat_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(chat_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Chat display
        self.chat_display = tk.Text(
            chat_frame,
            bg=self.colors['bg_primary'],
            fg=self.colors['text_primary'],
            font=("Arial", 11),
            wrap=tk.WORD,
            padx=20,
            pady=20,
            yscrollcommand=scrollbar.set,
            state=tk.DISABLED,
            relief=tk.FLAT,
            spacing3=15,
            borderwidth=0
        )
        self.chat_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.chat_display.yview)
        
        # Configure text tags
        self.chat_display.tag_config(
            "user",
            foreground=self.colors['text_primary'],
            background=self.colors['user_msg'],
            font=("Arial", 11),
            spacing1=10,
            spacing3=10,
            lmargin1=15,
            lmargin2=15,
            rmargin=15,
            borderwidth=1,
            relief=tk.SOLID
        )
        self.chat_display.tag_config(
            "bot",
            foreground=self.colors['text_primary'],
            background=self.colors['bot_msg'],
            font=("Arial", 11),
            spacing1=10,
            spacing3=10,
            lmargin1=15,
            lmargin2=15,
            rmargin=15
        )
        self.chat_display.tag_config(
            "header",
            foreground=self.colors['text_secondary'],
            font=("Arial", 9, "bold")
        )
        self.chat_display.tag_config(
            "system",
            foreground=self.colors['text_secondary'],
            font=("Arial", 9, "italic"),
            justify=tk.CENTER
        )
    
    def create_input_area(self, parent):
        """Create the message input area"""
        input_container = tk.Frame(parent, bg=self.colors['bg_primary'])
        input_container.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Input frame with border
        input_frame = tk.Frame(
            input_container,
            bg=self.colors['bg_secondary'],
            relief=tk.SOLID,
            borderwidth=1,
            highlightbackground=self.colors['border'],
            highlightthickness=1
        )
        input_frame.pack(fill=tk.X)
        
        # Attachment buttons row
        attach_frame = tk.Frame(input_frame, bg=self.colors['bg_secondary'])
        attach_frame.pack(fill=tk.X, padx=10, pady=(8, 0))
        
        # Attach buttons
        tk.Button(
            attach_frame,
            text="📁 File",
            command=self.attach_file,
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary'],
            font=("Arial", 9),
            relief=tk.FLAT,
            cursor="hand2",
            padx=10,
            pady=4
        ).pack(side=tk.LEFT, padx=2)
        
        tk.Button(
            attach_frame,
            text="🖼 Image",
            command=self.attach_image,
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary'],
            font=("Arial", 9),
            relief=tk.FLAT,
            cursor="hand2",
            padx=10,
            pady=4
        ).pack(side=tk.LEFT, padx=2)
        
        # Attachment preview
        self.attachment_preview = tk.Label(
            attach_frame,
            text="",
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary'],
            font=("Arial", 8)
        )
        self.attachment_preview.pack(side=tk.LEFT, padx=10)
        
        # Text input with send button
        text_frame = tk.Frame(input_frame, bg=self.colors['bg_secondary'])
        text_frame.pack(fill=tk.X, padx=10, pady=8)
        
        self.message_input = tk.Text(
            text_frame,
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            font=("Arial", 11),
            wrap=tk.WORD,
            height=3,
            relief=tk.FLAT,
            insertbackground=self.colors['accent'],
            borderwidth=0
        )
        self.message_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        self.message_input.bind("<Return>", self.on_enter_key)
        self.message_input.bind("<Shift-Return>", lambda e: None)
        
        # Send button
        self.send_button = tk.Button(
            text_frame,
            text="→",
            command=self.send_message,
            bg=self.colors['accent'],
            fg=self.colors['text_white'],
            font=("Arial", 16, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            width=3,
            height=1
        )
        self.send_button.pack(side=tk.RIGHT)
        self.send_button.bind("<Enter>", lambda e: self.send_button.configure(bg=self.colors['accent_hover']))
        self.send_button.bind("<Leave>", lambda e: self.send_button.configure(bg=self.colors['accent']))
    
    def create_compact_settings(self, parent):
        """Create compact settings area"""
        settings_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        settings_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        # Settings in one row
        tk.Label(
            settings_frame,
            text="Model:",
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary'],
            font=("Arial", 9)
        ).pack(side=tk.LEFT, padx=(10, 5))
        
        models = ["llama2", "llava", "mistral", "codellama", "llama3", "phi"]
        model_menu = ttk.Combobox(
            settings_frame,
            textvariable=self.current_model,
            values=models,
            state="readonly",
            font=("Arial", 9),
            width=12
        )
        model_menu.pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            settings_frame,
            text="Temp:",
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary'],
            font=("Arial", 9)
        ).pack(side=tk.LEFT, padx=(20, 5))
        
        self.temp_label = tk.Label(
            settings_frame,
            text=f"{self.temperature.get():.1f}",
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            font=("Arial", 9, "bold"),
            width=3
        )
        self.temp_label.pack(side=tk.LEFT, padx=2)
        
        temp_slider = tk.Scale(
            settings_frame,
            from_=0.0,
            to=2.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            variable=self.temperature,
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            troughcolor=self.colors['bg_tertiary'],
            highlightthickness=0,
            showvalue=0,
            command=self.update_temp_label,
            length=120
        )
        temp_slider.pack(side=tk.LEFT, padx=5)
        
        # Export button
        tk.Button(
            settings_frame,
            text="Export",
            command=self.export_chat,
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary'],
            font=("Arial", 9),
            relief=tk.FLAT,
            cursor="hand2",
            padx=10,
            pady=4
        ).pack(side=tk.RIGHT, padx=10)
        
        # Connection indicator
        self.connection_indicator = tk.Label(
            settings_frame,
            text="● Checking...",
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary'],
            font=("Arial", 8)
        )
        self.connection_indicator.pack(side=tk.RIGHT, padx=10)
    
    def update_temp_label(self, value):
        """Update temperature label"""
        self.temp_label.config(text=f"{float(value):.1f}")
    
    def check_ollama_connection(self):
        """Check if Ollama is running"""
        def check():
            try:
                response = requests.get("http://localhost:11434/api/tags", timeout=2)
                if response.status_code == 200:
                    self.connection_indicator.config(text="● Connected", fg="#2ecc71")
                else:
                    self.connection_indicator.config(text="● Error", fg="#e74c3c")
            except Exception:
                self.connection_indicator.config(text="● Disconnected", fg="#e74c3c")
        
        threading.Thread(target=check, daemon=True).start()
    
    # Chat session management
    def load_sessions(self):
        """Load chat sessions from file"""
        try:
            if os.path.exists(self.sessions_file):
                with open(self.sessions_file, 'rb') as f:
                    data = pickle.load(f)
                    self.chat_sessions = data
                    
                    if self.chat_sessions:
                        self.current_session = self.chat_sessions[-1]
        except Exception as e:
            print(f"Error loading sessions: {e}")
            self.chat_sessions = []
        
        # Create initial session if none exist
        if not self.chat_sessions:
            self.new_chat()
    
    def save_sessions(self):
        """Save chat sessions to file"""
        try:
            with open(self.sessions_file, 'wb') as f:
                pickle.dump(self.chat_sessions, f)
        except Exception as e:
            print(f"Error saving sessions: {e}")
    
    def new_chat(self):
        """Create a new chat session"""
        session = ChatSession(name="New Chat")
        self.chat_sessions.append(session)
        self.current_session = session
        
        # Clear display
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.config(state=tk.DISABLED)
        
        self.save_sessions()
        self.refresh_chat_list()
    
    def load_chat(self, session_id):
        """Load a specific chat session"""
        for session in self.chat_sessions:
            if session.id == session_id:
                self.current_session = session
                self.refresh_chat_list()
                self.display_chat_history()
                break
    
    def delete_chat(self, session_id):
        """Delete a chat session"""
        if messagebox.askyesno("Delete Chat", "Are you sure you want to delete this chat?"):
            self.chat_sessions = [s for s in self.chat_sessions if s.id != session_id]
            
            if self.current_session and self.current_session.id == session_id:
                if self.chat_sessions:
                    self.current_session = self.chat_sessions[-1]
                    self.display_chat_history()
                else:
                    self.new_chat()
            
            self.save_sessions()
            self.refresh_chat_list()
    
    def display_chat_history(self):
        """Display current session's chat history"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("1.0", tk.END)
        
        if self.current_session:
            for msg in self.current_session.messages:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                self.display_message(content, role, add_to_history=False)
        
        self.chat_display.config(state=tk.DISABLED)
    
    # File/Image handling
    def attach_file(self):
        """Attach a file"""
        file_path = filedialog.askopenfilename(
            title="Select a file",
            filetypes=[("All Files", "*.*"), ("Text Files", "*.txt"), ("Python Files", "*.py")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()[:5000]
                
                self.attached_files.append({
                    'name': os.path.basename(file_path),
                    'content': content
                })
                self.update_attachment_display()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read file: {str(e)}")
    
    def attach_image(self):
        """Attach an image"""
        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")]
        )
        
        if file_path:
            try:
                with open(file_path, 'rb') as f:
                    image_data = base64.b64encode(f.read()).decode('utf-8')
                
                self.attached_images.append({
                    'name': os.path.basename(file_path),
                    'data': image_data
                })
                self.current_image_data = image_data
                self.update_attachment_display()
                
                if self.current_model.get() != "llava":
                    if messagebox.askyesno("Switch Model?", "Switch to 'llava' for image analysis?"):
                        self.current_model.set("llava")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read image: {str(e)}")
    
    def update_attachment_display(self):
        """Update attachment preview"""
        total = len(self.attached_files) + len(self.attached_images)
        if total > 0:
            text = f"📎 {len(self.attached_files)} file(s), {len(self.attached_images)} image(s)"
            self.attachment_preview.config(text=text)
        else:
            self.attachment_preview.config(text="")
    
    def clear_attachments(self):
        """Clear attachments"""
        self.attached_files = []
        self.attached_images = []
        self.current_image_data = None
        self.update_attachment_display()
    
    # Messaging
    def on_enter_key(self, event):
        """Handle Enter key"""
        if not event.state & 0x1:
            self.send_message()
            return "break"
    
    def send_message(self):
        """Send message"""
        message = self.message_input.get("1.0", tk.END).strip()
        
        if not message and not self.attached_files and not self.attached_images:
            return
        
        if self.is_generating:
            messagebox.showwarning("Wait", "Please wait for current response.")
            return
        
        # Build full message with files
        full_message = message
        if self.attached_files:
            full_message += "\n\n--- Files ---\n"
            for f in self.attached_files:
                full_message += f"\n{f['name']}:\n{f['content']}\n"
        
        # Clear input
        self.message_input.delete("1.0", tk.END)
        
        # Display user message
        self.display_message(message, "user")
        
        # Add to session
        msg_obj = {"role": "user", "content": full_message}
        if self.attached_images and self.current_image_data:
            msg_obj["images"] = [self.current_image_data]
        
        self.current_session.messages.append(msg_obj)
        
        # Update chat name if first message
        if len(self.current_session.messages) == 1:
            self.current_session.name = message[:40] + "..." if len(message) > 40 else message
            self.refresh_chat_list()
        
        self.current_session.updated_at = datetime.now()
        self.save_sessions()
        
        # Clear attachments
        self.clear_attachments()
        
        # Get response
        self.is_generating = True
        self.send_button.config(state=tk.DISABLED, text="...")
        threading.Thread(target=self.get_bot_response, daemon=True).start()
    
    def get_bot_response(self):
        """Get AI response"""
        try:
            payload = {
                "model": self.current_model.get(),
                "messages": [{"role": "system", "content": self.system_prompt}] + self.current_session.messages,
                "stream": False,
                "options": {"temperature": self.temperature.get()}
            }
            
            response = requests.post(self.ollama_url, json=payload, timeout=120)
            
            if response.status_code == 200:
                result = response.json()
                bot_message = result.get("message", {}).get("content", "No response")
                
                self.current_session.messages.append({"role": "assistant", "content": bot_message})
                self.current_session.updated_at = datetime.now()
                self.save_sessions()
                
                self.root.after(0, lambda: self.display_message(bot_message, "bot"))
            else:
                error = f"Error: {response.status_code}"
                self.root.after(0, lambda: self.display_message(error, "system"))
        
        except Exception as e:
            error = f"Error: {str(e)}"
            self.root.after(0, lambda: self.display_message(error, "system"))
        
        finally:
            self.is_generating = False
            self.root.after(0, lambda: self.send_button.config(state=tk.NORMAL, text="→"))
    
    def display_message(self, message, sender, add_to_history=True):
        """Display a message"""
        self.chat_display.config(state=tk.NORMAL)
        
        if sender == "user":
            prefix = "You"
            tag = "user"
        elif sender == "bot" or sender == "assistant":
            prefix = "AI Assistant"
            tag = "bot"
        else:
            prefix = "System"
            tag = "system"
        
        self.chat_display.insert(tk.END, "\n")
        self.chat_display.insert(tk.END, f"{prefix}\n", "header")
        self.chat_display.insert(tk.END, f"{message}\n", tag)
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def export_chat(self):
        """Export current chat"""
        if not self.current_session or not self.current_session.messages:
            messagebox.showinfo("Export", "No chat to export.")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chat_{self.current_session.name[:20]}_{timestamp}.txt"
        
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"Chat Export: {self.current_session.name}\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n\n")
                
                for msg in self.current_session.messages:
                    role = msg["role"].upper()
                    content = msg["content"]
                    f.write(f"{role}:\n{content}\n\n")
            
            messagebox.showinfo("Export Complete", f"Saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}")


def main():
    root = tk.Tk()
    app = OllamaChatbotV3(root)
    root.mainloop()


if __name__ == "__main__":
    main()

