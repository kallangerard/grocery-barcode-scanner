import os

import usb.core
import usb.util


class Scan(object):
    base_url = None
    api_key = None

    def __init__(self, **kwds):
        # idVendor=0x05E0, idProduct=0x1200 Symbol Scanner

        if "SCANNER_VENDOR_ID" in os.environ:
            self.idVendor = os.environ["SCANNER_ID_VENDOR"]

        if "SCANNER_PRODUCT_ID" in os.environ:
            self.idProduct = os.environ["SCANNER_ID_PRODUCT"]

        for key in kwds:
            self.__dict__[key] = kwds[key]

        if self.idVendor is None or self.idProduct is None:
            # TODO: Logging
            pass

        # Find our device using the VID (Vendor ID) and PID (Product ID)
        device = usb.core.find(idVendor=self.idVendor, idProduct=self.idProduct)
        if device is None:
            raise ValueError("USB device not found")

        # Disconnect scanner from kernel so it doesn't input to terminal
        self.needs_reattach = False
        if device.is_kernel_driver_active(0):
            self.needs_reattach = True
            device.detach_kernel_driver(0)

        device.set_configuration()
        configuration = device.get_active_configuration()
        interface = configuration[(0, 0)]

        self.endpoint = usb.util.find_descriptor(
            interface,
            # match the first IN endpoint
            custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress)
            == usb.util.ENDPOINT_IN,
        )

    def Hid2Ascii(self, byte_array):
        conversion_table = {
            0: ["", ""],
            4: ["a", "A"],
            5: ["b", "B"],
            6: ["c", "C"],
            7: ["d", "D"],
            8: ["e", "E"],
            9: ["f", "F"],
            10: ["g", "G"],
            11: ["h", "H"],
            12: ["i", "I"],
            13: ["j", "J"],
            14: ["k", "K"],
            15: ["l", "L"],
            16: ["m", "M"],
            17: ["n", "N"],
            18: ["o", "O"],
            19: ["p", "P"],
            20: ["q", "Q"],
            21: ["r", "R"],
            22: ["s", "S"],
            23: ["t", "T"],
            24: ["u", "U"],
            25: ["v", "V"],
            26: ["w", "W"],
            27: ["x", "X"],
            28: ["y", "Y"],
            29: ["z", "Z"],
            30: ["1", "!"],
            31: ["2", "@"],
            32: ["3", "#"],
            33: ["4", "$"],
            34: ["5", "%"],
            35: ["6", "^"],
            36: ["7", "&"],
            37: ["8", "*"],
            38: ["9", "("],
            39: ["0", ")"],
            40: ["\n", "\n"],
            41: ["\x1b", "\x1b"],
            42: ["\b", "\b"],
            43: ["\t", "\t"],
            44: [" ", " "],
            45: ["_", "_"],
            46: ["=", "+"],
            47: ["[", "{"],
            48: ["]", "}"],
            49: ["\\", "|"],
            50: ["#", "~"],
            51: [";", ":"],
            52: ["'", '"'],
            53: ["`", "~"],
            54: [",", "<"],
            55: [".", ">"],
            56: ["/", "?"],
            100: ["\\", "|"],
            103: ["=", "="],
        }

        if byte_array[0] == 2:
            shift = 1
        else:
            shift = 0

        # The character to convert is in the third byte
        character = byte_array[2]
        if character not in conversion_table:
            # TODO: Logging
            print("Warning: data not in conversion table")
            return ""
        return conversion_table[character][shift]

    def PollScanner(self):
        line = ""
        data = ""
        while True:
            try:
                # Read 8 Bytes, Wait up to 200ms
                byte_array = self.endpoint.read(8, 200)
                # Until Carriage Return from Scanner (40)
                if data[2] == 40:
                    # TODO: Submit Barcode String Here
                    line = ""
                    continue
                character = self.Hid2Ascii(byte_array)
                line += character
            except usb.core.USBError:
                # Timed out. End of the data stream.
                line = ""
