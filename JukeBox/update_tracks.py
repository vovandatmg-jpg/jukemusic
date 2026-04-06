import tkinter as tk
import track_library as lib
import font_manager as fonts

from gui_utils import (
    BG, CARD, set_text,
    normalise_track_number, make_title,
    make_card, make_label, make_entry,
    make_button, make_text, make_status,
    set_status
)


def validate_rating(rating_text):
    # Remove extra spaces from the input
    rating_text = rating_text.strip()

    # Check if the input is empty
    if rating_text == "":
        return None, "Please enter a rating"

    # Check if the input is not a number
    if not rating_text.isdigit():
        return None, "Rating must be a number"

    # Change the text input into an integer
    rating = int(rating_text)

    # Check if the rating is outside the allowed range
    if rating < 1 or rating > 5:
        return None, "Rating must be between 1 and 5"

    # Return the valid rating
    return rating, None


class UpdateTracks:
    def __init__(self, window):
        # Save the window so we can use it in this class
        self.window = window

        # Set the window size, title, and background colour
        self.window.geometry("760x500")
        self.window.title("Update Tracks")
        self.window.configure(bg=BG)

        # Apply the shared font settings
        fonts.configure()

        # Create the title at the top of the window
        make_title(window, "Update Track Rating")

        # Main card area for the layout
        main_frame = make_card(window)

        # Form area for entering track number and new rating
        form_frame = tk.Frame(main_frame, bg=CARD)
        form_frame.pack(pady=(30, 20))

        # Label for track number input
        make_label(form_frame, "Enter track number:").grid(
            row=0, column=0, padx=10, pady=10, sticky="e"
        )

        # Entry box for the track number
        self.track_input = make_entry(form_frame, 15)
        self.track_input.grid(row=0, column=1, padx=10, pady=10)

        # Label for rating input
        make_label(form_frame, "Enter new rating (1-5):").grid(
            row=1, column=0, padx=10, pady=10, sticky="e"
        )

        # Entry box for the new rating
        self.rating_input = make_entry(form_frame, 15)
        self.rating_input.grid(row=1, column=1, padx=10, pady=10)

        # Button to update the rating
        make_button(form_frame, "Update Rating", self.update_rating_clicked, 18).grid(
            row=2, column=0, columnspan=2, pady=(15, 10)
        )

        # Label above the output area
        make_label(main_frame, "Updated Track Details", bg=CARD).pack(pady=(5, 10))

        # Text area used to show the result
        self.result_txt = make_text(main_frame, 62, 10)
        self.result_txt.pack(padx=20, pady=10)

        # Create the status label at the bottom of the window
        self.status_lbl = make_status(window)

        # Show the default message when the window opens
        set_status(self.status_lbl, "Ready")

        
    def update_rating_clicked(self):
        # Read and validate the track number
        track_number, track_error = normalise_track_number(self.track_input.get())

        # Read and validate the new rating
        new_rating, rating_error = validate_rating(self.rating_input.get())

        # If both inputs are invalid, show both errors
        if track_error and rating_error:
            set_text(self.result_txt, f"{track_error}\n{rating_error}")
            set_status(self.status_lbl, "Invalid track number and rating", ok=False)
            return

        # If only the track number is invalid, show that error
        if track_error:
            set_text(self.result_txt, track_error)
            set_status(self.status_lbl, track_error, ok=False)
            return

        # If only the rating is invalid, show that error
        if rating_error:
            set_text(self.result_txt, rating_error)
            set_status(self.status_lbl, rating_error, ok=False)
            return

        # Check if the track exists in the library
        if lib.get_name(track_number) is None:
            set_text(self.result_txt, "Track not found")
            set_status(self.status_lbl, "Track not found", ok=False)
        else:
            # Update the track rating in the library
            lib.set_rating(track_number, new_rating)

            # Build the result message
            result = (
                f"Track number: {track_number}\n"
                f"Name: {lib.get_name(track_number)}\n"
                f"Artist: {lib.get_artist(track_number)}\n"
                f"New rating: {'*' * lib.get_rating(track_number)}\n"
                f"Play count: {lib.get_play_count(track_number)}\n"
            )

            # Show the updated track details
            set_text(self.result_txt, result)

            # Show success message
            set_status(self.status_lbl, "Rating updated successfully", ok=True)

        # Clear both input boxes after the button is clicked
        self.track_input.delete(0, tk.END)
        self.rating_input.delete(0, tk.END)


if __name__ == "__main__":
    # Create the main window
    window = tk.Tk()

    # Start the UpdateTracks GUI
    UpdateTracks(window)

    # Keep the window running
    window.mainloop()