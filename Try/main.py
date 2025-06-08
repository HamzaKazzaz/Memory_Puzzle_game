import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
import random
import time
import pygame
import os

# Import enhanced map match game
from enhanced_map_match_game import MapMatchGame, WORLD_REGIONS, get_region

# Import two-player games
from player_vs_player import TwoPlayerGame, ColorWordGame, MathGame, TrueFalseGame

# Pygame başlatma (müzik ve ses efektleri için)
pygame.mixer.init()

# Ses dosyalarını yükleme
try:
    # Ensure the 'Try' directory exists or handle the error
    if not os.path.exists("Try"):
        os.makedirs("Try")
        print("Created 'Try' directory for assets.")
    if not os.path.exists("Try/Solo_images"):
        os.makedirs("Try/Solo_images")
        print("Created 'Try/Solo_images' directory.")
    if not os.path.exists("Try/maps"):
        os.makedirs("Try/maps")
        print("Created 'Try/maps' directory.")
    if not os.path.exists("Try/flags"):
        os.makedirs("Try/flags")
        print("Created 'Try/flags' directory.")
        
    # Dummy sound files if originals are missing
    click_sound_path = "Try/click-buton.wav"
    music_path = "Try/Main-game-music.mp3"
    if not os.path.exists(click_sound_path):
        # Create a dummy wav file if it doesn't exist
        with open(click_sound_path, 'wb') as f:
            # Minimal WAV header and some silence
            f.write(b'RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x80>\x00\x00\x00\xfa\x00\x00\x01\x00\x08\x00data\x00\x00\x00\x00')
        print(f"Created dummy sound file: {click_sound_path}")
        
    button_click_sound = pygame.mixer.Sound(click_sound_path)  # Tuş sesi
    
    if not os.path.exists(music_path):
         # Cannot create dummy mp3 easily, will skip loading if missing
         print(f"Warning: Background music file not found: {music_path}")
         background_music = None
    else:
        background_music = music_path

    # Arka plan müziğini başlatma (if available)
    if background_music:
        pygame.mixer.music.load(background_music)
        pygame.mixer.music.play(-1)  # Sonsuz döngüde çal
    else:
        print("Skipping background music playback.")
        
except Exception as e:
    print(f"Ses dosyaları yüklenirken/oluşturulurken hata: {e}")
    # Fallback to dummy sound object if loading fails
    button_click_sound = pygame.mixer.Sound(buffer=bytearray(100))
    # Cannot load music from buffer easily, skip music if error
    background_music = None 

# Tema değişkeni - tek bir yerde tanımlanıyor
current_theme = {"bg": "#FFEBEE"}

def play_button_sound():
    """Buton tıklama sesini çalar"""
    try:
        pygame.mixer.Sound.play(button_click_sound)
    except Exception as e:
        print(f"Error playing sound: {e}")

def exit_game():
    """Oyundan çıkış fonksiyonu"""
    if messagebox.askyesno("Çıkış", "Oyundan çıkmak istediğinize emin misiniz?"):
        root.destroy()

def on_enter(event):
    """Fare butonun üzerine geldiğinde yazı tipini değiştirir"""
    event.widget.config(font=("Comic Sans MS", 16, "bold"))

def on_leave(event):
    """Fare butondan ayrıldığında yazı tipini normale döndürür"""
    event.widget.config(font=("Comic Sans MS", 14))

def open_settings():
    """Ayarlar ekranını açar"""
    main_frame.pack_forget()
    settings_frame.pack(fill="both", expand=True)

def back_to_main():
    """Ana menüye geri döner"""
    # Check which frame is currently visible and hide it
    if settings_frame.winfo_ismapped():
        settings_frame.pack_forget()
    elif hasattr(root, 'current_sologame') and root.current_sologame and root.current_sologame.solo_game_frame.winfo_ismapped():
        root.current_sologame.solo_game_frame.pack_forget()
    elif hasattr(root, 'current_mapmatchgame') and root.current_mapmatchgame and root.current_mapmatchgame.map_canvas.winfo_ismapped():
         root.current_mapmatchgame.destroy_game() # Use a dedicated method to clean up map game
    elif hasattr(root, 'current_twoplayergame') and root.current_twoplayergame and root.current_twoplayergame.frame.winfo_ismapped():
         root.current_twoplayergame.frame.pack_forget()
         # Also handle sub-games within two player mode
         if hasattr(root.current_twoplayergame, 'active_game_frame') and root.current_twoplayergame.active_game_frame:
             root.current_twoplayergame.active_game_frame.pack_forget()
             root.current_twoplayergame.active_game_frame = None
             
    main_frame.pack(fill="both", expand=True)

