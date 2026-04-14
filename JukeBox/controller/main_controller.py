import tkinter as tk

from view.view_tracks import TrackViewer
from view.create_track_list import CreateTrackList
from view.update_tracks import UpdateTracks
from view.gui_utils import set_status


class MainController:
    def open_view_tracks(self, parent_window, status_label):
        TrackViewer(tk.Toplevel(parent_window))
        set_status(status_label, "Opened View Tracks")

    def open_create_track_list(self, parent_window, status_label):
        CreateTrackList(tk.Toplevel(parent_window))
        set_status(status_label, "Opened Create Track List")

    def open_update_tracks(self, parent_window, status_label):
        UpdateTracks(tk.Toplevel(parent_window))
        set_status(status_label, "Opened Update Tracks")