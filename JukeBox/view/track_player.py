import os
import tkinter as tk

try:
    import pygame
except ImportError:
    pygame = None

from view import font_manager as fonts
from view.gui_utils import (
    BG, CARD, PRIMARY, TEXT, SUBTEXT,
    WHITE, WELCOME_IMAGE_MAX_WIDTH, WELCOME_IMAGE_MAX_HEIGHT,
    FONT_FAMILY, load_png_image
)
from view.view_tracks import TrackViewer
from view.playlist_view import PlaylistView
from view.rating_update_view import RatingUpdateView


TAB_BG = "#F3E3DB"
TAB_ACTIVE = "#FFFFFF"


def build_tab(parent, text, command):
    tab_frame = tk.Frame(parent, bg=CARD)

    button = tk.Button(
        tab_frame,
        text=text,
        command=command,
        font=(FONT_FAMILY, 11, "bold"),
        bg=TAB_BG,
        fg=TEXT,
        relief="flat",
        bd=0,
        padx=24,
        pady=12
    )
    button.pack()

    indicator = tk.Frame(tab_frame, bg=CARD, height=4)
    indicator.pack(fill="x", pady=(6, 0))

    return {"frame": tab_frame, "button": button, "indicator": indicator}


def style_tab(tab, active=False):
    if active:
        tab["button"].config(bg=TAB_ACTIVE)
        tab["indicator"].config(bg=PRIMARY)
    else:
        tab["button"].config(bg=TAB_BG)
        tab["indicator"].config(bg=CARD)


def main():
    window = tk.Tk()
    window.geometry("1280x800")
    window.title("JukeBox")
    window.configure(bg=BG)

    fonts.configure()
    app_shell = tk.Frame(window, bg=BG)

    title_lbl = tk.Label(
        app_shell,
        text="JukeBox Music Player",
        bg=BG,
        fg=TEXT,
        font=(FONT_FAMILY, 16, "bold")
    )
    title_lbl.pack(pady=(18, 10))

    nav_card = tk.Frame(app_shell, bg=CARD, bd=1, relief="solid")
    nav_card.pack(fill="x", padx=24, pady=(0, 10))

    tab_bar = tk.Frame(nav_card, bg=CARD)
    tab_bar.pack(anchor="w", padx=16, pady=14)

    content_host = tk.Frame(app_shell, bg=BG)
    content_host.pack(fill="both", expand=True)

    view_page = tk.Frame(content_host, bg=BG)
    playlist_page = tk.Frame(content_host, bg=BG)
    update_page = tk.Frame(content_host, bg=BG)

    for page in [view_page, playlist_page, update_page]:
        page.place(relx=0, rely=0, relwidth=1, relheight=1)

    track_viewer = TrackViewer(view_page)
    playlist_viewer = PlaylistView(playlist_page)
    RatingUpdateView(update_page)

    tabs = {}

    def show_tab(name):
        if name == "view":
            view_page.tkraise()
        elif name == "playlist":
            playlist_page.tkraise()
        else:
            update_page.tkraise()

        for key in tabs:
            style_tab(tabs[key], active=(key == name))

    tabs["view"] = build_tab(tab_bar, "View Tracks", lambda: show_tab("view"))
    tabs["playlist"] = build_tab(tab_bar, "Create Track List", lambda: show_tab("playlist"))
    tabs["update"] = build_tab(tab_bar, "Update Rating", lambda: show_tab("update"))

    tabs["view"]["frame"].pack(side="left", padx=(0, 12))
    tabs["playlist"]["frame"].pack(side="left", padx=(0, 12))
    tabs["update"]["frame"].pack(side="left")

    welcome_page = tk.Frame(window, bg=BG)

    center_frame = tk.Frame(welcome_page, bg=BG)
    center_frame.place(relx=0.5, rely=0.42, anchor="center")

    welcome_title = tk.Label(
        center_frame,
        text="JukeBox Music Player",
        bg=BG,
        fg=TEXT,
        font=(FONT_FAMILY, 20, "bold")
    )
    welcome_title.pack(pady=(0, 8))

    welcome_subtitle = tk.Label(
        center_frame,
        text="Choose an option and enjoy your music collection",
        bg=BG,
        fg=SUBTEXT,
        font=(FONT_FAMILY, 10)
    )
    welcome_subtitle.pack(pady=(0, 12))

    def open_main_app():
        welcome_page.pack_forget()
        app_shell.pack(fill="both", expand=True)
        show_tab("view")

    enter_button = tk.Button(
        center_frame,
        text="Enter JukeBox",
        width=18,
        bg=PRIMARY,
        fg="white",
        font=(FONT_FAMILY, 10, "bold"),
        relief="flat",
        bd=0,
        padx=8,
        pady=8,
        command=open_main_app
    )
    enter_button.pack(pady=(0, 14))

    image_frame = tk.Frame(center_frame, bg=WHITE, bd=1, relief="solid", padx=6, pady=6)
    image_frame.pack()

    base_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
    image_path = os.path.join(base_dir, "img", "anhnen.png")

    welcome_image = load_png_image(
        image_path,
        max_width=WELCOME_IMAGE_MAX_WIDTH,
        max_height=WELCOME_IMAGE_MAX_HEIGHT
    )

    if welcome_image is not None:
        image_label = tk.Label(image_frame, image=welcome_image, bg=WHITE)
        image_label.image = welcome_image
        image_label.pack()
    else:
        image_label = tk.Label(
            image_frame,
            text="Image not found",
            bg=WHITE,
            fg=TEXT,
            font=(FONT_FAMILY, 12),
            width=60,
            height=15
        )
        image_label.pack()

    def on_app_close():
        track_viewer.on_close()
        playlist_viewer.on_close()

        if pygame is not None and pygame.mixer.get_init() is not None:
            pygame.mixer.quit()

        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_app_close)

    welcome_page.pack(fill="both", expand=True)
    window.mainloop()


if __name__ == "__main__":
    main()