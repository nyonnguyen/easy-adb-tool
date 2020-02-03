import wx


class BuildTab(wx.Panel):
    def __init__(self, parent, build_path):
        wx.Panel.__init__(self, parent)
        my_sizer = wx.BoxSizer(wx.VERTICAL)

        self.build_path_picker = wx.DirPickerCtrl(self, path=build_path, message="Select Build Directory")
        my_sizer.Add(self.build_path_picker, 0, wx.ALL | wx.EXPAND, 5)

        build_filter_combo = wx.BoxSizer(wx.HORIZONTAL)
        build_filter_label = wx.StaticText(parent, style=wx.ST_NO_AUTORESIZE, label="Build Filter ")
        build_filter_combo.Add(build_filter_label, 0, wx.ALL | wx.CENTER, 5)

        self.build_list_filter = wx.TextCtrl(self, size=wx.Size(300, 25))
        build_filter_combo.Add(self.build_list_filter, 0, wx.ALL | wx.CENTER, 5)
        my_sizer.Add(build_filter_combo, 0, wx.ALL | wx.LEFT, 5)

        self.build_files_list = wx.ListCtrl(
            self, size=(1, 200), style=wx.LC_REPORT | wx.BORDER_SUNKEN | wx.LC_SORT_DESCENDING
        )
        self.build_files_list.InsertColumn(0, "Name", width=340)
        self.build_files_list.InsertColumn(1, "Size (MB)", width=80)
        self.build_files_list.InsertColumn(2, "Date", width=180)
        my_sizer.Add(self.build_files_list, 0, wx.ALL | wx.EXPAND, 5)

        self.install_build_btn = wx.Button(self, label='Install Selected Build')
        my_sizer.Add(self.install_build_btn, 2, wx.ALL | wx.CENTER, 5)
        self.SetSizer(my_sizer)