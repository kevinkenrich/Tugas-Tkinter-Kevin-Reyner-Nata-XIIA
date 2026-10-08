import tkinter as tk
import json
import os
import hashlib

APP_WIDTH = 1280
APP_HEIGHT = 720
USERS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.json")
BOOKS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "books.json")
BORROWINGS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "borrowings.json")

# Palet baru: merah sebagai identitas utama 📖 PERPUSKITA
COLOR_PRIMARY = "#17191d"
COLOR_PRIMARY_2 = "#22262d"
COLOR_ACCENT = "#dc2626"
COLOR_ACCENT_DARK = "#b91c1c"
COLOR_ACCENT_SOFT = "#fef2f2"
COLOR_BG = "#f5f6f8"
COLOR_CARD = "#ffffff"
COLOR_TEXT = "#17191d"
COLOR_MUTED = "#737983"
COLOR_SUCCESS = "#16a34a"
COLOR_DANGER = "#dc2626"
COLOR_BORDER = "#e5e7eb"
COLOR_GOLD = "#d89b22"

FONT_TITLE = ("Segoe UI", 28, "bold")
FONT_SUBTITLE = ("Segoe UI", 12)
FONT_NAV = ("Segoe UI", 10, "bold")
FONT_CARD_TITLE = ("Segoe UI", 14, "bold")
FONT_CARD_BODY = ("Segoe UI", 10)
FONT_LABEL = ("Segoe UI", 10)
FONT_BUTTON = ("Segoe UI", 10, "bold")
FONT_BRAND = ("Segoe UI", 19, "bold")

ARTIKEL_PERPUSTAKAAN = [
    {"judul": "5 Rekomendasi Buku Fiksi Bulan Ini", "ringkasan": "Temukan lima judul fiksi terbaru yang tersedia di rak perpustakaan kami, mulai dari novel misteri hingga fantasi epik.", "kategori": "Rekomendasi"},
    {"judul": "Tips Efektif Membaca Cepat", "ringkasan": "Pelajari teknik speed reading sederhana agar kamu bisa menyelesaikan lebih banyak buku tanpa kehilangan pemahaman isi bacaan.", "kategori": "Tips & Trik"},
    {"judul": "Jadwal Kunjungan & Jam Operasional", "ringkasan": "Perpustakaan buka setiap hari Senin-Sabtu pukul 08.00-16.00. Cek jadwal lengkap dan agenda kegiatan bulanan di sini.", "kategori": "Pengumuman"},
    {"judul": "Cara Meminjam Buku Secara Online", "ringkasan": "Setelah login, anggota dapat memesan buku secara online dan mengambilnya langsung di meja sirkulasi perpustakaan.", "kategori": "Panduan"},
]

DEFAULT_BOOKS = [
    {"id": 1, "judul": "Laskar Pelangi", "penulis": "Andrea Hirata", "tahun": "2005", "stok": 5},
    {"id": 2, "judul": "Bumi", "penulis": "Tere Liye", "tahun": "2014", "stok": 3},
    {"id": 3, "judul": "Atomic Habits", "penulis": "James Clear", "tahun": "2018", "stok": 4},
]


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def load_users() -> dict:
    if not os.path.exists(USERS_FILE): return {}
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f: return json.load(f)
    except (json.JSONDecodeError, OSError): return {}


def save_users(users: dict) -> None:
    with open(USERS_FILE, "w", encoding="utf-8") as f: json.dump(users, f, indent=2, ensure_ascii=False)


def register_user(username: str, email: str, password: str) -> tuple[bool, str]:
    users = load_users()
    if username in users: return False, "Username sudah terdaftar. Silakan gunakan username lain."
    for data in users.values():
        if data.get("email", "").lower() == email.lower(): return False, "Email sudah terdaftar. Silakan gunakan email lain."
    users[username] = {"email": email, "password": hash_password(password)}
    save_users(users)
    return True, "Pendaftaran berhasil! Silakan login."


def verify_login(username: str, password: str) -> tuple[bool, str]:
    users = load_users()
    if username not in users: return False, "Username tidak ditemukan."
    if users[username]["password"] != hash_password(password): return False, "Password salah."
    return True, "Login berhasil!"


def delete_user(username: str) -> tuple[bool, str]:
    users = load_users()
    if username not in users: return False, "User tidak ditemukan."
    del users[username]; save_users(users); return True, "User berhasil dihapus."


