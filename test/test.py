# from ppadb.client import Client as AdbClient
# # Default is "127.0.0.1" and 5037
# client = AdbClient(host="127.0.0.1", port=5037)
# print(client.version())


# from ppadb.client import Client as AdbClient
# # Default is "127.0.0.1" and 5037
# client = AdbClient(host="127.0.0.1", port=5037)
# device = client.device("emulator-5554")



from ppadb.client import Client as AdbClient

apk_path = "example.apk"

# Default is "127.0.0.1" and 5037
client = AdbClient()
devices = client.devices()
print(devices)

for device in devices:
    device.install(apk_path)

# Check apk is installed
for device in devices:
    print(device.is_installed("example.package"))

# Uninstall
for device in devices:
    device.uninstall("example.package")

result = device.screencap()
with open("screen.png", "wb") as fp:
    fp.write(result)