def toggle_music():
    """Müziği açıp kapatır"""
    if background_music: # Only toggle if music loaded
        if music_var.get():
            pygame.mixer.music.unpause()
            if music_on_img: music_btn.config(image=music_on_img)
        else:
            pygame.mixer.music.pause()
            if music_off_img: music_btn.config(image=music_off_img)
    else:
        print("Background music not available to toggle.")

def toggle_sound():
    """Ses efektlerini açıp kapatır"""
    if sound_var.get():
        button_click_sound.set_volume(1.0)
        if sound_on_img: sound_btn.config(image=sound_on_img)
    else:
        button_click_sound.set_volume(0.0)
        if sound_off_img: sound_btn.config(image=sound_off_img)

def change_language():
    """Dil değişikliği yapar"""
    lang = language_var.get()
    if lang == "Türkçe":
        settings_label.config(text="AYARLAR")
        back_button.config(text="⬅️ Geri")
        solo_button.config(text="👤 Solo")
        vs_bot_button.config(text="👤 VS 🤖")
        vs_player_button.config(text="👤 VS 👤")
        settings_button.config(text="⚙️ Ayarlar")
        exit_button.config(text="❌ Çıkış")
        language_label.config(text="Dil / Language:")
        theme_button.config(text="Tema")
        if hasattr(root, 'current_sologame') and root.current_sologame:
             root.current_sologame.theme_btn.config(text="Tema")
             # Update other text elements in SoloGame if needed
        if hasattr(root, 'current_mapmatchgame') and root.current_mapmatchgame:
             root.current_mapmatchgame.score_labels[0].config(text="Oyuncu: 0")
             root.current_mapmatchgame.score_labels[1].config(text="Bot: 0")
             # Update other text elements in MapMatchGame if needed
             
    elif lang == "English":
        settings_label.config(text="SETTINGS")
        back_button.config(text="⬅️ Back")
        solo_button.config(text="👤 Solo")
        vs_bot_button.config(text="👤 VS 🤖")
        vs_player_button.config(text="👤 VS 👤")
        settings_button.config(text="⚙️ Settings")
        exit_button.config(text="❌ Exit")
        language_label.config(text="Language / Dil:")
        theme_button.config(text="Theme")
        if hasattr(root, 'current_sologame') and root.current_sologame:
             root.current_sologame.theme_btn.config(text="Theme")
             # Update other text elements in SoloGame if needed
        if hasattr(root, 'current_mapmatchgame') and root.current_mapmatchgame:
             root.current_mapmatchgame.score_labels[0].config(text="Player: 0")
             root.current_mapmatchgame.score_labels[1].config(text="Bot: 0")
             # Update other text elements in MapMatchGame if needed

def create_toggle_images(base_image_path, size=(30, 30)):
    """Create on and off versions of an image with a red cross for off state"""
    on_img_tk, off_img_tk = None, None
    try:
        if not os.path.exists(base_image_path):
             print(f"Warning: Toggle image not found: {base_image_path}. Creating placeholder.")
             # Create placeholder images if file is missing
             img_on = Image.new('RGB', size, (0, 255, 0)) # Green for ON
             img_off = Image.new('RGB', size, (255, 0, 0)) # Red for OFF
             on_img_tk = ImageTk.PhotoImage(img_on)
             off_img_tk = ImageTk.PhotoImage(img_off)
        else:
            img = Image.open(base_image_path).convert("RGBA").resize(size)
            on_img_tk = ImageTk.PhotoImage(img)
            
            off_img = img.copy()
            draw = ImageDraw.Draw(off_img)
            # Draw a more visible red cross
            draw.line((5, 5, size[0]-5, size[1]-5), fill="red", width=4)
            draw.line((5, size[1]-5, size[0]-5, 5), fill="red", width=4)
            off_img_tk = ImageTk.PhotoImage(off_img)
            
    except Exception as e:
        print(f"Error creating toggle images from {base_image_path}: {e}")
        # Fallback to simple colored squares if PIL fails
        img_on = Image.new('RGB', size, (0, 255, 0))
        img_off = Image.new('RGB', size, (255, 0, 0))
        on_img_tk = ImageTk.PhotoImage(img_on)
        off_img_tk = ImageTk.PhotoImage(img_off)
        
    return on_img_tk, off_img_tk