def update_user(old_username: str, new_username: str, email: str, new_password: str = "") -> tuple[bool, str]:
    users = load_users()
    if old_username not in users: return False, "User tidak ditemukan."
    if new_username != old_username and new_username in users: return False, "Username baru sudah dipakai user lain."
    for uname, data in users.items():
        if uname != old_username and data.get("email", "").lower() == email.lower(): return False, "Email sudah dipakai user lain."
    record = users.pop(old_username); record["email"] = email
    if new_password: record["password"] = hash_password(new_password)
    users[new_username] = record; save_users(users); return True, "User berhasil diperbarui."


def load_books() -> list:
    if not os.path.exists(BOOKS_FILE): save_books(DEFAULT_BOOKS); return list(DEFAULT_BOOKS)
    try:
        with open(BOOKS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f); return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError): return []


def save_books(books: list) -> None:
    with open(BOOKS_FILE, "w", encoding="utf-8") as f: json.dump(books, f, indent=2, ensure_ascii=False)


def get_next_book_id(books: list) -> int:
    return 1 if not books else max(int(b.get("id", 0)) for b in books) + 1


def add_book(judul: str, penulis: str, tahun: str, stok: int) -> tuple[bool, str]:
    books = load_books(); books.append({"id": get_next_book_id(books), "judul": judul, "penulis": penulis, "tahun": tahun, "stok": stok}); save_books(books); return True, "Buku berhasil ditambahkan."


def update_book(book_id: int, judul: str, penulis: str, tahun: str, stok: int) -> tuple[bool, str]:
    books = load_books()
    for b in books:
        if int(b.get("id", 0)) == int(book_id):
            b.update({"judul": judul, "penulis": penulis, "tahun": tahun, "stok": stok}); save_books(books); return True, "Buku berhasil diperbarui."
    return False, "Buku tidak ditemukan."


def delete_book(book_id: int) -> tuple[bool, str]:
    books = load_books(); borrowings = load_borrowings()
    if any(int(p.get("book_id", 0)) == int(book_id) and p.get("status") == "Dipinjam" for p in borrowings): return False, "Buku tidak bisa dihapus karena sedang dipinjam."
    filtered = [b for b in books if int(b.get("id", 0)) != int(book_id)]
    if len(filtered) == len(books): return False, "Buku tidak ditemukan."
    save_books(filtered); return True, "Buku berhasil dihapus."


def find_book(book_id: int):
    for b in load_books():
        if int(b.get("id", 0)) == int(book_id): return b
    return None


def adjust_book_stock(book_id: int, delta: int) -> bool:
    books = load_books()
    for b in books:
        if int(b.get("id", 0)) == int(book_id):
            b["stok"] = int(b.get("stok", 0)) + delta
            if b["stok"] < 0: return False
            save_books(books); return True
    return False


def load_borrowings() -> list:
    if not os.path.exists(BORROWINGS_FILE): return []
    try:
        with open(BORROWINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f); return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError): return []


def save_borrowings(borrowings: list) -> None:
    with open(BORROWINGS_FILE, "w", encoding="utf-8") as f: json.dump(borrowings, f, indent=2, ensure_ascii=False)


def get_next_borrowing_id(borrowings: list) -> int:
    return 1 if not borrowings else max(int(p.get("id", 0)) for p in borrowings) + 1


def add_borrowing(username: str, book_id: int, tanggal_pinjam: str, tanggal_kembali: str) -> tuple[bool, str]:
    users = load_users()
    if username not in users: return False, "Username tidak terdaftar."
    book = find_book(book_id)
    if book is None: return False, "Buku tidak ditemukan."
    if int(book.get("stok", 0)) <= 0: return False, "Stok buku habis."
    borrowings = load_borrowings()
    borrowings.append({"id": get_next_borrowing_id(borrowings), "username": username, "book_id": int(book_id), "judul": book.get("judul", ""), "tanggal_pinjam": tanggal_pinjam, "tanggal_kembali": tanggal_kembali, "status": "Dipinjam"})
    save_borrowings(borrowings); adjust_book_stock(book_id, -1); return True, "Peminjaman berhasil ditambahkan."


