import wx


class ScreenhotTab(wx.Panel):
    def __init__(self, parent, download_path):
        wx.Panel.__init__(self, parent)
        my_sizer = wx.BoxSizer(wx.VERTICAL)

        screenshot_combo = wx.BoxSizer(wx.HORIZONTAL)
        screenshot_label = wx.StaticText(self, style=wx.ST_NO_AUTORESIZE, label="Screenshot Name ")
        screenshot_combo.Add(screenshot_label, 0, wx.ALL | wx.CENTER, 5)

        self.screenshot_name_txt = wx.TextCtrl(self, size=(300, 20))
        screenshot_combo.Add(self.screenshot_name_txt, 0, wx.ALL | wx.CENTER, 5)
        my_sizer.Add(screenshot_combo, 0, wx.ALL | wx.LEFT, 5)

        save_screenshot_combo = wx.BoxSizer(wx.HORIZONTAL)
        save_path_label = wx.StaticText(self, style=wx.ST_NO_AUTORESIZE, label="Save Directory ")
        save_screenshot_combo.Add(save_path_label, 0, wx.ALL | wx.CENTER, 5)

        self.download_path_picker = wx.DirPickerCtrl(self, size=(500, 30), path=download_path, message="Select Save Directory")
        save_screenshot_combo.Add(self.download_path_picker, 0, wx.ALL | wx.CENTER, 5)
        my_sizer.Add(save_screenshot_combo, 0, wx.ALL | wx.LEFT, 5)

        self.capture_btn = wx.Button(self, label='Capture Screenshot')
        my_sizer.Add(self.capture_btn, 0, wx.ALL | wx.CENTER, 5)
        self.SetSizer(my_sizer)
