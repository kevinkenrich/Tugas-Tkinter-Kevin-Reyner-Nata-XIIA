import tkinter as tk
from tkinter import messagebox
from config import (
    COLOR_ACCENT, COLOR_ACCENT_DARK, COLOR_BG, COLOR_CARD, COLOR_TEXT, COLOR_MUTED,
    FONT_SUBTITLE, FONT_LABEL, FONT_BUTTON, HoverButton, register_user
)


class SignUpPage(tk.Frame):
    """Halaman pendaftaran mandiri tanpa sidebar/menu utama."""
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        tk.Label(self, text="PERPUSKITA", bg=COLOR_BG, fg=COLOR_ACCENT,
                 font=("Segoe UI", 22, "bold")).pack(anchor="nw", padx=42, pady=(24, 0))
        tk.Label(self, text="DIGITAL LIBRARY", bg=COLOR_BG, fg=COLOR_MUTED,
                 font=("Segoe UI", 8, "bold")).pack(anchor="nw", padx=47, pady=(2, 0))

        card = tk.Frame(self, bg=COLOR_CARD, padx=28, pady=24,
                        highlightthickness=1, highlightbackground="#dfe3e8")
        card.place(relx=.5, rely=.53, anchor="center")
        card.grid_columnconfigure(0, weight=1)
        card.grid_columnconfigure(1, weight=1)

        title = tk.Frame(card, bg=COLOR_CARD, width=300, height=350)
        title.grid(row=0, column=0, rowspan=8, padx=(8, 32), sticky="nsew")
        title.grid_propagate(False)
        tk.Label(title, text="📖", bg=COLOR_CARD, fg=COLOR_ACCENT,
                 font=("Segoe UI Emoji", 52)).pack(anchor="w", pady=(20, 2))
        tk.Label(title, text="Bangun akunmu\ndi PERPUSKITA", bg=COLOR_CARD, fg=COLOR_TEXT,
                 font=("Segoe UI", 23, "bold"), justify="left").pack(anchor="w")
        tk.Label(title, text="Daftar untuk mengakses koleksi buku,\npeminjaman, dan layanan digital\nperpustakaan.",
                 bg=COLOR_CARD, fg=COLOR_MUTED, font=FONT_SUBTITLE, justify="left").pack(anchor="w", pady=(12, 0))

        form = tk.Frame(card, bg=COLOR_CARD)
        form.grid(row=0, column=1, sticky="nsew", padx=(0, 8))
        tk.Label(form, text="Sign Up", bg=COLOR_CARD, fg=COLOR_TEXT,
                 font=("Segoe UI", 22, "bold")).pack(anchor="w")
        tk.Label(form, text="Isi data berikut untuk membuat akun baru.", bg=COLOR_CARD, fg=COLOR_MUTED,
                 font=FONT_SUBTITLE).pack(anchor="w", pady=(4, 18))

        fields = [("Username", "entry_username", False), ("Email", "entry_email", False),
                  ("Password", "entry_password", True), ("Konfirmasi Password", "entry_confirm", True)]
        for label, name, secret in fields:
            tk.Label(form, text=label, bg=COLOR_CARD, fg=COLOR_TEXT, font=FONT_LABEL).pack(anchor="w")
            ent = tk.Entry(form, font=FONT_LABEL, width=31, relief="solid", bd=1, show="*" if secret else "")
            ent.pack(fill="x", pady=(5, 8 if label != "Konfirmasi Password" else 16), ipady=6)
            setattr(self, name, ent)

        HoverButton(form, bg_normal=COLOR_ACCENT, bg_hover=COLOR_ACCENT_DARK, text="Daftar Sekarang",
                    fg="white", font=FONT_BUTTON, bd=0, cursor="hand2",
                    command=self.handle_signup).pack(fill="x", ipady=10)

        bottom = tk.Frame(form, bg=COLOR_CARD)
        bottom.pack(pady=(15, 0))
        tk.Label(bottom, text="Sudah punya akun?", bg=COLOR_CARD, fg=COLOR_MUTED, font=FONT_LABEL).pack(side="left")
        link = tk.Label(bottom, text=" Masuk di sini", bg=COLOR_CARD, fg=COLOR_ACCENT,
                         font=("Segoe UI", 10, "bold", "underline"), cursor="hand2")
        link.pack(side="left")
        link.bind("<Button-1>", lambda e: controller.show_frame("SignInPage"))

        home = tk.Label(self, text="← Kembali ke Beranda", bg=COLOR_BG, fg=COLOR_ACCENT,
                        font=("Segoe UI", 10, "bold"), cursor="hand2")
        home.place(relx=.5, rely=.95, anchor="center")
        home.bind("<Button-1>", lambda e: controller.show_frame("HomePage"))

    def handle_signup(self):
        username = self.entry_username.get().strip()
        email = self.entry_email.get().strip()
        password = self.entry_password.get()
        confirm = self.entry_confirm.get()
        if not username or not email or not password or not confirm:
            messagebox.showwarning("Data belum lengkap", "Mohon isi semua kolom.")
            return
        if "@" not in email or "." not in email:
            messagebox.showwarning("Email tidak valid", "Masukkan format email yang benar.")
            return
        if len(password) < 6:
            messagebox.showwarning("Password terlalu pendek", "Password minimal 6 karakter.")
            return
        if password != confirm:
            messagebox.showwarning("Password tidak cocok", "Konfirmasi password harus sama dengan password.")
            return
        success, message = register_user(username, email, password)
        if success:
            messagebox.showinfo("Berhasil", message)
            self.clear_fields()
            self.controller.show_frame("SignInPage")
        else:
            messagebox.showerror("Gagal Mendaftar", message)

    def clear_fields(self):
        for e in (self.entry_username, self.entry_email, self.entry_password, self.entry_confirm):
            e.delete(0, tk.END)

    def on_show(self):
        self.clear_fields()
        self.entry_username.focus_set()
