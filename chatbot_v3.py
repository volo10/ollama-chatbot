import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import requests, threading, os, pickle, base64
from datetime import datetime
import platform

# ======================================
# Platform-specific font configuration
# ======================================
def get_system_font():
    """Get the best font for the current platform"""
    system = platform.system()
    if system == "Darwin":  # macOS
        return "SF Pro Text"  # macOS system font
    elif system == "Windows":
        return "Segoe UI"  # Windows system font
    else:  # Linux
        return "Ubuntu"  # Linux common font
    
# Default fallback font
SYSTEM_FONT = get_system_font()

# ======================================
# Chat session model
# ======================================
class ChatSession:
    def __init__(self, name="New Chat", chat_id=None):
        self.id = chat_id or datetime.now().strftime("%Y%m%d_%H%M%S")
        self.name = name
        self.messages = []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()


# ======================================
# Avatar Selection Dialog
# ======================================
class AvatarSelectionDialog(tk.Toplevel):
    def __init__(self, parent, current_avatar):
        super().__init__(parent)
        self.title("Select Your Avatar")
        self.geometry("600x300")
        self.resizable(False, False)
        self.configure(bg="#2d3748")
        
        self.selected_avatar = current_avatar
        
        # Available avatars (emojis that look like round characters)
        self.avatars = [
            "👤",  # Default user
            "🐻",  # Bear (like the image)
            "🦁",  # Lion
            "🐯",  # Tiger
            "🐼",  # Panda
            "🐨",  # Koala
            "🐸",  # Frog
            "🐵",  # Monkey
            "🦊",  # Fox
            "🐶",  # Dog
            "🐱",  # Cat
            "🐰",  # Rabbit
        ]
        
        tk.Label(
            self,
            text="Select an avatar for your profile image.",
            bg="#2d3748",
            fg="white",
            font=("Segoe UI", 12),
            pady=20
        ).pack()
        
        # Avatar grid
        avatar_frame = tk.Frame(self, bg="#2d3748")
        avatar_frame.pack(pady=10)
        
        self.avatar_buttons = []
        for i, avatar in enumerate(self.avatars):
            btn = tk.Button(
                avatar_frame,
                text=avatar,
                font=("Segoe UI Emoji", 32),
                width=2,
                height=1,
                relief=tk.FLAT,
                bg="#4a5568" if avatar != current_avatar else "#2563eb",
                fg="white",
                cursor="hand2",
                command=lambda a=avatar: self.select_avatar(a)
            )
            btn.grid(row=i // 6, column=i % 6, padx=8, pady=8)
            self.avatar_buttons.append((btn, avatar))
        
        # Buttons
        btn_frame = tk.Frame(self, bg="#2d3748")
        btn_frame.pack(pady=20)
        
        confirm_btn = tk.Button(
            btn_frame,
            text="Confirm",
            command=self.confirm,
            font=("Segoe UI", 11, "bold"),
            bg="#e5e7eb",
            fg="#1f2937",
            activebackground="#d1d5db",
            activeforeground="#1f2937",
            relief=tk.FLAT,
            cursor="hand2",
            width=12,
            height=1,
            padx=10,
            pady=8
        )
        confirm_btn.pack(side=tk.LEFT, padx=5)
        confirm_btn.bind("<Enter>", lambda e: confirm_btn.config(bg="#d1d5db"))
        confirm_btn.bind("<Leave>", lambda e: confirm_btn.config(bg="#e5e7eb"))
        
        cancel_btn = tk.Button(
            btn_frame,
            text="Cancel",
            command=self.cancel,
            font=("Segoe UI", 11),
            bg="#e5e7eb",
            fg="#1f2937",
            activebackground="#d1d5db",
            activeforeground="#1f2937",
            relief=tk.FLAT,
            cursor="hand2",
            width=12,
            height=1,
            padx=10,
            pady=8
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)
        cancel_btn.bind("<Enter>", lambda e: cancel_btn.config(bg="#d1d5db"))
        cancel_btn.bind("<Leave>", lambda e: cancel_btn.config(bg="#e5e7eb"))
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
    def select_avatar(self, avatar):
        self.selected_avatar = avatar
        # Update button colors
        for btn, av in self.avatar_buttons:
            if av == avatar:
                btn.config(bg="#2563eb")
            else:
                btn.config(bg="#4a5568")
    
    def confirm(self):
        self.destroy()
    
    def cancel(self):
        self.selected_avatar = None
        self.destroy()


# ======================================
# Main App
# ======================================
class OllamaChatbotBlue(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ollama AI Assistant v3.6 – Thinking Indicator")
        self.geometry("1400x900")
        self.minsize(1200, 800)

        # Session state
        self.chat_sessions = []
        self.current_session = None
        self.sessions_file = "chat_sessions.pkl"
        self.attached_files, self.attached_images = [], []
        self.is_generating = False
        self.system_prompt = "You are a helpful AI assistant."
        self.ollama_url = "http://localhost:11434/api/chat"
        
        # Avatar settings
        self.user_avatar = "👤"
        self.bot_avatar = "🤖"
        self.settings_file = "app_settings.pkl"
        self.load_settings()
        
        # Sidebar state
        self.sidebar_visible = True
        
        # Thinking indicator
        self.thinking_animation_id = None
        self.thinking_frame_index = 0

        # Set favicon
        self.set_favicon()

        # ============================
        # Blue Theme Colors
        # ============================
        self.colors = {
            "bg": "#f5f7fb",
            "chat_bg": "#ffffff",
            "sidebar": "#182033",
            "accent": "#2563eb",
            "accent_hover": "#1e4fc2",
            "text": "#1f2937",
            "text_alt": "#6b7280",
            "bubble_user": "#ffffff",
            "bubble_bot": "#f3f4f6",
            "thinking": "#f97316",  # Orange color for thinking
        }

        # Model config
        self.current_model = tk.StringVar(value="llama2")
        self.temperature = tk.DoubleVar(value=0.7)

        # Build UI
        self.create_top_ticker()
        self.create_main_layout()
        self.create_status_bar()

        # Load history + check connection
        self.load_sessions()
        self.check_ollama_connection()

    # ======================================
    # Favicon Setup
    # ======================================
    def set_favicon(self):
        """Set window icon/favicon"""
        try:
            # Try to set icon if iconphoto is available
            # Create a simple colored square as icon (since we can't use external files)
            # Tkinter will use default icon if this fails
            pass
        except Exception:
            pass

    # ======================================
    # Settings Management
    # ======================================
    def load_settings(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, "rb") as f:
                    settings = pickle.load(f)
                    self.user_avatar = settings.get("user_avatar", "👤")
                    self.bot_avatar = settings.get("bot_avatar", "🤖")
            except Exception:
                pass
    
    def save_settings(self):
        try:
            with open(self.settings_file, "wb") as f:
                settings = {
                    "user_avatar": self.user_avatar,
                    "bot_avatar": self.bot_avatar
                }
                pickle.dump(settings, f)
        except Exception as e:
            print(f"Error saving settings: {e}")

    # ======================================
    # Layout setup
    # ======================================
    def create_top_ticker(self):
        ticker_container = tk.Frame(self, bg=self.colors["accent"], height=30)
        ticker_container.pack(fill=tk.X)
        
        # Toggle button for sidebar
        self.toggle_btn = tk.Button(
            ticker_container,
            text="☰",
            command=self.toggle_sidebar,
            font=("Segoe UI", 14, "bold"),
            bg=self.colors["accent"],
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            width=3,
            height=1
        )
        self.toggle_btn.pack(side=tk.LEFT, padx=10)
        
        self.ticker_label = tk.Label(
            ticker_container,
            text="💡 Ocean waves can travel thousands of miles without losing energy.",
            bg=self.colors["accent"],
            fg="white",
            font=("Segoe UI", 10, "italic"),
        )
        self.ticker_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        self.after(5000, self.update_ticker)

    def update_ticker(self):
        facts = [
            "🧠 Your brain uses 20% of your body's energy while being only 2% of its weight.",
            "🐋 Blue whales are the largest animals ever known to exist.",
            "🌌 There are more stars than grains of sand on Earth.",
            "🎵 Music can make plants grow faster!",
            "🌊 Ocean waves can travel thousands of miles without losing energy.",
        ]
        fact = facts[int(datetime.now().second) % len(facts)]
        self.ticker_label.config(text=f"💡 {fact}")
        self.after(6000, self.update_ticker)

    def create_main_layout(self):
        # Main container for sidebar and chat area
        self.main_container = tk.Frame(self, bg=self.colors["bg"])
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # Sidebar
        self.sidebar_frame = tk.Frame(self.main_container, bg=self.colors["sidebar"], width=280)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar_frame.pack_propagate(False)  # Maintain fixed width

        self.create_sidebar(self.sidebar_frame)

        # Chat area
        self.chat_area = tk.Frame(self.main_container, bg=self.colors["bg"])
        self.chat_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.create_chat_display(self.chat_area)
        self.create_input_area(self.chat_area)

    def toggle_sidebar(self):
        """Toggle sidebar visibility with slide animation"""
        if self.sidebar_visible:
            self.sidebar_frame.pack_forget()
            self.toggle_btn.config(text="☰")
            self.sidebar_visible = False
        else:
            self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, before=self.chat_area)
            self.toggle_btn.config(text="✕")
            self.sidebar_visible = True

    def create_sidebar(self, parent):
        # Scrollable container for sidebar content
        canvas = tk.Canvas(parent, bg=self.colors["sidebar"], highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors["sidebar"])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Header with app name
        tk.Label(
            scrollable_frame,
            text="Ollama AI Assistant",
            bg=self.colors["sidebar"],
            fg="white",
            font=("Segoe UI", 13, "bold"),
            pady=20,
        ).pack()

        # New Chat button with badge
        new_chat_container = tk.Frame(scrollable_frame, bg=self.colors["sidebar"])
        new_chat_container.pack(fill=tk.X, padx=20, pady=10)
        
        new_btn = tk.Button(
            new_chat_container,
            text="🆕  NEW    New Chat",
            command=self.new_chat,
            font=("Segoe UI", 11, "bold"),
            fg="#1f2937",
            bg="#f3f4f6",
            activebackground="#e5e7eb",
            activeforeground="#1f2937",
            relief=tk.FLAT,
            cursor="hand2",
            anchor="w",
            padx=15,
            pady=12,
        )
        new_btn.pack(fill=tk.X)
        
        # Hover effect
        new_btn.bind("<Enter>", lambda e: new_btn.config(bg="#e5e7eb"))
        new_btn.bind("<Leave>", lambda e: new_btn.config(bg="#f3f4f6"))

        # Avatar customization section
        avatar_section = tk.Frame(scrollable_frame, bg=self.colors["sidebar"])
        avatar_section.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            avatar_section,
            text="Customize",
            bg=self.colors["sidebar"],
            fg="white",
            font=("Segoe UI", 10, "bold"),
            anchor="w"
        ).pack(fill=tk.X, pady=(0, 8))
        
        # User avatar button (icon only)
        self.user_avatar_btn = tk.Button(
            avatar_section,
            text=f"{self.user_avatar}  User",
            command=self.change_user_avatar,
            font=("Segoe UI", 11),
            fg="#1f2937",
            bg="#f3f4f6",
            activebackground="#e5e7eb",
            activeforeground="#1f2937",
            relief=tk.FLAT,
            cursor="hand2",
            anchor="w",
            padx=15,
            pady=10
        )
        self.user_avatar_btn.pack(fill=tk.X, pady=3)
        
        # Hover effect
        self.user_avatar_btn.bind("<Enter>", lambda e: self.user_avatar_btn.config(bg="#e5e7eb"))
        self.user_avatar_btn.bind("<Leave>", lambda e: self.user_avatar_btn.config(bg="#f3f4f6"))
        
        # Bot avatar button (icon only)
        self.bot_avatar_btn = tk.Button(
            avatar_section,
            text=f"{self.bot_avatar}  Bot",
            command=self.change_bot_avatar,
            font=("Segoe UI", 11),
            fg="#1f2937",
            bg="#f3f4f6",
            activebackground="#e5e7eb",
            activeforeground="#1f2937",
            relief=tk.FLAT,
            cursor="hand2",
            anchor="w",
            padx=15,
            pady=10
        )
        self.bot_avatar_btn.pack(fill=tk.X, pady=3)
        
        # Hover effect
        self.bot_avatar_btn.bind("<Enter>", lambda e: self.bot_avatar_btn.config(bg="#e5e7eb"))
        self.bot_avatar_btn.bind("<Leave>", lambda e: self.bot_avatar_btn.config(bg="#f3f4f6"))

        # Chat list
        tk.Label(
            scrollable_frame,
            text="Recent Chats",
            bg=self.colors["sidebar"],
            fg="white",
            font=("Segoe UI", 10, "bold"),
            anchor="w",
            padx=20
        ).pack(fill=tk.X, pady=(10, 5))
        
        self.chat_list = tk.Frame(scrollable_frame, bg=self.colors["sidebar"])
        self.chat_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.refresh_chat_list()

    def create_chat_display(self, parent):
        self.chat_display = tk.Text(
            parent,
            bg=self.colors["chat_bg"],
            fg=self.colors["text"],
            font=("Segoe UI", 11),
            wrap=tk.WORD,
            relief=tk.FLAT,
            padx=20,
            pady=20,
            state=tk.DISABLED,
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 0))

    def create_input_area(self, parent):
        frame = tk.Frame(parent, bg="#eef2f7")
        frame.pack(fill=tk.X, padx=15, pady=15)

        # Larger icons
        attach_frame = tk.Frame(frame, bg="#eef2f7")
        attach_frame.pack(side=tk.LEFT, padx=10)
        icon_font = ("Segoe UI Emoji", 16)

        tk.Button(
            attach_frame,
            text="📁",
            command=self.attach_file,
            font=icon_font,
            relief=tk.FLAT,
            bg="#eef2f7",
            cursor="hand2",
            width=2,
        ).pack(side=tk.LEFT, padx=4)
        tk.Button(
            attach_frame,
            text="🖼️",
            command=self.attach_image,
            font=icon_font,
            relief=tk.FLAT,
            bg="#eef2f7",
            cursor="hand2",
            width=2,
        ).pack(side=tk.LEFT, padx=4)

        # Input box
        self.input_box = tk.Entry(
            frame,
            font=("Segoe UI", 11),
            bg="white",
            fg=self.colors["text"],
            relief=tk.FLAT,
        )
        self.input_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, ipady=10, padx=(10, 10))
        self.input_box.bind("<Return>", self.send_message)

        send_btn = tk.Button(
            frame,
            text="⬆️",
            command=self.send_message,
            font=icon_font,
            bg=self.colors["accent"],
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            width=3,
        )
        send_btn.pack(side=tk.RIGHT, padx=10)

    def create_status_bar(self):
        frame = tk.Frame(self, bg=self.colors["bg"], height=30)
        frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Status label on the left
        self.status_label = tk.Label(
            frame,
            text="Connecting to Ollama...",
            bg=self.colors["bg"],
            fg=self.colors["text_alt"],
            font=("Segoe UI", 9),
            anchor="w",
        )
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        # Model selector on the right
        model_frame = tk.Frame(frame, bg=self.colors["bg"])
        model_frame.pack(side=tk.RIGHT, padx=10)
        
        tk.Label(
            model_frame,
            text="Model:",
            bg=self.colors["bg"],
            fg=self.colors["text_alt"],
            font=("Segoe UI", 9)
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        models = ["llama2", "llava", "mistral", "codellama", "llama3", "phi", "gemma"]
        self.model_selector = ttk.Combobox(
            model_frame,
            textvariable=self.current_model,
            values=models,
            state="readonly",
            width=12,
            font=("Segoe UI", 9)
        )
        self.model_selector.pack(side=tk.LEFT)

    # ======================================
    # Thinking Indicator
    # ======================================
    def show_thinking_indicator(self):
        """Display animated thinking indicator like Claude"""
        self.chat_display.config(state=tk.NORMAL)
        
        # Add spacing
        self.chat_display.insert(tk.END, "\n")
        
        # Insert avatar and label
        self.chat_display.insert(tk.END, f"{self.bot_avatar}  Assistant\n", "header")
        
        # Insert thinking text with marker
        self.thinking_start = self.chat_display.index("end-1c")
        self.chat_display.insert(tk.END, "● Thinking...", "thinking")
        self.chat_display.insert(tk.END, "\n")
        
        # Configure thinking style
        self.chat_display.tag_configure(
            "thinking",
            font=("Segoe UI", 11, "italic"),
            foreground=self.colors["thinking"],
            lmargin1=55,
            lmargin2=55,
            spacing3=15,
        )
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
        # Start animation
        self.thinking_frame_index = 0
        self.animate_thinking()
    
    def animate_thinking(self):
        """Animate the thinking indicator"""
        if not self.is_generating:
            return
        
        # Animation frames (rotating dots pattern)
        frames = ["●", "○", "◉", "○"]
        icon = frames[self.thinking_frame_index % len(frames)]
        
        # Update the thinking text
        self.chat_display.config(state=tk.NORMAL)
        
        # Find and replace the thinking indicator
        try:
            thinking_line = self.chat_display.search("Thinking...", self.thinking_start, tk.END)
            if thinking_line:
                line_start = f"{thinking_line} linestart"
                line_end = f"{thinking_line} lineend"
                self.chat_display.delete(line_start, line_end)
                self.chat_display.insert(line_start, f"{icon} Thinking...", "thinking")
        except:
            pass
        
        self.chat_display.config(state=tk.DISABLED)
        
        # Schedule next frame
        self.thinking_frame_index += 1
        self.thinking_animation_id = self.after(300, self.animate_thinking)
    
    def hide_thinking_indicator(self):
        """Remove the thinking indicator"""
        if self.thinking_animation_id:
            self.after_cancel(self.thinking_animation_id)
            self.thinking_animation_id = None
        
        self.chat_display.config(state=tk.NORMAL)
        
        # Remove the thinking line
        try:
            thinking_line = self.chat_display.search("Thinking...", "1.0", tk.END)
            if thinking_line:
                # Delete the entire thinking message block (avatar + thinking text)
                line_start = self.chat_display.search(f"{self.bot_avatar}  Assistant", f"{thinking_line} linestart -3l", thinking_line)
                if line_start:
                    end_pos = f"{thinking_line} lineend +1c"
                    self.chat_display.delete(line_start, end_pos)
        except:
            pass
        
        self.chat_display.config(state=tk.DISABLED)

    # ======================================
    # Avatar Management
    # ======================================
    def change_user_avatar(self):
        dialog = AvatarSelectionDialog(self, self.user_avatar)
        self.wait_window(dialog)
        if dialog.selected_avatar:
            self.user_avatar = dialog.selected_avatar
            try:
                if self.user_avatar_btn.winfo_exists():
                    self.user_avatar_btn.config(text=f"{self.user_avatar}  User")
            except:
                pass
            self.save_settings()
            self.refresh_chat_display()
    
    def change_bot_avatar(self):
        dialog = AvatarSelectionDialog(self, self.bot_avatar)
        self.wait_window(dialog)
        if dialog.selected_avatar:
            self.bot_avatar = dialog.selected_avatar
            try:
                if self.bot_avatar_btn.winfo_exists():
                    self.bot_avatar_btn.config(text=f"{self.bot_avatar}  Bot")
            except:
                pass
            self.save_settings()
            self.refresh_chat_display()
    
    def refresh_chat_display(self):
        """Refresh the current chat display with new avatars"""
        if self.current_session:
            self.display_chat_history()

    # ======================================
    # Core chat logic
    # ======================================
    def refresh_chat_list(self):
        for w in self.chat_list.winfo_children():
            w.destroy()
        for s in reversed(self.chat_sessions):
            btn = tk.Button(
                self.chat_list,
                text=f"💬 {s.name[:25]}",
                bg="#f3f4f6",
                fg="#1f2937",
                activebackground="#e5e7eb",
                activeforeground="#1f2937",
                relief=tk.FLAT,
                anchor="w",
                font=("Segoe UI", 10),
                padx=10,
                pady=8,
                cursor="hand2",
                command=lambda sid=s.id: self.load_chat(sid),
            )
            btn.pack(fill=tk.X, pady=3, padx=5)
            
            # Hover effect
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#e5e7eb"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#f3f4f6"))

    def new_chat(self):
        s = ChatSession()
        self.chat_sessions.append(s)
        self.current_session = s
        self.refresh_chat_list()
        self.display_message("New chat started.", "assistant")

    def load_chat(self, sid):
        for s in self.chat_sessions:
            if s.id == sid:
                self.current_session = s
                self.display_chat_history()
                break

    def display_chat_history(self):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("1.0", tk.END)
        for msg in self.current_session.messages:
            self.display_message(msg["content"], msg["role"], add_to_history=False)
        self.chat_display.config(state=tk.DISABLED)

    def display_message(self, msg, role, add_to_history=True):
        """Display Claude-style left-aligned messages with custom round avatars"""
        self.chat_display.config(state=tk.NORMAL)

        # Role-based visuals with custom avatars
        if role == "user":
            avatar = self.user_avatar
            label = "You"
            bg_color = self.colors["chat_bg"]
            text_color = self.colors["text"]
        elif role == "assistant":
            avatar = self.bot_avatar
            label = "Assistant"
            bg_color = self.colors["bubble_bot"]
            text_color = self.colors["text"]
        else:
            avatar = "ℹ️"
            label = "System"
            bg_color = "#f0f0f0"
            text_color = self.colors["text_alt"]

        # Add spacing between messages
        self.chat_display.insert(tk.END, "\n")
        
        # Insert avatar and label on one line
        self.chat_display.insert(tk.END, f"{avatar}  {label}\n", "header")
        
        # Insert message content with proper indentation (left-aligned)
        self.chat_display.insert(tk.END, f"{msg}\n", f"content_{role}")
        
        # Configure header style (avatar + label)
        self.chat_display.tag_configure(
            "header",
            font=("Segoe UI", 10, "bold"),
            foreground=self.colors["text_alt"],
            lmargin1=20,
            lmargin2=20,
            spacing1=10,
            spacing3=5,
        )
        
        # Configure content style (message text) - all left-aligned
        self.chat_display.tag_configure(
            f"content_{role}",
            font=("Segoe UI", 11),
            foreground=text_color,
            background=bg_color,
            lmargin1=55,  # Indent to align with text after avatar
            lmargin2=55,
            rmargin=20,
            spacing3=15,
            wrap="word",
        )

        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def attach_file(self):
        # Cross-platform file dialog (works on macOS, Windows, Linux)
        f = filedialog.askopenfilename(
            title="Select a File",
            filetypes=[
                ("Text Files", "*.txt *.md *.py *.js *.html *.css *.json *.xml"),
                ("Code Files", "*.py *.js *.java *.cpp *.c *.h *.cs *.rb *.go"),
                ("Documents", "*.pdf *.doc *.docx"),
                ("All Files", "*.*")
            ]
        )
        if f:
            with open(f, "r", errors="ignore") as fp:
                content = fp.read()[:5000]
            self.attached_files.append({"name": os.path.basename(f), "content": content})
            messagebox.showinfo("Attached", f"Attached file: {os.path.basename(f)}\n\n📄 Size: {len(content)} characters")

    def attach_image(self):
        # Cross-platform file dialog (works on macOS, Windows, Linux)
        # Note: Use space-separated extensions, not semicolons
        f = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("PNG Files", "*.png"),
                ("JPEG Files", "*.jpg *.jpeg"),
                ("All Files", "*.*")
            ]
        )
        if f:
            with open(f, "rb") as fp:
                data = base64.b64encode(fp.read()).decode("utf-8")
            self.attached_images.append({"name": os.path.basename(f), "data": data})
            
            # Suggest llava model for image analysis
            if self.current_model.get() != "llava":
                response = messagebox.askyesno(
                    "Switch to Vision Model?",
                    "For image analysis, 'llava' model is recommended.\n\nSwitch to llava now?"
                )
                if response:
                    self.current_model.set("llava")
            
            messagebox.showinfo("Attached", f"Attached image: {os.path.basename(f)}\n\n📷 Total: {len(self.attached_images)} image(s)")

    def send_message(self, event=None):
        msg = self.input_box.get().strip()
        if not msg and not self.attached_images:
            return
        self.input_box.delete(0, tk.END)
        
        # Build display message
        display_msg = msg if msg else "Analyzing image..."
        if self.attached_images:
            display_msg += f"\n📷 {len(self.attached_images)} image(s) attached"
        
        self.display_message(display_msg, "user")
        
        if not self.current_session:
            self.new_chat()
        
        # Create message with content and images
        user_msg = {"role": "user", "content": msg}
        if self.attached_images:
            user_msg["images"] = [img["data"] for img in self.attached_images]
        
        self.current_session.messages.append(user_msg)
        
        # Clear attachments after adding to message
        self.attached_images = []
        
        # Show thinking indicator
        self.is_generating = True
        self.show_thinking_indicator()
        
        threading.Thread(target=self.get_bot_response, daemon=True).start()

    def get_bot_response(self):
        try:
            payload = {
                "model": self.current_model.get(),
                "messages": [{"role": "system", "content": self.system_prompt}] + self.current_session.messages,
                "stream": False,
                "options": {"temperature": self.temperature.get()},
            }
            
            # Debug: Print payload info
            print(f"\n🔍 DEBUG: Sending request to {self.ollama_url}")
            print(f"📦 Model: {payload['model']}")
            print(f"📝 Messages count: {len(payload['messages'])}")
            for i, msg in enumerate(payload['messages']):
                has_images = "images" in msg
                img_count = len(msg.get("images", []))
                print(f"  Message {i}: role={msg['role']}, has_images={has_images}, image_count={img_count}")
            
            r = requests.post(self.ollama_url, json=payload, timeout=120)
            
            print(f"✅ Response status: {r.status_code}")
            
            # Hide thinking indicator
            self.is_generating = False
            self.after(0, self.hide_thinking_indicator)
            
            if r.status_code == 200:
                resp = r.json().get("message", {}).get("content", "No response.")
                self.current_session.messages.append({"role": "assistant", "content": resp})
                self.after(0, lambda: self.display_message(resp, "assistant"))
            else:
                error_msg = f"Error {r.status_code}: {r.text}"
                print(f"❌ {error_msg}")
                self.after(0, lambda: self.display_message(error_msg, "system"))
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
            import traceback
            traceback.print_exc()
            self.is_generating = False
            self.after(0, self.hide_thinking_indicator)
            self.after(0, lambda: self.display_message(f"Error: {str(e)}", "system"))

    def check_ollama_connection(self):
        def check():
            try:
                r = requests.get("http://localhost:11434/api/tags", timeout=2)
                if r.status_code == 200:
                    self.status_label.config(text=f"✅ Connected to Ollama | Model: {self.current_model.get()}")
                else:
                    self.status_label.config(text="⚠️ Error connecting to Ollama.")
            except Exception:
                self.status_label.config(text="❌ Disconnected.")
        threading.Thread(target=check, daemon=True).start()

    def load_sessions(self):
        if os.path.exists(self.sessions_file):
            try:
                with open(self.sessions_file, "rb") as f:
                    self.chat_sessions = pickle.load(f)
                    if self.chat_sessions:
                        self.current_session = self.chat_sessions[-1]
            except Exception:
                self.chat_sessions = []
        if not self.chat_sessions:
            self.new_chat()


if __name__ == "__main__":
    OllamaChatbotBlue().mainloop()