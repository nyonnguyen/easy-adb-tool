import wx


class VideoTab(wx.Panel):
    def __init__(self, parent, download_path):
        wx.Panel.__init__(self, parent)
        my_sizer = wx.BoxSizer(wx.VERTICAL)

        video_combo = wx.BoxSizer(wx.HORIZONTAL)
        video_label = wx.StaticText(self, style=wx.ST_NO_AUTORESIZE, label="Video Name ")
        video_combo.Add(video_label, 0, wx.ALL | wx.CENTER, 5)

        self.video_name_txt = wx.TextCtrl(self, size=(200, 20))
        video_combo.Add(self.video_name_txt, 0, wx.ALL | wx.CENTER, 5)

        video_slider_label = wx.StaticText(self, style=wx.ST_NO_AUTORESIZE, label="Limit length (second) ")
        video_combo.Add(video_slider_label, 0, wx.ALL | wx.CENTER, 5)

        self.video_slider = wx.Slider(self, value=12, minValue=1, maxValue=180, style=wx.SL_LABELS)
        video_combo.Add(self.video_slider, 0, wx.ALL | wx.CENTER, 5)

        my_sizer.Add(video_combo, 0, wx.ALL | wx.LEFT, 5)

        save_video_combo = wx.BoxSizer(wx.HORIZONTAL)
        save_path_label = wx.StaticText(self, style=wx.ST_NO_AUTORESIZE, label="Save Directory ")
        save_video_combo.Add(save_path_label, 0, wx.ALL | wx.CENTER, 5)

        self.download_path_picker = wx.DirPickerCtrl(self, size=(500, 30), path=download_path,
                                                     message="Select Save Directory")
        save_video_combo.Add(self.download_path_picker, 0, wx.ALL | wx.CENTER, 5)
        my_sizer.Add(save_video_combo, 0, wx.ALL | wx.LEFT, 5)

        self.video_btn = wx.Button(self, label='Capture Video')
        my_sizer.Add(self.video_btn, 0, wx.ALL | wx.CENTER, 5)
        self.SetSizer(my_sizer)

    def get_video_length(self):
        return self.video_slider.GetValue()