def get_flying_card_colors():
    """Tema rengine göre uçuşan kart renklerini döndürür"""
    if current_theme["bg"] == "#263238": # Dark theme
        return ["#FFD600", "#00B8D4", "#FF8A65", "#A7FFEB", "#FF80AB", "#B388FF", "#B0BEC5"]
    else: # Light theme (default)
        return ["#FFCDD2", "#F8BBD0", "#E1BEE7", "#BBDEFB", "#B2EBF2", "#C8E6C9", "#FFF9C4"]

def update_flying_card_colors():
    """Uçuşan kartların renklerini günceller"""
    colors = get_flying_card_colors()
    for card in flying_cards:
        if canvas.winfo_exists() and canvas.type(card["id"]) == 'text': # Check if item exists and is text
             canvas.itemconfig(card["id"], fill=random.choice(colors))

def toggle_theme():
    """Tema değişikliği yapar"""
    if current_theme["bg"] == "#FFEBEE":
        current_theme["bg"] = "#263238" # Dark theme
    else:
        current_theme["bg"] = "#FFEBEE" # Light theme
    apply_theme(current_theme["bg"])

def apply_theme(bg_color):
    """Temayı uygular"""
    fg_color = "white" if bg_color == "#263238" else "black"
    light_button_bg = "#BBDEFB" if bg_color == "#FFEBEE" else "#37474F"
    dark_button_bg = "#B2EBF2" if bg_color == "#FFEBEE" else "#607D8B"
    
    root.configure(bg=bg_color)
    main_frame.configure(bg=bg_color)
    if canvas.winfo_exists(): canvas.configure(bg=bg_color)
    settings_frame.configure(bg=bg_color)
    settings_label.configure(bg=bg_color, fg=fg_color)
    language_label.configure(bg=bg_color, fg=fg_color)
    language_menu.configure(bg=bg_color, fg=fg_color, activebackground=dark_button_bg)
    back_button.configure(bg=light_button_bg, fg=fg_color)
    theme_button.configure(bg=dark_button_bg, fg=fg_color)
    
    # Configure main menu buttons
    solo_button.configure(fg=fg_color)
    vs_bot_button.configure(fg=fg_color)
    vs_player_button.configure(fg=fg_color)
    settings_button.configure(bg=light_button_bg, fg=fg_color)
    exit_button.configure(bg=dark_button_bg)
    
    # Configure sound/music buttons
    if sound_btn: sound_btn.configure(bg=bg_color)
    if music_btn: music_btn.configure(bg=bg_color)
    
    update_flying_card_colors()

    # Apply theme to active game screens
    sg = getattr(root, "current_sologame", None)
    if sg and sg.solo_game_frame.winfo_exists():
        sg.solo_game_frame.configure(bg=bg_color)
        sg.stats_frame.configure(bg=bg_color)
        # Update colors of stat boxes based on theme
        sg.time_box.configure(bg="#BBDEFB" if bg_color == "#FFEBEE" else "#37474F")
        sg.time_icon.configure(bg=sg.time_box.cget("bg"), fg=fg_color)
        sg.timer_label.configure(bg=sg.time_box.cget("bg"), fg=fg_color)
        sg.score_box.configure(bg="#FFF176" if bg_color == "#FFEBEE" else "#607D8B")
        sg.star_icon.configure(bg=sg.score_box.cget("bg")) # Icon bg matches box
        sg.score_value.configure(bg=sg.score_box.cget("bg"), fg=fg_color)
        sg.click_box.configure(bg="#AED581" if bg_color == "#FFEBEE" else "#789262")
        sg.click_icon.configure(bg=sg.click_box.cget("bg"), fg=fg_color)
        sg.click_label.configure(bg=sg.click_box.cget("bg"), fg=fg_color)
        
        if hasattr(sg, "board_frame") and sg.board_frame.winfo_exists():
            sg.board_frame.configure(bg=bg_color)
            for row in getattr(sg, "buttons", []):
                for btn in row:
                    if btn.winfo_exists(): btn.configure(bg=bg_color) # Apply to existing buttons
        if hasattr(sg, "back_btn") and sg.back_btn.winfo_exists():
            sg.back_btn.configure(bg=bg_color)
        if hasattr(sg, "theme_btn") and sg.theme_btn.winfo_exists():
            sg.theme_btn.configure(bg=dark_button_bg, fg=fg_color)
            
    mg = getattr(root, "current_mapmatchgame", None)
    if mg and mg.map_canvas.winfo_exists():
        mg.map_canvas.configure(bg="#B0BEC5" if bg_color == "#FFEBEE" else "#455A64") # Adjust map bg slightly
        mg.flag_frame.configure(bg=bg_color)
        mg.flags_container.configure(bg=bg_color)
        mg.status_label.configure(bg="#FFF9C4" if bg_color == "#FFEBEE" else "#424242", fg=fg_color)
        mg.score_labels[0].configure(bg="#FFF9C4" if bg_color == "#FFEBEE" else "#424242", fg=fg_color)
        mg.score_labels[1].configure(bg="#FFF9C4" if bg_color == "#FFEBEE" else "#424242", fg=fg_color)
        for lbl in mg.flag_labels:
            if lbl.winfo_exists(): lbl.configure(bg=bg_color)
        # Update box label colors
        for box in mg.flag_boxes:
            if box.winfo_exists():
                 for child in box.winfo_children():
                     if isinstance(child, tk.Label):
                         child.configure(fg=fg_color) # Adjust text color in boxes

    tp = getattr(root, "current_twoplayergame", None)
    if tp and tp.frame.winfo_exists():
         tp.frame.configure(bg=bg_color)
         for widget in tp.frame.winfo_children():
             if isinstance(widget, tk.Label): widget.configure(bg=bg_color, fg=fg_color)
             elif isinstance(widget, tk.Button): widget.configure(fg=fg_color)
         # Apply theme to active sub-game if any
         if hasattr(tp, 'active_game_frame') and tp.active_game_frame and tp.active_game_frame.winfo_exists():
             tp.active_game_frame.configure(bg=bg_color)
             for widget in tp.active_game_frame.winfo_children():
                 if isinstance(widget, tk.Label): widget.configure(bg=bg_color, fg=fg_color)
                 elif isinstance(widget, tk.Button): widget.configure(fg=fg_color)
                 elif isinstance(widget, tk.Frame): widget.configure(bg=bg_color)


