import tkinter as tk

BG = "#FFF4EE"
CARD = "#FFF9F6"
PRIMARY = "#C65D4A"
SECONDARY = "#BFA79A"
TEXT = "#4B2A26"
SUBTEXT = "#8A5A52"
SUCCESS = "#6E8B5B"
ERROR = "#B14A3D"


def set_text(text_area, content):
    text_area.config(state="normal")

    text_area.delete("1.0", tk.END)
    text_area.insert("1.0", content)

    text_area.config(state="disabled")


def normalise_track_number(track_number):
    track_number = track_number.strip()

    if track_number == "":
        return None, "Please enter a track number"
    if not track_number.isdigit():
        return None, "Track number must be numeric"
    if len(track_number) > 2:
        return None, "Track number must be 1 or 2 digits"

    return track_number.zfill(2), None


def make_title(parent, text):
    lbl = tk.Label(
        parent,
        text=text,
        bg=BG,
        fg=TEXT,
        font=("Segoe UI", 16, "bold")
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
        bg="white",
        fg=TEXT,
        relief="solid",
        bd=1,
        wrap="word"
    )

    text_area.config(state="disabled")
    return text_area


def make_status(parent):
    lbl = tk.Label(
        parent,
        text="",
        bg=BG,
        fg=SUBTEXT,
        font=("Segoe UI", 10, "italic")
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