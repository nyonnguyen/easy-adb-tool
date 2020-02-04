import wx
import wx.adv
import wx.lib.scrolledpanel
from Helpers.adbservices import AdbTool
from datetime import datetime
import time
import os
import glob
from Helpers.adblog import AdbLog
from Pages import *

logger = AdbLog.get_logger("easy_android_tool")


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Easy Android Tool')
        self.config = wx.FileConfig(localFilename="adb_config")

        self.devices = []
        self.selected_device = None
        self.screenshot_name = None
        self.video_name = None
        self.video_length = None
        self.sc_download_path = self.config.Read("download_path", "Screenshots/")
        self.video_download_path = self.config.Read("v_download_path", "Videos/")
        self.build_lists = []
        self.selected_build = None
        self.build_filter_string = None
        self.installed_packages = None
        self.selected_installed_package = None
        self.package_filter_string = None
        self.build_path = self.config.Read("build_path", "Builds/")
        self.adb_path = self.config.Read("adb_path", "/usr/local/bin")
        self.adb = AdbTool(self.adb_path)

        self.SetBackgroundColour(wx.Colour(150, 150, 150))

        self.panel = wx.lib.scrolledpanel.ScrolledPanel(self)
        # self.panel = wx.Panel(self)
        my_sizer = wx.BoxSizer(wx.VERTICAL)

        self.device_section = wx.Notebook(self.panel)
        self.device_section = wx.Notebook(self.panel)
        self.device_tab = DeviceTab(self.device_section, self.adb_path)
        self.device_tab.my_browser.Bind(wx.EVT_DIRPICKER_CHANGED, self.on_browse)
        self.device_tab.scan_device_btn.Bind(wx.EVT_BUTTON, self.on_browse)
        self.device_tab.device_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_device_change)
        self.device_section.AddPage(self.device_tab, "Device Settings")
        my_sizer.Add(self.device_section, 0, wx.ALL | wx.EXPAND, 5)

        # Divide Take screenshot/Capture video to different tabs
        self.capture_section = wx.Notebook(self.panel)

        self.screenshot_tab = ScreenhotTab(self.capture_section, self.sc_download_path)
        self.screenshot_tab.screenshot_name_txt.Bind(wx.EVT_TEXT, self.on_screenshot_name_change)
        self.screenshot_tab.download_path_picker.Bind(wx.EVT_DIRPICKER_CHANGED, self.on_change_download)
        self.screenshot_tab.capture_btn.Bind(wx.EVT_BUTTON, self.do_screenshot)
        self.capture_section.AddPage(self.screenshot_tab, "ScreenShot")

        self.video_tab = VideoTab(self.capture_section, self.video_download_path)
        self.video_tab.video_name_txt.Bind(wx.EVT_TEXT, self.on_video_name_change)
        self.video_tab.download_path_picker.Bind(wx.EVT_DIRPICKER_CHANGED, self.on_change_video_download)
        self.video_tab.video_slider.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.on_video_length_change)
        self.video_tab.video_btn.Bind(wx.EVT_BUTTON, self.do_video)
        self.capture_section.AddPage(self.video_tab, "Video")

        my_sizer.Add(self.capture_section, 0, wx.ALL | wx.EXPAND, 5)

        # Divide Install/Uninstall to different tabs
        self.build_section = wx.Notebook(self.panel)

        self.build_tab = BuildTab(self.build_section, self.build_path)
        self.build_tab.build_list_filter.Bind(wx.EVT_TEXT, self.on_build_filter)
        self.build_tab.build_files_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_build_select)
        self.build_tab.build_files_list.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.on_build_deselect)
        self.build_tab.install_build_btn.Bind(wx.EVT_BUTTON, self.install_selected_build)
        self.build_tab.build_path_picker.Bind(wx.EVT_DIRPICKER_CHANGED, self.on_change_build_path)
        self.build_section.AddPage(self.build_tab, "Build Installation")

        self.package_tab = PackageTab(self.build_section)
        self.package_tab.package_filter.Bind(wx.EVT_TEXT, self.on_package_filter)
        self.package_tab.installed_package_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_installed_build_select)
        self.package_tab.installed_package_list.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.on_installed_build_deselect)
        self.package_tab.uninstall_build_btn.Bind(wx.EVT_BUTTON, self.uninstall_selected_build)

        self.build_section.AddPage(self.package_tab, "Installed Packages")

        my_sizer.Add(self.build_section, 0, wx.ALL | wx.EXPAND, 5)
        ########

        self.panel.SetSizer(my_sizer)
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
            self.video_length = self.video_tab.get_video_length()
            logger.info("App init successfully!")
        except Exception as error:
            self.open_info_dialog("No build found!", "Warning")
            logger.error("App init failed: " + error.args[0])

    def disable_controls(self):
        self.selected_device = None
        self.screenshot_tab.capture_btn.Disable()
        self.build_tab.install_build_btn.Disable()
        self.build_tab.build_files_list.Disable()
        self.package_tab.uninstall_build_btn.Disable()

    def enable_controls(self):
        self.screenshot_tab.capture_btn.Enable()
        self.build_tab.build_files_list.Enable()
        if self.selected_build:
            self.build_tab.install_build_btn.Enable()
        if self.selected_installed_package:
            self.package_tab.uninstall_build_btn.Enable()

    def lock_win_size(self):
        # win_width = self.Rect.Width
        win_width = 680
        # win_height = self.Rect.Bottom + self.Rect.Top
        win_height = 800
        self.SetSize(win_width, win_height)
        # self.SetMaxSize(wx.Size(win_width, win_height))
        self.SetMinSize(wx.Size(win_width, win_height))
        self.Center()

    def on_window_resize(self, event):
        print(self.GetSize())

    def on_change_download(self, event):
        self.sc_download_path = self.screenshot_tab.download_path_picker.GetPath()
        self.config.Write("download_path", self.sc_download_path)
        logger.info("Change download path: " + self.sc_download_path)

    def on_change_video_download(self, event):
        self.video_download_path = self.video_tab.download_path_picker.GetPath()
        self.config.Write("v_download_path", self.video_download_path)
        logger.info("Change download path: " + self.video_download_path)

    def on_video_length_change(self, event):
        self.video_length = self.video_tab.get_video_length()

    def on_build_filter(self, event):
        self.build_filter_string = self.build_tab.build_list_filter.GetValue()
        self.on_change_build_path(self)

    def on_package_filter(self, event):
        self.package_filter_string = self.package_tab.package_filter.GetValue()
        self.load_installed_packages()

    def on_change_build_path(self, event):
        filter_string = self.build_filter_string if self.build_filter_string else ""
        self.build_tab.build_files_list.DeleteAllItems()
        self.selected_build = None
        self.build_path = self.build_tab.build_path_picker.GetPath()
        self.config.Write("build_path", self.build_path)
        build_files = glob.glob(self.build_path + "/*.apk")
        build_files = [b for b in build_files if filter_string in os.path.basename(b)]
        for i in range(len(build_files)):
            build_name = os.path.basename(build_files[i])
            self.build_tab.build_files_list.InsertItem(i, "  " + build_name)
            self.build_tab.build_files_list.SetItem(i, 1, str(round(os.path.getsize(build_files[i])/1048576, 2)))
            self.build_tab.build_files_list.SetItem(i, 2, time.ctime(os.path.getmtime(build_files[i])))
            self.build_lists.append([build_files[i], build_name])
        logger.info("Load builds successfully at " + self.build_path)

    def on_build_select(self, event):
        self.selected_build = self.build_tab.build_files_list.GetItemText(self.build_tab.build_files_list.GetFirstSelected(), 0).strip()
        if self.selected_build and self.selected_device:
            self.build_tab.install_build_btn.Enable()
        logger.info("Select build: " + self.selected_build)

    def on_build_deselect(self, event):
        self.selected_build = None
        self.build_tab.install_build_btn.Disable()

    def on_installed_build_select(self, event):
        self.selected_installed_package = self.package_tab.installed_package_list.GetItemText(self.package_tab.installed_package_list.GetFirstSelected(), 0).strip()
        if self.selected_installed_package and self.selected_device:
            self.package_tab.uninstall_build_btn.Enable()
        logger.info("Select installed package: " + self.selected_installed_package)

    def on_installed_build_deselect(self, event):
        self.selected_installed_package = None
        self.package_tab.uninstall_build_btn.Disable()

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
        self.adb_path = self.device_tab.my_browser.GetPath()
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
        self.device_tab.device_list.DeleteAllItems()
        try:
            self.adb = self.prepare_service()
            self.devices.clear()
            for device in self.adb.get_adb_devices():
                self.devices.append(device)
            if self.devices:
                # self.device_list.InsertItems([d.serial for d in self.devices], 0)
                for i in range(len(self.devices)):
                    self.device_tab.device_list.InsertItem(i, " " + self.devices[i].serial)
                    self.device_tab.device_list.SetItem(i, 1, self.devices[i].status)
            else:
                self.open_info_dialog("No devices found!", "Warning")
                logger.info("No devices found")
            logger.info("Device scan successfully: " + ''.join([d.serial for d in self.devices]))
        except Exception as error:
            self.disable_controls()
            self.open_info_dialog("Error to scan ADB devices.\n"
                                  "Make sure devices are connected.", "Error")
            logger.error("Scan device: {}".format(error.args[0]))

    def on_device_change(self, event):
        self.selected_device = self.devices[self.device_tab.device_list.GetFirstSelected()]
        logger.info("Select device: " + self.selected_device.serial)
        self.renew_scrnshot_name()
        self.renew_video_name()
        if self.selected_device.is_device():
            self.enable_controls()
            self.load_installed_packages()
        else:
            self.on_browse(self)
            self.disable_controls()
            self.open_info_dialog("Error to scan ADB devices.\n"
                                  "Make sure your devices are connected and authorized.", "Error")
            logger.info("Selected device status: {}".format(self.selected_device.get_status()))

    def renew_scrnshot_name(self):
        self.screenshot_name = "IMG-" + self.selected_device.serial + "-" + datetime.now().strftime("%Y%m%d%H%M%S")
        self.screenshot_tab.screenshot_name_txt.SetLabelText(self.screenshot_name)

    def renew_video_name(self):
        self.video_name = "VIDEO-" + self.selected_device.serial + "-" + datetime.now().strftime("%Y%m%d%H%M%S")
        self.video_tab.video_name_txt.SetLabelText(self.video_name)

    def load_installed_packages(self):
        logger.info("Load installed package")
        self.package_tab.installed_package_list.DeleteAllItems()
        self.package_tab.uninstall_build_btn.Disable()
        filter_string = self.package_filter_string if self.package_filter_string else ""
        if self.selected_device:
            try:
                self.installed_packages = self.selected_device.get_installed_packages()
                filterred_installed_packages = [p for p in self.installed_packages if filter_string in str(p[0])]
                for i in range(len(filterred_installed_packages)):
                    self.package_tab.installed_package_list.InsertItem(i, " " + str(filterred_installed_packages[i][0]))
                    self.package_tab.installed_package_list.SetItem(i, 1, str(filterred_installed_packages[i][1]))
                logger.info("Load installed package Successfully ")
            except Exception as error:
                logger.error("Load installed package: " + error.args[0])

    def on_screenshot_name_change(self, event):
        self.screenshot_name = self.screenshot_tab.screenshot_name_txt.GetValue()

    def on_video_name_change(self, event):
        self.video_name = self.video_tab.video_name_txt.GetValue()

    def do_screenshot(self, event):
        logger.info("Taking screenshot")
        if self.selected_device:
            try:
                if self.screenshot_name:
                    self.selected_device.take_screen_shot(self.screenshot_name)
                    self.selected_device.pull_screen_shot(self.screenshot_name, self.sc_download_path)
                    self.selected_device.clean_screen_shot(self.screenshot_name)
                    actual_screenshot_name = os.path.join(self.sc_download_path, self.screenshot_name+".png")
                    self.renew_scrnshot_name()
                    self.open_info_dialog(actual_screenshot_name, "ScreenShot Captured")
                    logger.info("Screenshot saved: " + actual_screenshot_name)
                else:
                    self.open_info_dialog("Screenshot name is not empty!", "Error")
                    logger.error("Screenshot name is empty")
            except Exception as error:
                self.open_info_dialog("Cannot take screenshot!", "Error")
                logger.error("Take screenshot error: " + error.args[0])
        else:
            self.open_info_dialog("No device seleted!", "Error")
            logger.error("No devices selected")

    def do_video(self, event):
        logger.info("Taking video")
        if self.selected_device:
            try:
                if self.video_name:
                    self.selected_device.take_video(self.video_name, self.video_length)
                    self.selected_device.pull_video(self.video_name, self.video_download_path)
                    self.selected_device.clean_video(self.video_name)
                    actual_video_name = os.path.join(self.video_download_path, self.video_name + ".mp4")
                    self.renew_video_name()
                    self.open_info_dialog(actual_video_name, "Video Captured")
                    logger.info("Video saved: " + actual_video_name)
                else:
                    self.open_info_dialog("Video name is not empty!", "Error")
                    logger.error("Video name is empty")
            except Exception as error:
                self.open_info_dialog("Cannot take video!", "Error")
                logger.error("Take video error: " + error.args[0])
        else:
            self.open_info_dialog("No device seleted!", "Error")
            logger.error("No devices selected")


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
