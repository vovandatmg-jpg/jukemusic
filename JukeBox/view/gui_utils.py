import os
import tkinter as tk

FONT_FAMILY = "Segoe UI"

BG = "#FFF4EE"
CARD = "#FFF9F6"
PRIMARY = "#C65D4A"
SECONDARY = "#BFA79A"
TEXT = "#4B2A26"
SUBTEXT = "#8A5A52"
SUCCESS = "#6E8B5B"
ERROR = "#B14A3D"

WHITE = "#FFFFFF"
SOFT_PANEL = "#FFF8F3"

DETAIL_IMAGE_MAX_WIDTH = 180
DETAIL_IMAGE_MAX_HEIGHT = 220

PLAYLIST_IMAGE_MAX_WIDTH = 220
PLAYLIST_IMAGE_MAX_HEIGHT = 220

WELCOME_IMAGE_MAX_WIDTH = 820
WELCOME_IMAGE_MAX_HEIGHT = 620


def set_text(text_area, content):
    text_area.config(state="normal")
    text_area.delete("1.0", tk.END)
    text_area.insert("1.0", content)
    text_area.config(state="disabled")


def make_title(parent, text):
    lbl = tk.Label(
        parent,
        text=text,
        bg=BG,
        fg=TEXT,
        font=(FONT_FAMILY, 16, "bold")
    )
    lbl.pack(pady=(18, 10))
    return lbl


def make_card(parent):
    frame = tk.Frame(parent, bg=CARD, bd=1, relief="solid")
    frame.pack(padx=25, pady=10, fill="both", expand=True)
    return frame


def make_label(parent, text, bg=CARD):
    return tk.Label(parent, text=text, bg=bg, fg=TEXT)


def make_entry(parent, width=15):
    return tk.Entry(parent, width=width, relief="solid", bd=1)


def make_button(parent, text, command, width=14, bg=PRIMARY):
    return tk.Button(
        parent,
        text=text,
        command=command,
        width=width,
        bg=bg,
        fg="white",
        relief="flat",
        bd=0
    )


def make_text(parent, width=60, height=10):
    text_area = tk.Text(
        parent,
        width=width,
        height=height,
        bg=WHITE,
        fg=TEXT,
        relief="solid",
        bd=1,
        wrap="word",
        insertbackground=TEXT
    )
    text_area.config(state="disabled")
    return text_area


def make_status(parent):
    lbl = tk.Label(
        parent,
        text="",
        bg=BG,
        fg=SUBTEXT,
        font=(FONT_FAMILY, 10, "italic")
    )
    lbl.pack(pady=(6, 14))
    return lbl


def set_status(label, text, ok=None):
    if ok is True:
        color = SUCCESS
    elif ok is False:
        color = ERROR
    else:
        color = SUBTEXT

    label.configure(text=text, fg=color)


def load_png_image(image_path, max_width=180, max_height=220):
    if not image_path or not os.path.exists(image_path):
        return None

    try:
        image = tk.PhotoImage(file=image_path)

        width = image.width()
        height = image.height()

        scale_x = (width + max_width - 1) // max_width if width > max_width else 1
        scale_y = (height + max_height - 1) // max_height if height > max_height else 1
        scale = max(scale_x, scale_y)

        if scale > 1:
            image = image.subsample(scale, scale)

        return image

    except tk.TclError:
        return None


def clear_image_label(
    label,
    message="No image",
    bg=WHITE,
    fg=TEXT,
    font=(FONT_FAMILY, 10, "italic")
):
    label.configure(
        text=message,
        image="",
        bg=bg,
        fg=fg,
        font=font
    )
    label.image = None


def set_image_label(label, photo, bg=WHITE):
    label.configure(image=photo, text="", bg=bg)
    label.image = photo


def init_audio_system(pygame_module):
    if pygame_module is None:
        return False

    try:
        if pygame_module.mixer.get_init() is None:
            pygame_module.mixer.init()
        return True
    except Exception:
        return False