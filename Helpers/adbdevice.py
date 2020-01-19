from ppadb.device import Device
import re

SCREEN_SHOT_SOURCE = "/sdcard/{}.png"
SCREEN_SHOT_DEST = "{}/{}.png"
REMOVE_FILE_CMD = "rm -f /sdcard/{}.{}"
PACKAGE_VERSION_DUMP_CMD = "dumpsys package packages | grep -E 'Package \[|versionName'"
PACKAGE_VERSION_RGX = "Package \[(.*)\].*\s*versionName=(.*)"


class AdbDevice(Device):
    def __init__(self, client, serial, status):
        Device.__init__(self, client, serial)
        self.status = status

    def get_status(self):
        return self.status

    def is_offline(self):
        return self.status == "offline"

    def is_device(self):
        return self.status == "device"

    def is_unauthorize(self):
        return self.status == "unauthorize"

    def take_screen_shot(self, filename):
        conn = self.create_connection()

        with conn:
            cmd = "shell:/system/bin/screencap -p " + SCREEN_SHOT_SOURCE
            conn.send(cmd.format(filename))
            result = conn.read_all()
        return result

    def pull_screen_shot(self, filename, dest_path):
        return self.pull(SCREEN_SHOT_SOURCE.format(filename), SCREEN_SHOT_DEST.format(dest_path, filename))

    def clean_screen_shot(self, filename):
        return self.shell(REMOVE_FILE_CMD.format(filename, "png"))

    def install_file(self, file,
                     forward_lock=False,  # -l
                     reinstall=False,  # -r
                     test=False,  # -t
                     installer_package_name=False,  # -i
                     shared_mass_storage=False,  # -s
                     internal_system_memory=False,  # -f
                     downgrade=False,  # -d
                     grand_all_permissions=False  # -g
                     ):
        return self.install(file, forward_lock, reinstall, test, installer_package_name,
                            shared_mass_storage, internal_system_memory, downgrade,
                            grand_all_permissions)

    def get_installed_packages(self):
        raw_list = self.shell(PACKAGE_VERSION_DUMP_CMD)
        pkg_regx = PACKAGE_VERSION_RGX
        return re.findall(pkg_regx, raw_list)

    def uninstall_package(self, pkg_name):
        return self.uninstall(pkg_name)
