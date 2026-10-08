import tkinter as tk
from config import (
    COLOR_BG, COLOR_CARD, COLOR_TEXT, COLOR_MUTED, COLOR_ACCENT, COLOR_ACCENT_DARK,
    COLOR_PRIMARY, COLOR_PRIMARY_2, FONT_TITLE, FONT_SUBTITLE, FONT_NAV,
    FONT_CARD_TITLE, FONT_CARD_BODY, HoverButton, refresh_sidebar, set_user_label,
    load_books, load_users, load_borrowings, add_hover_card
)


class DashboardPage(tk.Frame):
    """Dashboard yang dapat discroll secara vertikal agar tidak terpotong."""

    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller
        self.user_label = None
        self._wheel_bound = False
        self.build_content()

    def build_content(self):
        # Area utama di sebelah kanan sidebar.
        self.content = tk.Frame(self, bg=COLOR_BG)
        self.content.pack(side="left", fill="both", expand=True)

        # Canvas + scrollbar membuat seluruh dashboard bisa digeser ke bawah.
        self.dashboard_canvas = tk.Canvas(
            self.content, bg=COLOR_BG, highlightthickness=0, bd=0
        )
        self.v_scroll = tk.Scrollbar(
            self.content, orient="vertical", command=self.dashboard_canvas.yview
        )
        self.dashboard_canvas.configure(yscrollcommand=self.v_scroll.set)

        self.v_scroll.pack(side="right", fill="y")
        self.dashboard_canvas.pack(side="left", fill="both", expand=True)

        self.scroll_frame = tk.Frame(self.dashboard_canvas, bg=COLOR_BG)
        self.window_id = self.dashboard_canvas.create_window(
            (0, 0), window=self.scroll_frame, anchor="nw"
        )

        self.scroll_frame.bind("<Configure>", self._update_scrollregion)
        self.dashboard_canvas.bind("<Configure>", self._resize_scroll_frame)
        self.dashboard_canvas.bind("<Enter>", self._bind_mousewheel)
        self.dashboard_canvas.bind("<Leave>", self._unbind_mousewheel)

        # Isi dashboard dibuat di dalam frame yang dapat discroll.
        content = self.scroll_frame

        top = tk.Frame(content, bg=COLOR_BG)
        top.pack(fill="x", padx=32, pady=(26, 12))
        left = tk.Frame(top, bg=COLOR_BG)
        left.pack(side="left", fill="x", expand=True)
        tk.Label(left, text="Dashboard", bg=COLOR_BG, fg=COLOR_TEXT,
                 font=("Segoe UI", 28, "bold")).pack(anchor="w")
        tk.Label(left, text="Ringkasan aktivitas perpustakaan digital.", bg=COLOR_BG,
                 fg=COLOR_MUTED, font=FONT_SUBTITLE).pack(anchor="w", pady=(3, 0))

        right = tk.Frame(top, bg=COLOR_BG)
        right.pack(side="right")
        tk.Label(right, text="▣", bg=COLOR_BG, fg=COLOR_TEXT,
                 font=("Segoe UI", 18)).pack(side="left", padx=(0, 8))
        tk.Label(right, text="Perpustakaan Digital", bg=COLOR_BG, fg=COLOR_MUTED,
                 font=("Segoe UI", 9)).pack(side="left")

        self.stats = tk.Frame(content, bg=COLOR_BG)
        self.stats.pack(fill="x", padx=32, pady=(0, 18))
        for i in range(4):
            self.stats.grid_columnconfigure(i, weight=1, uniform="stats")

        self.stat_cards = []
        cards = [
            ("Total Buku", "0", "koleksi tersedia", "▣", COLOR_ACCENT),
            ("Stok Tersedia", "0", "buku siap dipinjam", "□", "#16a34a"),
            ("Sedang Dipinjam", "0", "buku dipinjam saat ini", "↔", "#f59e0b"),
            ("Total Anggota", "0", "anggota terdaftar", "♟", "#7c3aed"),
        ]
        for i, (title, value, desc, icon, icon_bg) in enumerate(cards):
            card = tk.Frame(self.stats, bg=COLOR_CARD, highlightbackground="#e5e7eb",
                            highlightthickness=1)
            card.grid(row=0, column=i, sticky="nsew", padx=(0 if i == 0 else 7, 0))
            self.stat_cards.append((card, title))
            icon_box = tk.Frame(card, bg=icon_bg, width=58, height=58)
            icon_box.pack(side="left", padx=16, pady=16)
            icon_box.pack_propagate(False)
            tk.Label(icon_box, text=icon, bg=icon_bg, fg="white",
                     font=("Segoe UI", 22, "bold")).pack(expand=True)
            info = tk.Frame(card, bg=COLOR_CARD)
            info.pack(side="left", fill="both", expand=True, pady=13)
            tk.Label(info, text=title, bg=COLOR_CARD, fg=COLOR_MUTED,
                     font=("Segoe UI", 9, "bold")).pack(anchor="w")
            val = tk.Label(info, text=value, bg=COLOR_CARD, fg=COLOR_TEXT,
                           font=("Segoe UI", 22, "bold"))
            val.pack(anchor="w")
            tk.Label(info, text=desc, bg=COLOR_CARD, fg=COLOR_MUTED,
                     font=("Segoe UI", 8)).pack(anchor="w")
            card._value_label = val
            add_hover_card(card)

        middle = tk.Frame(content, bg=COLOR_BG)
        middle.pack(fill="x", padx=32, pady=(0, 18))
        middle.grid_columnconfigure(0, weight=3)
        middle.grid_columnconfigure(1, weight=2)

        collection = tk.Frame(middle, bg=COLOR_CARD, highlightbackground="#e5e7eb", highlightthickness=1)
        collection.grid(row=0, column=0, sticky="nsew", padx=(0, 9))
        tk.Label(collection, text="Koleksi Unggulan", bg=COLOR_CARD, fg=COLOR_TEXT,
                 font=FONT_CARD_TITLE).pack(anchor="w", padx=18, pady=(16, 12))
        self.book_area = tk.Frame(collection, bg=COLOR_CARD)
        self.book_area.pack(fill="x", padx=14, pady=(0, 14))

        overview = tk.Frame(middle, bg=COLOR_CARD, highlightbackground="#e5e7eb", highlightthickness=1)
        overview.grid(row=0, column=1, sticky="nsew", padx=(9, 0))
        tk.Label(overview, text="Perpustakaan dalam satu tampilan", bg=COLOR_CARD, fg=COLOR_TEXT,
                 font=FONT_CARD_TITLE).pack(anchor="w", padx=20, pady=(18, 5))
        tk.Label(overview, text="Visual, ringkas, dan mudah dipantau.", bg=COLOR_CARD, fg=COLOR_MUTED,
                 font=FONT_CARD_BODY).pack(anchor="w", padx=20)
        canvas = tk.Canvas(overview, bg=COLOR_CARD, highlightthickness=0, height=180)
        canvas.pack(fill="x", padx=15, pady=8)
        canvas.create_oval(25, 30, 155, 160, outline="#fecaca", width=2)
        canvas.create_oval(50, 45, 125, 120, fill="#fee2e2", outline="")
        canvas.create_rectangle(90, 90, 150, 160, fill=COLOR_ACCENT, outline="")
        canvas.create_rectangle(185, 90, 245, 160, fill="#16a34a", outline="")
        canvas.create_rectangle(152, 132, 183, 140, fill=COLOR_TEXT, outline="")
        canvas.create_text(120, 125, text="BOOK", fill="white", font=("Segoe UI", 9, "bold"))
        canvas.create_text(215, 125, text="READ", fill="white", font=("Segoe UI", 9, "bold"))
        status = tk.Frame(overview, bg="#fafafa", highlightbackground="#e5e7eb", highlightthickness=1)
        status.pack(fill="x", padx=20, pady=(0, 18), ipady=9)
        tk.Label(status, text="●", bg="#fafafa", fg="#16a34a", font=("Segoe UI", 10)).pack(side="left", padx=(12, 6))
        tk.Label(status, text="Sistem siap digunakan", bg="#fafafa", fg=COLOR_TEXT,
                 font=("Segoe UI", 9)).pack(side="left")
        tk.Label(status, text="PERPUSKITA", bg="#fafafa", fg=COLOR_ACCENT,
                 font=("Segoe UI", 9, "bold")).pack(side="right", padx=12)

        bottom = tk.Frame(content, bg=COLOR_BG)
        bottom.pack(fill="x", padx=32, pady=(0, 30))
        recent = tk.Frame(bottom, bg=COLOR_CARD, highlightbackground="#e5e7eb", highlightthickness=1)
        recent.pack(fill="x")
        tk.Label(recent, text="Peminjaman Terbaru", bg=COLOR_CARD, fg=COLOR_TEXT,
                 font=FONT_CARD_TITLE).pack(anchor="w", padx=18, pady=(14, 9))
        self.table = tk.Frame(recent, bg=COLOR_CARD)
        self.table.pack(fill="x", padx=12, pady=(0, 12))

    def _update_scrollregion(self, event=None):
        self.dashboard_canvas.configure(scrollregion=self.dashboard_canvas.bbox("all"))

    def _resize_scroll_frame(self, event):
        # Lebar mengikuti jendela agar tidak ada area kosong horizontal.
        self.dashboard_canvas.itemconfigure(self.window_id, width=event.width)

    def _bind_mousewheel(self, event=None):
        if not self._wheel_bound:
            self.dashboard_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
            self.dashboard_canvas.bind_all("<Button-4>", self._on_mousewheel_linux)
            self.dashboard_canvas.bind_all("<Button-5>", self._on_mousewheel_linux)
            self._wheel_bound = True

    def _unbind_mousewheel(self, event=None):
        # Tetap aktif selama pointer berada di area dashboard/scrollbar; dilepas
        # ketika pindah ke halaman lain supaya tidak mengganggu halaman lain.
        if self._wheel_bound:
            self.dashboard_canvas.unbind_all("<MouseWheel>")
            self.dashboard_canvas.unbind_all("<Button-4>")
            self.dashboard_canvas.unbind_all("<Button-5>")
            self._wheel_bound = False

    def _on_mousewheel(self, event):
        if event.delta:
            self.dashboard_canvas.yview_scroll(int(-event.delta / 120), "units")

    def _on_mousewheel_linux(self, event):
        self.dashboard_canvas.yview_scroll(-1 if event.num == 4 else 1, "units")

    def refresh_data(self):
        books = load_books()
        users = load_users()
        borrowings = load_borrowings()
        total_books = len(books)
        stock = sum(int(b.get("stok", 0)) for b in books)
        active = sum(1 for b in borrowings if b.get("status") == "Dipinjam")
        members = len(users)
        values = [total_books, stock, active, members]
        for (card, _), value in zip(self.stat_cards, values):
            card._value_label.config(text=str(value))

        for child in self.book_area.winfo_children():
            child.destroy()
        featured = books[:5]
        for i in range(5):
            self.book_area.grid_columnconfigure(i, weight=1, uniform="books")
        for i, book in enumerate(featured):
            card = tk.Frame(self.book_area, bg="#fafafa", highlightbackground="#e5e7eb", highlightthickness=1)
            card.grid(row=0, column=i, sticky="nsew", padx=4)
            cover = tk.Frame(card, bg=COLOR_ACCENT, width=72, height=92)
            cover.pack(pady=(10, 7)); cover.pack_propagate(False)
            tk.Label(cover, text="BOOK", bg=COLOR_ACCENT, fg="white",
                     font=("Segoe UI", 10, "bold")).pack(expand=True)
            tk.Label(card, text=book.get("judul", "-"), bg="#fafafa", fg=COLOR_TEXT,
                     font=("Segoe UI", 9, "bold"), wraplength=115).pack(anchor="w", padx=8)
            tk.Label(card, text=book.get("penulis", "-"), bg="#fafafa", fg=COLOR_MUTED,
                     font=("Segoe UI", 8), wraplength=115).pack(anchor="w", padx=8, pady=(2, 0))
            tk.Label(card, text=f"Stok: {book.get('stok', 0)}", bg="#fafafa", fg=COLOR_MUTED,
                     font=("Segoe UI", 8)).pack(anchor="w", padx=8, pady=(4, 9))

        for child in self.table.winfo_children():
            child.destroy()
        headers = ["Anggota", "Buku", "Tanggal Pinjam", "Tanggal Kembali", "Status"]
        widths = [16, 24, 18, 18, 14]
        for col, (header, width) in enumerate(zip(headers, widths)):
            tk.Label(self.table, text=header, bg=COLOR_ACCENT, fg="white",
                     font=("Segoe UI", 9, "bold"), anchor="w", width=width,
                     padx=8, pady=7).grid(row=0, column=col, sticky="ew")
        for r, item in enumerate(borrowings[-4:][::-1], start=1):
            book = next((b for b in books if int(b.get("id", 0)) == int(item.get("book_id", 0))), None)
            title = book.get("judul") if book else item.get("judul", "-")
            vals = [item.get("username", "-"), title, item.get("tanggal_pinjam", "-"),
                    item.get("tanggal_kembali", "-"), item.get("status", "-")]
            for c, val in enumerate(vals):
                bg = "#ffffff" if r % 2 else "#fafafa"
                tk.Label(self.table, text=val, bg=bg, fg=COLOR_TEXT,
                         font=("Segoe UI", 8), anchor="w", width=widths[c],
                         padx=8, pady=6).grid(row=r, column=c, sticky="ew")

        self.after_idle(self._update_scrollregion)

    def on_show(self):
        self.user_label = refresh_sidebar(self, self.controller, "dashboard")
        set_user_label(self.user_label, self.controller)
        self.refresh_data()
        self.after_idle(self._update_scrollregion)