def update_borrowing(borrow_id: int, username: str, book_id: int, tanggal_pinjam: str, tanggal_kembali: str, status: str) -> tuple[bool, str]:
    borrowings = load_borrowings(); target = next((p for p in borrowings if int(p.get("id", 0)) == int(borrow_id)), None)
    if target is None: return False, "Data peminjaman tidak ditemukan."
    old_status = target.get("status"); old_book_id = int(target.get("book_id", 0)); new_book_id = int(book_id)
    if old_status == "Dipinjam" and status == "Kembali" and old_book_id == new_book_id: adjust_book_stock(old_book_id, 1)
    elif old_status == "Kembali" and status == "Dipinjam":
        book = find_book(new_book_id)
        if book is None: return False, "Buku tidak ditemukan."
        if int(book.get("stok", 0)) <= 0: return False, "Stok buku habis."
        adjust_book_stock(new_book_id, -1)
    elif old_book_id != new_book_id and old_status == "Dipinjam" and status == "Dipinjam":
        book = find_book(new_book_id)
        if book is None: return False, "Buku tidak ditemukan."
        if int(book.get("stok", 0)) <= 0: return False, "Stok buku habis."
        adjust_book_stock(old_book_id, 1); adjust_book_stock(new_book_id, -1)
    target.update({"username": username, "book_id": new_book_id, "tanggal_pinjam": tanggal_pinjam, "tanggal_kembali": tanggal_kembali, "status": status})
    book_now = find_book(new_book_id)
    if book_now is not None: target["judul"] = book_now.get("judul", target.get("judul", ""))
    save_borrowings(borrowings); return True, "Data peminjaman berhasil diperbarui."


def delete_borrowing(borrow_id: int) -> tuple[bool, str]:
    borrowings = load_borrowings(); target = next((p for p in borrowings if int(p.get("id", 0)) == int(borrow_id)), None)
    if target is None: return False, "Data peminjaman tidak ditemukan."
    if target.get("status") == "Dipinjam": adjust_book_stock(int(target.get("book_id", 0)), 1)
    save_borrowings([p for p in borrowings if int(p.get("id", 0)) != int(borrow_id)]); return True, "Data peminjaman berhasil dihapus."


class HoverButton(tk.Button):
    def __init__(self, master, bg_normal, bg_hover, **kwargs):
        super().__init__(master, bg=bg_normal, activebackground=bg_hover, **kwargs)
        self.bg_normal, self.bg_hover = bg_normal, bg_hover
        self.bind("<Enter>", lambda e: self.config(bg=self.bg_hover))
        self.bind("<Leave>", lambda e: self.config(bg=self.bg_normal))


def add_hover_card(card, hover="#fef2f2"):
    """Menambahkan efek hover lembut pada kartu."""
    normal = card.cget("bg")
    def enter(event):
        card.configure(bg=hover)
        for child in card.winfo_children():
            try:
                if child.cget("bg") == normal:
                    child.configure(bg=hover)
            except tk.TclError:
                pass
    def leave(event):
        card.configure(bg=normal)
        for child in card.winfo_children():
            try:
                if child.cget("bg") == hover:
                    child.configure(bg=normal)
            except tk.TclError:
                pass
    card.bind("<Enter>", enter)
    card.bind("<Leave>", leave)


