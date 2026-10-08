import tkinter as tk
from config import (COLOR_PRIMARY, COLOR_ACCENT, COLOR_ACCENT_DARK, COLOR_BG, COLOR_CARD,
    COLOR_TEXT, COLOR_MUTED, FONT_TITLE, FONT_SUBTITLE, FONT_NAV, FONT_CARD_TITLE,
    FONT_CARD_BODY, ARTIKEL_PERPUSTAKAAN, HoverButton, build_sidebar, refresh_sidebar, set_user_label, add_hover_card)

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller
        self.user_label = build_sidebar(self, controller, "home")

        main = tk.Frame(self, bg=COLOR_BG); main.pack(side="left", fill="both", expand=True)
        top = tk.Frame(main, bg=COLOR_CARD, height=62); top.pack(fill="x"); top.pack_propagate(False)
        tk.Label(top, text="Beranda", bg=COLOR_CARD, fg=COLOR_TEXT, font=("Segoe UI", 18, "bold")).pack(side="left", padx=28)
        self.status = tk.Label(top, text="SMART LIBRARY SYSTEM", bg=COLOR_CARD, fg=COLOR_ACCENT, font=("Segoe UI", 9, "bold"))
        self.status.pack(side="right", padx=28)

        hero = tk.Frame(main, bg=COLOR_ACCENT, height=205); hero.pack(fill="x", padx=24, pady=(22, 0)); hero.pack_propagate(False)
        left = tk.Frame(hero, bg=COLOR_ACCENT); left.pack(side="left", fill="both", expand=True, padx=30)
        tk.Label(left, text="Kelola Perpustakaan\nDengan Lebih Mudah.", bg=COLOR_ACCENT, fg="white", font=FONT_TITLE, justify="left").pack(anchor="w", pady=(30, 6))
        tk.Label(left, text="Cari koleksi, kelola peminjaman, dan pantau aktivitas perpustakaan\ndalam satu tampilan yang rapi dan modern.", bg=COLOR_ACCENT, fg="#fee2e2", font=FONT_SUBTITLE, justify="left").pack(anchor="w")

        self.canvas = tk.Canvas(hero, width=300, height=180, bg=COLOR_ACCENT, highlightthickness=0); self.canvas.pack(side="right", padx=22)
        self.book_y = 0; self.book_dir = 1
        self.canvas.create_oval(30, 18, 270, 155, outline="#ff8c8c", width=2)
        self.book1 = self.canvas.create_rectangle(70, 55, 145, 140, fill="#20242a", outline="")
        self.canvas.create_text(107, 100, text="PERPUS", fill="white", font=("Segoe UI", 10, "bold"))
        self.book2 = self.canvas.create_rectangle(145, 48, 220, 133, fill="#ffffff", outline="")
        self.canvas.create_text(182, 90, text="READ", fill=COLOR_ACCENT, font=("Segoe UI", 10, "bold"))
        self.canvas.create_line(125, 148, 165, 148, fill="#17191d", width=5)
        self.animate_books()

        stats = tk.Frame(main, bg=COLOR_BG); stats.pack(fill="x", padx=24, pady=20)
        cards = [("KOLEKSI", "load_books"), ("ANGGOTA", "load_users"), ("DIPINJAM", "load_borrowings")]
        from config import load_books, load_users, load_borrowings
        funcs = {"load_books": load_books, "load_users": load_users, "load_borrowings": load_borrowings}
        for i, (title, key) in enumerate(cards):
            c = tk.Frame(stats, bg=COLOR_CARD, highlightthickness=1, highlightbackground="#e7e8eb", padx=18, pady=13)
            c.grid(row=0, column=i, sticky="ew", padx=(0 if i == 0 else 8, 0)); stats.grid_columnconfigure(i, weight=1)
            value = len(funcs[key]())
            tk.Label(c, text=str(value), bg=COLOR_CARD, fg=COLOR_TEXT, font=("Segoe UI", 20, "bold")).pack(anchor="w")
            tk.Label(c, text=title, bg=COLOR_CARD, fg=COLOR_MUTED, font=("Segoe UI", 8, "bold")).pack(anchor="w")

        content = tk.Frame(main, bg=COLOR_BG); content.pack(fill="both", expand=True, padx=24, pady=(0, 18))
        tk.Label(content, text="Informasi & Rekomendasi", bg=COLOR_BG, fg=COLOR_TEXT, font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=(0, 6))
        tk.Label(content, text="Update singkat untuk membantu aktivitas membaca dan pengelolaan perpustakaan.", bg=COLOR_BG, fg=COLOR_MUTED, font=FONT_CARD_BODY).pack(anchor="w", pady=(0, 8))
        grid = tk.Frame(content, bg=COLOR_BG); grid.pack(fill="both", expand=True); grid.grid_columnconfigure(0, weight=1); grid.grid_columnconfigure(1, weight=1)
        for idx, artikel in enumerate(ARTIKEL_PERPUSTAKAAN): self._build_article_card(grid, artikel, *divmod(idx, 2))

    def _build_article_card(self, parent, artikel, row, col):
        card = tk.Frame(parent, bg=COLOR_CARD, highlightthickness=1, highlightbackground="#e7e8eb", padx=18, pady=13)
        card.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")
        add_hover_card(card)
        tk.Label(card, text=artikel["kategori"].upper(), bg=COLOR_ACCENT, fg="white", font=("Segoe UI", 8, "bold"), padx=8, pady=3).pack(anchor="w")
        tk.Label(card, text=artikel["judul"], bg=COLOR_CARD, fg=COLOR_TEXT, font=FONT_CARD_TITLE, wraplength=430, justify="left").pack(anchor="w", pady=(8, 3))
        tk.Label(card, text=artikel["ringkasan"], bg=COLOR_CARD, fg=COLOR_MUTED, font=FONT_CARD_BODY, wraplength=430, justify="left").pack(anchor="w")

    def animate_books(self):
        if not self.winfo_exists(): return
        self.book_y += self.book_dir * 0.5
        if self.book_y > 5 or self.book_y < -5: self.book_dir *= -1
        self.canvas.coords(self.book1, 70, 55 + self.book_y, 145, 140 + self.book_y)
        self.canvas.coords(self.book2, 145, 48 - self.book_y, 220, 133 - self.book_y)
        self.canvas.after(45, self.animate_books)

    def on_show(self):
        self.user_label = refresh_sidebar(self, self.controller, "home")
        set_user_label(self.user_label, self.controller)
