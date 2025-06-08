import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import pygame

def set_theme(bg_color, root):
    global THEME_BG
    THEME_BG = bg_color

    def update_widget_bg(widget):
        try:
            widget.config(bg=THEME_BG)
        except Exception:
            pass
        for child in widget.winfo_children():
            update_widget_bg(child)

    for widget in root.winfo_children():
        update_widget_bg(widget)

class TwoPlayerGame:
    def __init__(self, root, main_frame):
        self.root = root
        self.main_frame = main_frame
        self.main_frame.pack_forget()
        THEME_BG = "#FFEBEE"
        self.frame = tk.Frame(self.root, bg=THEME_BG)
        self.frame.pack(fill="both", expand=True)

        title = tk.Label(self.frame, text="İki Kişilik Oyun Seç", font=("Comic Sans MS", 24, "bold"), bg=THEME_BG)
        title.pack(pady=40)

        color_word_btn = tk.Button(self.frame, text="🎨", font=("Comic Sans MS", 16, "bold"),
                                   bg="#FFCDD2", fg="black", width=20, height=2,
                                   command=self.start_color_word_game)
        color_word_btn.pack(pady=20)

        math_btn = tk.Button(self.frame, text="➕➖", font=("Comic Sans MS", 16, "bold"),
                             bg="#C8E6C9", fg="black", width=20, height=2,
                             command=self.start_math_game)
        math_btn.pack(pady=20)

        true_false_btn = tk.Button(self.frame, text="✔️❌", font=("Comic Sans MS", 16, "bold"),
                                   bg="#FFCCBC", fg="black", width=20, height=2,
                                   command=self.start_true_false_game)
        true_false_btn.pack(pady=20)
        
        back_btn = tk.Button(self.frame, text="⬅ Geri", font=("Comic Sans MS", 14),
                             bg="#B3E5FC", command=self.back_to_main)
        back_btn.place(relx = 0.05, rely = 0.1, anchor="w")  # Sol üst köşe

    def start_color_word_game(self):
        self.frame.pack_forget()
        ColorWordGame(self.root, self.main_frame)

    def start_math_game(self):
        self.frame.pack_forget()
        MathGame(self.root, self.main_frame)

    def start_true_false_game(self):
        self.frame.pack_forget()
        TrueFalseGame(self.root, self.main_frame)

    def back_to_main(self):
        self.frame.pack_forget()
        self.main_frame.pack(fill="both", expand=True)
        
