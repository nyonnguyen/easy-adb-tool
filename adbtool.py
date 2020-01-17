import wx
import wx.adv
import wx.lib.scrolledpanel
from adbservices import AdbTool
from datetime import datetime
import time
import os
import glob
from adblog import AdbLog

logger = AdbLog.get_logger("easy_android_tool")


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Easy Android Tool')
        self.SetBackgroundColour(wx.Colour(150, 150, 150))
        self.config = wx.FileConfig(localFilename="adb_config")

        self.panel = wx.lib.scrolledpanel.ScrolledPanel(self)
        # self.panel = wx.Panel(self)
        my_sizer = wx.BoxSizer(wx.VERTICAL)

        adb_path_label = wx.StaticText(self.panel, style=wx.ST_NO_AUTORESIZE, label="ADB Path:")
        my_sizer.Add(adb_path_label, 0, wx.ALL | wx.EXPAND, 5)

        self.adb_path = self.config.Read("adb_path", "/usr/local/bin")
        self.my_browser = wx.DirPickerCtrl(self.panel, path=self.adb_path, message="Select ADB Path")
        self.my_browser.Bind(wx.EVT_DIRPICKER_CHANGED, self.on_browse)
        my_sizer.Add(self.my_browser, 0, wx.ALL | wx.EXPAND, 5)

        self.adb = AdbTool(self.adb_path)
        self.devices = []
        self.selected_device = None

        my_btn = wx.Button(self.panel, label='Scan Attached Devices')
        my_btn.Bind(wx.EVT_BUTTON, self.on_browse)
        my_sizer.Add(my_btn, 0, wx.ALL | wx.CENTER, 5)

        list_device_label = wx.StaticText(self.panel, style=wx.ST_NO_AUTORESIZE, label="List of devices attached:")
        my_sizer.Add(list_device_label, 0, wx.ALL | wx.EXPAND, 5)

        self.device_list = wx.ListCtrl(
            self.panel, size=(-1, 100), style=wx.LC_REPORT | wx.BORDER_SUNKEN | wx.LC_SORT_DESCENDING
        )
        self.device_list.InsertColumn(0, "Device Name", width=400)
        self.device_list.InsertColumn(1, "Status", width=200)
        my_sizer.Add(self.device_list, 0, wx.ALL | wx.EXPAND, 5)
        self.device_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_device_change)

        self.screenshot_label = wx.StaticText(self.panel, style=wx.ST_NO_AUTORESIZE, label="Screenshot Name:")
        my_sizer.Add(self.screenshot_label, 0, wx.ALL | wx.EXPAND, 5)

        self.screenshot_name_txt = wx.TextCtrl(self.panel)
        self.screenshot_name = None
        my_sizer.Add(self.screenshot_name_txt, 0, wx.ALL | wx.EXPAND, 5)
        self.screenshot_name_txt.Bind(wx.EVT_TEXT, self.on_screenshot_name_change)

        save_path_label = wx.StaticText(self.panel, style=wx.ST_NO_AUTORESIZE, label="Save Directory:")
        my_sizer.Add(save_path_label, 0, wx.ALL | wx.EXPAND, 5)

        self.download_path = self.config.Read("download_path", "Screenshots/")
        self.download_path_picker = wx.DirPickerCtrl(self.panel, path=self.download_path, message="Select Save Directory")

        self.download_path_picker.Bind(wx.EVT_DIRPICKER_CHANGED, self.on_change_download)
        my_sizer.Add(self.download_path_picker, 0, wx.ALL | wx.EXPAND, 5)

        self.capture_btn = wx.Button(self.panel, label='Capture Screenshot')
        self.capture_btn.Bind(wx.EVT_BUTTON, self.do_screenshot)
        my_sizer.Add(self.capture_btn, 0, wx.ALL | wx.CENTER, 5)

        self.build_path = self.config.Read("build_path", "Builds/")
        self.build_lists = []
        self.selected_build = None
        self.build_path_picker = wx.DirPickerCtrl(self.panel, path=self.build_path, message="Select Build Directory")
        self.build_path_picker.Bind(wx.EVT_DIRPICKER_CHANGED, self.on_change_build_path)
        my_sizer.Add(self.build_path_picker, 0, wx.ALL | wx.EXPAND, 5)

        build_filter_combo = wx.BoxSizer(wx.HORIZONTAL)
        build_filter_label = wx.StaticText(self.panel, style=wx.ST_NO_AUTORESIZE, label="Build Filter ")
        build_filter_combo.Add(build_filter_label, 0, wx.ALL | wx.CENTER, 5)

        self.build_filter_string = None
        self.build_list_filter = wx.TextCtrl(self.panel, size=wx.Size(300, 25))
        self.build_list_filter.Bind(wx.EVT_TEXT, self.on_build_filter)
        build_filter_combo.Add(self.build_list_filter, 0, wx.ALL | wx.CENTER, 5)
        my_sizer.Add(build_filter_combo, 0, wx.ALL | wx.LEFT, 5)

        self.build_files_list = wx.ListCtrl(
            self.panel, size=(-1, 200), style=wx.LC_REPORT | wx.BORDER_SUNKEN | wx.LC_SORT_DESCENDING
        )
        self.build_files_list.InsertColumn(0, "Name", width=340)
        self.build_files_list.InsertColumn(1, "Size (MB)", width=80)
        self.build_files_list.InsertColumn(2, "Date", width=180)
        self.build_files_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_build_select)
        self.build_files_list.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.on_build_deselect)
        my_sizer.Add(self.build_files_list, 0, wx.ALL | wx.EXPAND, 5)

        self.install_build_btn = wx.Button(self.panel, label='Install Selected Build')
        self.install_build_btn.Bind(wx.EVT_BUTTON, self.install_selected_build)
        my_sizer.Add(self.install_build_btn, 0, wx.ALL | wx.CENTER, 5)

        pkg_filter_combo = wx.BoxSizer(wx.HORIZONTAL)
        package_filter_label = wx.StaticText(self.panel, style=wx.ST_NO_AUTORESIZE, label="Package Filter ")
        pkg_filter_combo.Add(package_filter_label, 0, wx.ALL | wx.CENTER, 5)

        self.package_filter_string = None
        self.package_filter = wx.TextCtrl(self.panel, size=wx.Size(300, 25))
        self.package_filter.Bind(wx.EVT_TEXT, self.on_package_filter)
        pkg_filter_combo.Add(self.package_filter, 0, wx.ALL | wx.CENTER, 5)
        my_sizer.Add(pkg_filter_combo, 0, wx.ALL | wx.LEFT, 5)

        self.installed_packages = None
        self.selected_installed_package = None
        self.installed_package_list = wx.ListCtrl(
            self.panel, size=(-1, 200), style=wx.LC_REPORT | wx.BORDER_SUNKEN | wx.LC_SORT_DESCENDING
        )
        self.installed_package_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_installed_build_select)
        self.installed_package_list.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.on_installed_build_deselect)
        self.installed_package_list.InsertColumn(0, "Package Name", width=380)
        self.installed_package_list.InsertColumn(1, "Version", width=220)
        # self.installed_package_list.InsertColumn(2, "Date", width=180)
        my_sizer.Add(self.installed_package_list, 0, wx.ALL | wx.EXPAND, 5)

        self.uninstall_build_btn = wx.Button(self.panel, label='Uninstall Selected Build')
        self.uninstall_build_btn.Bind(wx.EVT_BUTTON, self.uninstall_selected_build)
        my_sizer.Add(self.uninstall_build_btn, 0, wx.ALL | wx.CENTER, 5)

        self.panel.SetSizer(my_sizer)
        # self.panel.SetAutoLayout(1)
        self.panel.SetupScrolling()

        self.Bind(wx.EVT_SIZING, self.on_window_resize)
        self.lock_win_size()
        self.disable_controls()
        self.Show()
        self.init_app()

    def init_app(self):
        logger.info("App initialize")
        try:
            self.on_change_build_path(self)
            logger.info("App init successfully!")
        except Exception as error:
            self.open_info_dialog("No build found!", "Warning")
            logger.error("App init failed: " + error.args[0])

    def disable_controls(self):
        self.selected_device = None
        self.capture_btn.Disable()
        self.install_build_btn.Disable()
        self.build_files_list.Disable()
        self.uninstall_build_btn.Disable()

    def enable_controls(self):
        self.capture_btn.Enable()
        self.build_files_list.Enable()
        if self.selected_build:
            self.install_build_btn.Enable()
        if self.selected_installed_package:
            self.uninstall_build_btn.Enable()

    def lock_win_size(self):
        # win_width = self.Rect.Width
        win_width = 650
        # win_height = self.Rect.Bottom + self.Rect.Top
        win_height = 700
        self.SetSize(win_width, win_height)
        # self.SetMaxSize(wx.Size(win_width, win_height))
        self.SetMinSize(wx.Size(win_width, win_height))
        self.Center()

    def on_window_resize(self, event):
        print(self.GetSize())

    def on_change_download(self, event):
        self.download_path = self.download_path_picker.GetPath()
        self.config.Write("download_path", self.download_path)
        logger.info("Change download path: " + self.download_path)

    def on_build_filter(self, event):
        self.build_filter_string = self.build_list_filter.GetValue()
        self.on_change_build_path(self)

    def on_package_filter(self, event):
        self.package_filter_string = self.package_filter.GetValue()
        self.load_installed_packages()

    def on_change_build_path(self, event):
        filter_string = self.build_filter_string if self.build_filter_string else ""
        self.build_files_list.DeleteAllItems()
        self.selected_build = None
        self.build_path = self.build_path_picker.GetPath()
        self.config.Write("build_path", self.build_path)
        build_files = glob.glob(self.build_path + "/*.apk")
        build_files = [b for b in build_files if filter_string in os.path.basename(b)]
        for i in range(len(build_files)):
            build_name = os.path.basename(build_files[i])
            self.build_files_list.InsertItem(i, "  " + build_name)
            self.build_files_list.SetItem(i, 1, str(round(os.path.getsize(build_files[i])/1048576, 2)))
            self.build_files_list.SetItem(i, 2, time.ctime(os.path.getmtime(build_files[i])))
            self.build_lists.append([build_files[i], build_name])
        logger.info("Load builds successfully at " + self.build_path)

    def on_build_select(self, event):
        self.selected_build = self.build_files_list.GetItemText(self.build_files_list.GetFirstSelected(), 0).strip()
        if self.selected_build and self.selected_device:
            self.install_build_btn.Enable()
        logger.info("Select build: " + self.selected_build)

    def on_build_deselect(self, event):
        self.selected_build = None
        self.install_build_btn.Disable()

    def on_installed_build_select(self, event):
        self.selected_installed_package = self.installed_package_list.GetItemText(self.installed_package_list.GetFirstSelected(), 0).strip()
        if self.selected_installed_package and self.selected_device:
            self.uninstall_build_btn.Enable()
        logger.info("Select installed package: " + self.selected_installed_package)

    def on_installed_build_deselect(self, event):
        self.selected_installed_package = None
        self.uninstall_build_btn.Disable()

    def install_selected_build(self, event):
        if not self.selected_device:
            self.open_info_dialog("No devices!!!", "Warning")
            logger.warning("No selected device")
        else:
            if self.selected_build:
                build_file = self.build_path + "/" + self.selected_build
                alert_msg = "Install Build To Selected Device"
                message = "Install build {}?".format(self.selected_build)
                alert = wx.MessageDialog(self, message=message, caption="Install selected build", style=wx.YES_NO)
                alert.SetYesNoLabels("Install", "Cancel")
                if alert.ShowModal() == wx.ID_NO:
                    logger.info("Installation cancelled")
                else:
                    logger.info("Install build {} to device {}".format(self.selected_build, self.selected_device.serial))
                    alert.SetMessage("Wait to complete...")
                    alert.Freeze()
                    try:
                        inst_status = self.selected_device.install_file(build_file, reinstall=True, grand_all_permissions=True)
                        inst_status_str = "Install successfully!" if inst_status else "Failed to install!"
                        self.open_info_dialog(inst_status_str, "Installation")
                        self.load_installed_packages()
                        logger.info(inst_status_str)
                    except Exception as error:
                        self.open_info_dialog(error.args[0], "Installation Failed")
                        logger.error(error.args[0])

    def uninstall_selected_build(self, event):
        if not self.selected_device:
            self.open_info_dialog("No devices!!!", "Warning")
            logger.info("No devices found")
        else:
            if self.selected_installed_package:
                message = "Uninstall package {}?".format(self.selected_installed_package)
                alert = wx.MessageDialog(self, message=message, caption="Uninstall selected package", style=wx.YES_NO)
                alert.SetYesNoLabels("Uninstall", "Cancel")
                if alert.ShowModal() == wx.ID_NO:
                    logger.info("Uninstallation cancelled")
                else:
                    logger.info("Uninstall {} from {}".format(self.selected_installed_package, self.selected_device.serial))
                    uninst_status = self.selected_device.uninstall_package(self.selected_installed_package)
                    uninst_status_str = "Uninstall successfully!" if uninst_status else "Failed to uninstall!"
                    self.open_info_dialog(uninst_status_str, "Uninstallion")
                    logger.info(uninst_status_str)
                self.load_installed_packages()

    def open_info_dialog(self, message, caption):
        alert = wx.MessageDialog(self, message=message, caption=caption, style=wx.OK)
        alert.ShowModal()

    def prepare_service(self):
        self.adb_path = self.my_browser.GetPath()
        adb_server = AdbTool(self.adb_path)
        if adb_server:
            self.config.Write("adb_path", self.adb_path)
            adb_server.start_adb_services()
            logger.info("Preparing ADB services")
            return adb_server
        else:
            self.open_info_dialog("ADB not found at: " + self.adb_path, "Error")
            logger.error("ADB not found at: {}".format(self.adb_path))
        return

    def on_browse(self, event):
        logger.info("Scan ADB devices")
        self.device_list.DeleteAllItems()
        try:
            self.adb = self.prepare_service()
            self.devices.clear()
            for device in self.adb.get_adb_devices():
                self.devices.append(device)
            if self.devices:
                # self.device_list.InsertItems([d.serial for d in self.devices], 0)
                for i in range(len(self.devices)):
                    self.device_list.InsertItem(i, " " + self.devices[i].serial)
                    self.device_list.SetItem(i, 1, self.devices[i].status)
            else:
                self.open_info_dialog("No devices found!", "Warning")
                logger.info("No devices found")
            logger.info("Device scan successfully: " + ''.join([d.serial for d in self.devices]))
        except Exception as error:
            self.disable_controls()
            self.open_info_dialog("Error to scan ADB devices.\n"
                                  "Make sure toConnect to your devices.", "Error")
            logger.error("Scan device: {}".format(error.args[0]))

    def on_device_change(self, event):
        self.selected_device = self.devices[self.device_list.GetFirstSelected()]
        logger.info("Select device: " + self.selected_device.serial)
        self.screenshot_name = self.selected_device.serial + "-" + datetime.now().strftime("%Y%m%d%H%M%S")
        self.screenshot_name_txt.SetLabelText(self.screenshot_name)
        if self.selected_device.is_device():
            self.enable_controls()
            self.load_installed_packages()
        else:
            self.on_browse(self)
            self.disable_controls()
            self.open_info_dialog("Error to scan ADB devices.\n"
                                  "Make sure your devices are connected and authorized.", "Error")
            logger.info("Selected device status: {}".format(self.selected_device.get_status()))

    def load_installed_packages(self):
        logger.info("Load installed package")
        self.installed_package_list.DeleteAllItems()
        self.selected_installed_package = None
        self.uninstall_build_btn.Disable()
        self.install_build_btn.Disable()
        filter_string = self.package_filter_string if self.package_filter_string else ""
        if self.selected_device:
            try:
                self.installed_packages = self.selected_device.get_installed_packages()
                filterred_installed_packages = [p for p in self.installed_packages if filter_string in str(p[0])]
                for i in range(len(filterred_installed_packages)):
                    self.installed_package_list.InsertItem(i, " " + str(filterred_installed_packages[i][0]))
                    self.installed_package_list.SetItem(i, 1, str(filterred_installed_packages[i][1]))
                logger.info("Load installed package Successfully ")
            except Exception as error:
                logger.error("Load installed package: " + error.args[0])

    def on_screenshot_name_change(self, event):
        self.screenshot_name = self.screenshot_name_txt.GetValue()

    def do_screenshot(self, event):
        logger.info("Taking screenshot")
        if self.selected_device:
            try:
                if self.screenshot_name:
                    self.selected_device.take_screen_shot(self.screenshot_name)
                    self.selected_device.pull_screen_shot(self.screenshot_name, self.download_path)
                    self.selected_device.clean_screen_shot(self.screenshot_name)
                    logger.info("Screenshot saved: " + os.path.join(self.download_path, self.screenshot_name+".png"))
                else:
                    self.open_info_dialog("Screenshot name is not empty!", "Error")
                    logger.error("Screenshot name is empty")
            except Exception as error:
                self.open_info_dialog("Cannot take screenshot!", "Error")
                logger.error("Take screenshot error: " + error.args[0])
        else:
            self.open_info_dialog("No device seleted!", "Error")
            logger.error("No devices selected")


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