class SoloGame:
    def __init__(self, root, main_frame, level=2):
        self.root = root
        self.main_frame = main_frame
        self.level = level  # 2, 4, 6
        self.grid_size = self.level
        self.score = 0
        self.click_count = 0
        self.time_limit = 180 # 3 minutes
        self.remaining_time = self.time_limit
        self.game_over_flag = False
        self.timer_update_id = None
        self.back_popup_frame = None # Initialize popup attribute
        root.current_sologame = self # Store reference

        self.main_frame.pack_forget()
        self.solo_game_frame = tk.Frame(root, bg=current_theme["bg"])
        self.solo_game_frame.pack(fill="both", expand=True)

        # Stats frame on the right
        self.stats_frame = tk.Frame(self.solo_game_frame, bg=current_theme["bg"])
        self.stats_frame.pack(side="right", fill="y", padx=20, pady=20)

        # Time box
        self.time_box = tk.Frame(self.stats_frame, bg="#BBDEFB", bd=2, relief="ridge")
        self.time_box.pack(side="top", pady=10, fill="x")
        self.time_icon = tk.Label(self.time_box, text="⏳", font=("Comic Sans MS", 22), bg="#BBDEFB")
        self.time_icon.pack(side="left", padx=5, pady=5)
        self.timer_label = tk.Label(self.time_box, text="", font=("Comic Sans MS", 16, "bold"), bg="#BBDEFB")
        self.timer_label.pack(side="left", padx=5, pady=5)

        # Score box
        self.score_box = tk.Frame(self.stats_frame, bg="#FFF176", bd=2, relief="ridge")
        self.score_box.pack(side="top", pady=10, fill="x")
        self.star_img = None
        try:
            star_path = "Try/Solo_images/star.png"
            if os.path.exists(star_path):
                 self.star_img = ImageTk.PhotoImage(Image.open(star_path).resize((32, 32)))
            else:
                 print(f"Warning: Star image not found: {star_path}")
        except Exception as e:
            print(f"Error loading star image: {e}")
        self.star_icon = tk.Label(self.score_box, image=self.star_img, text="⭐" if not self.star_img else "", font=("Comic Sans MS", 22), bg="#FFF176")
        if self.star_img:
            self.star_icon.image = self.star_img
        self.star_icon.pack(side="left", padx=5, pady=5)
        self.score_value = tk.Label(self.score_box, text="0", font=("Comic Sans MS", 16, "bold"), bg="#FFF176")
        self.score_value.pack(side="left", padx=5, pady=5)

        # Click count box
        self.click_box = tk.Frame(self.stats_frame, bg="#AED581", bd=2, relief="ridge")
        self.click_box.pack(side="top", pady=10, fill="x")
        self.click_icon = tk.Label(self.click_box, text="🖱️", font=("Comic Sans MS", 22), bg="#AED581")
        self.click_icon.pack(side="left", padx=5, pady=5)
        self.click_label = tk.Label(self.click_box, text="0", font=("Comic Sans MS", 16, "bold"), bg="#AED581")
        self.click_label.pack(side="left", padx=5, pady=5)

        # Theme button
        self.theme_btn = tk.Button(self.stats_frame, text="Tema", font=("Comic Sans MS", 12), 
                                   bg="#B2EBF2" if current_theme["bg"] == "#FFEBEE" else "#607D8B", 
                                   fg="black" if current_theme["bg"] == "#FFEBEE" else "white", 
                                   command=toggle_theme)
        self.theme_btn.pack(side="top", pady=10, fill="x")

        # Back button (top left)
        self.back_img = None
        try:
            back_path = "Try/Solo_images/back.png"
            if os.path.exists(back_path):
                 self.back_img = ImageTk.PhotoImage(Image.open(back_path).resize((48, 48)))
            else:
                 print(f"Warning: Back image not found: {back_path}")
        except Exception as e:
            print(f"Error loading back image: {e}")
        self.back_btn = tk.Button(
            self.solo_game_frame, image=self.back_img, text="⬅" if not self.back_img else "", 
            font=("Arial", 24) if not self.back_img else None,
            bd=0, bg=current_theme["bg"],
            command=self.ask_back_to_menu, width=56, height=56
        )
        if self.back_img: self.back_btn.image = self.back_img
        self.back_btn.place(relx=0.05, rely=0.05, anchor="nw")
        
        # Board frame in the center
        self.board_frame = tk.Frame(self.solo_game_frame, bg=current_theme["bg"])
        self.board_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.update_timer()
        self.setup_board()
        apply_theme(current_theme["bg"]) # Apply theme initially

    def ask_back_to_menu(self):
        # Stop timer
        if self.timer_update_id:
            self.root.after_cancel(self.timer_update_id)
            self.timer_update_id = None

        # Show confirmation popup
        if self.back_popup_frame and self.back_popup_frame.winfo_exists():
            return  # Popup already open

        popup_bg = "#FFF9C4" if current_theme["bg"] == "#FFEBEE" else "#424242"
        popup_fg = "black" if current_theme["bg"] == "#FFEBEE" else "white"
        button_bg = "#FFEBEE" if current_theme["bg"] == "#FFEBEE" else "#616161"
        
        self.back_popup_frame = tk.Frame(self.solo_game_frame, bg=popup_bg, bd=3, relief="ridge")
        self.back_popup_frame.place(relx=0.5, rely=0.5, anchor="center")

        label = tk.Label(
            self.back_popup_frame, 
            text="Ana menüye dönmek istediğinize emin misiniz?", 
            font=("Comic Sans MS", 13, "bold"), bg=popup_bg, fg=popup_fg
        )
        label.pack(padx=20, pady=(15, 10))

        btn_frame = tk.Frame(self.back_popup_frame, bg=popup_bg)
        btn_frame.pack(pady=(0, 15))

        def on_yes():
            self.back_popup_frame.destroy()
            self.back_popup_frame = None
            self.destroy_game()

        def on_no():
            self.back_popup_frame.destroy()
            self.back_popup_frame = None
            # Resume timer if game not over
            if not self.game_over_flag:
                self.timer_update_id = self.root.after(1000, self.update_timer)

        yes_btn = tk.Button(
            btn_frame, text="✔️ Evet", font=("Comic Sans MS", 14, "bold"), 
            bg=button_bg, fg=popup_fg, width=8, command=on_yes, activebackground="#FFE082"
        )
        yes_btn.pack(side="left", padx=10)

        no_btn = tk.Button(
            btn_frame, text="❌ Hayır", font=("Comic Sans MS", 14, "bold"), 
            bg=button_bg, fg=popup_fg, width=8, command=on_no, activebackground="#FFE082"
        )
        no_btn.pack(side="left", padx=10)

    def update_timer(self):
        if self.game_over_flag:
            if self.timer_update_id:
                self.root.after_cancel(self.timer_update_id)
                self.timer_update_id = None
            return

        if self.remaining_time > 0:
            self.remaining_time -= 1
            minutes = self.remaining_time // 60
            seconds = self.remaining_time % 60
            self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
            self.timer_update_id = self.root.after(1000, self.update_timer)
        else:
            if not self.game_over_flag:
                self.game_over_flag = True
                self.timer_label.config(text="00:00")
                self.show_time_up_screen()
            if self.timer_update_id:
                self.root.after_cancel(self.timer_update_id)
                self.timer_update_id = None

    def show_time_up_screen(self):
        # Disable remaining buttons
        for r_idx, row_buttons in enumerate(self.buttons):
            for c_idx, btn in enumerate(row_buttons):
                if btn.winfo_exists() and btn['state'] == 'normal':
                    try:
                        btn.config(state="disabled", bg="#E0E0E0")
                    except tk.TclError: 
                        pass
        
        messagebox.showinfo("Oyun Bitti", "Süre doldu! 😟 Tekrar denemek ister misin?", parent=self.solo_game_frame)
        self.destroy_game()

    def destroy_game(self):
        """Cleans up the game frame and returns to the main menu."""
        if self.timer_update_id:
            self.root.after_cancel(self.timer_update_id)
            self.timer_update_id = None
        if self.back_popup_frame and self.back_popup_frame.winfo_exists():
            self.back_popup_frame.destroy()
        self.solo_game_frame.destroy() # Destroy the game frame
        root.current_sologame = None # Clear reference
        main_frame.pack(fill="both", expand=True) # Show main menu

    def setup_board(self):
        image_dir = "Try/Solo_images"
        try:
            if not os.path.exists(image_dir):
                 raise FileNotFoundError(f"Directory not found: {image_dir}")
            all_image_files = [f for f in os.listdir(image_dir) if f.startswith("image") and f.endswith(".jpeg")]
            if not all_image_files:
                 raise FileNotFoundError(f"No image files found in {image_dir}")
            all_image_files.sort()
        except FileNotFoundError as e:
            messagebox.showerror("Hata", f"Solo oyun resimleri bulunamadı veya yüklenemedi:\n{e}", parent=self.solo_game_frame)
            self.destroy_game()
            return
        except Exception as e:
            messagebox.showerror("Hata", f"Resim dosyaları okunurken hata: {e}", parent=self.solo_game_frame)
            self.destroy_game()
            return

        # Determine required images based on grid size
        if self.grid_size == 2:
            needed = 2
        elif self.grid_size == 4:
            needed = 8
        else: # 6x6
            needed = 18
            
        if len(all_image_files) < needed:
             messagebox.showwarning("Uyarı", f"Yeterli resim dosyası yok ({len(all_image_files)}/{needed}). Oyun başlatılamıyor.", parent=self.solo_game_frame)
             self.destroy_game()
             return
             
        image_files = random.sample(all_image_files, needed)

        self.images = []
        self.back_image = None
        try:
            # Load game images
            for img_file in image_files:
                img_path = os.path.join(image_dir, img_file)
                img = Image.open(img_path).resize((100, 100))
                self.images.append(ImageTk.PhotoImage(img))
            self.images *= 2 # Duplicate for pairs
            random.shuffle(self.images)
            
            # Load back image
            back_img_path = os.path.join(image_dir, "question_mark.jpg")
            if os.path.exists(back_img_path):
                 self.back_image = ImageTk.PhotoImage(Image.open(back_img_path).resize((100, 100)))
            else:
                 print(f"Warning: Back image 'question_mark.jpg' not found. Using placeholder.")
                 # Create placeholder if missing
                 back_placeholder = Image.new('RGB', (100, 100), (100, 100, 200)) # Blue placeholder
                 draw = ImageDraw.Draw(back_placeholder)
                 draw.text((30, 30), "?", fill="white")
                 self.back_image = ImageTk.PhotoImage(back_placeholder)
                 
        except Exception as e:
            messagebox.showerror("Hata", f"Oyun resimleri yüklenirken hata: {e}", parent=self.solo_game_frame)
            self.destroy_game()
            return

        self.flipped = []
        self.matched = []
        self.buttons = []
        self.lock = False

        # Clear previous board if any
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        # Create buttons
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                btn = tk.Button(
                    self.board_frame,
                    image=self.back_image,
                    width=100,
                    height=100,
                    command=lambda r=i, c=j: self.flip_card(r, c),
                    bg=current_theme["bg"],
                    relief="flat", bd=0 # Flat look
                )
                if self.back_image: btn.image = self.back_image
                btn.grid(row=i, column=j, padx=5, pady=5)
                row.append(btn)
            self.buttons.append(row)

    def flip_card(self, r, c):
        if self.lock or (r, c) in self.matched or (r, c) in self.flipped:
            return

        # Increment click count
        self.click_count += 1
        self.click_label.config(text=str(self.click_count))

        play_button_sound()
        btn = self.buttons[r][c]
        img_index = r * self.grid_size + c
        if img_index >= len(self.images):
             print(f"Error: Image index {img_index} out of bounds for {len(self.images)} images.")
             return # Avoid index error
             
        img = self.images[img_index]

        # Simple flip without animation for now
        btn.config(image=img, bg="white")
        btn.image = img # Keep reference
        
        self.flipped.append((r, c))

        if len(self.flipped) == 2:
            self.lock = True
            self.root.after(800, self.check_match) # Slightly faster check

    def check_match(self):
        (r1, c1), (r2, c2) = self.flipped
        idx1, idx2 = r1 * self.grid_size + c1, r2 * self.grid_size + c2
        btn1, btn2 = self.buttons[r1][c1], self.buttons[r2][c2]

        # Check if images match (using the PhotoImage objects directly might be unreliable, compare underlying data if needed)
        # For simplicity, let's assume PhotoImage comparison works if they load the same base image
        if self.images[idx1] == self.images[idx2]:
            # Match found
            btn1.config(state="disabled", bg="#A5D6A7") # Greenish background for matched
            btn2.config(state="disabled", bg="#A5D6A7")
            self.matched.extend([(r1, c1), (r2, c2)])
            self.score += 1
            self.score_value.config(text=str(self.score))
            self.lock = False
            
            # Check if all pairs are matched
            if len(self.matched) == self.grid_size * self.grid_size:
                if not self.game_over_flag:
                    self.game_over_flag = True
                    if self.timer_update_id:
                        self.root.after_cancel(self.timer_update_id)
                        self.timer_update_id = None
                    self.root.after(500, self.next_level_or_victory) # Delay before next level/victory
        else:
            # No match, flip back
            btn1.config(image=self.back_image, bg=current_theme["bg"])
            btn2.config(image=self.back_image, bg=current_theme["bg"])
            btn1.image = self.back_image
            btn2.image = self.back_image
            self.lock = False

        self.flipped.clear()

    def next_level_or_victory(self):
        """Decides whether to advance level or show victory screen."""
        if self.grid_size == 6:
            self.show_victory_screen()
        else:
            self.advance_level()
            
    def advance_level(self):
        """Advances to the next level (2x2 -> 4x4 -> 6x6)."""
        # Determine next level size
        next_level = 4 if self.grid_size == 2 else 6
        self.grid_size = next_level
        self.level = next_level
        
        # Reset game state for new level (keep score and clicks)
        self.game_over_flag = False
        self.timer_update_id = None # Timer will be restarted by setup_board
        self.flipped = []
        self.matched = []
        self.buttons = []
        self.lock = False

        # Setup the board for the new level
        self.setup_board()
        self.update_timer() # Restart timer for the new level

    def show_victory_screen(self):
        """Shows victory message and returns to main menu."""
        messagebox.showinfo(
            "Tebrikler!",
            f"Tüm seviyeleri tamamladınız!\nToplam Süre: {self.time_limit - self.remaining_time} saniye\nSkor: {self.score}\nTıklama: {self.click_count}",
            parent=self.solo_game_frame
        )
        self.destroy_game()