def build_sidebar(parent, controller, active="home"):
    """Sidebar kiri ala dashboard pada referensi pengguna."""
    sidebar = tk.Frame(parent, bg=COLOR_PRIMARY, width=235)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    brand = tk.Frame(sidebar, bg=COLOR_PRIMARY)
    brand.pack(fill="x", padx=18, pady=(24, 28))
    tk.Label(brand, text="📖 PERPUSKITA", bg=COLOR_PRIMARY, fg=COLOR_ACCENT,
             font=FONT_BRAND).pack(anchor="w")
    tk.Label(brand, text="DIGITAL LIBRARY", bg=COLOR_PRIMARY, fg="#aeb4bd",
             font=("Segoe UI", 8, "bold")).pack(anchor="w", pady=(3, 0))

    menu = tk.Frame(sidebar, bg=COLOR_PRIMARY); menu.pack(fill="x", padx=10)
    # Menu dibuat dinamis berdasarkan status login.
    # Saat belum login, tampilkan tombol Masuk dan Daftar.
    # Setelah login, tampilkan menu pengelolaan perpustakaan.
    items = [
        ("dashboard", "▦", "Dashboard", "DashboardPage"),
        ("home", "⌂", "Beranda", "HomePage"),
    ] if controller.current_user else [
        ("home", "⌂", "Beranda", "HomePage"),
    ]
    if controller.current_user:
        items += [
            ("books", "▤", "Koleksi Buku", "BookManagementPage"),
            ("borrow", "↔", "Peminjaman", "BorrowingManagementPage"),
            ("users", "♙", "Pengguna", "UsersManagementPage"),
        ]
    else:
        items += [
            ("signin", "→", "Masuk", "SignInPage"),
            ("signup", "+", "Daftar", "SignUpPage"),
        ]
    for key, icon, label, page in items:
        bg = COLOR_ACCENT if key == active else COLOR_PRIMARY
        hover = COLOR_ACCENT_DARK if key == active else COLOR_PRIMARY_2
        b = HoverButton(menu, bg_normal=bg, bg_hover=hover, text=f"  {icon}   {label}",
                        fg="white", font=FONT_NAV, bd=0, relief="flat", anchor="w",
                        padx=16, pady=12, cursor="hand2",
                        command=lambda p=page: controller.show_frame(p))
        b.pack(fill="x", pady=3)

    spacer = tk.Frame(sidebar, bg=COLOR_PRIMARY); spacer.pack(fill="both", expand=True)
    user_box = tk.Frame(sidebar, bg=COLOR_PRIMARY_2)
    user_box.pack(fill="x", padx=12, pady=12)
    user_label = tk.Label(
        user_box,
        text=(f"●  {controller.current_user}" if controller.current_user else "○  Tamu"),
        bg=COLOR_PRIMARY_2, fg="#e8eaed", font=FONT_NAV
    )
    user_label.pack(anchor="w", padx=12, pady=(10, 8))

    if controller.current_user:
        HoverButton(
            user_box, bg_normal=COLOR_ACCENT, bg_hover=COLOR_ACCENT_DARK,
            text="Keluar", fg="white", font=FONT_NAV, bd=0, cursor="hand2",
            command=controller.logout
        ).pack(fill="x", padx=8, pady=(0, 8), ipady=5)
    else:
        HoverButton(
            user_box, bg_normal=COLOR_ACCENT, bg_hover=COLOR_ACCENT_DARK,
            text="Masuk", fg="white", font=FONT_NAV, bd=0, cursor="hand2",
            command=lambda: controller.show_frame("SignInPage")
        ).pack(fill="x", padx=8, pady=(0, 6), ipady=5)
        HoverButton(
            user_box, bg_normal=COLOR_ACCENT, bg_hover=COLOR_ACCENT_DARK,
            text="Daftar Akun", fg="white", font=FONT_NAV, bd=0, cursor="hand2",
            command=lambda: controller.show_frame("SignUpPage")
        ).pack(fill="x", padx=8, pady=(0, 8), ipady=5)
    parent._sidebar = sidebar
    parent._sidebar_user_label = user_label
    return user_label


def refresh_sidebar(parent, controller, active="home"):
    """Bangun ulang sidebar tanpa mengubah posisinya.

    Sidebar selalu ditempatkan di paling kiri, di depan area konten.
    Ini penting karena halaman management sudah memiliki widget konten
    yang lebih dulu dibuat; jika sidebar langsung di-pack ulang tanpa
    opsi `before`, Tkinter dapat menaruhnya di sebelah kanan.
    """
    old = getattr(parent, "_sidebar", None)
    if old is not None and old.winfo_exists():
        old.destroy()

    user_label = build_sidebar(parent, controller, active)
    sidebar = getattr(parent, "_sidebar", None)
    if sidebar is not None and sidebar.winfo_exists():
        # Cari widget konten pertama dan letakkan sidebar sebelum widget itu.
        siblings = parent.pack_slaves()
        before = next((w for w in siblings if w is not sidebar), None)
        sidebar.pack_forget()
        if before is not None:
            sidebar.pack(side="left", fill="y", before=before)
        else:
            sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
    return user_label


def set_user_label(label, controller):
    if controller.current_user:
        label.config(text=f"●  {controller.current_user}")
    else:
        label.config(text="○  Tamu")





def apply_theme(root, dark=False):
    """Compatibility function; this version uses a fixed light theme."""
    return None
