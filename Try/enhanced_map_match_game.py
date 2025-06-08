import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import time
import os

class MapMatchGame:
    def __init__(self, root, main_frame):
        self.root = root
        self.main_frame = main_frame
        self.player_score = 0
        self.bot_score = 0
        self.turn = "player"  # "player" or "bot"
        self.map_canvas = None
        self.flag_frame = None
        self.flags_container = None
        self.status_label = None
        self.score_labels = []
        self.flag_labels = []
        self.flag_boxes = []
        self.drag_data = {"widget": None, "x": 0, "y": 0}
        self.bot_memory = {}  # Bot's remembered matches
        self.player_moves = []  # Player's moves (for hard level)
        self.turn_indicator = None
        self.animation_duration = 500  # ms per flash step (total 3 seconds for 6 steps)
        root.current_mapmatchgame = self
        
        self.setup_world_map_game()

    def get_bot_level(self):
        # Determine bot level from player score
        if self.player_score >= 8:
            return "zor"
        elif self.player_score >= 4:
            return "orta"
        else:
            return "kolay"

    def update_turn_label(self):
        if not self.status_label or not self.status_label.winfo_exists(): 
            return
            
        lang = getattr(self.root, 'language_var', None)
        lang = lang.get() if lang else "Türkçe"
        
        if self.turn == "player":
            bot_level = self.get_bot_level()
            bot_level_text = bot_level.capitalize()
            self.status_label.config(text=f"Sıra: Oyuncu | Bot Seviyesi: {bot_level_text}" if lang == "Türkçe" else f"Turn: Player | Bot Level: {bot_level_text}")
        else:
            bot_level = self.get_bot_level()
            bot_level_text = bot_level.capitalize()
            self.status_label.config(text=f"Sıra: Bot (Düşünüyor...) | Bot Seviyesi: {bot_level_text}" if lang == "Türkçe" else f"Turn: Bot (Thinking...) | Bot Level: {bot_level_text}")
            
        # Update turn indicator
        if self.turn_indicator:
            if self.turn == "player":
                self.turn_indicator.config(text="👤", bg="#4CAF50")  # Green for player
            else:
                self.turn_indicator.config(text="🤖", bg="#FF9800")  # Orange for bot

    def update_scores(self):
        if not self.score_labels or not self.score_labels[0].winfo_exists(): 
            return
            
        lang = getattr(self.root, 'language_var', None)
        lang = lang.get() if lang else "Türkçe"
        
        self.score_labels[0].config(text=f"Oyuncu: {self.player_score}" if lang == "Türkçe" else f"Player: {self.player_score}")
        self.score_labels[1].config(text=f"Bot: {self.bot_score}" if lang == "Türkçe" else f"Bot: {self.bot_score}")
        
        self.check_game_over()

    def check_game_over(self):
        # Check if all flags are placed
        placed_flags = sum(1 for lbl in self.flag_labels if hasattr(lbl, 'placed') and lbl.placed)
        if placed_flags == len(WORLD_REGIONS):
            lang = getattr(self.root, 'language_var', None)
            lang = lang.get() if lang else "Türkçe"
            winner = "Oyuncu" if self.player_score > self.bot_score else "Bot"
            if lang != "Türkçe":
                winner = "Player" if self.player_score > self.bot_score else "Bot"
            messagebox.showinfo("Oyun Bitti" if lang == "Türkçe" else "Game Over", 
                              f"{winner} kazandı!" if lang == "Türkçe" else f"{winner} wins!")
            self.destroy_game()

    def setup_world_map_game(self):
        self.clear_screen()
        
        map_width = 800
        map_height = 600
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_pos = (screen_width // 2) - (map_width // 2)
        y_pos = (screen_height // 2) - (map_height // 2) - 50
        self.root.geometry(f"{map_width+200}x{map_height}+{x_pos}+{y_pos}")
        self.root.resizable(False, False)

        current_theme = getattr(self.root, 'current_theme', {"bg": "#FFEBEE"})
        bg_color = current_theme["bg"]
        map_bg_color = "#B0BEC5" if bg_color == "#FFEBEE" else "#455A64"
        
        self.map_canvas = tk.Canvas(self.root, width=map_width, height=map_height, bg=map_bg_color, highlightthickness=0)
        self.map_canvas.pack(side="left", fill="both", expand=True)

        try:
            map_path = "Try/maps/world.png"
            if os.path.exists(map_path):
                map_img = Image.open(map_path).resize((map_width, map_height))
                self.map_photo = ImageTk.PhotoImage(map_img)
                self.map_canvas.create_image(0, 0, anchor="nw", image=self.map_photo)
            else:
                print(f"Warning: World map image not found: {map_path}. Using background color only.")
                self.map_photo = None
        except Exception as e:
            messagebox.showerror("Hata", f"Harita resmi yüklenirken hata: {e}")
            self.destroy_game()
            return

        self.flag_frame = tk.Frame(self.root, bg=bg_color)
        flag_frame_width = 150
        self.flag_frame.pack(side="right", fill="y", padx=10, pady=10)

        top_frame = tk.Frame(self.root, bg=bg_color)
        top_frame.place(relx=0.5, rely=0.05, anchor="n")
        
        self.turn_indicator = tk.Label(self.root, text="👤", font=("Arial", 36, "bold"), 
                                      bg="#4CAF50", fg="white", width=3, height=1,
                                      relief="raised", bd=5)
        self.turn_indicator.place(relx=0.5, rely=0.5, anchor="center")
        
        self.status_label = tk.Label(top_frame, text="", font=("Comic Sans MS", 16, "bold"), 
                                     bg="#FFF9C4" if bg_color == "#FFEBEE" else "#424242",
                                     fg="black" if bg_color == "#FFEBEE" else "white", padx=10, pady=5)
        self.status_label.pack(pady=5)
        
        score_frame = tk.Frame(self.root, bg=bg_color)
        score_frame.place(relx=0.5, rely=0.15, anchor="n")
        score_label_bg = "#FFF9C4" if bg_color == "#FFEBEE" else "#424242"
        score_label_fg = "black" if bg_color == "#FFEBEE" else "white"
        self.score_labels = [
            tk.Label(score_frame, text="Oyuncu: 0", font=("Comic Sans MS", 14), bg=score_label_bg, fg=score_label_fg, padx=10),
            tk.Label(score_frame, text="Bot: 0", font=("Comic Sans MS", 14), bg=score_label_bg, fg=score_label_fg, padx=10)
        ]
        self.score_labels[0].pack(side="left", padx=20)
        self.score_labels[1].pack(side="right", padx=20)
        self.update_turn_label()
        self.update_scores()

        self.flag_scroll_index = 0
        self.max_flags_visible = 7
        
        self.up_btn = tk.Button(self.flag_frame, text="▲", font=("Comic Sans MS", 16, "bold"), command=self.scroll_flags_up, bg="#FFF9C4")
        self.up_btn.pack(pady=(5, 0), fill="x")

        self.flags_container = tk.Frame(self.flag_frame, bg=bg_color)
        self.flags_container.pack(fill="both", expand=True, pady=5)

        self.down_btn = tk.Button(self.flag_frame, text="▼", font=("Comic Sans MS", 16, "bold"), command=self.scroll_flags_down, bg="#FFF9C4")
        self.down_btn.pack(pady=(0, 5), fill="x")

        self.load_flags()
        self.add_flag_boxes(map_width, map_height)
        
        self.back_btn_map = tk.Button(self.flag_frame, text="⬅ Geri", font=("Comic Sans MS", 14),
                                      bg="#B3E5FC" if bg_color == "#FFEBEE" else "#37474F", 
                                      fg="black" if bg_color == "#FFEBEE" else "white", 
                                      command=self.destroy_game)
        self.back_btn_map.pack(side="bottom", fill="x", pady=10, padx=5)

    def load_flags(self):
        for widget in self.flags_container.winfo_children():
            widget.destroy()
        self.flag_labels = []
        
        start = self.flag_scroll_index
        end = min(start + self.max_flags_visible, len(WORLD_REGIONS))
        
        flag_dir = "Try/flags"
        if not os.path.exists(flag_dir):
            messagebox.showerror("Hata", f"Bayrak resim dizini bulunamadı: {flag_dir}", parent=self.root)
            self.destroy_game()
            return
             
        visible_regions = WORLD_REGIONS[start:end]
        
        for i, (country, flag_file) in enumerate(visible_regions):
            flag_path = os.path.join(flag_dir, os.path.basename(flag_file))
            try:
                if not os.path.exists(flag_path):
                    lbl = tk.Label(self.flags_container, text=country[:3], font=("Arial", 10), 
                                   bg="gray", fg="white", width=10, height=3, relief="solid", bd=1)
                else:
                    img = Image.open(flag_path).resize((80, 50))
                    photo = ImageTk.PhotoImage(img)
                    lbl = tk.Label(self.flags_container, image=photo, bg=getattr(self.root, 'current_theme', {"bg": "#FFEBEE"})["bg"], bd=0, highlightthickness=0)
                    lbl.image = photo
                    
                lbl.pack(pady=5)
                lbl.country_name = country 
                lbl.placed = False  # Track if flag has been placed
                lbl.bind("<ButtonPress-1>", lambda e, w=lbl: self.start_drag(e, w))
                lbl.bind("<B1-Motion>", self.do_drag)
                lbl.bind("<ButtonRelease-1>", lambda e, w=lbl: self.drop_flag(e, w))
                self.flag_labels.append(lbl)
            except Exception as e:
                print(f"Bayrak yüklenirken hata ({flag_path}): {e}")
                lbl = tk.Label(self.flags_container, text="ERR", font=("Arial", 10), 
                              bg="red", fg="white", width=10, height=3, relief="solid", bd=1)
                lbl.pack(pady=5)
                self.flag_labels.append(lbl)

        self.up_btn.config(state="normal" if self.flag_scroll_index > 0 else "disabled")
        self.down_btn.config(state="normal" if end < len(WORLD_REGIONS) else "disabled")

    def add_flag_boxes(self, map_width, map_height):
        region_boxes_data = {
            "Kuzey Amerika": {"name": "K. Amerika", "color": "#FFF176"},
            "Güney Amerika": {"name": "G. Amerika", "color": "#FF8A65"},
            "Avrupa":        {"name": "Avrupa", "color": "#81D4FA"},
            "Afrika":        {"name": "Afrika", "color": "#A1887F"},
            "Asya":          {"name": "Asya", "color": "#AED581"},
            "Okyanusya":     {"name": "Okyanusya", "color": "#B388FF"}
        }
        self.flag_boxes = []
        self.box_region_map = {}
        
        box_width = 120
        box_height = 80
        box_pad = 15
        num_boxes = len(region_boxes_data)
        total_width = num_boxes * (box_width + box_pad) - box_pad
        start_x = (map_width - total_width) // 2
        y = map_height - box_height - 20
        
        box_index = 0
        for region, data in region_boxes_data.items():
            x = start_x + box_index * (box_width + box_pad)
            box = tk.Frame(self.map_canvas, width=box_width, height=box_height, bg=data["color"], bd=3, relief="sunken")
            self.map_canvas.create_window(x, y, anchor="nw", window=box)
            bg_color = getattr(self.root, 'current_theme', {"bg": "#FFEBEE"})["bg"]
            label_fg = "black" if bg_color == "#FFEBEE" else "white"
            label = tk.Label(box, text=data["name"], bg=data["color"], fg=label_fg, font=("Comic Sans MS", 14, "bold"))
            label.pack(expand=True, fill="both", padx=5, pady=5)
            box.region_name = region
            self.flag_boxes.append(box)
            self.box_region_map[box_index] = region
            box_index += 1

    def scroll_flags_up(self):
        if self.flag_scroll_index > 0:
            self.flag_scroll_index -= 1
            self.load_flags()

    def scroll_flags_down(self):
        if self.flag_scroll_index + self.max_flags_visible < len(WORLD_REGIONS):
            self.flag_scroll_index += 1
            self.load_flags()

    def start_drag(self, event, widget):
        if self.turn != "player": return
        if not hasattr(widget, 'country_name'): return
        
        self.drag_data["widget"] = widget
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        
        start_x_root = widget.winfo_rootx()
        start_y_root = widget.winfo_rooty()
        canvas_x_root = self.map_canvas.winfo_rootx()
        canvas_y_root = self.map_canvas.winfo_rooty()
        
        canvas_x = start_x_root - canvas_x_root
        canvas_y = start_y_root - canvas_y_root
        
        widget.pack_forget()
        widget.place(in_=self.map_canvas, x=canvas_x, y=canvas_y)
        widget.lift()

    def do_drag(self, event):
        widget = self.drag_data["widget"]
        if not widget or self.turn != "player": return

        canvas_x_root = self.map_canvas.winfo_rootx()
        canvas_y_root = self.map_canvas.winfo_rooty()
        
        new_x = event.x_root - canvas_x_root - self.drag_data["x"]
        new_y = event.y_root - canvas_y_root - self.drag_data["y"]
        
        max_x = self.map_canvas.winfo_width() - widget.winfo_width()
        max_y = self.map_canvas.winfo_height() - widget.winfo_height()
        new_x = max(0, min(new_x, max_x))
        new_y = max(0, min(new_y, max_y))

        widget.place(in_=self.map_canvas, x=new_x, y=new_y)

    def drop_flag(self, event, flag_widget):
        if self.drag_data["widget"] != flag_widget or self.turn != "player": 
            self.drag_data["widget"] = None
            return

        country = flag_widget.country_name
        region = get_region(country)
        correct_box_region = region
        dropped_on_box = False
        target_box = None
        dropped_box_region = None

        flag_center_x_root = event.x_root - self.drag_data["x"] + flag_widget.winfo_width() // 2
        flag_center_y_root = event.y_root - self.drag_data["y"] + flag_widget.winfo_height() // 2

        for box in self.flag_boxes:
            box_x1 = box.winfo_rootx()
            box_y1 = box.winfo_rooty()
            box_x2 = box_x1 + box.winfo_width()
            box_y2 = box_y1 + box.winfo_height()

            if box_x1 < flag_center_x_root < box_x2 and box_y1 < flag_center_y_root < box_y2:
                dropped_on_box = True
                target_box = box
                dropped_box_region = box.region_name
                break

        if dropped_on_box:
            self.player_moves.append((country, dropped_box_region))
            
            if self.get_bot_level() in ["orta", "zor"]:
                self.bot_memory[country] = correct_box_region
            
            if dropped_box_region == correct_box_region:
                def flash_green(step=0):
                    if step < 6:
                        color = "#A5D6A7" if step % 2 == 0 else target_box.cget("bg")
                        flag_widget.config(bg=color)
                        self.root.after(self.animation_duration, lambda: flash_green(step + 1))
                    else:
                        flag_widget.config(bg=target_box.cget("bg"))
                        flag_widget.place(in_=target_box, relx=0.5, rely=0.5, anchor="center")
                        flag_widget.placed = True
                        self.player_score += 1
                        self.update_scores()
                        self.update_turn_label()
                        self.drag_data["widget"] = None
                flash_green()
            else:
                def flash_red(step=0):
                    if step < 6:
                        color = "#FF5252" if step % 2 == 0 else getattr(self.root, 'current_theme', {"bg": "#FFEBEE"})["bg"]
                        flag_widget.config(bg=color)
                        self.root.after(self.animation_duration, lambda: flash_red(step + 1))
                    else:
                        flag_widget.place_forget()
                        flag_widget.pack(in_=self.flags_container, pady=5)
                        flag_widget.config(bg=getattr(self.root, 'current_theme', {"bg": "#FFEBEE"})["bg"])
                        self.load_flags()
                        self.turn = "bot"
                        self.update_turn_label()
                        self.root.after(1000, self.bot_move)
                        self.drag_data["widget"] = None
                flash_red()
        else:
            flag_widget.place_forget()
            flag_widget.pack(in_=self.flags_container, pady=5)
            flag_widget.config(bg=getattr(self.root, 'current_theme', {"bg": "#FFEBEE"})["bg"])
            self.load_flags()
            self.drag_data["widget"] = None

    def bot_move(self):
        self.update_turn_label()
        self.root.after(1500, self._execute_bot_move)
    
    def _execute_bot_move(self):
        available_flags = []
        for i, lbl in enumerate(self.flag_labels):
            if lbl.winfo_manager() == "pack" and not hasattr(lbl, 'placed'):
                available_flags.append(lbl)
        
        if not available_flags:
            self.check_game_over()
            return
            
        bot_level = self.get_bot_level()
        selected_flag = None
        
        if bot_level == "kolay":
            selected_flag = random.choice(available_flags)
            target_box_idx = random.randint(0, len(self.flag_boxes) - 1)
            
        elif bot_level == "orta":
            selected_flag = random.choice(available_flags)
            country = selected_flag.country_name
            correct_region = get_region(country)
            
            if country in self.bot_memory:
                remembered_region = self.bot_memory[country]
                target_box_idx = next((i for i, box in enumerate(self.flag_boxes) 
                                     if box.region_name == remembered_region), None)
                if target_box_idx is None:
                    target_box_idx = random.randint(0, len(self.flag_boxes) - 1)
            else:
                if random.random() < 0.7:
                    target_box_idx = next((i for i, box in enumerate(self.flag_boxes) 
                                         if box.region_name == correct_region), None)
                    if target_box_idx is None:
                        target_box_idx = random.randint(0, len(self.flag_boxes) - 1)
                else:
                    target_box_idx = random.randint(0, len(self.flag_boxes) - 1)
                    
        else:  # "zor"
            known_flags = [lbl for lbl in available_flags if lbl.country_name in self.bot_memory]
            
            if known_flags:
                if random.random() < 0.9:
                    selected_flag = random.choice(known_flags)
                    country = selected_flag.country_name
                    remembered_region = self.bot_memory[country]
                    target_box_idx = next((i for i, box in enumerate(self.flag_boxes) 
                                         if box.region_name == remembered_region), None)
                    if target_box_idx is None:
                        target_box_idx = random.randint(0, len(self.flag_boxes) - 1)
                else:
                    selected_flag = random.choice(available_flags)
                    target_box_idx = random.randint(0, len(self.flag_boxes) - 1)
            else:
                if self.player_moves:
                    correct_moves = [(country, region) for country, region in self.player_moves 
                                    if get_region(country) == region]
                    
                    if correct_moves:
                        selected_flag = random.choice(available_flags)
                        country = selected_flag.country_name
                        correct_region = get_region(country)
                        
                        if random.random() < 0.8:
                            target_box_idx = next((i for i, box in enumerate(self.flag_boxes) 
                                                if box.region_name == correct_region), None)
                            if target_box_idx is None:
                                target_box_idx = random.randint(0, len(self.flag_boxes) - 1)
                        else:
                            target_box_idx = random.randint(0, len(self.flag_boxes) - 1)
                    else:
                        selected_flag = random.choice(available_flags)
                        target_box_idx = random.randint(0, len(self.flag_boxes) - 1)
                else:
                    selected_flag = random.choice(available_flags)
                    target_box_idx = random.randint(0, len(self.flag_boxes) - 1)
        
        if selected_flag and 0 <= target_box_idx < len(self.flag_boxes):
            self._animate_bot_move(selected_flag, target_box_idx)
        else:
            selected_flag = random.choice(available_flags)
            target_box_idx = random.randint(0, len(self.flag_boxes) - 1)
            self._animate_bot_move(selected_flag, target_box_idx)
    
    def _animate_bot_move(self, flag_widget, box_idx):
        target_box = self.flag_boxes[box_idx]
        country = flag_widget.country_name
        correct_region = get_region(country)
        is_correct = (target_box.region_name == correct_region)
        
        flag_widget.pack_forget()
        flag_widget.place(in_=self.map_canvas, relx=0.5, rely=0.5, anchor="center")
        
        thinking_text = tk.Label(self.map_canvas, 
                               text="Düşünüyor..." if getattr(self.root, 'language_var', 'Türkçe') == "Türkçe" else "Thinking...",
                               font=("Arial", 16), bg="white")
        self.map_canvas.create_window(400, 300, window=thinking_text)
        
        def thinking_animation(step=0):
            if step < 6:
                color = "#FFD600" if step % 2 == 0 else getattr(self.root, 'current_theme', {"bg": "#FFEBEE"})["bg"]
                flag_widget.config(bg=color)
                self.root.after(250, lambda: thinking_animation(step + 1))
            else:
                self.map_canvas.delete(thinking_text)
                self._complete_bot_move(flag_widget, target_box, is_correct)
        
        thinking_animation()
    
    def _complete_bot_move(self, flag_widget, target_box, is_correct):
        if is_correct:
            def flash_green(step=0):
                if step < 6:
                    color = "#A5D6A7" if step % 2 == 0 else target_box.cget("bg")
                    flag_widget.config(bg=color)
                    self.root.after(self.animation_duration, lambda: flash_green(step + 1))
                else:
                    flag_widget.config(bg=target_box.cget("bg"))
                    flag_widget.place(in_=target_box, relx=0.5, rely=0.5, anchor="center")
                    flag_widget.placed = True
                    self.bot_score += 1
                    self.update_scores()
                    self.root.after(1000, self.bot_move)
            flash_green()
        else:
            def flash_red(step=0):
                if step < 6:
                    color = "#FF5252" if step % 2 == 0 else getattr(self.root, 'current_theme', {"bg": "#FFEBEE"})["bg"]
                    flag_widget.config(bg=color)
                    self.root.after(self.animation_duration, lambda: flash_red(step + 1))
                else:
                    flag_widget.place_forget()
                    flag_widget.pack(in_=self.flags_container, pady=5)
                    flag_widget.config(bg=getattr(self.root, 'current_theme', {"bg": "#FFEBEE"})["bg"])
                    self.load_flags()
                    self.turn = "player"
                    self.update_turn_label()
            flash_red()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def destroy_game(self):
        self.clear_screen()
        self.root.current_mapmatchgame = None
        self.root.attributes('-fullscreen', False)
        self.main_frame.pack(fill="both", expand=True)

WORLD_REGIONS = [
    # Kuzey Amerika
    ("Alaska", "Try/flags/alaska.png"),
    ("Alberta", "Try/flags/alberta.png"),
    ("Orta Amerika", "Try/flags/orta_amerika.png"),
    ("Doğu Amerika", "Try/flags/dogu_amerika.png"),
    ("Grönland", "Try/flags/gronland.png"),
    ("Kuzeybatı Toprakları", "Try/flags/kuzeybati_topraklari.png"),
    ("Ontario", "Try/flags/ontario.png"),
    ("Quebec", "Try/flags/quebec.png"),
    ("Batı Amerika", "Try/flags/bati_amerika.png"),
    # Güney Amerika
    ("Arjantin", "Try/flags/arjantin.png"),
    ("Brezilya", "Try/flags/brezilya.png"),
    ("Peru", "Try/flags/peru.png"),
    ("Venezuela", "Try/flags/venezuela.png"),
    # Avrupa
    ("Büyük Britanya", "Try/flags/britanya.png"),
    ("İzlanda", "Try/flags/izlanda.png"),
    ("Kuzey Avrupa", "Try/flags/kuzey_avrupa.png"),
    ("İskandinavya", "Try/flags/iskandinavya.png"),
    ("Güney Avrupa", "Try/flags/guney_avrupa.png"),
    ("Ukrayna", "Try/flags/ukrayna.png"),
    ("Batı Avrupa", "Try/flags/bati_avrupa.png"),
    # Afrika
    ("Kuzey Afrika", "Try/flags/kuzey_afrika.png"),
    ("Mısır", "Try/flags/misir.png"),
    ("Doğu Afrika", "Try/flags/dogu_afrika.png"),
    ("Kongo", "Try/flags/kongo.png"),
    ("Güney Afrika", "Try/flags/guney_afrika.png"),
    ("Madagaskar", "Try/flags/madagaskar.png"),
    # Asya
    ("Afganistan", "Try/flags/afganistan.png"),
    ("Çin", "Try/flags/cin.png"),
    ("Hindistan", "Try/flags/hindistan.png"),
    ("İrkutsk", "Try/flags/irkutsk.png"),
    ("Japonya", "Try/flags/japonya.png"),
    ("Kamçatka", "Try/flags/kamcatka.png"),
    ("Orta Doğu", "Try/flags/orta_dogu.png"),
    ("Moğolistan", "Try/flags/mogolistan.png"),
    ("Sibirya", "Try/flags/sibirya.png"),
    ("Siam (Tayland)", "Try/flags/siam.png"),
    ("Urallar", "Try/flags/urallar.png"),
    ("Yakutistan", "Try/flags/yakutistan.png"),
    # Okyanusya
    ("Endonezya", "Try/flags/endonezya.png"),
    ("Yeni Gine", "Try/flags/yeni_gine.png"),
    ("Doğu Avustralya", "Try/flags/dogu_avustralya.png"),
    ("Batı Avustralya", "Try/flags/bati_avustralya.png"),
]

def get_region(country):
    if country in ["Alaska", "Alberta", "Orta Amerika", "Doğu Amerika", "Grönland", "Kuzeybatı Toprakları", "Ontario", "Quebec", "Batı Amerika"]:
        return "Kuzey Amerika"
    elif country in ["Arjantin", "Brezilya", "Peru", "Venezuela"]:
        return "Güney Amerika"
    elif country in ["Büyük Britanya", "İzlanda", "Kuzey Avrupa", "İskandinavya", "Güney Avrupa", "Ukrayna", "Batı Avrupa"]:
        return "Avrupa"
    elif country in ["Kuzey Afrika", "Mısır", "Doğu Afrika", "Kongo", "Güney Afrika", "Madagaskar"]:
        return "Afrika"
    elif country in ["Afganistan", "Çin", "Hindistan", "İrkutsk", "Japonya", "Kamçatka", "Orta Doğu", "Moğolistan", "Sibirya", "Siam (Tayland)", "Urallar", "Yakutistan"]:
        return "Asya"
    elif country in ["Endonezya", "Yeni Gine", "Doğu Avustralya", "Batı Avustralya"]:
        return "Okyanusya"
    return None