import os

class StripPort:

    def __init__(self, ip_address: str, index: int):
        self.ip_address = ip_address
        self.index = index

    def turn_on(self):
        self._on_off(True)

    def turn_off(self):
        self._on_off(False)

    def _on_off(self, on: bool):
        if on:
            command = "on"
        else:
            command = "off"
        os.system(f"kasa --type strip --host {self.ip_address} {command} --index {self.index}")

