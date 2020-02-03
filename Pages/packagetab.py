import wx


class PackageTab(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        my_sizer = wx.BoxSizer(wx.VERTICAL)
        pkg_filter_combo = wx.BoxSizer(wx.HORIZONTAL)
        package_filter_label = wx.StaticText(self, style=wx.ST_NO_AUTORESIZE, label="Package Filter ")
        pkg_filter_combo.Add(package_filter_label, 0, wx.ALL | wx.CENTER, 5)

        self.package_filter = wx.TextCtrl(self, size=wx.Size(300, 25))
        pkg_filter_combo.Add(self.package_filter, 0, wx.ALL | wx.CENTER, 5)
        my_sizer.Add(pkg_filter_combo, 0, wx.ALL | wx.LEFT, 5)

        self.installed_package_list = wx.ListCtrl(
            self, size=(1, 200), style=wx.LC_REPORT | wx.BORDER_SUNKEN | wx.LC_SORT_DESCENDING
        )
        self.installed_package_list.InsertColumn(0, "Package Name", width=380)
        self.installed_package_list.InsertColumn(1, "Version", width=220)
        # self.installed_package_list.InsertColumn(2, "Date", width=180)
        my_sizer.Add(self.installed_package_list, 0, wx.ALL | wx.EXPAND, 5)

        self.uninstall_build_btn = wx.Button(self, label='Uninstall Selected Build')
        my_sizer.Add(self.uninstall_build_btn, 0, wx.ALL | wx.CENTER, 5)
        self.SetSizer(my_sizer)