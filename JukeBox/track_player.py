import tkinter as tk
import os

import font_manager as fonts
from view_tracks import TrackViewer
from create_track_list import CreateTrackList
from update_tracks import UpdateTracks

from gui_utils import (
    BG, CARD,
    SUBTEXT, make_title,
    make_button, make_status,
    set_status
)


def main():
    # Create the main tkinter window
    window = tk.Tk()

    # Set the size, title, and background colour of the window
    window.geometry("900x560")
    window.title("JukeBox")
    window.configure(bg=BG)

    # Apply the shared font settings
    fonts.configure()

    def open_view_tracks():
        # Open the View Tracks window in a new top-level window
        TrackViewer(tk.Toplevel(window))

        # Show a status message in the main window
        set_status(status_lbl, "Opened View Tracks")

    def open_create_track_list():
        # Open the Create Track List window in a new top-level window
        CreateTrackList(tk.Toplevel(window))

        # Show a status message in the main window
        set_status(status_lbl, "Opened Create Track List")

    def open_update_tracks():
        # Open the Update Tracks window in a new top-level window
        UpdateTracks(tk.Toplevel(window))

        # Show a status message in the main window
        set_status(status_lbl, "Opened Update Tracks")

    # Create the main title at the top of the window
    make_title(window, "JukeBox Music Player")

    # Create a short subtitle under the main title
    sub_lbl = tk.Label(
        window,
        text="Choose an option and enjoy your music collection",
        bg=BG,
        fg=SUBTEXT
    )
    sub_lbl.pack(pady=(0, 18))

    # Create a frame to hold the three main buttons
    button_frame = tk.Frame(window, bg=BG)
    button_frame.pack(pady=(0, 20))

    # Button to open the View Tracks window
    make_button(button_frame, "View Tracks", open_view_tracks, 16).grid(
        row=0, column=0, padx=8
    )

    # Button to open the Create Track List window
    make_button(button_frame, "Create Track List", open_create_track_list, 16).grid(
        row=0, column=1, padx=8
    )

    # Button to open the Update Tracks window
    make_button(button_frame, "Update Tracks", open_update_tracks, 16).grid(
        row=0, column=2, padx=8
    )

    # Create a frame to hold the main image
    image_frame = tk.Frame(window, bg=CARD, bd=1, relief="solid")
    image_frame.pack(pady=(0, 14))

    # Build the path to the background image inside the img folder
    image_path = os.path.join(os.path.dirname(__file__), "img", "anhnen.png")

    # Check if the image file exists
    if os.path.exists(image_path):
        try:
            # Load the image file
            bg_image = tk.PhotoImage(file=image_path)

            # Resize the image to make it smaller
            bg_image = bg_image.subsample(2, 2)

            # Show the image inside a label
            image_lbl = tk.Label(image_frame, image=bg_image, bg=CARD, bd=0)

            # Keep a reference to the image so it does not disappear
            image_lbl.image = bg_image

        except tk.TclError:
            # Show a message if tkinter cannot load the image
            image_lbl = tk.Label(
                image_frame,
                text="[Image cannot be loaded]",
                bg="white",
                width=60,
                height=18
            )
    else:
        # Show a placeholder message if the image file is missing
        image_lbl = tk.Label(
            image_frame,
            text="[JukeBox Image Here]",
            bg="white",
            width=60,
            height=18
        )

    # Display the image label or placeholder label
    image_lbl.pack(padx=10, pady=10)

    # Create the status label at the bottom of the window
    status_lbl = make_status(window)

    # Show the default status message
    set_status(status_lbl, "Ready")

    # Keep the window running
    window.mainloop()


if __name__ == "__main__":
    # Run the main function when this file is opened directly
    main()