import wx
import json
import os

PLAYLIST_FILE = "playlist.json"


class PlaylistApp(wx.Frame):
    def __init__(self):
        super().__init__(None, title="🎵 Music Playlist Manager", size=(820, 520))
        panel = wx.Panel(self)
        panel.SetBackgroundColour("#121212")

        self.playlist = []

    
        title = wx.StaticText(panel, label="Music Playlist Manager")
        title.SetFont(wx.Font(20, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        title.SetForegroundColour("#1DB954")

    
        song_label = wx.StaticText(panel, label="Song Name")
        song_label.SetForegroundColour("white")
        self.song_input = wx.TextCtrl(panel, size=(260, -1))

        artist_label = wx.StaticText(panel, label="Artist Name")
        artist_label.SetForegroundColour("white")
        self.artist_input = wx.TextCtrl(panel, size=(260, -1))

        add_btn = wx.Button(panel, label="➕ Add Song")
        add_btn.Bind(wx.EVT_BUTTON, self.add_song)

    
        search_label = wx.StaticText(panel, label="Search")
        search_label.SetForegroundColour("white")
        self.search_input = wx.TextCtrl(panel, size=(220, -1))
        self.search_input.Bind(wx.EVT_TEXT, self.search_song)

        
        self.list_box = wx.ListBox(panel, size=(640, 260))

        delete_btn = wx.Button(panel, label="🗑 Delete")
        delete_btn.Bind(wx.EVT_BUTTON, self.delete_song)

        sort_az_btn = wx.Button(panel, label="🔤 Sort A–Z")
        sort_az_btn.Bind(wx.EVT_BUTTON, self.sort_az)

        sort_za_btn = wx.Button(panel, label="🔠 Sort Z–A")
        sort_za_btn.Bind(wx.EVT_BUTTON, self.sort_za)

        save_btn = wx.Button(panel, label="💾 Save")
        save_btn.Bind(wx.EVT_BUTTON, self.save_playlist)

        load_btn = wx.Button(panel, label="📂 Load")
        load_btn.Bind(wx.EVT_BUTTON, self.load_playlist)

        
        main = wx.BoxSizer(wx.VERTICAL)
        main.Add(title, 0, wx.ALIGN_CENTER | wx.TOP, 15)

        input_row = wx.BoxSizer(wx.HORIZONTAL)
        input_row.Add(song_label, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)
        input_row.Add(self.song_input, 0, wx.RIGHT, 15)
        input_row.Add(artist_label, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)
        input_row.Add(self.artist_input, 0, wx.RIGHT, 15)
        input_row.Add(add_btn)

        main.Add(input_row, 0, wx.ALIGN_CENTER | wx.TOP, 15)

        search_row = wx.BoxSizer(wx.HORIZONTAL)
        search_row.Add(search_label, 0, wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)
        search_row.Add(self.search_input)

        main.Add(search_row, 0, wx.ALIGN_CENTER | wx.TOP, 10)
        main.Add(self.list_box, 0, wx.ALIGN_CENTER | wx.TOP, 10)

        controls = wx.BoxSizer(wx.HORIZONTAL)
        controls.Add(delete_btn, 0, wx.RIGHT, 10)
        controls.Add(sort_az_btn, 0, wx.RIGHT, 10)
        controls.Add(sort_za_btn, 0, wx.RIGHT, 10)
        controls.Add(save_btn, 0, wx.RIGHT, 10)
        controls.Add(load_btn)

        main.Add(controls, 0, wx.ALIGN_CENTER | wx.TOP, 10)

        panel.SetSizer(main)
        self.Centre()

        self.load_playlist()

    
    def add_song(self, event):
        song = self.song_input.GetValue().strip()
        artist = self.artist_input.GetValue().strip()

        if not song or not artist:
            wx.MessageBox("Please enter both song and artist.", "Error")
            return

        entry = f"{song} — {artist}"
        self.playlist.append(entry)
        self.refresh_list()

        self.song_input.SetValue("")
        self.artist_input.SetValue("")

    def delete_song(self, event):
        idx = self.list_box.GetSelection()
        if idx != wx.NOT_FOUND:
            selected = self.list_box.GetString(idx)
            self.playlist.remove(selected)
            self.refresh_list()

    def sort_az(self, event):
        self.playlist.sort()
        self.refresh_list()

    def sort_za(self, event):
        self.playlist.sort(reverse=True)
        self.refresh_list()

    def search_song(self, event):
        keyword = self.search_input.GetValue().strip().lower()
        self.list_box.Clear()

        if keyword == "":
            for song in self.playlist:
                self.list_box.Append(song)
            return

        for song in self.playlist:
            if keyword in song.lower():
                self.list_box.Append(song)

    def refresh_list(self):
        self.search_song(None)

    def save_playlist(self, event):
        with open(PLAYLIST_FILE, "w") as f:
            json.dump(self.playlist, f)
        wx.MessageBox("Playlist saved successfully!", "Success")

    def load_playlist(self, event=None):
        if os.path.exists(PLAYLIST_FILE):
            with open(PLAYLIST_FILE, "r") as f:
                self.playlist = json.load(f)
            self.refresh_list()



app = wx.App()
frame = PlaylistApp()
frame.Show()
app.MainLoop()
