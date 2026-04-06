import tkinter as tk
import track_library as lib
import font_manager as fonts

from gui_utils import (
    BG, CARD, SECONDARY,
    set_text, normalise_track_number,
    make_title, make_card, make_label, make_entry,
    make_button, make_text, make_status, set_status
)


class CreateTrackList:
    def __init__(self, window):
        # Save the window so we can use it in this class
        self.window = window

        # Set the window size, title, and background colour
        self.window.geometry("820x520")
        self.window.title("Create Track List")
        self.window.configure(bg=BG)

        # Apply the shared font settings
        fonts.configure()

        # Create an empty playlist
        self.playlist = []

        # Create the title at the top of the window
        make_title(window, "Create Track List")

        # Main card area for the layout
        main_frame = make_card(window)

        # Input area for entering a track number
        input_frame = tk.Frame(main_frame, bg=CARD)
        input_frame.pack(pady=(25, 15))

        # Label for track number input
        make_label(input_frame, "Enter track number:").grid(row=0, column=0, padx=10, pady=10)

        # Entry box where the user types the track number
        self.track_input = make_entry(input_frame, 15)
        self.track_input.grid(row=0, column=1, padx=10, pady=10)

        # Button to add the track to the playlist
        make_button(input_frame, "Add Track", self.add_track_clicked, 14).grid(
            row=0, column=2, padx=10, pady=10
        )

        # Frame for playlist action buttons
        button_frame = tk.Frame(main_frame, bg=CARD)
        button_frame.pack(pady=(0, 15))

        # Button to play the playlist
        make_button(
            button_frame,
            "Play Playlist",
            self.play_playlist_clicked,
            16
        ).pack(side="left", padx=8)

        # Button to reset the playlist
        make_button(
            button_frame,
            "Reset Playlist",
            self.reset_playlist_clicked,
            16,
            bg=SECONDARY
        ).pack(side="left", padx=8)

        # Label above the playlist display area
        make_label(main_frame, "Playlist", bg=CARD).pack(pady=(5, 10))

        # Text area used to show the playlist
        self.list_txt = make_text(main_frame, 72, 14)
        self.list_txt.pack(padx=20, pady=10)

        # Create the status label at the bottom of the window
        self.status_lbl = make_status(window)

        # Show the default message when the window opens
        set_status(self.status_lbl, "Ready")

    def add_track_clicked(self):
        # Read and validate the track number entered by the user
        track_number, error = normalise_track_number(self.track_input.get())

        # If the input is invalid, show an error message
        if error:
            set_status(self.status_lbl, error, ok=False)
            self.track_input.delete(0, tk.END)
            return

        # Check whether the track exists in the library
        if lib.get_name(track_number) is None:
            set_status(self.status_lbl, "Track not found", ok=False)
            self.track_input.delete(0, tk.END)
            return

        # Optional: stop duplicate track numbers in the playlist
        if track_number in self.playlist:
            set_status(self.status_lbl, "Track already in playlist", ok=False)
            self.track_input.delete(0, tk.END)
            return

        # Add the valid track to the playlist
        self.playlist.append(track_number)

        # Update the playlist display
        self.show_playlist()

        # Show success message
        set_status(self.status_lbl, "Track added successfully", ok=True)

        # Clear the input box after the button is clicked
        self.track_input.delete(0, tk.END)

    def show_playlist(self):
        # Create an empty list to store display lines
        lines = []

        # Go through each track in the playlist
        for count, track_number in enumerate(self.playlist, start=1):
            name = lib.get_name(track_number)
            artist = lib.get_artist(track_number)
            play_count = lib.get_play_count(track_number)

            # Create one line of text for each track
            lines.append(f"{count}. {track_number} - {name} - {artist} - Play count: {play_count}")

        # Show all playlist lines in the text area
        set_text(self.list_txt, "\n".join(lines))

    def play_playlist_clicked(self):
        # Check if the playlist is empty
        if not self.playlist:
            set_status(self.status_lbl, "Playlist is empty", ok=False)
            return

        # Increment play count for every track in the playlist
        for track_number in self.playlist:
            lib.increment_play_count(track_number, save=False)

        # Save all changes once after updating every track
        lib.save_changes()

        # Refresh playlist display so new play counts appear
        self.show_playlist()

        # Show success message
        set_status(self.status_lbl, "Playlist played successfully", ok=True)

    def reset_playlist_clicked(self):
        # Clear the playlist
        self.playlist = []

        # Clear the text area
        set_text(self.list_txt, "")

        # Show success message
        set_status(self.status_lbl, "Playlist reset", ok=True)


if __name__ == "__main__":
    # Create the main window
    window = tk.Tk()

    # Start the CreateTrackList GUI
    CreateTrackList(window)

    # Keep the window running
    window.mainloop()