class ColorWordGame:
    def __init__(self, root, main_frame):
        self.root = root
        self.main_frame = main_frame
        THEME_BG = "#FFEBEE"  # Tema rengine göre değiştir
        self.frame = tk.Frame(self.root, bg=THEME_BG)
        self.frame.pack(fill="both", expand=True)

        self.title_label = tk.Label(self.frame, text="Renk-Kelime Oyunu", font=("Comic Sans MS", 22, "bold"), bg=THEME_BG)
        self.title_label.pack(pady=20)

        self.colors = ["KIRMIZI", "MAVİ", "YEŞİL", "SARI", "TURUNCU", "MOR", "PEMBE", "KAHVERENGİ"]
        self.color_values = ["red", "blue", "green", "yellow", "orange", "purple", "pink", "brown"]
        self.current_color = None

        self.player1_score = 0
        self.player2_score = 0
        self.player_turn = random.choice([1, 2])  # Rastgele oyuncu seçimi
        self.first_turn = True  # Sadece ilk başta animasyon için

        self.create_widgets()
        self.show_turn_animation()
        self.show_new_word()

    def create_widgets(self):
        self.word_label = tk.Label(self.frame, font=("Comic Sans MS", 48), bg="#FFF8E1")
        self.word_label.pack(pady=20)

        # PUANLAR SAĞ ÜSTTE
        self.score_frame = tk.Frame(self.frame, bg="#FFF8E1")
        self.score_frame.place(relx=1.0, rely=0.0, anchor="ne")
        self.score_title = tk.Label(self.score_frame, text="Puanlar", font=("Comic Sans MS", 14, "bold"), bg="#FFF8E1")
        self.score_title.pack()
        self.score_label = tk.Label(self.score_frame, text="Oyuncu 1: 0\nOyuncu 2: 0", font=("Comic Sans MS", 12), bg="#FFF8E1", justify="right")
        self.score_label.pack()

        self.turn_frame = tk.Frame(self.frame, bg="#FFF8E1")
        self.turn_frame.pack(pady=5)
        self.player1_turn_label = tk.Label(self.turn_frame, text="Oyuncu 1", font=("Comic Sans MS", 16, "bold"), width=10)
        self.player1_turn_label.pack(side="left", padx=5)
        self.player2_turn_label = tk.Label(self.turn_frame, text="Oyuncu 2", font=("Comic Sans MS", 16, "bold"), width=10)
        self.player2_turn_label.pack(side="left", padx=5)

        self.status_label = tk.Label(self.frame, text="", font=("Comic Sans MS", 16, "bold"), bg="#FFF8E1")
        self.status_label.pack(pady=5)

        self.color_buttons_frame = tk.Frame(self.frame, bg="#FFF8E1")
        self.color_buttons_frame.pack(pady=20)

        for color, color_value in zip(self.colors, self.color_values):
            button = tk.Button(self.color_buttons_frame, bg=color_value, width=5, height=2,
                               command=lambda c=color: self.check_answer(c))
            button.pack(side="left", padx=5)

        back_btn = tk.Button(self.frame, text="⬅ Geri", font=("Comic Sans MS", 14),
                             bg="#B3E5FC", command=self.back_to_game_selection)
        back_btn.place(relx = 0.05, rely = 0.1, anchor="w") # Sol üst köşe

        # TIMER LABEL
        self.timer_label = tk.Label(self.frame, text="", font=("Comic Sans MS", 48, "bold"), fg="red", bg="#FFF8E1")
        self.timer_label.place_forget()
        self.random_number_label = tk.Label(self.frame, text="", font=("Comic Sans MS", 32, "bold"), bg="#FFF8E1", fg="gray")
        self.random_number_label.place_forget()

    def show_new_word(self):
        self.current_color = random.choice(self.colors)
        self.word_label.config(text=self.current_color, fg=random.choice(self.color_values))
        self.start_timer()

    def show_turn_animation(self):
        self.status_label.config(text="Sıra çekiliyor...")
        self.frame.after(2000, self.update_turn_labels)

    def update_turn_labels(self):
        if self.player_turn == 1:
            self.player1_turn_label.config(bg="lightgreen")
            self.player2_turn_label.config(bg="lightgray")
            self.status_label.config(text="Sıra: Oyuncu 1'de")
        else:
            self.player1_turn_label.config(bg="lightgray")
            self.player2_turn_label.config(bg="lightgreen")
            self.status_label.config(text="Sıra: Oyuncu 2'de")
        self.first_turn = False

    def check_answer(self, selected_color):
        if self.timer_running:
            self.stop_timer()
            if selected_color == self.current_color:
                if self.player_turn == 1:
                    self.player1_score += 1
                else:
                    self.player2_score += 1
                messagebox.showinfo("Doğru!", f"Oyuncu {self.player_turn} doğru tahmin etti!")
            else:
                messagebox.showinfo("Yanlış!", f"Oyuncu {self.player_turn} yanlış tahmin etti!")
            self.update_scores()
            self.next_turn()

    def update_scores(self):
        self.score_label.config(text=f"Oyuncu 1: {self.player1_score}\nOyuncu 2: {self.player2_score}")

    def next_turn(self):
        self.player_turn = 2 if self.player_turn == 1 else 1
        self.show_turn_animation()  # Sıra animasyonu göster

    def show_turn_animation(self):
        self.status_label.config(text="Sıra çekiliyor...")
        self.timer_label.place_forget()
        self.frame.after(2000, self.after_turn_animation)

    def after_turn_animation(self):
        self.update_turn_labels()
        # Her oyunda ilgili yeni soru/kelime/ifade fonksiyonunu çağırın
        self.show_new_word()  # ColorWordGame için
        # self.generate_question()  # MathGame için
        # self.show_new_statement()  # TrueFalseGame için

    # TIMER FONKSİYONLARI
    def start_timer(self):
        self.timer_seconds = 5
        self.timer_running = True
        self.show_timer()
        self.countdown()

    def show_timer(self):
        x = random.randint(100, 400)
        y = random.randint(100, 300)
        size = 72
        self.timer_label.place(x=x, y=y)
        self.timer_label.config(text=str(self.timer_seconds), font=("Comic Sans MS", size, "bold"), fg="red")
        self.timer_label.lift()
        # Rastgele sayı göster
        rx = random.randint(50, 500)
        ry = random.randint(50, 350)
        rand_num = random.randint(10, 99)
        self.random_number_label.place(x=rx, y=ry)
        self.random_number_label.config(text=str(rand_num))
        self.random_number_label.lift()

    def countdown(self):
        if not self.timer_running:
            return
        if self.timer_seconds > 0:
            self.show_timer()
            self.frame.after(500, self.animate_timer)
            self.frame.after(1000, self.decrement_timer)
        else:
            self.timer_label.place_forget()
            self.timer_running = False
            messagebox.showinfo("Süre doldu!", f"Oyuncu {self.player_turn} süresinde cevaplayamadı!")
            self.next_turn()

    def animate_timer(self):
        # Fontu küçült
        size = max(24, 72 - (5 - self.timer_seconds) * 10)
        self.timer_label.config(font=("Comic Sans MS", size, "bold"))

    def decrement_timer(self):
        self.timer_seconds -= 1
        self.countdown()

    def stop_timer(self):
        self.timer_running = False
        self.timer_label.place_forget()
        self.random_number_label.place_forget()

    def back_to_game_selection(self):
        self.frame.pack_forget()
        TwoPlayerGame(self.root, self.main_frame)


