import tkinter as tk
import tkinter.scrolledtext as tkst
import os

try:
    import pygame
except ImportError:
    pygame = None

import font_manager as fonts
from controller.track_controller import TrackController

from gui_utils import (
    BG, CARD, TEXT, SECONDARY,
    set_text,
    make_title, make_card,
    make_label, make_entry,
    make_button, make_text,
    make_status, set_status
)


class TrackViewer:
    def __init__(self, window):
        self.window = window
        self.window.geometry("980x660")
        self.window.title("View Tracks")
        self.window.configure(bg=BG)

        fonts.configure()

        self.controller = TrackController()
        self.current_track = None

        self.audio_ready = False
        if pygame is not None:
            try:
                pygame.mixer.init()
                self.audio_ready = True
            except pygame.error:
                self.audio_ready = False

        make_title(window, "View Tracks")

        main_frame = make_card(window)

        left_frame = tk.Frame(main_frame, bg=CARD)
        left_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        right_frame = tk.Frame(main_frame, bg=CARD)
        right_frame.pack(side="right", fill="y", padx=(0, 20), pady=20)

        top_controls = tk.Frame(left_frame, bg=CARD)
        top_controls.pack(anchor="w", pady=(0, 12))

        make_button(top_controls, "List All Tracks", self.list_tracks_clicked, 16).grid(
            row=0, column=0, padx=(0, 10), pady=5
        )

        make_label(top_controls, "Enter Track Number").grid(
            row=0, column=1, padx=5, pady=5
        )

        self.input_txt = make_entry(top_controls, 8)
        self.input_txt.grid(row=0, column=2, padx=5, pady=5)

        make_button(top_controls, "View Track Details", self.view_tracks_clicked, 14).grid(
            row=0, column=3, padx=10, pady=5
        )

        search_frame = tk.Frame(left_frame, bg=CARD)
        search_frame.pack(anchor="w", pady=(0, 12))

        make_label(search_frame, "Search track or artist").grid(
            row=0, column=0, padx=(0, 10), pady=5
        )

        self.search_txt = make_entry(search_frame, 22)
        self.search_txt.grid(row=0, column=1, padx=5, pady=5)

        make_button(search_frame, "Search", self.search_tracks_clicked, 12).grid(
            row=0, column=2, padx=10, pady=5
        )

        filter_frame = tk.Frame(left_frame, bg=CARD)
        filter_frame.pack(anchor="w", pady=(0, 15))

        make_label(filter_frame, "Filter by artist").grid(
            row=0, column=0, padx=(0, 10), pady=5
        )

        artists = self.controller.get_artists()

        self.artist_var = tk.StringVar(window)
        self.artist_var.set(artists[0] if artists else "")

        self.artist_menu = tk.OptionMenu(filter_frame, self.artist_var, *artists)
        self.artist_menu.config(width=18, bg="white", fg=TEXT, highlightthickness=0)
        self.artist_menu["menu"].config(bg="white", fg=TEXT)
        self.artist_menu.grid(row=0, column=1, padx=5, pady=5)

        make_button(filter_frame, "Filter", self.filter_tracks_clicked, 12).grid(
            row=0, column=2, padx=10, pady=5
        )

        self.list_txt = tkst.ScrolledText(
            left_frame,
            width=58,
            height=16,
            wrap="none",
            bg="white",
            fg=TEXT,
            relief="solid",
            bd=1,
            insertbackground=TEXT
        )
        self.list_txt.pack(fill="both", expand=True)
        self.list_txt.config(state="disabled")

        details_title = tk.Label(
            right_frame,
            text="Track Details",
            bg=CARD,
            fg=TEXT,
            font=("Segoe UI", 12, "bold")
        )
        details_title.pack(pady=(5, 12))

        image_frame = tk.Frame(right_frame, bg=CARD, bd=1, relief="solid")
        image_frame.pack(pady=(0, 10))

        self.image_lbl = tk.Label(
            image_frame,
            text="No image",
            bg="white",
            fg=TEXT
        )
        self.image_lbl.pack(padx=6, pady=6)

        self.track_txt = make_text(right_frame, 28, 10)
        self.track_txt.pack()

        audio_frame = tk.Frame(right_frame, bg=CARD)
        audio_frame.pack(pady=(10, 0))

        make_button(audio_frame, "Play", self.play_track_clicked, 10).grid(
            row=0, column=0, padx=6
        )

        make_button(audio_frame, "Stop", self.stop_track_clicked, 10, bg=SECONDARY).grid(
            row=0, column=1, padx=6
        )

        self.status_lbl = make_status(window)

        self.list_tracks_clicked()

        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

    def load_png_image(self, image_path, max_width=180, max_height=220):
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

    def clear_image(self, message="No image"):
        self.image_lbl.configure(text=message, image="", bg="white")
        self.image_lbl.image = None

    def clear_track_details(self):
        set_text(self.track_txt, "")
        self.clear_image()
        self.current_track = None

    def show_track_image(self, image_path):
        photo = self.load_png_image(image_path)

        if photo is None:
            self.clear_image("No image available")
            return

        self.image_lbl.configure(image=photo, text="", bg="white")
        self.image_lbl.image = photo

    def update_track_details(self, track_number):
        details = self.controller.get_track_details_text(track_number)
        set_text(self.track_txt, details)

    def view_tracks_clicked(self):
        result = self.controller.view_track(self.input_txt.get())

        if not result["success"]:
            set_text(self.track_txt, result["details"])
            self.clear_image()
            set_status(self.status_lbl, result["status"], ok=result["ok"])
            self.input_txt.delete(0, tk.END)
            return

        self.current_track = result["track_number"]
        set_text(self.track_txt, result["details"])
        self.show_track_image(result["image_path"])
        set_status(self.status_lbl, result["status"], ok=result["ok"])

        self.input_txt.delete(0, tk.END)

    def play_track_clicked(self):
        if pygame is None or not self.audio_ready:
            set_status(self.status_lbl, "Audio system could not start", ok=False)
            return

        if self.current_track is None:
            set_status(self.status_lbl, "Please view a track first", ok=False)
            return

        audio_path = self.controller.get_audio_path(self.current_track)

        if audio_path is None:
            set_status(self.status_lbl, "Audio file not found", ok=False)
            return

        try:
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()

            details = self.controller.register_play(self.current_track)
            set_text(self.track_txt, details)

            set_status(self.status_lbl, "Playing track", ok=True)

        except pygame.error:
            set_status(self.status_lbl, "Cannot play this audio file", ok=False)

    def stop_track_clicked(self):
        if pygame is None or not self.audio_ready:
            set_status(self.status_lbl, "Audio system could not start", ok=False)
            return

        pygame.mixer.music.stop()
        set_status(self.status_lbl, "Playback stopped", ok=True)

    def list_tracks_clicked(self):
        result = self.controller.list_tracks()

        self.clear_track_details()
        set_text(self.list_txt, result["text"])
        set_status(self.status_lbl, result["status"], ok=result["ok"])

    def search_tracks_clicked(self):
        result = self.controller.search_tracks(self.search_txt.get())

        self.clear_track_details()
        set_text(self.list_txt, result["text"])
        set_status(self.status_lbl, result["status"], ok=result["ok"])

    def filter_tracks_clicked(self):
        result = self.controller.filter_tracks(self.artist_var.get())

        self.clear_track_details()
        set_text(self.list_txt, result["text"])
        set_status(self.status_lbl, result["status"], ok=result["ok"])

    def on_close(self):
        if pygame is not None and self.audio_ready:
            pygame.mixer.music.stop()
            pygame.mixer.quit()

        self.window.destroy()


if __name__ == "__main__":
    window = tk.Tk()
    TrackViewer(window)
    window.mainloop()