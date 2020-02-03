import wx


class VideoTab(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        text = wx.StaticText(self, style=wx.ST_NO_AUTORESIZE, label="This function is coming soon!")