class MathGame:
    def __init__(self, root, main_frame):
        self.root = root
        self.main_frame = main_frame
        THEME_BG = "#FFEBEE"  # Tema rengine uygun
        self.frame = tk.Frame(self.root, bg=THEME_BG)
        self.frame.pack(fill="both", expand=True)

        self.title_label = tk.Label(self.frame, text="Matematik Oyunu", font=("Comic Sans MS", 22, "bold"), bg=THEME_BG)
        self.title_label.pack(pady=20)

        self.player1_score = 0
        self.player2_score = 0
        self.player_turn = random.choice([1, 2])
        self.first_turn = True

        self.create_widgets()
        self.show_turn_animation()
        self.generate_question()

    def create_widgets(self):
        # PUANLAR SAĞ ÜSTTE
        self.score_frame = tk.Frame(self.frame, bg="#FFF8E1")
        self.score_frame.place(relx=1.0, rely=0.0, anchor="ne")
        self.score_title = tk.Label(self.score_frame, text="Puanlar", font=("Comic Sans MS", 14, "bold"), bg="#FFF8E1")
        self.score_title.pack()
        self.score_label = tk.Label(self.score_frame, text="Oyuncu 1: 0\nOyuncu 2: 0", font=("Comic Sans MS", 12), bg="#FFF8E1", justify="right")
        self.score_label.pack()

        self.question_label = tk.Label(self.frame, font=("Comic Sans MS", 24), bg="#FFF8E1")
        self.question_label.pack(pady=20)

        self.answer_buttons_frame = tk.Frame(self.frame, bg="#FFF8E1")
        self.answer_buttons_frame.pack(pady=20)

        self.answer_buttons = []
        for i in range(3):
            button = tk.Button(self.answer_buttons_frame, font=("Comic Sans MS", 14),
                               command=lambda idx=i: self.check_answer(idx))
            button.pack(side="left", padx=5)
            self.answer_buttons.append(button)

        self.turn_frame = tk.Frame(self.frame, bg="#FFF8E1")
        self.turn_frame.pack(pady=5)
        self.player1_turn_label = tk.Label(self.turn_frame, text="Oyuncu 1", font=("Comic Sans MS", 16, "bold"), width=10)
        self.player1_turn_label.pack(side="left", padx=5)
        self.player2_turn_label = tk.Label(self.turn_frame, text="Oyuncu 2", font=("Comic Sans MS", 16, "bold"), width=10)
        self.player2_turn_label.pack(side="left", padx=5)
        self.status_label = tk.Label(self.frame, text="", font=("Comic Sans MS", 16, "bold"), bg="#FFF8E1")
        self.status_label.pack(pady=5)

        back_btn = tk.Button(self.frame, text="⬅ Geri", font=("Comic Sans MS", 14),
                             bg="#B3E5FC", command=self.back_to_game_selection)
        back_btn.place(relx=0.05, rely=0.1, anchor="w")

        # TIMER LABEL
        self.timer_label = tk.Label(self.frame, text="", font=("Comic Sans MS", 48, "bold"), fg="red", bg="#FFF8E1")
        self.timer_label.place_forget()

    def generate_question(self):
        self.num1 = random.randint(1, 10)
        self.num2 = random.randint(1, 10)
        self.operation = random.choice(["+", "-"])
        correct_answer = eval(f"{self.num1} {self.operation} {self.num2}")

        self.question_label.config(text=f"{self.num1} {self.operation} {self.num2} = ?")
        self.correct_answer = correct_answer

        wrong_answers = set()
        while len(wrong_answers) < 2:
            wrong = random.randint(1, 20)
            if wrong != correct_answer:
                wrong_answers.add(wrong)

        options = [correct_answer] + list(wrong_answers)
        random.shuffle(options)

        for i, button in enumerate(self.answer_buttons):
            button.config(text=str(options[i]))

        self.start_timer()

    def check_answer(self, selected_index):
        if self.timer_running:
            self.stop_timer()
            selected = int(self.answer_buttons[selected_index]['text'])
            if selected == self.correct_answer:
                if self.player_turn == 1:
                    self.player1_score += 1
                else:
                    self.player2_score += 1
                messagebox.showinfo("Doğru!", f"Oyuncu {self.player_turn} doğru cevabı verdi!")
            else:
                messagebox.showinfo("Yanlış!", f"Oyuncu {self.player_turn} yanlış cevabı verdi!")
            self.update_scores()
            self.next_turn()

    def update_scores(self):
        self.score_label.config(text=f"Oyuncu 1: {self.player1_score}\nOyuncu 2: {self.player2_score}")

    def next_turn(self):
        self.player_turn = 2 if self.player_turn == 1 else 1
        self.show_turn_animation()

    def show_turn_animation(self):
        self.status_label.config(text="Sıra çekiliyor...")
        self.timer_label.place_forget()
        self.frame.after(2000, self.after_turn_animation) 

    def after_turn_animation(self):
        self.update_turn_labels()
        self.generate_question()

    def show_turn_animation(self):
        if self.first_turn:
            self.status_label.config(text="Sıra çekiliyor...")
            self.frame.after(2000, self.update_turn_labels)
            self.first_turn = False
        else:
            self.update_turn_labels()

    def update_turn_labels(self):
        if self.player_turn == 1:
            self.player1_turn_label.config(bg="lightgreen")
            self.player2_turn_label.config(bg="lightgray")
            self.status_label.config(text="Sıra: Oyuncu 1'de")
        else:
            self.player1_turn_label.config(bg="lightgray")
            self.player2_turn_label.config(bg="lightgreen")
            self.status_label.config(text="Sıra: Oyuncu 2'de")

    # TIMER FONKSİYONLARI
    def start_timer(self):
        self.timer_seconds = 5
        self.timer_running = True
        self.show_timer()
        self.countdown()

    def show_timer(self):
        x = random.randint(100, 400)
        y = random.randint(100, 300)
        size = 72
        self.timer_label.place(x=x, y=y)
        self.timer_label.config(text=str(self.timer_seconds), font=("Comic Sans MS", size, "bold"), fg="red")
        self.timer_label.lift()

    def countdown(self):
        if not self.timer_running:
            return
        if self.timer_seconds > 0:
            self.show_timer()
            self.frame.after(500, self.animate_timer)
            self.frame.after(1000, self.decrement_timer)
        else:
            self.timer_label.place_forget()
            self.timer_running = False
            messagebox.showinfo("Süre doldu!", f"Oyuncu {self.player_turn} süresinde cevaplayamadı!")
            self.next_turn()

    def animate_timer(self):
        size = max(24, 72 - (5 - self.timer_seconds) * 10)
        self.timer_label.config(font=("Comic Sans MS", size, "bold"))

    def decrement_timer(self):
        self.timer_seconds -= 1
        self.countdown()

    def stop_timer(self):
        self.timer_running = False
        self.timer_label.place_forget()

    def back_to_game_selection(self):
        self.frame.pack_forget()
        TwoPlayerGame(self.root, self.main_frame)

