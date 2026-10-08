import tkinter as tk
from tkinter import messagebox
from config import (
    COLOR_ACCENT, COLOR_ACCENT_DARK, COLOR_BG, COLOR_CARD, COLOR_TEXT, COLOR_MUTED,
    FONT_SUBTITLE, FONT_LABEL, FONT_BUTTON, HoverButton, verify_login
)


class SignInPage(tk.Frame):
    """Halaman login mandiri tanpa sidebar/menu utama."""
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        tk.Label(self, text="PERPUSKITA", bg=COLOR_BG, fg=COLOR_ACCENT,
                 font=("Segoe UI", 24, "bold")).pack(anchor="nw", padx=42, pady=(28, 0))
        tk.Label(self, text="DIGITAL LIBRARY", bg=COLOR_BG, fg=COLOR_MUTED,
                 font=("Segoe UI", 8, "bold")).pack(anchor="nw", padx=47, pady=(2, 0))

        card = tk.Frame(self, bg=COLOR_CARD, padx=28, pady=28,
                        highlightthickness=1, highlightbackground="#dfe3e8")
        card.place(relx=.5, rely=.53, anchor="center")
        card.grid_columnconfigure(0, weight=1)
        card.grid_columnconfigure(1, weight=1)

        title = tk.Frame(card, bg=COLOR_CARD, width=390, height=310)
        title.grid(row=0, column=0, rowspan=6, padx=(8, 35), sticky="nsew")
        title.grid_propagate(False)
        tk.Label(title, text="Selamat Datang\nkembali!", bg=COLOR_CARD, fg=COLOR_TEXT,
                 font=("Segoe UI", 25, "bold"), justify="left").pack(anchor="w")
        tk.Label(title, text="Masuk untuk mengakses koleksi,\npeminjaman, dan layanan digital\nPERPUSKITA.",
                 bg=COLOR_CARD, fg=COLOR_MUTED, font=FONT_SUBTITLE, justify="left").pack(anchor="w", pady=(12, 0))

        form = tk.Frame(card, bg=COLOR_CARD)
        form.grid(row=0, column=1, sticky="nsew", padx=(0, 8))
        tk.Label(form, text="Sign In", bg=COLOR_CARD, fg=COLOR_TEXT,
                 font=("Segoe UI", 22, "bold")).pack(anchor="w")
        tk.Label(form, text="Masukkan akun kamu untuk melanjutkan.", bg=COLOR_CARD, fg=COLOR_MUTED,
                 font=FONT_SUBTITLE).pack(anchor="w", pady=(4, 25))

        tk.Label(form, text="Username", bg=COLOR_CARD, fg=COLOR_TEXT, font=FONT_LABEL).pack(anchor="w")
        self.entry_username = tk.Entry(form, font=FONT_LABEL, width=31, relief="solid", bd=1)
        self.entry_username.pack(fill="x", pady=(6, 16), ipady=8)

        tk.Label(form, text="Password", bg=COLOR_CARD, fg=COLOR_TEXT, font=FONT_LABEL).pack(anchor="w")
        self.entry_password = tk.Entry(form, font=FONT_LABEL, width=31, relief="solid", bd=1, show="*")
        self.entry_password.pack(fill="x", pady=(6, 22), ipady=8)
        self.entry_password.bind("<Return>", lambda e: self.handle_signin())

        HoverButton(form, bg_normal=COLOR_ACCENT, bg_hover=COLOR_ACCENT_DARK, text="Masuk",
                    fg="white", font=FONT_BUTTON, bd=0, cursor="hand2",
                    command=self.handle_signin).pack(fill="x", ipady=11)

        bottom = tk.Frame(form, bg=COLOR_CARD)
        bottom.pack(pady=(18, 0))
        tk.Label(bottom, text="Belum punya akun?", bg=COLOR_CARD, fg=COLOR_MUTED, font=FONT_LABEL).pack(side="left")
        link = tk.Label(bottom, text=" Daftar di sini", bg=COLOR_CARD, fg=COLOR_ACCENT,
                         font=("Segoe UI", 10, "bold", "underline"), cursor="hand2")
        link.pack(side="left")
        link.bind("<Button-1>", lambda e: controller.show_frame("SignUpPage"))

        home = tk.Label(self, text="← Kembali ke Beranda", bg=COLOR_BG, fg=COLOR_ACCENT,
                        font=("Segoe UI", 10, "bold"), cursor="hand2")
        home.place(relx=.5, rely=.93, anchor="center")
        home.bind("<Button-1>", lambda e: controller.show_frame("HomePage"))

    def handle_signin(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get()
        if not username or not password:
            messagebox.showwarning("Data belum lengkap", "Mohon isi username dan password.")
            return
        success, message = verify_login(username, password)
        if success:
            self.controller.set_current_user(username)
            self.clear_fields()
            self.controller.show_frame("HomePage")
        else:
            messagebox.showerror("Login Gagal", message)

    def clear_fields(self):
        self.entry_username.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)

    def on_show(self):
        self.clear_fields()
        self.entry_username.focus_set()
