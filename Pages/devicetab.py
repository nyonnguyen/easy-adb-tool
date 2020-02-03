import wx


class DeviceTab(wx.Panel):
    def __init__(self, parent, adb_path):
        wx.Panel.__init__(self, parent)
        my_sizer = wx.BoxSizer(wx.VERTICAL)
        adb_path_label = wx.StaticText(self, style=wx.ST_NO_AUTORESIZE, label="ADB Path:")
        my_sizer.Add(adb_path_label, 0, wx.ALL | wx.EXPAND, 5)

        self.my_browser = wx.DirPickerCtrl(self, path=adb_path, message="Select ADB Path")
        my_sizer.Add(self.my_browser, 0, wx.ALL | wx.EXPAND, 5)

        self.scan_device_btn = wx.Button(self, label='Scan Attached Devices')
        my_sizer.Add(self.scan_device_btn, 0, wx.ALL | wx.CENTER, 5)

        list_device_label = wx.StaticText(self, style=wx.ST_NO_AUTORESIZE, label="List of devices attached:")
        my_sizer.Add(list_device_label, 0, wx.ALL | wx.EXPAND, 5)

        self.device_list = wx.ListCtrl(
            self, size=(-1, 100), style=wx.LC_REPORT | wx.BORDER_SUNKEN | wx.LC_SORT_DESCENDING
        )
        self.device_list.InsertColumn(0, "Device Name", width=400)
        self.device_list.InsertColumn(1, "Status", width=200)
        my_sizer.Add(self.device_list, 1, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(my_sizer)
