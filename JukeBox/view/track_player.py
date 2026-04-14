import tkinter as tk
import os

from view import font_manager as fonts
from controller.main_controller import MainController

from view.gui_utils import (
    BG, CARD,
    SUBTEXT, make_title,
    make_button, make_status,
    set_status
)


def main():
    window = tk.Tk()

    window.geometry("900x560")
    window.title("JukeBox")
    window.configure(bg=BG)

    fonts.configure()

    controller = MainController()

    make_title(window, "JukeBox Music Player")

    sub_lbl = tk.Label(
        window,
        text="Choose an option and enjoy your music collection",
        bg=BG,
        fg=SUBTEXT
    )
    sub_lbl.pack(pady=(0, 18))

    button_frame = tk.Frame(window, bg=BG)
    button_frame.pack(pady=(0, 20))

    image_frame = tk.Frame(window, bg=CARD, bd=1, relief="solid")
    image_frame.pack(pady=(0, 14))

    image_path = os.path.join(os.path.dirname(__file__), "..", "img", "anhnen.png")

    if os.path.exists(image_path):
        try:
            bg_image = tk.PhotoImage(file=image_path)
            bg_image = bg_image.subsample(2, 2)

            image_lbl = tk.Label(image_frame, image=bg_image, bg=CARD, bd=0)
            image_lbl.image = bg_image

        except tk.TclError:
            image_lbl = tk.Label(
                image_frame,
                text="[Image cannot be loaded]",
                bg="white",
                width=60,
                height=18
            )
    else:
        image_lbl = tk.Label(
            image_frame,
            text="[JukeBox Image Here]",
            bg="white",
            width=60,
            height=18
        )

    image_lbl.pack(padx=10, pady=10)

    status_lbl = make_status(window)
    set_status(status_lbl, "Ready")

    make_button(
        button_frame,
        "View Tracks",
        lambda: controller.open_view_tracks(window, status_lbl),
        16
    ).grid(row=0, column=0, padx=8)

    make_button(
        button_frame,
        "Create Track List",
        lambda: controller.open_create_track_list(window, status_lbl),
        16
    ).grid(row=0, column=1, padx=8)

    make_button(
        button_frame,
        "Update Tracks Rating",
        lambda: controller.open_update_tracks(window, status_lbl),
        18
    ).grid(row=0, column=2, padx=8)

    window.mainloop()


if __name__ == "__main__":
    main()