# Ana uygulama başlangıcı
root = tk.Tk()
root.title("NINTENDO")
root.geometry("400x300")
root.configure(bg="#FFEBEE")

# Create toggle images for sound and music buttons
try:
    sound_on_img, sound_off_img = create_toggle_images("Try/Solo_images/sound_on.png")
    music_on_img, music_off_img = create_toggle_images("Try/Solo_images/music_on.png")
except Exception as e:
    print(f"Ses ve müzik simgeleri yüklenirken hata: {e}")
    # Fallback to text if images fail
    sound_on_img = sound_off_img = music_on_img = music_off_img = None

# Ana menü frame'i
main_frame = tk.Frame(root, bg="#FFEBEE")
main_frame.pack(fill="both", expand=True)

# Canvas'ı tam ekran yap
canvas = tk.Canvas(main_frame, bg="#FFEBEE", highlightthickness=0)
canvas.pack(fill="both", expand=True)

def update_canvas_size(event=None):
    canvas.config(width=root.winfo_width(), height=root.winfo_height())

root.bind("<Configure>", update_canvas_size)

# Uçuşan kartlar
flying_cards = []
card_count = 30
for _ in range(card_count):
    x = random.randint(0, root.winfo_width() or 400)
    y = random.randint(0, root.winfo_height() or 300)
    dx, dy = random.choice([-2, -1, 1, 2]), random.choice([-2, -1, 1, 2])
    color = random.choice(get_flying_card_colors())
    card = canvas.create_text(x, y, text="🃏", font=("Comic Sans MS", 14), fill=color)
    flying_cards.append({"id": card, "dx": dx, "dy": dy})

