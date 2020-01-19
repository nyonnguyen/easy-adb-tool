from ppadb.client import Client as AdbClient
from Helpers.adbdevice import AdbDevice
import os
import subprocess


class AdbTool(AdbClient):
    def __init__(self, adb_path):
        AdbClient.__init__(self)
        self.target_device = None
        self.adb_path = adb_path

    def get_device_string(self):
        return self.target_device.serial

    def get_adb_devices(self,):
        cmd = "host:devices"
        result = self._execute_cmd(cmd)
        devices = []
        for line in result.split('\n'):
            if not line:
                break
            tokens = line.split()
            if len(tokens) > 1:
                devices.append(AdbDevice(self, tokens[0], tokens[1]))
        return devices

    def set_adb_path(self, path):
        self.adb_path = path

    def get_adb_path(self):
        return self.adb_path

    def run_cmd(self, cmd):
        return self._execute_cmd(cmd)

    def start_adb_services(self):
        subprocess.run([os.path.join(self.adb_path, "adb"), "kill-server"])
        subprocess.run([os.path.join(self.adb_path, "adb"), "start-server"])
