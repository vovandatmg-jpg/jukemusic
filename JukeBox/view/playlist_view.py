import tkinter as tk

try:
    import pygame
except ImportError:
    pygame = None

from view import font_manager as fonts
from controller.playlist_controller import PlaylistController

from view.gui_utils import (
    CARD, TEXT, SECONDARY, WHITE, SOFT_PANEL,
    PLAYLIST_IMAGE_MAX_WIDTH, PLAYLIST_IMAGE_MAX_HEIGHT,
    FONT_FAMILY,
    set_text,
    make_title, make_card, make_label, make_entry,
    make_button, make_text, make_status, set_status,
    load_png_image, clear_image_label, set_image_label,
    init_audio_system
)


class PlaylistView:
    def __init__(self, window):
        self.window = window

        fonts.configure()

        self.controller = PlaylistController()

        self.after_id = None
        self.audio_ready = init_audio_system(pygame)

        make_title(window, "Create Track List")

        main_frame = make_card(window)

        left_frame = tk.Frame(main_frame, bg=CARD)
        left_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        right_frame = tk.Frame(main_frame, bg=CARD, width=320)
        right_frame.pack(side="right", fill="y", padx=(0, 20), pady=20)
        right_frame.pack_propagate(False)

        input_frame = tk.Frame(left_frame, bg=CARD)
        input_frame.pack(anchor="w", pady=(0, 15))

        make_label(input_frame, "Enter track number:").grid(row=0, column=0, padx=10, pady=10)

        self.track_input = make_entry(input_frame, 15)
        self.track_input.grid(row=0, column=1, padx=10, pady=10)

        make_button(input_frame, "Add Track", self.add_track_clicked, 14).grid(
            row=0, column=2, padx=10, pady=10
        )

        button_frame = tk.Frame(left_frame, bg=CARD)
        button_frame.pack(anchor="w", pady=(0, 15))

        make_button(
            button_frame,
            "Play Playlist",
            self.play_playlist_clicked,
            16
        ).pack(side="left", padx=(0, 8))

        make_button(
            button_frame,
            "Stop",
            self.stop_playlist_clicked,
            12,
            bg=SECONDARY
        ).pack(side="left", padx=8)

        make_button(
            button_frame,
            "Reset Playlist",
            self.reset_playlist_clicked,
            16,
            bg=SECONDARY
        ).pack(side="left", padx=8)

        make_label(left_frame, "Playlist", bg=CARD).pack(anchor="w", pady=(5, 10))

        self.list_txt = make_text(left_frame, 68, 16)
        self.list_txt.pack(fill="both", expand=True)

        now_title = tk.Label(
            right_frame,
            text="Now Playing",
            bg=CARD,
            fg=TEXT,
            font=(FONT_FAMILY, 15, "bold")
        )
        now_title.pack(pady=(4, 14))

        now_card = tk.Frame(
            right_frame,
            bg=WHITE,
            bd=1,
            relief="solid"
        )
        now_card.pack(fill="both", expand=True)

        image_outer = tk.Frame(
            now_card,
            bg=SOFT_PANEL,
            bd=1,
            relief="solid",
            width=240,
            height=240
        )
        image_outer.pack(padx=22, pady=(22, 14))
        image_outer.pack_propagate(False)

        self.image_lbl = tk.Label(
            image_outer,
            text="No image",
            bg=SOFT_PANEL,
            fg=TEXT,
            font=(FONT_FAMILY, 10, "italic")
        )
        self.image_lbl.pack(expand=True, fill="both")

        info_title = tk.Label(
            now_card,
            text="Track Information",
            bg=WHITE,
            fg=TEXT,
            font=(FONT_FAMILY, 11, "bold")
        )
        info_title.pack(anchor="w", padx=22, pady=(0, 8))

        info_frame = tk.Frame(
            now_card,
            bg=SOFT_PANEL,
            bd=1,
            relief="solid"
        )
        info_frame.pack(fill="both", expand=True, padx=22, pady=(0, 22))

        self.track_txt = tk.Text(
            info_frame,
            width=28,
            height=11,
            bg=SOFT_PANEL,
            fg=TEXT,
            relief="flat",
            bd=0,
            wrap="word",
            font=(FONT_FAMILY, 11),
            padx=12,
            pady=12
        )
        self.track_txt.pack(fill="both", expand=True)
        self.track_txt.config(state="disabled")

        self.status_lbl = make_status(window)
        set_status(self.status_lbl, "Ready")

    def clear_image(self, message="No image"):
        clear_image_label(
            self.image_lbl,
            message=message,
            bg=SOFT_PANEL,
            fg=TEXT,
            font=(FONT_FAMILY, 10, "italic")
        )

    def clear_track_details(self):
        set_text(self.track_txt, "")
        self.clear_image()

    def show_track_image(self, track_number):
        image_path = self.controller.get_image_path(track_number)
        photo = load_png_image(
            image_path,
            max_width=PLAYLIST_IMAGE_MAX_WIDTH,
            max_height=PLAYLIST_IMAGE_MAX_HEIGHT
        )

        if photo is None:
            self.clear_image("No image available")
            return

        set_image_label(self.image_lbl, photo, bg=SOFT_PANEL)

    def show_track_details(self, track_number):
        details = self.controller.get_track_details_text(track_number)
        set_text(self.track_txt, details)
        self.show_track_image(track_number)

    def add_track_clicked(self):
        result = self.controller.add_track_to_playlist(self.track_input.get())

        set_text(self.list_txt, result["text"])
        set_status(self.status_lbl, result["status"], ok=result["ok"])

        if result["ok"]:
            items = self.controller.get_playlist_items()
            if items:
                last_track = items[-1]
                self.show_track_details(last_track.track_number)

        self.track_input.delete(0, tk.END)

    def play_playlist_clicked(self):
        if pygame is None or not self.audio_ready:
            set_status(self.status_lbl, "Audio system could not start", ok=False)
            return

        self.stop_playback(save_changes=False)

        result = self.controller.play_playlist()
        set_text(self.list_txt, result["text"])
        set_status(self.status_lbl, result["status"], ok=result["ok"])

        if not result["ok"]:
            return

        self.play_current_track()

    def play_current_track(self):
        if not self.controller.is_playing():
            return

        track = self.controller.get_current_track()

        if track is None:
            self.finish_playlist()
            return

        track_number = track.track_number
        audio_path = self.controller.get_audio_path(track_number)

        self.show_track_details(track_number)

        if audio_path is None:
            set_status(
                self.status_lbl,
                f"Audio file not found for track {track_number}, skipping",
                ok=False
            )
            self.controller.move_next_track()
            self.after_id = self.window.after(400, self.play_current_track)
            return

        try:
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()

            details = self.controller.register_play(track_number, save=False)
            set_text(self.track_txt, details)
            set_text(self.list_txt, self.controller.get_playlist_text())

            set_status(
                self.status_lbl,
                f"Playing: {track.name}",
                ok=True
            )

            self.check_playback()

        except pygame.error:
            set_status(
                self.status_lbl,
                f"Cannot play track {track_number}, skipping",
                ok=False
            )
            self.controller.move_next_track()
            self.after_id = self.window.after(400, self.play_current_track)

    def check_playback(self):
        if not self.controller.is_playing():
            return

        if pygame.mixer.music.get_busy():
            self.after_id = self.window.after(500, self.check_playback)
        else:
            next_track = self.controller.move_next_track()
            if next_track is None:
                self.finish_playlist()
            else:
                self.play_current_track()

    def finish_playlist(self):
        self.controller.save_changes()
        self.controller.stop_playlist()
        self.after_id = None
        set_text(self.list_txt, self.controller.get_playlist_text())
        set_status(self.status_lbl, "Playlist finished", ok=True)

    def stop_playback(self, save_changes=True):
        was_playing = self.controller.is_playing()

        if self.after_id is not None:
            self.window.after_cancel(self.after_id)
            self.after_id = None

        if pygame is not None and self.audio_ready and pygame.mixer.get_init() is not None:
            pygame.mixer.music.stop()

        if was_playing and save_changes:
            self.controller.save_changes()

        self.controller.stop_playlist()

    def stop_playlist_clicked(self):
        self.stop_playback()
        set_status(self.status_lbl, "Playback stopped", ok=True)

    def reset_playlist_clicked(self):
        self.stop_playback(save_changes=False)

        result = self.controller.reset_playlist()
        set_text(self.list_txt, result["text"])
        set_text(self.track_txt, "")
        self.clear_image()

        set_status(self.status_lbl, result["status"], ok=result["ok"])

    def on_close(self):
        self.stop_playback()


if __name__ == "__main__":
    window = tk.Tk()
    PlaylistView(window)
    window.mainloop()