def animate_cards():
    w = root.winfo_width()
    h = root.winfo_height()
    for card in flying_cards:
        x, y = canvas.coords(card["id"])
        dx, dy = card["dx"], card["dy"]
        # Wrap-around mantığı
        x_new = (x + dx) % w
        y_new = (y + dy) % h
        canvas.coords(card["id"], x_new, y_new)
    canvas.after(30, animate_cards)

animate_cards()

def start_solo_game():
    main_frame.pack_forget()
    root.current_sologame = SoloGame(root, main_frame)

def start_vs_bot_game():
    main_frame.pack_forget()
    root.current_mapmatchgame = MapMatchGame(root, main_frame)

def start_vs_player_game():
    main_frame.pack_forget()
    root.current_twoplayergame = TwoPlayerGame(root, main_frame)

# Butonlar
solo_button = tk.Button(main_frame, text="👤 Solo", font=("Comic Sans MS", 14, "bold"), bg="#FFCDD2", fg="black", bd=5, relief="ridge", command=start_solo_game)
vs_bot_button = tk.Button(main_frame, text="👤 VS 🤖", font=("Comic Sans MS", 14, "bold"), bg="#F8BBD0", fg="black", bd=5, relief="ridge", command=start_vs_bot_game)
vs_player_button = tk.Button(main_frame, text="👤 VS 👤", font=("Comic Sans MS", 14, "bold"), bg="#E1BEE7", fg="black", bd=5, relief="ridge", command=start_vs_player_game)
settings_button = tk.Button(main_frame, text="⚙️ Ayarlar", font=("Comic Sans MS", 14), bg="#BBDEFB", fg="black", command=open_settings)
exit_button = tk.Button(main_frame, text="❌ Çıkış", font=("Comic Sans MS", 14), bg="#B2EBF2", fg="red", command=exit_game)

