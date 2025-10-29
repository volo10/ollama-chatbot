"""
Ollama Chatbot v2.0 with File & Image Support
A professional chatbot application with file/image input capabilities.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import requests
import json
import threading
from datetime import datetime
import os
import base64
from PIL import Image, ImageTk
import io

class OllamaChatbotV2:
    def __init__(self, root):
        self.root = root
        self.root.title("Ollama AI Assistant v2.0")
        self.root.geometry("1200x800")
        self.root.minsize(900, 700)
        
        # Color scheme
        self.colors = {
            'bg_primary': '#1a1a2e',
            'bg_secondary': '#16213e',
            'bg_tertiary': '#0f3460',
            'accent': '#e94560',
            'accent_hover': '#ff6b81',
            'text_primary': '#ffffff',
            'text_secondary': '#a0a0a0',
            'success': '#2ecc71',
            'warning': '#f39c12',
            'user_msg': '#2d4059',
            'bot_msg': '#16213e',
            'file_bg': '#2c3e50',
        }
        
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Configuration
        self.ollama_url = "http://localhost:11434/api/chat"
        self.current_model = tk.StringVar(value="llama2")
        self.temperature = tk.DoubleVar(value=0.7)
        self.system_prompt = "You are a helpful AI assistant that can analyze files and images."
        self.chat_history = []
        self.is_generating = False
        
        # File/Image handling
        self.attached_files = []
        self.attached_images = []
        self.current_image_data = None
        
        # Setup GUI
        self.setup_gui()
        
        # Check Ollama connection
        self.root.after(100, self.check_ollama_connection)
    
    def setup_gui(self):
        """Setup the main GUI layout"""
        self.create_top_bar()
        
        main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.create_chat_display(main_container)
        self.create_attachment_preview(main_container)
        self.create_input_area(main_container)
        self.create_side_panel(main_container)
        self.create_status_bar()
    
    def create_top_bar(self):
        """Create the top bar with logo and controls"""
        top_bar = tk.Frame(self.root, bg=self.colors['bg_secondary'], height=60)
        top_bar.pack(fill=tk.X, padx=10, pady=(10, 5))
        top_bar.pack_propagate(False)
        
        # Logo/Title
        title_frame = tk.Frame(top_bar, bg=self.colors['bg_secondary'])
        title_frame.pack(side=tk.LEFT, padx=20, pady=10)
        
        logo_label = tk.Label(
            title_frame,
            text="🤖",
            font=("Arial", 24),
            bg=self.colors['bg_secondary'],
            fg=self.colors['accent']
        )
        logo_label.pack(side=tk.LEFT, padx=(0, 10))
        
        title_label = tk.Label(
            title_frame,
            text="Ollama AI Assistant v2.0",
            font=("Arial", 18, "bold"),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary']
        )
        title_label.pack(side=tk.LEFT)
        
        version_label = tk.Label(
            title_frame,
            text="📁🖼️",
            font=("Arial", 16),
            bg=self.colors['bg_secondary'],
            fg=self.colors['warning']
        )
        version_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Control Buttons
        btn_frame = tk.Frame(top_bar, bg=self.colors['bg_secondary'])
        btn_frame.pack(side=tk.RIGHT, padx=20, pady=10)
        
        self.create_styled_button(
            btn_frame,
            text="Clear Chat",
            command=self.clear_chat,
            width=12
        ).pack(side=tk.LEFT, padx=5)
        
        self.create_styled_button(
            btn_frame,
            text="Export Chat",
            command=self.export_chat,
            width=12
        ).pack(side=tk.LEFT, padx=5)
    
    def create_chat_display(self, parent):
        """Create the chat display area"""
        chat_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        chat_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=5)
        
        canvas_frame = tk.Frame(chat_frame, bg=self.colors['bg_secondary'], relief=tk.RIDGE, bd=2)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(canvas_frame, bg=self.colors['bg_tertiary'])
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.chat_display = tk.Text(
            canvas_frame,
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            font=("Arial", 11),
            wrap=tk.WORD,
            padx=15,
            pady=15,
            yscrollcommand=scrollbar.set,
            state=tk.DISABLED,
            relief=tk.FLAT,
            spacing3=10
        )
        self.chat_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.chat_display.yview)
        
        # Configure text tags
        self.chat_display.tag_config(
            "user",
            foreground=self.colors['text_primary'],
            background=self.colors['user_msg'],
            font=("Arial", 11),
            spacing1=5,
            spacing3=5,
            lmargin1=10,
            lmargin2=10,
            rmargin=10
        )
        self.chat_display.tag_config(
            "bot",
            foreground=self.colors['text_primary'],
            background=self.colors['bot_msg'],
            font=("Arial", 11),
            spacing1=5,
            spacing3=5,
            lmargin1=10,
            lmargin2=10,
            rmargin=10
        )
        self.chat_display.tag_config(
            "timestamp",
            foreground=self.colors['text_secondary'],
            font=("Arial", 8)
        )
        self.chat_display.tag_config(
            "system",
            foreground=self.colors['accent'],
            font=("Arial", 9, "italic"),
            justify=tk.CENTER
        )
        self.chat_display.tag_config(
            "file_attach",
            foreground=self.colors['warning'],
            font=("Arial", 9),
            background=self.colors['file_bg']
        )
    
    def create_attachment_preview(self, parent):
        """Create attachment preview area"""
        self.preview_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        # Initially hidden, will pack when attachments are added
        
        preview_container = tk.Frame(
            self.preview_frame,
            bg=self.colors['bg_secondary'],
            relief=tk.RIDGE,
            bd=2
        )
        preview_container.pack(fill=tk.X, pady=(0, 5))
        
        preview_label = tk.Label(
            preview_container,
            text="📎 Attachments:",
            font=("Arial", 10, "bold"),
            bg=self.colors['bg_secondary'],
            fg=self.colors['warning']
        )
        preview_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.attachment_list = tk.Frame(preview_container, bg=self.colors['bg_secondary'])
        self.attachment_list.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        
        clear_attach_btn = tk.Button(
            preview_container,
            text="Clear All",
            command=self.clear_attachments,
            bg=self.colors['accent'],
            fg=self.colors['text_primary'],
            font=("Arial", 9),
            relief=tk.FLAT,
            cursor="hand2"
        )
        clear_attach_btn.pack(side=tk.RIGHT, padx=10)
    
    def create_input_area(self, parent):
        """Create the message input area with file/image buttons"""
        input_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        input_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=(5, 0))
        
        input_container = tk.Frame(input_frame, bg=self.colors['bg_secondary'], relief=tk.RIDGE, bd=2)
        input_container.pack(fill=tk.BOTH, expand=True)
        
        # Attachment buttons row
        attach_frame = tk.Frame(input_container, bg=self.colors['bg_secondary'])
        attach_frame.pack(fill=tk.X, padx=5, pady=(5, 0))
        
        self.create_styled_button(
            attach_frame,
            text="📁 Attach File",
            command=self.attach_file,
            width=12,
            height=1
        ).pack(side=tk.LEFT, padx=2)
        
        self.create_styled_button(
            attach_frame,
            text="🖼️ Attach Image",
            command=self.attach_image,
            width=12,
            height=1
        ).pack(side=tk.LEFT, padx=2)
        
        # File type hint
        hint_label = tk.Label(
            attach_frame,
            text="Supports: Images (JPG, PNG), Text, Code, PDFs, etc.",
            font=("Arial", 8),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary']
        )
        hint_label.pack(side=tk.LEFT, padx=10)
        
        # Text input
        self.message_input = tk.Text(
            input_container,
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary'],
            font=("Arial", 11),
            wrap=tk.WORD,
            height=4,
            padx=10,
            pady=10,
            relief=tk.FLAT,
            insertbackground=self.colors['accent']
        )
        self.message_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.message_input.bind("<Return>", self.on_enter_key)
        self.message_input.bind("<Shift-Return>", lambda e: None)
        
        # Send button
        btn_container = tk.Frame(input_container, bg=self.colors['bg_secondary'])
        btn_container.pack(side=tk.RIGHT, padx=5, pady=5)
        
        self.send_button = self.create_styled_button(
            btn_container,
            text="Send\n→",
            command=self.send_message,
            width=8,
            height=2
        )
        self.send_button.pack()
    
    def create_side_panel(self, parent):
        """Create the settings side panel"""
        side_panel = tk.Frame(parent, bg=self.colors['bg_secondary'], width=280, relief=tk.RIDGE, bd=2)
        side_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0), pady=5)
        side_panel.pack_propagate(False)
        
        # Title
        title = tk.Label(
            side_panel,
            text="⚙️ Settings",
            font=("Arial", 14, "bold"),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary']
        )
        title.pack(pady=(15, 10))
        
        sep = tk.Frame(side_panel, height=2, bg=self.colors['accent'])
        sep.pack(fill=tk.X, padx=20, pady=5)
        
        # Model Selection
        self.create_setting_section(
            side_panel,
            "Model:",
            self.create_model_selector
        )
        
        # Vision model info
        vision_info = tk.Label(
            side_panel,
            text="💡 Use 'llava' for image analysis",
            font=("Arial", 8, "italic"),
            bg=self.colors['bg_secondary'],
            fg=self.colors['warning'],
            wraplength=240
        )
        vision_info.pack(pady=(0, 10))
        
        # Temperature
        self.create_setting_section(
            side_panel,
            "Temperature:",
            self.create_temperature_slider
        )
        
        # System Prompt
        self.create_setting_section(
            side_panel,
            "System Prompt:",
            self.create_system_prompt_input
        )
        
        # Connection Status
        self.create_connection_status(side_panel)
    
    def create_setting_section(self, parent, label_text, widget_creator):
        """Create a setting section"""
        section = tk.Frame(parent, bg=self.colors['bg_secondary'])
        section.pack(fill=tk.X, padx=15, pady=10)
        
        label = tk.Label(
            section,
            text=label_text,
            font=("Arial", 10, "bold"),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary'],
            anchor=tk.W
        )
        label.pack(anchor=tk.W, pady=(0, 5))
        
        widget_creator(section)
    
    def create_model_selector(self, parent):
        """Create model selection dropdown"""
        models = ["llama2", "llava", "mistral", "codellama", "llama3", "phi", "gemma"]
        
        model_menu = ttk.Combobox(
            parent,
            textvariable=self.current_model,
            values=models,
            state="readonly",
            font=("Arial", 10)
        )
        model_menu.pack(fill=tk.X)
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            'TCombobox',
            fieldbackground=self.colors['bg_tertiary'],
            background=self.colors['bg_tertiary'],
            foreground=self.colors['text_primary'],
            arrowcolor=self.colors['accent']
        )
    
    def create_temperature_slider(self, parent):
        """Create temperature slider"""
        slider_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        slider_frame.pack(fill=tk.X)
        
        self.temp_label = tk.Label(
            slider_frame,
            text=f"{self.temperature.get():.1f}",
            font=("Arial", 9),
            bg=self.colors['bg_secondary'],
            fg=self.colors['accent']
        )
        self.temp_label.pack(side=tk.RIGHT)
        
        slider = tk.Scale(
            slider_frame,
            from_=0.0,
            to=2.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            variable=self.temperature,
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            troughcolor=self.colors['bg_tertiary'],
            highlightthickness=0,
            activebackground=self.colors['accent'],
            command=self.update_temp_label,
            showvalue=0
        )
        slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    def create_system_prompt_input(self, parent):
        """Create system prompt text area"""
        self.system_prompt_text = tk.Text(
            parent,
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary'],
            font=("Arial", 9),
            wrap=tk.WORD,
            height=4,
            relief=tk.FLAT,
            padx=5,
            pady=5
        )
        self.system_prompt_text.pack(fill=tk.BOTH, expand=True)
        self.system_prompt_text.insert("1.0", self.system_prompt)
    
    def create_connection_status(self, parent):
        """Create connection status indicator"""
        status_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        status_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=15)
        
        tk.Label(
            status_frame,
            text="Connection:",
            font=("Arial", 9),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary']
        ).pack(anchor=tk.W)
        
        self.connection_indicator = tk.Label(
            status_frame,
            text="● Checking...",
            font=("Arial", 10, "bold"),
            bg=self.colors['bg_secondary'],
            fg=self.colors['warning']
        )
        self.connection_indicator.pack(anchor=tk.W, pady=(5, 0))
    
    def create_status_bar(self):
        """Create bottom status bar"""
        self.status_bar = tk.Label(
            self.root,
            text="Ready | v2.0 with File & Image Support",
            font=("Arial", 9),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary'],
            anchor=tk.W,
            padx=10
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, pady=(5, 10), padx=10)
    
    def create_styled_button(self, parent, text, command, width=10, height=1):
        """Create a styled button"""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=self.colors['accent'],
            fg=self.colors['text_primary'],
            font=("Arial", 10, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            width=width,
            height=height,
            activebackground=self.colors['accent_hover'],
            activeforeground=self.colors['text_primary']
        )
        
        btn.bind("<Enter>", lambda e: btn.configure(bg=self.colors['accent_hover']))
        btn.bind("<Leave>", lambda e: btn.configure(bg=self.colors['accent']))
        
        return btn
    
    def update_temp_label(self, value):
        """Update temperature label"""
        self.temp_label.config(text=f"{float(value):.1f}")
    
    def attach_file(self):
        """Attach a file to the message"""
        file_path = filedialog.askopenfilename(
            title="Select a file",
            filetypes=[
                ("All Files", "*.*"),
                ("Text Files", "*.txt"),
                ("Python Files", "*.py"),
                ("PDF Files", "*.pdf"),
                ("Markdown Files", "*.md"),
                ("JSON Files", "*.json"),
            ]
        )
        
        if file_path:
            try:
                file_name = os.path.basename(file_path)
                file_size = os.path.getsize(file_path)
                
                # Read file content
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                self.attached_files.append({
                    'name': file_name,
                    'path': file_path,
                    'size': file_size,
                    'content': content
                })
                
                self.update_attachment_preview()
                self.update_status(f"Attached file: {file_name}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read file: {str(e)}")
    
    def attach_image(self):
        """Attach an image to the message"""
        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("PNG Files", "*.png"),
                ("JPEG Files", "*.jpg *.jpeg"),
                ("All Files", "*.*"),
            ]
        )
        
        if file_path:
            try:
                file_name = os.path.basename(file_path)
                
                # Read and encode image
                with open(file_path, 'rb') as f:
                    image_data = base64.b64encode(f.read()).decode('utf-8')
                
                self.attached_images.append({
                    'name': file_name,
                    'path': file_path,
                    'data': image_data
                })
                
                self.current_image_data = image_data
                
                self.update_attachment_preview()
                self.update_status(f"Attached image: {file_name}")
                
                # Suggest using llava if not already
                if self.current_model.get() != "llava":
                    response = messagebox.askyesno(
                        "Switch to Vision Model?",
                        "For image analysis, 'llava' model is recommended. Switch now?"
                    )
                    if response:
                        self.current_model.set("llava")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read image: {str(e)}")
    
    def update_attachment_preview(self):
        """Update the attachment preview display"""
        # Clear existing previews
        for widget in self.attachment_list.winfo_children():
            widget.destroy()
        
        # Show preview frame if there are attachments
        if self.attached_files or self.attached_images:
            self.preview_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, before=self.message_input.master)
            
            # Show files
            for file_info in self.attached_files:
                file_tag = tk.Label(
                    self.attachment_list,
                    text=f"📄 {file_info['name']} ({file_info['size']} bytes)",
                    bg=self.colors['file_bg'],
                    fg=self.colors['text_primary'],
                    font=("Arial", 9),
                    padx=5,
                    pady=2
                )
                file_tag.pack(side=tk.LEFT, padx=2)
            
            # Show images
            for img_info in self.attached_images:
                img_tag = tk.Label(
                    self.attachment_list,
                    text=f"🖼️ {img_info['name']}",
                    bg=self.colors['file_bg'],
                    fg=self.colors['warning'],
                    font=("Arial", 9),
                    padx=5,
                    pady=2
                )
                img_tag.pack(side=tk.LEFT, padx=2)
        else:
            self.preview_frame.pack_forget()
    
    def clear_attachments(self):
        """Clear all attachments"""
        self.attached_files = []
        self.attached_images = []
        self.current_image_data = None
        self.update_attachment_preview()
        self.update_status("Attachments cleared")
    
    def check_ollama_connection(self):
        """Check if Ollama is running"""
        def check():
            try:
                response = requests.get("http://localhost:11434/api/tags", timeout=2)
                if response.status_code == 200:
                    self.connection_indicator.config(
                        text="● Connected",
                        fg=self.colors['success']
                    )
                    self.update_status("Connected to Ollama | v2.0")
                else:
                    self.connection_indicator.config(
                        text="● Error",
                        fg=self.colors['accent']
                    )
                    self.update_status("Ollama connection error")
            except Exception:
                self.connection_indicator.config(
                    text="● Disconnected",
                    fg=self.colors['accent']
                )
                self.update_status("Ollama not running")
        
        threading.Thread(target=check, daemon=True).start()
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_bar.config(text=f"{message} | v2.0 with File & Image Support")
    
    def on_enter_key(self, event):
        """Handle Enter key press"""
        if not event.state & 0x1:
            self.send_message()
            return "break"
    
    def send_message(self):
        """Send a message to the chatbot"""
        message = self.message_input.get("1.0", tk.END).strip()
        
        if not message and not self.attached_files and not self.attached_images:
            messagebox.showwarning("Empty Message", "Please enter a message or attach a file/image.")
            return
        
        if self.is_generating:
            messagebox.showwarning("Please Wait", "Please wait for the current response to complete.")
            return
        
        # Build message with file context
        full_message = message
        
        if self.attached_files:
            full_message += "\n\n--- Attached Files ---\n"
            for file_info in self.attached_files:
                full_message += f"\nFile: {file_info['name']}\n"
                full_message += f"Content:\n{file_info['content'][:5000]}\n"  # Limit to 5000 chars per file
                if len(file_info['content']) > 5000:
                    full_message += "... (truncated)\n"
        
        # Clear input
        self.message_input.delete("1.0", tk.END)
        
        # Update system prompt
        self.system_prompt = self.system_prompt_text.get("1.0", tk.END).strip()
        
        # Display user message
        display_msg = message
        if self.attached_files:
            display_msg += f"\n📎 {len(self.attached_files)} file(s) attached"
        if self.attached_images:
            display_msg += f"\n🖼️ {len(self.attached_images)} image(s) attached"
        
        self.display_message(display_msg, "user")
        
        # Add to history
        msg_obj = {"role": "user", "content": full_message}
        
        # Add images for vision models
        if self.attached_images and self.current_image_data:
            msg_obj["images"] = [self.current_image_data]
        
        self.chat_history.append(msg_obj)
        
        # Clear attachments after sending
        self.clear_attachments()
        
        # Get bot response
        self.is_generating = True
        self.send_button.config(state=tk.DISABLED, text="...")
        self.update_status("Generating response...")
        
        threading.Thread(target=self.get_bot_response, daemon=True).start()
    
    def get_bot_response(self):
        """Get response from Ollama"""
        try:
            payload = {
                "model": self.current_model.get(),
                "messages": [
                    {"role": "system", "content": self.system_prompt}
                ] + self.chat_history,
                "stream": False,
                "options": {
                    "temperature": self.temperature.get()
                }
            }
            
            response = requests.post(
                self.ollama_url,
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                bot_message = result.get("message", {}).get("content", "No response")
                
                self.chat_history.append({"role": "assistant", "content": bot_message})
                
                self.root.after(0, lambda: self.display_message(bot_message, "bot"))
                self.root.after(0, lambda: self.update_status("Ready"))
            else:
                error_msg = f"Error: {response.status_code} - {response.text}"
                self.root.after(0, lambda: self.display_message(error_msg, "system"))
                self.root.after(0, lambda: self.update_status("Error occurred"))
        
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.root.after(0, lambda: self.display_message(error_msg, "system"))
            self.root.after(0, lambda: self.update_status("Error occurred"))
        
        finally:
            self.is_generating = False
            self.root.after(0, lambda: self.send_button.config(state=tk.NORMAL, text="Send\n→"))
    
    def display_message(self, message, sender):
        """Display a message in the chat"""
        self.chat_display.config(state=tk.NORMAL)
        
        timestamp = datetime.now().strftime("%H:%M")
        
        if sender == "user":
            prefix = "You"
            tag = "user"
        elif sender == "bot":
            prefix = "AI"
            tag = "bot"
        else:
            prefix = "System"
            tag = "system"
        
        self.chat_display.insert(tk.END, "\n")
        header = f"[{timestamp}] {prefix}:\n"
        self.chat_display.insert(tk.END, header, "timestamp")
        self.chat_display.insert(tk.END, f"{message}\n", tag)
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def clear_chat(self):
        """Clear the chat history"""
        if messagebox.askyesno("Clear Chat", "Are you sure you want to clear the chat?"):
            self.chat_history = []
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete("1.0", tk.END)
            self.chat_display.config(state=tk.DISABLED)
            self.display_message("Chat cleared", "system")
            self.update_status("Chat cleared")
    
    def export_chat(self):
        """Export chat history to a file"""
        if not self.chat_history:
            messagebox.showinfo("Export Chat", "No chat history to export.")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chat_export_v2_{timestamp}.txt"
        
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"Ollama Chat Export v2.0 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Model: {self.current_model.get()}\n")
                f.write(f"Temperature: {self.temperature.get()}\n")
                f.write("=" * 80 + "\n\n")
                
                for msg in self.chat_history:
                    role = msg["role"].upper()
                    content = msg["content"]
                    f.write(f"{role}:\n{content}\n\n")
            
            messagebox.showinfo("Export Complete", f"Chat exported to {filename}")
            self.update_status(f"Chat exported to {filename}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export chat: {str(e)}")


def main():
    root = tk.Tk()
    app = OllamaChatbotV2(root)
    root.mainloop()


if __name__ == "__main__":
    main()

