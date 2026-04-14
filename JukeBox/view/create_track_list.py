import tkinter as tk
import font_manager as fonts

from controller.playlist_controller import PlaylistController

from gui_utils import (
    BG, CARD, SECONDARY,
    set_text,
    make_title, make_card, make_label, make_entry,
    make_button, make_text, make_status, set_status
)


class CreateTrackList:
    def __init__(self, window):
        self.window = window
        self.window.geometry("820x520")
        self.window.title("Create Track List")
        self.window.configure(bg=BG)

        fonts.configure()

        self.controller = PlaylistController()

        make_title(window, "Create Track List")

        main_frame = make_card(window)

        input_frame = tk.Frame(main_frame, bg=CARD)
        input_frame.pack(pady=(25, 15))

        make_label(input_frame, "Enter track number:").grid(row=0, column=0, padx=10, pady=10)

        self.track_input = make_entry(input_frame, 15)
        self.track_input.grid(row=0, column=1, padx=10, pady=10)

        make_button(input_frame, "Add Track", self.add_track_clicked, 14).grid(
            row=0, column=2, padx=10, pady=10
        )

        button_frame = tk.Frame(main_frame, bg=CARD)
        button_frame.pack(pady=(0, 15))

        make_button(
            button_frame,
            "Play Playlist",
            self.play_playlist_clicked,
            16
        ).pack(side="left", padx=8)

        make_button(
            button_frame,
            "Reset Playlist",
            self.reset_playlist_clicked,
            16,
            bg=SECONDARY
        ).pack(side="left", padx=8)

        make_label(main_frame, "Playlist", bg=CARD).pack(pady=(5, 10))

        self.list_txt = make_text(main_frame, 72, 14)
        self.list_txt.pack(padx=20, pady=10)

        self.status_lbl = make_status(window)
        set_status(self.status_lbl, "Ready")

    def add_track_clicked(self):
        result = self.controller.add_track(self.track_input.get())
        set_text(self.list_txt, result["text"])
        set_status(self.status_lbl, result["status"], ok=result["ok"])
        self.track_input.delete(0, tk.END)

    def play_playlist_clicked(self):
        result = self.controller.play_playlist()
        set_text(self.list_txt, result["text"])
        set_status(self.status_lbl, result["status"], ok=result["ok"])

    def reset_playlist_clicked(self):
        result = self.controller.reset_playlist()
        set_text(self.list_txt, result["text"])
        set_status(self.status_lbl, result["status"], ok=result["ok"])


if __name__ == "__main__":
    window = tk.Tk()
    CreateTrackList(window)
    window.mainloop()