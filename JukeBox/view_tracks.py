import tkinter as tk
import tkinter.scrolledtext as tkst
import os

try:
    import pygame
except ImportError:
    pygame = None

# Import the track library so this GUI can read track information
import track_library as lib

# Import shared font settings
import font_manager as fonts

from gui_utils import (
    BG, CARD, TEXT, SECONDARY,
    set_text, normalise_track_number,
    make_title, make_card,
    make_label, make_entry,
    make_button, make_text,
    make_status, set_status
)


# This class creates the View Tracks window and handles
# listing, searching, filtering, displaying track details,
# and playing audio
class TrackViewer:
    def __init__(self, window):
        # Save the window so we can use it in this class
        self.window = window

        # Set the window size, title, and background colour
        self.window.geometry("980x660")
        self.window.title("View Tracks")
        self.window.configure(bg=BG)

        # Apply the shared font settings
        fonts.configure()

        # Store the currently selected track for audio playback
        self.current_track = None

        # Try to start the audio system
        self.audio_ready = False
        if pygame is not None:
            try:
                pygame.mixer.init()
                self.audio_ready = True
            except pygame.error:
                self.audio_ready = False

        # Create the title at the top of the window
        make_title(window, "View Tracks")

        # Main card area that contains the whole layout
        main_frame = make_card(window)

        # Left side: controls and track list
        left_frame = tk.Frame(main_frame, bg=CARD)
        left_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        # Right side: track details and image
        right_frame = tk.Frame(main_frame, bg=CARD)
        right_frame.pack(side="right", fill="y", padx=(0, 20), pady=20)

        # Top control area for listing and viewing tracks
        top_controls = tk.Frame(left_frame, bg=CARD)
        top_controls.pack(anchor="w", pady=(0, 12))

        # Button to show all tracks
        make_button(top_controls, "List All Tracks", self.list_tracks_clicked, 16).grid(
            row=0, column=0, padx=(0, 10), pady=5
        )

        # Label for the track number input box
        make_label(top_controls, "Enter Track Number").grid(
            row=0, column=1, padx=5, pady=5
        )

        # Entry box where the user types a track number
        self.input_txt = make_entry(top_controls, 8)
        self.input_txt.grid(row=0, column=2, padx=5, pady=5)

        # Button to show one selected track
        make_button(top_controls, "View Track", self.view_tracks_clicked, 14).grid(
            row=0, column=3, padx=10, pady=5
        )

        # Search area
        search_frame = tk.Frame(left_frame, bg=CARD)
        search_frame.pack(anchor="w", pady=(0, 12))

        # Label for search input
        make_label(search_frame, "Search track or artist").grid(
            row=0, column=0, padx=(0, 10), pady=5
        )

        # Entry box for typing the search keyword
        self.search_txt = make_entry(search_frame, 22)
        self.search_txt.grid(row=0, column=1, padx=5, pady=5)

        # Button to search by track name or artist
        make_button(search_frame, "Search", self.search_tracks_clicked, 12).grid(
            row=0, column=2, padx=10, pady=5
        )

        # Filter area
        filter_frame = tk.Frame(left_frame, bg=CARD)
        filter_frame.pack(anchor="w", pady=(0, 15))

        # Label for artist filter
        make_label(filter_frame, "Filter by artist").grid(
            row=0, column=0, padx=(0, 10), pady=5
        )

        # Get all artists from the track library
        artists = lib.get_artists()

        # Variable used to store the selected artist
        self.artist_var = tk.StringVar(window)
        self.artist_var.set(artists[0] if artists else "")

        # Drop-down menu for choosing an artist
        self.artist_menu = tk.OptionMenu(filter_frame, self.artist_var, *artists)
        self.artist_menu.config(width=18, bg="white", fg=TEXT, highlightthickness=0)
        self.artist_menu["menu"].config(bg="white", fg=TEXT)
        self.artist_menu.grid(row=0, column=1, padx=5, pady=5)

        # Button to apply the artist filter
        make_button(filter_frame, "Filter", self.filter_tracks_clicked, 12).grid(
            row=0, column=2, padx=10, pady=5
        )

        # Scrolled text area to show all tracks, search results, or filtered results
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

        # Title for the details section on the right
        details_title = tk.Label(
            right_frame,
            text="Track Details",
            bg=CARD,
            fg=TEXT,
            font=("Segoe UI", 12, "bold")
        )
        details_title.pack(pady=(5, 12))

        # Frame to hold the image
        image_frame = tk.Frame(right_frame, bg=CARD, bd=1, relief="solid")
        image_frame.pack(pady=(0, 10))

        # Label used to show the track image
        self.image_lbl = tk.Label(
            image_frame,
            text="No image",
            bg="white",
            fg=TEXT
        )
        self.image_lbl.pack(padx=6, pady=6)

        # Text area used to show the selected track details
        self.track_txt = make_text(right_frame, 28, 10)
        self.track_txt.pack()

        # Audio control buttons
        audio_frame = tk.Frame(right_frame, bg=CARD)
        audio_frame.pack(pady=(10, 0))

        make_button(audio_frame, "Play", self.play_track_clicked, 10).grid(
            row=0, column=0, padx=6
        )

        make_button(audio_frame, "Stop", self.stop_track_clicked, 10, bg=SECONDARY).grid(
            row=0, column=1, padx=6
        )

        # Status label at the bottom of the window
        self.status_lbl = make_status(window)

        # Show all tracks when the window first opens
        self.list_tracks_clicked()

        # Handle closing the window safely
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

    def load_png_image(self, image_path, max_width=180, max_height=220):
        # Return None if the image path is empty or the file does not exist
        if not image_path or not os.path.exists(image_path):
            return None

        try:
            # Load the PNG image
            image = tk.PhotoImage(file=image_path)

            # Get the original size of the image
            width = image.width()
            height = image.height()

            # Work out how much the image needs to be reduced
            scale_x = (width + max_width - 1) // max_width if width > max_width else 1
            scale_y = (height + max_height - 1) // max_height if height > max_height else 1
            scale = max(scale_x, scale_y)

            # Resize the image if it is too large
            if scale > 1:
                image = image.subsample(scale, scale)

            return image

        except tk.TclError:
            # Return None if tkinter cannot load the image
            return None

    def clear_image(self, message="No image"):
        # Remove the current image and show a text message instead
        self.image_lbl.configure(text=message, image="", bg="white")
        self.image_lbl.image = None

    def clear_track_details(self):
        # Clear the text area that shows the selected track details
        set_text(self.track_txt, "")

        # Clear the image area and show the default message
        self.clear_image()

        # Clear current selected track
        self.current_track = None

    def show_track_image(self, track_number):
        # Get the image path for the selected track
        image_path = lib.get_image_path(track_number)

        # Try to load the image
        photo = self.load_png_image(image_path)

        # If the image cannot be loaded, show a message
        if photo is None:
            self.clear_image("No image available")
            return

        # Show the loaded image
        self.image_lbl.configure(image=photo, text="", bg="white")
        self.image_lbl.image = photo

    def update_track_details(self, key):
        name = lib.get_name(key)
        artist = lib.get_artist(key)
        rating = lib.get_rating(key)
        play_count = lib.get_play_count(key)

        details = (
            f"Track Number: {key}\n"
            f"Track Name: {name}\n"
            f"Artist: {artist}\n"
            f"Rating: {'*' * rating}\n"
            f"Play Count: {play_count}"
        )

        set_text(self.track_txt, details)

    def view_tracks_clicked(self):
        # Read and validate the track number entered by the user
        key, error = normalise_track_number(self.input_txt.get())

        # If the input is invalid, show the validation error
        if error:
            set_text(self.track_txt, error)
            self.clear_image()
            set_status(self.status_lbl, "Invalid track number", ok=False)
            self.input_txt.delete(0, tk.END)
            return

        # Get the track name first to check whether the track exists
        name = lib.get_name(key)

        # If there is no matching track, show an error message
        if name is None:
            set_text(self.track_txt, f"Track {key} not found")
            self.clear_image()
            set_status(self.status_lbl, "Track not found", ok=False)
            self.input_txt.delete(0, tk.END)
            return

        # Save the current selected track
        self.current_track = key

        # Show the selected track details in the text area
        self.update_track_details(key)

        # Show the matching track image on the right side
        self.show_track_image(key)

        # Update the status label to confirm success
        set_status(self.status_lbl, "Track displayed successfully", ok=True)

        # Clear the input box after the track has been displayed
        self.input_txt.delete(0, tk.END)

    def play_track_clicked(self):
        # Check whether pygame is available and the audio system started correctly
        if pygame is None or not self.audio_ready:
            set_status(self.status_lbl, "Audio system could not start", ok=False)
            return

        # Make sure the user has selected a track first
        if self.current_track is None:
            set_status(self.status_lbl, "Please view a track first", ok=False)
            return

        # Get the audio path for the selected track
        audio_path = lib.get_audio_path(self.current_track)

        # Show an error if the audio file cannot be found
        if audio_path is None:
            set_status(self.status_lbl, "Audio file not found", ok=False)
            return

        try:
            # Load and play the selected audio file
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()

            # Increase play count and save to CSV
            lib.increment_play_count(self.current_track)

            # Refresh details so the new play count appears
            self.update_track_details(self.current_track)

            # Show success status
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
        # Clear the details panel on the right before showing the full list
        self.clear_track_details()

        # Show all tracks in the list area
        set_text(self.list_txt, lib.list_all())

        # Update the status label
        set_status(self.status_lbl, "Tracks listed successfully", ok=True)

    def search_tracks_clicked(self):
        # Get the search keyword entered by the user
        keyword = self.search_txt.get().strip()

        # If the search box is empty, show an error
        if keyword == "":
            self.clear_track_details()
            set_status(self.status_lbl, "Please enter a track name or artist", ok=False)
            return

        # Clear the details panel before showing search results
        self.clear_track_details()

        # Search for matching tracks
        results = lib.search_tracks(keyword)

        # Show the search results
        set_text(self.list_txt, results)

        # Update the status depending on the result
        if results == "No matching tracks found":
            set_status(self.status_lbl, "No matching tracks found", ok=False)
        elif results == "Please enter a search keyword":
            set_status(self.status_lbl, "Please enter a search keyword", ok=False)
        else:
            set_status(self.status_lbl, "Search completed", ok=True)

    def filter_tracks_clicked(self):
        # Get the selected artist from the drop-down menu
        artist_name = self.artist_var.get()

        # Clear the details panel before showing filtered results
        self.clear_track_details()

        # Filter the tracks by artist
        results = lib.filter_by_artist(artist_name)

        # Show the filtered results
        set_text(self.list_txt, results)

        # Update the status depending on the result
        if results == "No tracks found for this artist":
            set_status(self.status_lbl, "No tracks found for this artist", ok=False)
        else:
            set_status(self.status_lbl, "Artist filter applied", ok=True)

    def on_close(self):
        # Stop music before closing the window
        if pygame is not None and self.audio_ready:
            pygame.mixer.music.stop()
            pygame.mixer.quit()

        self.window.destroy()


if __name__ == "__main__":
    # Create the main window
    window = tk.Tk()

    # Start the TrackViewer class
    TrackViewer(window)

    # Keep the window open
    window.mainloop()