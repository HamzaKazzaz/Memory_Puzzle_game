import tkinter as tk
from tkinter import messagebox
import random
import pygame

# Pygame başlatma (müzik ve ses efektleri için)
pygame.mixer.init()

# Ses dosyalarını yükleme
button_click_sound = pygame.mixer.Sound("Try/click-buton.wav")  # Tuş sesi
background_music = "Try/Main-game-music.mp3"  # Arka plan müziği 

# Arka plan müziğini başlatma
pygame.mixer.music.load(background_music)
pygame.mixer.music.play(-1)  # Sonsuz döngüde çal

def play_button_sound():
    pygame.mixer.Sound.play(button_click_sound)

def exit_game():
    if messagebox.askyesno("Çıkış", "Oyundan çıkmak istediğinize emin misiniz?"):
        root.destroy()

def on_enter(event):
    event.widget.config(font=("Comic Sans MS", 16, "bold"))

def on_leave(event):
    event.widget.config(font=("Comic Sans MS", 14))

def open_settings():
    main_frame.pack_forget()
    settings_frame.pack(fill="both", expand=True)

def back_to_main():
    settings_frame.pack_forget()
    main_frame.pack(fill="both", expand=True)

def toggle_music():
    if music_var.get():
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.pause()

def toggle_sound():
    if sound_var.get():
        button_click_sound.set_volume(1.0)
    else:
        button_click_sound.set_volume(0.0)

def change_language():
    if language_var.get() == "Türkçe":
        # Ayarlar ekranı metinleri
        settings_label.config(text="⚙️ AYARLAR")
        sound_check.config(text="Ses Efektleri")
        music_check.config(text="Arka Plan Müziği")
        back_button.config(text="⬅️ Geri")
        
        # Ana menü metinleri
        solo_button.config(text="👤 Solo")
        vs_bot_button.config(text="👤 VS 🤖")
        vs_player_button.config(text="👤 VS 👤")
        settings_button.config(text="⚙️ Ayarlar")
        exit_button.config(text="❌ Çıkış")
    elif language_var.get() == "English":
        # Ayarlar ekranı metinleri
        settings_label.config(text="⚙️ SETTINGS")
        sound_check.config(text="Sound Effects")
        music_check.config(text="Background Music")
        back_button.config(text="⬅️ Back")
        
        # Ana menü metinleri
        solo_button.config(text="👤 Solo")
        vs_bot_button.config(text="👤 VS 🤖")
        vs_player_button.config(text="👤 VS 👤")
        settings_button.config(text="⚙️ Settings")
        exit_button.config(text="❌ Exit")

root = tk.Tk()
root.title("NINTENDO")
root.geometry("400x300")
root.configure(bg="#FFEBEE")

# Ana menü frame'i
main_frame = tk.Frame(root, bg="#FFEBEE")
main_frame.pack(fill="both", expand=True)

# Arka plana küçük kart simgeleri ekleme
canvas = tk.Canvas(main_frame, width=4500, height=3000, bg="#FFEBEE", highlightthickness=0)
canvas.pack(fill="both", expand=True)

for _ in range(200):
    x, y = random.randint(50, 2000), random.randint(30, 1500)
    canvas.create_text(x, y, text="🃏", font=("Comic Sans MS", 12), fill=random.choice(["#FFCDD2", "#F8BBD0", "#E1BEE7"]))

# Butonlar
solo_button = tk.Button(main_frame, text="👤 Solo", font=("Comic Sans MS", 14, "bold"), bg="#FFCDD2", fg="black", bd=5, relief="ridge")
vs_bot_button = tk.Button(main_frame, text="👤 VS 🤖", font=("Comic Sans MS", 14, "bold"), bg="#F8BBD0", fg="black", bd=5, relief="ridge", command=lambda: print("VS Bot Modu Seçildi"))
vs_player_button = tk.Button(main_frame, text="👤 VS 👤", font=("Comic Sans MS", 14, "bold"), bg="#E1BEE7", fg="black", bd=5, relief="ridge", command=lambda: print("VS Kişi Modu Seçildi"))
settings_button = tk.Button(main_frame, text="⚙️ Ayarlar", font=("Comic Sans MS", 14), bg="#BBDEFB", fg="black", command=open_settings)
exit_button = tk.Button(main_frame, text="❌ Çıkış", font=("Comic Sans MS", 14), bg="#B2EBF2", fg="red", command=exit_game)

# Animasyon için hover efektleri
for button in [solo_button, vs_bot_button, vs_player_button, settings_button, exit_button]:
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

for button in [solo_button, vs_bot_button, vs_player_button, settings_button, exit_button]:
    button.bind("<Button-1>", lambda event: play_button_sound())

solo_button.place(relx=0.5, rely=0.3, anchor="center")
vs_bot_button.place(relx=0.5, rely=0.5, anchor="center")
vs_player_button.place(relx=0.5, rely=0.7, anchor="center")
settings_button.place(relx=0.05, rely=0.95, anchor='sw')
exit_button.place(relx=0.95, rely=0.95, anchor='se')

# Settings frame'i
settings_frame = tk.Frame(root, bg="#FFEBEE")

settings_label = tk.Label(settings_frame, text="⚙️ AYARLAR", font=("Comic Sans MS", 20, "bold"), bg="#FFEBEE")
settings_label.pack(pady=10)

# Dil seçimi
language_var = tk.StringVar(value="Türkçe")
language_label = tk.Label(settings_frame, text="Dil / Language:", font=("Comic Sans MS", 12), bg="#FFEBEE")
language_label.pack(pady=5)
language_menu = tk.OptionMenu(settings_frame, language_var, "Türkçe", "English", command=lambda _: change_language())
language_menu.pack(pady=5)

# Ses ve müzik seçenekleri
sound_var = tk.IntVar(value=1)
sound_check = tk.Checkbutton(settings_frame, text="Ses Efektleri", variable=sound_var, font=("Comic Sans MS", 12), bg="#FFEBEE", command=toggle_sound)
sound_check.pack(pady=5)

music_var = tk.IntVar(value=1)
music_check = tk.Checkbutton(settings_frame, text="Arka Plan Müziği", variable=music_var, font=("Comic Sans MS", 12), bg="#FFEBEE", command=toggle_music)
music_check.pack(pady=5)

# Geri ve kapatma düğmeleri
back_button = tk.Button(settings_frame, text="⬅️ Geri", font=("Comic Sans MS", 14), bg="#BBDEFB", command=back_to_main)
back_button.pack(side="left", padx=5, pady=5)
back_button.place(relx=0.05, rely=0.1, anchor="w")

root.mainloop()
