import tkinter as tk  # import tkinter to create the GUI
import tkinter.scrolledtext as tkst  # used to create a text area with a scrollbar

# pygame is used to play music. If pygame is not installed, the program can still open.
try:
    import pygame  # used for audio playback
except ImportError:
    pygame = None  # prevents the program from crashing if pygame is missing

from view import font_manager as fonts  # uses the shared font settings for the GUI
from controller.track_controller import TrackController  # controller handles track-related logic

from view.gui_utils import (
    CARD, TEXT, SECONDARY,  # background colour, text colour, and secondary button colour
    set_text,  # function used to put text into a text area
    make_title, make_card,  # functions used to create the title and main card
    make_label, make_entry,  # functions used to create labels and entry boxes
    make_button, make_text,  # functions used to create buttons and text areas
    make_status, set_status,  # functions used to create and update the status label
    load_png_image, clear_image_label, set_image_label,  # functions used to handle images
    init_audio_system  # function used to start the audio system
)


class TrackViewer:
    """
    Purpose:
        This class creates the View Tracks screen.
    Input:
        window: the parent window or frame where this screen is placed.
    Output:
        It does not return a value.
        It creates a GUI screen for viewing tracks, searching tracks,
        filtering artists, showing images, and playing music.
    Used by:
        track_player.py when the View Tracks tab is opened.
    """

    def __init__(self, window):
        """
        Purpose:
            This method builds the View Tracks GUI.
        Input:
            window: the parent window or frame for this screen.
        Output:
            It does not return a value.
            It creates all widgets such as buttons, entry boxes,
            text areas, image labels, and status labels.
        """

        self.window = window  # stores the parent window so widgets can be placed inside it
        fonts.configure()  # applies the shared font style to this screen

        self.controller = TrackController()  # handles track data and logic for this view
        self.current_track = None  # stores the currently selected track number
        self.audio_ready = init_audio_system(pygame)  # checks if pygame audio is ready to use

        make_title(window, "View Tracks")  # creates the title for this screen

        main_frame = make_card(window)  # creates the main container for this screen

        left_frame = tk.Frame(main_frame, bg=CARD)  # creates the left side for controls and track list
        left_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        # side="left" places it on the left, fill/expand lets it resize, and padx/pady adds spacing

        right_frame = tk.Frame(main_frame, bg=CARD, width=320)  # creates the right side for image and details
        right_frame.pack(side="right", fill="y", padx=(0, 20), pady=20)
        # side="right" places it on the right, fill="y" expands vertically, and padding adds spacing

        right_frame.pack_propagate(False)  # keeps the right section fixed at width 320

        details_panel = tk.Frame(right_frame, bg=CARD)  # groups title, image, details, and audio buttons
        details_panel.pack(expand=True)  # helps position the details panel nicely inside the right frame

        top_controls = tk.Frame(left_frame, bg=CARD)  # creates a frame for the top row of controls
        top_controls.pack(anchor="w", pady=(0, 12))  # aligns controls to the left and adds space below

        make_button(top_controls, "List All Tracks", self.list_tracks_clicked, 16).grid(
            row=0, column=0, padx=(0, 10), pady=5
        )  # creates a button that displays the full track list

        make_label(top_controls, "Enter Track Number").grid(
            row=0, column=1, padx=5, pady=5
        )  # creates a label telling the user to enter a track number

        self.input_txt = make_entry(top_controls, 8)  # creates an entry box for the track number
        self.input_txt.grid(row=0, column=2, padx=5, pady=5)  # places the entry box beside the label

        make_button(top_controls, "View Track Details", self.view_tracks_clicked, 14).grid(
            row=0, column=3, padx=10, pady=5
        )  # creates a button that shows details for the entered track number

        search_frame = tk.Frame(left_frame, bg=CARD)  # creates a frame for the search area
        search_frame.pack(anchor="w", pady=(0, 12))  # places the search area below the top controls

        make_label(search_frame, "Search track or artist").grid(
            row=0, column=0, padx=(0, 10), pady=5
        )  # creates a label for the search box

        self.search_txt = make_entry(search_frame, 22)  # creates an entry box for the search keyword
        self.search_txt.grid(row=0, column=1, padx=5, pady=5)  # places the search box next to the label

        make_button(search_frame, "Search", self.search_tracks_clicked, 12).grid(
            row=0, column=2, padx=10, pady=5
        )  # creates a button that searches by track name or artist

        filter_frame = tk.Frame(left_frame, bg=CARD)  # creates a frame for filtering tracks by artist
        filter_frame.pack(anchor="w", pady=(0, 15))  # places the filter frame below the search frame

        make_label(filter_frame, "Filter by artist").grid(
            row=0, column=0, padx=(0, 10), pady=5
        )  # creates a label for the artist filter

        artists = self.controller.get_artists()  # gets the list of artists from the controller
        self.artist_var = tk.StringVar(window)  # stores the artist selected in the dropdown menu
        self.artist_var.set(artists[0] if artists else "")  # sets the first artist as default if available

        self.artist_menu = tk.OptionMenu(filter_frame, self.artist_var, *artists)  # creates the artist dropdown
        self.artist_menu.config(width=18, bg="white", fg=TEXT, highlightthickness=0)
        # width sets size, bg/fg set colours, and highlightthickness removes the default border

        self.artist_menu["menu"].config(bg="white", fg=TEXT)  # sets the colour of the dropdown list
        self.artist_menu.grid(row=0, column=1, padx=5, pady=5)  # places the dropdown next to the label

        make_button(filter_frame, "Filter", self.filter_tracks_clicked, 12).grid(
            row=0, column=2, padx=10, pady=5
        )  # creates a button that filters tracks by selected artist

        self.list_txt = tkst.ScrolledText(
            left_frame,
            width=58,  # controls the visible width of the text area
            height=16,  # controls the visible height of the text area
            wrap="none",  # keeps each track on one line
            bg="white",  # makes the result area stand out
            fg=TEXT,  # uses the shared text colour
            relief="solid",  # creates a visible border
            bd=1,  # creates a thin border
            insertbackground=TEXT  # sets the cursor colour
        )  # creates a scrollable text area to display the track list

        self.list_txt.pack(fill="both", expand=True)  # allows the text area to expand inside the left frame
        self.list_txt.config(state="disabled")  # prevents the user from typing into the track list

        details_title = tk.Label(
            details_panel,
            text="Track Details",
            bg=CARD,  # matches the panel colour
            fg=TEXT,  # makes the text readable
            font=("Segoe UI", 12, "bold")  # makes the title stand out
        )  # creates the title for the track details area

        details_title.pack(pady=(5, 12))  # places the title inside the details panel

        image_frame = tk.Frame(details_panel, bg=CARD, bd=1, relief="solid")  # creates a frame for the image
        image_frame.pack(pady=(0, 10))  # places the image frame below the title

        self.image_lbl = tk.Label(
            image_frame,
            text="No image",  # default text before an image is loaded
            bg="white",  # image area background
            fg=TEXT  # text colour
        )  # this label displays the track image or a message

        self.image_lbl.pack(padx=6, pady=6)  # adds spacing around the image label

        self.track_txt = make_text(details_panel, 28, 10)  # creates a text area for track details
        self.track_txt.pack()  # places the track details text area below the image

        audio_frame = tk.Frame(details_panel, bg=CARD)  # creates a frame for the Play and Stop buttons
        audio_frame.pack(pady=(10, 0))  # places the audio buttons below the track details

        make_button(audio_frame, "Play", self.play_track_clicked, 10).grid(
            row=0, column=0, padx=6
        )  # creates a Play button

        make_button(audio_frame, "Stop", self.stop_track_clicked, 10, bg=SECONDARY).grid(
            row=0, column=1, padx=6
        )  # creates a Stop button; SECONDARY shows it is not the main action

        self.status_lbl = make_status(window)  # creates a status label for success/error messages
        self.list_tracks_clicked()  # automatically displays all tracks when the screen opens

    def clear_image(self, message="No image"):
        """
        Purpose:
            Clear the current image from the image display area.
        Input:
            message: the text shown after the image is cleared.
            The default message is "No image".
        Output:
            It does not return a value.
            It updates self.image_lbl to show text instead of an image.
        Used by:
            clear_track_details(), show_track_image(), and view_tracks_clicked().
        """

        clear_image_label(self.image_lbl, message=message, bg="white", fg=TEXT)  # clears image and shows message

    def clear_track_details(self):
        """
        Purpose:
            Clear the currently selected track details.
        Input:
            No direct input.
        Output:
            It does not return a value.
            It clears the detail text area, clears the image, and resets current_track to None.
        Used by:
            list_tracks_clicked(), search_tracks_clicked(), and filter_tracks_clicked().
        """

        set_text(self.track_txt, "")  # clears the track details text area
        self.clear_image()  # clears the current track image
        self.current_track = None  # resets the selected track so old track is not played

    def show_track_image(self, image_path):
        """
        Purpose:
            Display the image for the selected track.
        Input:
            image_path: the file path of the track image.
        Output:
            It does not return a value.
            If the image is valid, it displays the image.
            If the image is missing or invalid, it shows "No image available".
        Used by:
            view_tracks_clicked().
        """

        photo = load_png_image(image_path, max_width=180, max_height=220)  # loads and resizes the image

        if photo is None:  # checks if the image cannot be loaded
            self.clear_image("No image available")  # shows a message instead of an image
            return  # stops the method because there is no image to display

        set_image_label(self.image_lbl, photo, bg="white")  # displays the image in the label

    def view_tracks_clicked(self):
        """
        Purpose:
            Show details for the track number entered by the user.
        Input:
            It reads the track number from self.input_txt.
        Output:
            It does not return a value.
            If the track is valid, it displays the track details and image.
            If the track is invalid, it displays an error message.
        Used by:
            The "View Track Details" button.
        """

        result = self.controller.view_track(self.input_txt.get())  # validates input and gets track data

        if not result["ok"]:  # handles invalid input or missing track
            set_text(self.track_txt, result["details"])  # shows the error message in the details area
            self.clear_image()  # clears the old image because the input is invalid
            set_status(self.status_lbl, result["status"], ok=result["ok"])  # updates the status label
            self.input_txt.delete(0, tk.END)  # clears the entry box
            return  # stops the method because no valid track was found

        self.current_track = result["track_number"]  # saves the valid track number for the Play button
        set_text(self.track_txt, result["details"])  # displays the track details
        self.show_track_image(result["image_path"])  # displays the track image if available
        set_status(self.status_lbl, result["status"], ok=result["ok"])  # updates the status label
        self.input_txt.delete(0, tk.END)  # clears the entry box after displaying the track

    def play_track_clicked(self):
        """
        Purpose:
            Play the currently selected track.
        Input:
            It does not read directly from an entry box.
            It uses self.current_track, which is set after the user views a valid track.
        Output:
            It does not return a value.
            It plays the audio, increases the play count, updates track details,
            and refreshes the track list.
        Used by:
            The "Play" button.
        """

        if pygame is None or not self.audio_ready:  # checks if pygame/audio is available
            set_status(self.status_lbl, "Audio system could not start", ok=False)  # shows audio error
            return  # stops the method because music cannot be played

        result = self.controller.prepare_track_for_play(self.current_track)  # checks selected track and audio file

        if not result["ok"]:  # handles no selected track or missing audio
            set_status(self.status_lbl, result["status"], ok=False)  # shows the problem message
            return

        try:
            pygame.mixer.music.load(result["audio_path"])  # loads the audio file into pygame
            pygame.mixer.music.play()  # starts playing the music

            details = self.controller.register_play(self.current_track, save=True)  # increases and saves play count
            set_text(self.track_txt, details)  # updates the details area with the new play count


            set_status(
                self.status_lbl,
                f"Playing: {result['track_name']}",
                ok=True
            )  # shows which track is currently playing

        except pygame.error:
            set_status(self.status_lbl, "Cannot play this audio file", ok=False)  # shows audio file error

    def stop_track_clicked(self):
        """
        Purpose:
            Stop the currently playing music.
        Input:
            No direct input.
        Output:
            It does not return a value.
            It stops the audio and updates the status label.
        Used by:
            The "Stop" button.
        """

        if pygame is None or not self.audio_ready:  # checks if audio is available
            set_status(self.status_lbl, "Audio system could not start", ok=False)  # shows audio error
            return

        pygame.mixer.music.stop()  # stops the currently playing music
        set_status(self.status_lbl, "Playback stopped", ok=True)  # shows that playback has stopped

    def list_tracks_clicked(self):
        """
        Purpose:
            Display all tracks.
        Input:
            No direct input.
        Output:
            It does not return a value.
            It updates self.list_txt with the full track list.
        Used by:
            The "List All Tracks" button.
            It is also called when the screen first opens.
        """

        result = self.controller.list_tracks()  # gets all tracks from the controller
        self.clear_track_details()  # clears old selected track details before showing the full list
        set_text(self.list_txt, result["text"])  # displays the track list in the text area
        set_status(self.status_lbl, result["status"], ok=result["ok"])  # updates the status label

    def search_tracks_clicked(self):
        """
        Purpose:
            Search for tracks by track name or artist.
        Input:
            It reads the search keyword from self.search_txt.
        Output:
            It does not return a value.
            It displays the search results or an error message in self.list_txt.
        Used by:
            The "Search" button.
        """

        result = self.controller.search_tracks(self.search_txt.get())  # searches using the entered keyword
        self.clear_track_details()  # clears old track details before showing search results
        set_text(self.list_txt, result["text"])  # displays the search results
        set_status(self.status_lbl, result["status"], ok=result["ok"])  # updates the search status

    def filter_tracks_clicked(self):
        """
        Purpose:
            Filter the track list by the selected artist.
        Input:
            It reads the selected artist from self.artist_var.
        Output:
            It does not return a value.
            It displays tracks by the selected artist.
        Used by:
            The "Filter" button.
        """

        result = self.controller.filter_tracks(self.artist_var.get())  # filters tracks by selected artist
        self.clear_track_details()  # clears old track details before showing filtered results
        set_text(self.list_txt, result["text"])  # displays the filtered track list
        set_status(self.status_lbl, result["status"], ok=result["ok"])  # updates the status label

    def on_close(self):
        """
        Purpose:
            Stop music safely when the program is closing.
        Input:
            No direct input.
        Output:
            It does not return a value.
            If music is playing, it stops the music.
        Used by:
            track_player.py when the user closes the main window.
        """

        if pygame is not None and self.audio_ready and pygame.mixer.get_init() is not None:
            pygame.mixer.music.stop()  # stops the music before closing the app


if __name__ == "__main__":
    # This part only runs when view_tracks.py is opened directly.
    # It is useful for testing this screen by itself.

    window = tk.Tk()  # creates the main Tkinter window
    TrackViewer(window)  # creates the View Tracks screen inside the window
    window.mainloop()  # keeps the window open and waits for user actions