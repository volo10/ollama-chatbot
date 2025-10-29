"""
Ollama Chatbot with Modern GUI
A professional chatbot application using Ollama with a sleek, customizable interface.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests
import json
import threading
from datetime import datetime
import os


class OllamaChatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("Ollama AI Assistant")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Color scheme - Professional dark theme with accent colors
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
        }
        
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Configuration
        self.ollama_url = "http://localhost:11434/api/chat"
        self.current_model = tk.StringVar(value="llama2")
        self.temperature = tk.DoubleVar(value=0.7)
        self.system_prompt = "You are a helpful AI assistant."
        self.chat_history = []
        self.is_generating = False
        
        # Setup GUI
        self.setup_gui()
        
        # Check Ollama connection on startup
        self.root.after(100, self.check_ollama_connection)
    
    def setup_gui(self):
        """Setup the main GUI layout"""
        
        # Top Bar
        self.create_top_bar()
        
        # Main Container
        main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Chat Display Area
        self.create_chat_display(main_container)
        
        # Input Area
        self.create_input_area(main_container)
        
        # Side Panel (Settings)
        self.create_side_panel(main_container)
        
        # Status Bar
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
            text="Ollama AI Assistant",
            font=("Arial", 18, "bold"),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary']
        )
        title_label.pack(side=tk.LEFT)
        
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
        
        # Chat canvas with scrollbar
        canvas_frame = tk.Frame(chat_frame, bg=self.colors['bg_secondary'], relief=tk.RIDGE, bd=2)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(canvas_frame, bg=self.colors['bg_tertiary'])
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Chat display
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
        
        # Configure text tags for styling
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
    
    def create_input_area(self, parent):
        """Create the message input area"""
        input_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        input_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=(5, 0))
        
        input_container = tk.Frame(input_frame, bg=self.colors['bg_secondary'], relief=tk.RIDGE, bd=2)
        input_container.pack(fill=tk.BOTH, expand=True)
        
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
        side_panel = tk.Frame(parent, bg=self.colors['bg_secondary'], width=250, relief=tk.RIDGE, bd=2)
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
        
        # Separator
        sep = tk.Frame(side_panel, height=2, bg=self.colors['accent'])
        sep.pack(fill=tk.X, padx=20, pady=5)
        
        # Model Selection
        self.create_setting_section(
            side_panel,
            "Model:",
            self.create_model_selector
        )
        
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
        models = ["llama2", "mistral", "codellama", "llama3", "phi", "gemma"]
        
        model_menu = ttk.Combobox(
            parent,
            textvariable=self.current_model,
            values=models,
            state="readonly",
            font=("Arial", 10)
        )
        model_menu.pack(fill=tk.X)
        
        # Style the combobox
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
            text="Ready",
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
        
        # Hover effects
        btn.bind("<Enter>", lambda e: btn.configure(bg=self.colors['accent_hover']))
        btn.bind("<Leave>", lambda e: btn.configure(bg=self.colors['accent']))
        
        return btn
    
    def update_temp_label(self, value):
        """Update temperature label"""
        self.temp_label.config(text=f"{float(value):.1f}")
    
    def check_ollama_connection(self):
        """Check if Ollama is running and accessible"""
        def check():
            try:
                response = requests.get("http://localhost:11434/api/tags", timeout=2)
                if response.status_code == 200:
                    self.connection_indicator.config(
                        text="● Connected",
                        fg=self.colors['success']
                    )
                    self.update_status("Connected to Ollama")
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
                self.update_status("Ollama not running - Please start Ollama")
        
        threading.Thread(target=check, daemon=True).start()
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_bar.config(text=message)
    
    def on_enter_key(self, event):
        """Handle Enter key press"""
        if not event.state & 0x1:  # If Shift is not pressed
            self.send_message()
            return "break"
    
    def send_message(self):
        """Send a message to the chatbot"""
        message = self.message_input.get("1.0", tk.END).strip()
        
        if not message:
            return
        
        if self.is_generating:
            messagebox.showwarning("Please Wait", "Please wait for the current response to complete.")
            return
        
        # Clear input
        self.message_input.delete("1.0", tk.END)
        
        # Update system prompt
        self.system_prompt = self.system_prompt_text.get("1.0", tk.END).strip()
        
        # Display user message
        self.display_message(message, "user")
        
        # Add to history
        self.chat_history.append({"role": "user", "content": message})
        
        # Get bot response in thread
        self.is_generating = True
        self.send_button.config(state=tk.DISABLED, text="...")
        self.update_status("Generating response...")
        
        threading.Thread(
            target=self.get_bot_response,
            daemon=True
        ).start()
    
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
                
                # Add to history
                self.chat_history.append({"role": "assistant", "content": bot_message})
                
                # Display bot message
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
        
        # Add spacing
        self.chat_display.insert(tk.END, "\n")
        
        # Add timestamp and sender
        header = f"[{timestamp}] {prefix}:\n"
        self.chat_display.insert(tk.END, header, "timestamp")
        
        # Add message
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
        filename = f"chat_export_{timestamp}.txt"
        
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"Ollama Chat Export - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
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
    app = OllamaChatbot(root)
    root.mainloop()


if __name__ == "__main__":
    main()

