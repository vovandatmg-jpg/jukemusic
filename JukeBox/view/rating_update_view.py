import tkinter as tk
import tkinter.scrolledtext as tkst

from view import font_manager as fonts
from controller.track_controller import TrackController

from view.gui_utils import (
    CARD, TEXT,
    set_text,
    make_title, make_card, make_label, make_entry,
    make_button, make_text, make_status,
    set_status
)


class RatingUpdateView:
    def __init__(self, window):
        self.window = window

        fonts.configure()

        self.controller = TrackController()

        make_title(window, "Update Track Rating")

        main_frame = make_card(window)

        # ===== LEFT SIDE: FIXED TRACK LIST =====
        left_frame = tk.Frame(main_frame, bg=CARD)
        left_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        make_label(left_frame, "Track List - Choose a track number", bg=CARD).pack(
            anchor="w", pady=(0, 10)
        )

        self.track_list_txt = tkst.ScrolledText(
            left_frame,
            width=62,
            height=22,
            wrap="none",
            bg="white",
            fg=TEXT,
            relief="solid",
            bd=1,
            insertbackground=TEXT
        )
        self.track_list_txt.pack(fill="both", expand=True)

        self.track_list_txt.config(state="disabled")
        self.track_list_txt.bind("<ButtonRelease-1>", self.track_list_clicked)

        # ===== RIGHT SIDE: UPDATE FORM =====
        right_frame = tk.Frame(main_frame, bg=CARD, width=460)
        right_frame.pack(side="right", fill="both", padx=(0, 20), pady=20)
        right_frame.pack_propagate(False)

        # chia tỉ lệ chiều cao cho các phần bên phải
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(0, weight=0)  # form
        right_frame.grid_rowconfigure(1, weight=0)  # selected label
        right_frame.grid_rowconfigure(2, weight=2)  # selected details
        right_frame.grid_rowconfigure(3, weight=0)  # result label
        right_frame.grid_rowconfigure(4, weight=3)  # updated result

        form_frame = tk.Frame(right_frame, bg=CARD)
        form_frame.grid(row=0, column=0, sticky="ew", pady=(10, 20))

        make_label(form_frame, "Enter track number:").grid(
            row=0, column=0, padx=10, pady=10, sticky="e"
        )

        self.track_input = make_entry(form_frame, 15)
        self.track_input.grid(row=0, column=1, padx=10, pady=10)

        make_button(
            form_frame,
            "View Track",
            self.view_track_clicked,
            14
        ).grid(row=1, column=0, columnspan=2, pady=(5, 10))

        make_label(form_frame, "Enter new rating (1-5):").grid(
            row=2, column=0, padx=10, pady=10, sticky="e"
        )

        self.rating_input = make_entry(form_frame, 15)
        self.rating_input.grid(row=2, column=1, padx=10, pady=10)

        make_button(
            form_frame,
            "Update Rating",
            self.update_rating_clicked,
            18
        ).grid(row=3, column=0, columnspan=2, pady=(15, 10))

        make_label(right_frame, "Selected Track Details", bg=CARD).grid(
            row=1, column=0, sticky="w", pady=(10, 8)
        )

        self.selected_track_txt = make_text(right_frame, 42, 11)
        self.selected_track_txt.grid(row=2, column=0, sticky="nsew", pady=(0, 15))

        make_label(right_frame, "Updated Result", bg=CARD).grid(
            row=3, column=0, sticky="w", pady=(5, 8)
        )

        self.result_txt = make_text(right_frame, 42, 12)
        self.result_txt.grid(row=4, column=0, sticky="nsew")

        self.status_lbl = make_status(window)
        set_status(self.status_lbl, "Ready")

        self.load_track_list()

    def load_track_list(self):
        result = self.controller.list_tracks()
        set_text(self.track_list_txt, result["text"])

    def track_list_clicked(self, event):
        index = self.track_list_txt.index(f"@{event.x},{event.y}")
        line_number = index.split(".")[0]

        line_text = self.track_list_txt.get(
            f"{line_number}.0",
            f"{line_number}.end"
        ).strip()

        if line_text == "":
            return

        track_number = line_text.split()[0]

        if not track_number.isdigit():
            return

        self.track_input.delete(0, tk.END)
        self.track_input.insert(0, track_number)

        self.view_track_clicked()

    def view_track_clicked(self):
        result = self.controller.view_track(self.track_input.get())

        set_text(self.selected_track_txt, result["details"])
        set_status(self.status_lbl, result["status"], ok=result["ok"])

    def update_rating_clicked(self):
        result = self.controller.update_rating(
            self.track_input.get(),
            self.rating_input.get()
        )

        set_text(self.result_txt, result["text"])
        set_status(self.status_lbl, result["status"], ok=result["ok"])

        if result["ok"]:
            self.load_track_list()
            preview_result = self.controller.view_track(self.track_input.get())
            set_text(self.selected_track_txt, preview_result["details"])
            self.rating_input.delete(0, tk.END)


if __name__ == "__main__":
    window = tk.Tk()
    RatingUpdateView(window)
    window.mainloop()