# --- TRUE FALSE GAME ---

class TrueFalseGame:
    def __init__(self, root, main_frame):
        self.root = root
        self.main_frame = main_frame
        THEME_BG = "#FFEBEE"
        self.frame = tk.Frame(self.root, bg=THEME_BG)
        self.frame.pack(fill="both", expand=True)

        self.title_label = tk.Label(self.frame, text="Doğru mu Yanlış mı Oyunu", font=("Comic Sans MS", 22, "bold"), bg=THEME_BG)
        self.title_label.pack(pady=20)

        self.statements = [
            ("Zürafa uçar", False),
            ("Dünya yuvarlaktır", True),
            ("Su sıvıdır", True),
            ("Kediler köpeklerden daha büyüktür", False),
            ("Güneş doğudan doğar", True),
            ("Ay, Dünya'nın etrafında döner", True),
            ("Şeytan öldü", False),
            ("Kelebekler 5 yıl yaşar", False),
            ("Kuşlar uçar", True),
            ("Balıklar karada yaşar", False)
        ]
        self.current_statement = None
        self.player1_score = 0
        self.player2_score = 0
        self.player_turn = random.choice([1, 2])
        self.first_turn = True

        self.create_widgets()
        self.show_turn_animation()
        self.show_new_statement()

    def create_widgets(self):
        # PUANLAR SAĞ ÜSTTE
        self.score_frame = tk.Frame(self.frame, bg="#FFF8E1")
        self.score_frame.place(relx=1.0, rely=0.0, anchor="ne")
        self.score_title = tk.Label(self.score_frame, text="Puanlar", font=("Comic Sans MS", 14, "bold"), bg="#FFF8E1")
        self.score_title.pack()
        self.score_label = tk.Label(self.score_frame, text="Oyuncu 1: 0\nOyuncu 2: 0", font=("Comic Sans MS", 12), bg="#FFF8E1", justify="right")
        self.score_label.pack()

        self.statement_label = tk.Label(self.frame, font=("Comic Sans MS", 24), bg="#FFF8E1")
        self.statement_label.pack(pady=20)

        self.turn_frame = tk.Frame(self.frame, bg="#FFF8E1")
        self.turn_frame.pack(pady=5)
        self.player1_turn_label = tk.Label(self.turn_frame, text="Oyuncu 1", font=("Comic Sans MS", 16, "bold"), width=10)
        self.player1_turn_label.pack(side="left", padx=5)
        self.player2_turn_label = tk.Label(self.turn_frame, text="Oyuncu 2", font=("Comic Sans MS", 16, "bold"), width=10)
        self.player2_turn_label.pack(side="left", padx=5)
        self.status_label = tk.Label(self.frame, text="", font=("Comic Sans MS", 16, "bold"), bg="#FFF8E1")
        self.status_label.pack(pady=5)

        self.true_button = tk.Button(self.frame, text="Doğru", font=("Comic Sans MS", 14),
                                     command=lambda: self.check_answer(True))
        self.true_button.pack(pady=10)
        self.false_button = tk.Button(self.frame, text="Yanlış", font=("Comic Sans MS", 14),
                                      command=lambda: self.check_answer(False))
        self.false_button.pack(pady=10)

        back_btn = tk.Button(self.frame, text="⬅ Geri", font=("Comic Sans MS", 14),
                             bg="#B3E5FC", command=self.back_to_game_selection)
        back_btn.place(relx = 0.05, rely = 0.1, anchor="w")

        # TIMER LABEL
        self.timer_label = tk.Label(self.frame, text="", font=("Comic Sans MS", 48, "bold"), fg="red", bg="#FFF8E1")
        self.timer_label.place_forget()

    def show_new_statement(self):
        self.current_statement = random.choice(self.statements)
        self.statement_label.config(text=self.current_statement[0])
        self.start_timer()

    def show_turn_animation(self):
        if self.first_turn:
            self.status_label.config(text="Sıra çekiliyor...")
            self.frame.after(2000, self.update_turn_labels)
            self.first_turn = False
        else:
            self.update_turn_labels()

    def update_turn_labels(self):
        if self.player_turn == 1:
            self.player1_turn_label.config(bg="lightgreen")
            self.player2_turn_label.config(bg="lightgray")
            self.status_label.config(text="Sıra: Oyuncu 1'de")
        else:
            self.player1_turn_label.config(bg="lightgray")
            self.player2_turn_label.config(bg="lightgreen")
            self.status_label.config(text="Sıra: Oyuncu 2'de")

    def check_answer(self, answer):
        if self.timer_running:
            self.stop_timer()
            correct_answer = self.current_statement[1]
            if answer == correct_answer:
                if self.player_turn == 1:
                    self.player1_score += 1
                else:
                    self.player2_score += 1
                messagebox.showinfo("Doğru!", f"Oyuncu {self.player_turn} doğru cevabı verdi!")
            else:
                messagebox.showinfo("Yanlış!", f"Oyuncu {self.player_turn} yanlış cevap verdi!")
            self.update_scores()
            self.next_turn()

    def update_scores(self):
        self.score_label.config(text=f"Oyuncu 1: {self.player1_score}\nOyuncu 2: {self.player2_score}")

    def next_turn(self):
        self.player_turn = 2 if self.player_turn == 1 else 1
        self.show_turn_animation()

    def show_turn_animation(self):
        self.status_label.config(text="Sıra çekiliyor...")
        self.timer_label.place_forget()
        self.frame.after(2000, self.after_turn_animation)

    def after_turn_animation(self):
        self.update_turn_labels()
        self.show_new_statement()

    # TIMER FONKSİYONLARI
    def start_timer(self):
        self.timer_seconds = 5
        self.timer_running = True
        self.show_timer()
        self.countdown()

    def show_timer(self):
        x = random.randint(100, 400)
        y = random.randint(100, 300)
        size = 72
        self.timer_label.place(x=x, y=y)
        self.timer_label.config(text=str(self.timer_seconds), font=("Comic Sans MS", size, "bold"), fg="red")
        self.timer_label.lift()

    def countdown(self):
        if not self.timer_running:
            return
        if self.timer_seconds > 0:
            self.show_timer()
            self.frame.after(500, self.animate_timer)
            self.frame.after(1000, self.decrement_timer)
        else:
            self.timer_label.place_forget()
            self.timer_running = False
            messagebox.showinfo("Süre doldu!", f"Oyuncu {self.player_turn} süresinde cevaplayamadı!")
            self.next_turn()

    def animate_timer(self):
        size = max(24, 72 - (5 - self.timer_seconds) * 10)
        self.timer_label.config(font=("Comic Sans MS", size, "bold"))

    def decrement_timer(self):
        self.timer_seconds -= 1
        self.countdown()

    def stop_timer(self):
        self.timer_running = False
        self.timer_label.place_forget()

    def back_to_game_selection(self):
        self.frame.pack_forget()
        TwoPlayerGame(self.root, self.main_frame)

if __name__ == "__main__":
    root = tk.Tk()
    set_theme("#FFF9C4", root)
    root.mainloop()