# Sound and music toggle buttons
sound_var = tk.IntVar(value=1)
sound_btn = tk.Button(main_frame, image=sound_on_img, bg="#FFEBEE", bd=0, 
                     command=lambda: [sound_var.set(0 if sound_var.get() else 1), toggle_sound()])
sound_btn.place(relx=0.95, rely=0.05, anchor="ne")

music_var = tk.IntVar(value=1)
music_btn = tk.Button(main_frame, image=music_on_img, bg="#FFEBEE", bd=0, 
                     command=lambda: [music_var.set(0 if music_var.get() else 1), toggle_music()])
music_btn.place(relx=0.95, rely=0.15, anchor="ne")

# Animasyon için hover efektleri
for button in [solo_button, vs_bot_button, vs_player_button, settings_button, exit_button]:
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

for button in [solo_button, vs_bot_button, vs_player_button, settings_button, exit_button]:
    button.bind("<Button-1>", lambda event: play_button_sound())

solo_button.place(relx=0.5, rely=0.3, anchor="center")
vs_bot_button.place(relx=0.5, rely=0.5, anchor="center")
vs_player_button.place(relx=0.5, rely=0.7, anchor="center")
settings_button.place(relx=0.5, rely=0.95, anchor='se')
exit_button.place(relx=0.5, rely=0.95, anchor='sw')

# Settings frame'i
settings_frame = tk.Frame(root, bg="#FFEBEE")

settings_label = tk.Label(settings_frame, text="AYARLAR", font=("Comic Sans MS", 20, "bold"), bg="#FFEBEE")
settings_label.pack(pady=10)

# Dil seçimi
language_var = tk.StringVar(value="Türkçe")
language_label = tk.Label(settings_frame, text="Dil / Language:", font=("Comic Sans MS", 12), bg="#FFEBEE")
language_label.pack(pady=5)
language_menu = tk.OptionMenu(settings_frame, language_var, "Türkçe", "English", command=lambda _: change_language())
language_menu.pack(pady=5)

# Geri düğmesi
back_button = tk.Button(settings_frame, text="⬅️ Geri", font=("Comic Sans MS", 14), bg="#BBDEFB", command=back_to_main)
back_button.pack(side="left", padx=5, pady=5)
back_button.place(relx=0.05, rely=0.1, anchor="w")

# Ayarlara tema butonu ekle
theme_button = tk.Button(settings_frame, text="Tema", font=("Comic Sans MS", 14), bg="#B2EBF2", command=toggle_theme)
theme_button.pack(pady=10)

# Ana döngüyü başlat
if __name__ == "__main__":
    root.mainloop()
