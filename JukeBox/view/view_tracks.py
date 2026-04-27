import tkinter as tk  # used to build the main GUI
import tkinter.scrolledtext as tkst  # used for a text box with a scrollbar

# pygame is used to play music files
# if it is not installed, the program can still open
try:
    import pygame
except ImportError:
    pygame = None

from view import font_manager as fonts  # shared font settings
from controller.track_controller import TrackController  # handles track-related logic

from view.gui_utils import (
    CARD, TEXT, SECONDARY,  # colours used in the GUI
    set_text,  # puts text into a text box
    make_title, make_card,  # creates common title and card layout
    make_label, make_entry,  # creates labels and input boxes
    make_button, make_text,  # creates buttons and text areas
    make_status, set_status,  # creates and updates the status label
    load_png_image, clear_image_label, set_image_label,  # image helper functions
    init_audio_system  # starts the audio system
)


class TrackViewer:
    def __init__(self, window):
        self.window = window  # the main window for this screen

        fonts.configure()  # apply the shared font style

        self.controller = TrackController()  # gets track data and handles logic
        self.current_track = None  # stores the selected track number
        self.audio_ready = init_audio_system(pygame)  # checks if audio can be used

        make_title(window, "View Tracks")  # screen title

        main_frame = make_card(window)  # main container

        left_frame = tk.Frame(main_frame, bg=CARD)  # left side: controls and track list
        left_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        right_frame = tk.Frame(main_frame, bg=CARD, width=320)  # right side: image and details
        right_frame.pack(side="right", fill="y", padx=(0, 20), pady=20)
        right_frame.pack_propagate(False)  # keep the width fixed

        details_panel = tk.Frame(right_frame, bg=CARD)  # groups the detail widgets
        details_panel.pack(expand=True)

        top_controls = tk.Frame(left_frame, bg=CARD)  # top buttons and track number input
        top_controls.pack(anchor="w", pady=(0, 12))

        make_button(top_controls, "List All Tracks", self.list_tracks_clicked, 16).grid(
            row=0, column=0, padx=(0, 10), pady=5
        )  # shows all tracks

        make_label(top_controls, "Enter Track Number").grid(
            row=0, column=1, padx=5, pady=5
        )  # tells the user what to type

        self.input_txt = make_entry(top_controls, 8)  # box for track number
        self.input_txt.grid(row=0, column=2, padx=5, pady=5)

        make_button(top_controls, "View Track Details", self.view_tracks_clicked, 14).grid(
            row=0, column=3, padx=10, pady=5
        )  # shows details for one track

        search_frame = tk.Frame(left_frame, bg=CARD)  # search area
        search_frame.pack(anchor="w", pady=(0, 12))

        make_label(search_frame, "Search track or artist").grid(
            row=0, column=0, padx=(0, 10), pady=5
        )  # label for search

        self.search_txt = make_entry(search_frame, 22)  # box for search keyword
        self.search_txt.grid(row=0, column=1, padx=5, pady=5)

        make_button(search_frame, "Search", self.search_tracks_clicked, 12).grid(
            row=0, column=2, padx=10, pady=5
        )  # runs the search

        filter_frame = tk.Frame(left_frame, bg=CARD)  # filter area
        filter_frame.pack(anchor="w", pady=(0, 15))

        make_label(filter_frame, "Filter by artist").grid(
            row=0, column=0, padx=(0, 10), pady=5
        )  # label for artist filter

        artists = self.controller.get_artists()  # get all artist names

        self.artist_var = tk.StringVar(window)  # stores the selected artist
        self.artist_var.set(artists[0] if artists else "")  # first artist is the default value

        self.artist_menu = tk.OptionMenu(filter_frame, self.artist_var, *artists)  # artist dropdown
        self.artist_menu.config(width=18, bg="white", fg=TEXT, highlightthickness=0)
        self.artist_menu["menu"].config(bg="white", fg=TEXT)
        self.artist_menu.grid(row=0, column=1, padx=5, pady=5)

        make_button(filter_frame, "Filter", self.filter_tracks_clicked, 12).grid(
            row=0, column=2, padx=10, pady=5
        )  # shows only tracks by the selected artist

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
        )  # area for track list, search results, and filter results
        self.list_txt.pack(fill="both", expand=True)
        self.list_txt.config(state="disabled")  # user cannot type here

        details_title = tk.Label(
            details_panel,
            text="Track Details",
            bg=CARD,
            fg=TEXT,
            font=("Segoe UI", 12, "bold")
        )  # title for the details section
        details_title.pack(pady=(5, 12))

        image_frame = tk.Frame(details_panel, bg=CARD, bd=1, relief="solid")  # frame for the image
        image_frame.pack(pady=(0, 10))

        self.image_lbl = tk.Label(
            image_frame,
            text="No image",
            bg="white",
            fg=TEXT
        )  # shows the track image or a message
        self.image_lbl.pack(padx=6, pady=6)

        self.track_txt = make_text(details_panel, 28, 10)  # shows track details
        self.track_txt.pack()

        audio_frame = tk.Frame(details_panel, bg=CARD)  # frame for audio buttons
        audio_frame.pack(pady=(10, 0))

        make_button(audio_frame, "Play", self.play_track_clicked, 10).grid(
            row=0, column=0, padx=6
        )  # plays the selected track

        make_button(audio_frame, "Stop", self.stop_track_clicked, 10, bg=SECONDARY).grid(
            row=0, column=1, padx=6
        )  # stops the music

        self.status_lbl = make_status(window)  # shows success or error messages

        self.list_tracks_clicked()  # show all tracks when the screen opens

    def clear_image(self, message="No image"):
        clear_image_label(self.image_lbl, message=message, bg="white", fg=TEXT)
        # clears the old image and shows a message instead

    def clear_track_details(self):
        set_text(self.track_txt, "")  # clear the details text
        self.clear_image()  # clear the image
        self.current_track = None  # no track is selected now

    def show_track_image(self, image_path):
        photo = load_png_image(image_path, max_width=180, max_height=220)
        # load the image from file

        if photo is None:
            self.clear_image("No image available")  # show message if image cannot be loaded
            return

        set_image_label(self.image_lbl, photo, bg="white")  # show the image

    def view_tracks_clicked(self):
        result = self.controller.view_track(self.input_txt.get())
        # check the entered track number and get its data

        if not result["ok"]:
            set_text(self.track_txt, result["details"])  # show the error message
            self.clear_image()  # remove old image
            set_status(self.status_lbl, result["status"], ok=result["ok"])  # update status
            self.input_txt.delete(0, tk.END)  # clear input box
            return

        self.current_track = result["track_number"]  # save selected track number
        set_text(self.track_txt, result["details"])  # show track details
        self.show_track_image(result["image_path"])  # show track image
        set_status(self.status_lbl, result["status"], ok=result["ok"])  # show success message
        self.input_txt.delete(0, tk.END)  # clear input box

    def play_track_clicked(self):
        if pygame is None or not self.audio_ready:
            set_status(self.status_lbl, "Audio system could not start", ok=False)
            return
        # stop here if audio is not available

        result = self.controller.prepare_track_for_play(self.current_track)
        # check if a track is selected and if its audio file exists

        if not result["ok"]:
            set_status(self.status_lbl, result["status"], ok=False)
            return
        # show an error if the track cannot be played

        try:
            pygame.mixer.music.load(result["audio_path"])  # load the audio file
            pygame.mixer.music.play()  # start playback

            details = self.controller.register_play(self.current_track, save=True)
            set_text(self.track_txt, details)
            # update play count and refresh the details text

            list_result = self.controller.list_tracks()  # get the latest track list
            set_text(self.list_txt, list_result["text"]) # update the left list to show the new play count

            set_status(
                self.status_lbl,
                f"Playing: {result['track_name']}",
                ok=True
            )  # show the track currently playing

        except pygame.error:
            set_status(self.status_lbl, "Cannot play this audio file", ok=False)
            # show an error if playback fails

    def stop_track_clicked(self):
        if pygame is None or not self.audio_ready:
            set_status(self.status_lbl, "Audio system could not start", ok=False)
            return
        # stop here if audio is not available

        pygame.mixer.music.stop()  # stop the music
        set_status(self.status_lbl, "Playback stopped", ok=True)  # update status

    def list_tracks_clicked(self):
        result = self.controller.list_tracks()  # get all tracks

        self.clear_track_details()  # remove old details
        set_text(self.list_txt, result["text"])  # show all tracks
        set_status(self.status_lbl, result["status"], ok=result["ok"])  # update status

    def search_tracks_clicked(self):
        result = self.controller.search_tracks(self.search_txt.get())
        # search using the keyword in the search box

        self.clear_track_details()  # clear old details
        set_text(self.list_txt, result["text"])  # show search results
        set_status(self.status_lbl, result["status"], ok=result["ok"])  # update status

    def filter_tracks_clicked(self):
        result = self.controller.filter_tracks(self.artist_var.get())
        # filter tracks by the selected artist

        self.clear_track_details()  # clear old details
        set_text(self.list_txt, result["text"])  # show filtered results
        set_status(self.status_lbl, result["status"], ok=result["ok"])  # update status

    def on_close(self):
        if pygame is not None and self.audio_ready and pygame.mixer.get_init() is not None:
            pygame.mixer.music.stop()
        # stop music before closing the window


if __name__ == "__main__":
    window = tk.Tk()  # create the main window
    TrackViewer(window)  # open the View Tracks screen
    window.mainloop()  # keep the GUI running