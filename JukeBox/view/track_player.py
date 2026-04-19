import tkinter as tk

try:
    import pygame
except ImportError:
    pygame = None

from view import font_manager as fonts
from view.gui_utils import BG, CARD, PRIMARY, TEXT, make_title
from view.view_tracks import TrackViewer
from view.create_track_list import CreateTrackList
from view.update_tracks import UpdateTracks


TAB_BG = "#F3E3DB"
TAB_HOVER = "#EAD7CE"
TAB_ACTIVE = "#FFFFFF"
TAB_BORDER = "#E1CCC1"


def build_tab(parent, text, command):
    tab_frame = tk.Frame(parent, bg=CARD)

    button = tk.Button(
        tab_frame,
        text=text,
        command=command,
        font=("Segoe UI", 11, "bold"),
        bg=TAB_BG,
        fg=TEXT,
        activebackground=TAB_HOVER,
        activeforeground=TEXT,
        relief="flat",
        bd=0,
        padx=24,
        pady=12,
        cursor="hand2",
        highlightthickness=1,
        highlightbackground=TAB_BORDER,
        highlightcolor=TAB_BORDER
    )
    button.pack()

    indicator = tk.Frame(tab_frame, bg=CARD, height=4)
    indicator.pack(fill="x", pady=(6, 0))

    return {
        "frame": tab_frame,
        "button": button,
        "indicator": indicator
    }


def style_tab(tab, active=False, hover=False):
    if active:
        tab["button"].config(
            bg=TAB_ACTIVE,
            fg=TEXT,
            activebackground=TAB_ACTIVE,
            activeforeground=TEXT
        )
        tab["indicator"].config(bg=PRIMARY)
    else:
        bg = TAB_HOVER if hover else TAB_BG
        tab["button"].config(
            bg=bg,
            fg=TEXT,
            activebackground=TAB_HOVER,
            activeforeground=TEXT
        )
        tab["indicator"].config(bg=CARD)


def main():
    window = tk.Tk()
    window.geometry("1280x800")
    window.minsize(1180, 760)
    window.title("JukeBox")
    window.configure(bg=BG)

    fonts.configure()
    make_title(window, "JukeBox Music Player")

    nav_card = tk.Frame(
        window,
        bg=CARD,
        bd=1,
        relief="solid"
    )
    nav_card.pack(fill="x", padx=24, pady=(0, 10))

    tab_bar = tk.Frame(nav_card, bg=CARD)
    tab_bar.pack(anchor="w", padx=16, pady=14)

    content_host = tk.Frame(window, bg=BG)
    content_host.pack(fill="both", expand=True)

    pages = {
        "view": tk.Frame(content_host, bg=BG),
        "playlist": tk.Frame(content_host, bg=BG),
        "update": tk.Frame(content_host, bg=BG)
    }

    for page in pages.values():
        page.place(relx=0, rely=0, relwidth=1, relheight=1)

    track_viewer = TrackViewer(pages["view"])
    playlist_viewer = CreateTrackList(pages["playlist"])
    update_viewer = UpdateTracks(pages["update"])

    tabs = {}
    active_tab = {"name": "view"}

    def show_tab(name):
        active_tab["name"] = name
        pages[name].tkraise()

        for key, tab in tabs.items():
            style_tab(tab, active=(key == name))

    tabs["view"] = build_tab(tab_bar, "View Tracks", lambda: show_tab("view"))
    tabs["playlist"] = build_tab(tab_bar, "Create Track List", lambda: show_tab("playlist"))
    tabs["update"] = build_tab(tab_bar, "Update Rating", lambda: show_tab("update"))

    tabs["view"]["frame"].pack(side="left", padx=(0, 12))
    tabs["playlist"]["frame"].pack(side="left", padx=(0, 12))
    tabs["update"]["frame"].pack(side="left")

    def bind_hover(tab_name):
        button = tabs[tab_name]["button"]

        def on_enter(event):
            if active_tab["name"] != tab_name:
                style_tab(tabs[tab_name], active=False, hover=True)

        def on_leave(event):
            if active_tab["name"] != tab_name:
                style_tab(tabs[tab_name], active=False, hover=False)

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    bind_hover("view")
    bind_hover("playlist")
    bind_hover("update")

    def on_app_close():
        track_viewer.on_close()
        playlist_viewer.on_close()

        if pygame is not None and pygame.mixer.get_init() is not None:
            pygame.mixer.quit()

        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_app_close)

    show_tab("view")
    window.mainloop()


if __name__ == "__main__":
    main()