from pathlib import Path
from bluetooth.ble import BeaconService
from datetime import datetime

class Beacon:

    def __init__(self, data, address):
        self._uuid = data[0]
        self._major = data[1]
        self._minor = data[2]
        self._power = data[3]
        self._rssi = data[4]
        self._address = address

    def __str__(self):
        ret = "Beacon: address:{ADDR} uuid:{UUID} major:{MAJOR} " \
              "minor:{MINOR} txpower:{POWER} rssi:{RSSI}" \
              .format(ADDR=self._address, UUID=self._uuid, MAJOR=self._major,
                      MINOR=self._minor, POWER=self._power, RSSI=self._rssi)
        return ret

value = 'key_control'

# Initialize control file
control_file = Path(value).resolve()
control_file.touch()
control_file.chmod(0o777)
with control_file.open(mode='w') as f:
    f.write("1")

control_file_handle = None

with open(control_file, 'w') as f:
    f.write("1")

control_file_handle = control_file.open(mode='r+')

# Initialize bluetooth
BLE_DEVICE = "hci0"
service = BeaconService(BLE_DEVICE)

run = True
while run:
    control_file_handle.seek(0)
    control_flag = control_file_handle.read()
    # 0 = off
    # 1 = on
    # 2 = scan

    if control_flag == "0":
        run = False
        print('done')
    if control_flag == "1":
        continue
    if control_flag == "2":
        print('scan')
        service = BeaconService()
        devices = service.scan(1)

        print(datetime.now())
        for address, data in list(devices.items()):
            b = Beacon(data, address)
            print(b)

        print("Done.")
        with open(control_file, 'w') as f:
            f.write("1")
    if control_flag == "3":
        run = False
        print('done')

if control_file_handle is not None:
    control_file_handle.close()
control_file.unlink()