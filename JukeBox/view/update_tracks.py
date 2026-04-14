import tkinter as tk
from view import font_manager as fonts

from controller.track_controller import TrackController, validate_rating

from view.gui_utils import (
    BG, CARD, set_text,
    make_title, make_card, make_label, make_entry,
    make_button, make_text, make_status,
    set_status
)


class UpdateTracks:
    def __init__(self, window):
        self.window = window
        self.window.geometry("760x500")
        self.window.title("Update Track Rating")
        self.window.configure(bg=BG)

        fonts.configure()

        self.controller = TrackController()

        make_title(window, "Update Track Rating")

        main_frame = make_card(window)

        form_frame = tk.Frame(main_frame, bg=CARD)
        form_frame.pack(pady=(30, 20))

        make_label(form_frame, "Enter track number:").grid(
            row=0, column=0, padx=10, pady=10, sticky="e"
        )

        self.track_input = make_entry(form_frame, 15)
        self.track_input.grid(row=0, column=1, padx=10, pady=10)

        make_label(form_frame, "Enter new rating (1-5):").grid(
            row=1, column=0, padx=10, pady=10, sticky="e"
        )

        self.rating_input = make_entry(form_frame, 15)
        self.rating_input.grid(row=1, column=1, padx=10, pady=10)

        make_button(form_frame, "Update Rating", self.update_rating_clicked, 18).grid(
            row=2, column=0, columnspan=2, pady=(15, 10)
        )

        make_label(main_frame, "Updated Track Details", bg=CARD).pack(pady=(5, 10))

        self.result_txt = make_text(main_frame, 62, 10)
        self.result_txt.pack(padx=20, pady=10)

        self.status_lbl = make_status(window)
        set_status(self.status_lbl, "Ready")

    def update_rating_clicked(self):
        result = self.controller.update_rating(
            self.track_input.get(),
            self.rating_input.get()
        )

        set_text(self.result_txt, result["text"])
        set_status(self.status_lbl, result["status"], ok=result["ok"])

        self.track_input.delete(0, tk.END)
        self.rating_input.delete(0, tk.END)


if __name__ == "__main__":
    window = tk.Tk()
    UpdateTracks(window)
    window.mainloop()