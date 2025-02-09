import tkinter as tk
from pymodbus.client import ModbusTcpClient
import asyncio

class ModbusExample:

    DEFAULT_ADDR = "192.168.1.128"
    DEFAULT_PORT = 502

    COLOR_FORMAT_STRING = "#%02x%02x%02x"
    MAC_FORMAT_STRING = "#%02x:%02x:%02x:%02x:%02x"
    IP_FORMAT_STRING = "%d,%d,%d,%d"

    CONNECT_COLOR = COLOR_FORMAT_STRING % (0, 255, 0)
    DISCONNECT_COLOR = COLOR_FORMAT_STRING % (255, 0, 0)

    ON_COLOUR = COLOR_FORMAT_STRING % (56, 177, 224)
    OFF_COLOUR = COLOR_FORMAT_STRING % (87, 32, 32)

    # REGISTER MAP

    EN_COIL_ADDR = 10001
    BRIGHTNESS_INPUT_ADDR = 20001
    
    RED_CHAN_INPUT_ADDR = 20002
    GREEN_CHAN_INPUT_ADDR = 20003
    BLUE_CHAN_INPUT_ADDR = 20004
    BRIGHTNESS_INPUT_ADDR = 20005

    UID_HOLDING_REG = 40001
    MAC_HOLDING_RED = 40002


    def __init__(self, master):

        self.en_bool = False
        self.r_int = 0
        self.b_int = 0
        self.g_int = 0
        
        self.ip_addr = ModbusExample.DEFAULT_ADDR
        self.mac = 0
        self.uid = 0

        self.client = ModbusTcpClient(host=self.ip_addr, port=ModbusExample.DEFAULT_PORT)

        self.master = master
        self.master.title("Modbus Example App")
        self.master.geometry("500x450")

        # First Column of data in column 0 & 1, leave 2 blank

        # Enable Button
        self.en_label = tk.Label(self.master, text="Neo Pixel:")
        self.en_label.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
        self.en_button = tk.Button(self.master, text="Off", command=self.on_en_click)
        self.en_button.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Red slider
        self.r_label = tk.Label(self.master, text="Red Slider:")
        self.r_label.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
        self.r_slider = tk.Scale(self.master, from_=0, to=255, orient="horizontal", command=self.on_value_change)
        self.r_slider.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Blue Slider
        self.b_label = tk.Label(self.master, text="Blue Slider:")
        self.b_label.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")
        self.b_slider = tk.Scale(self.master, from_=0, to=255, orient="horizontal", command=self.on_value_change)
        self.b_slider.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
        
        # Green Slider
        self.g_label = tk.Label(self.master, text="Green Slider:")
        self.g_label.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")        
        self.g_slider = tk.Scale(self.master, from_=0, to=255, orient="horizontal", command=self.on_value_change)
        self.g_slider.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")

        # Brightness Slider
        self.bright_label = tk.Label(self.master, text="Brightness Slider:")
        self.bright_label.grid(row=4, column=0, padx=5, pady=10, sticky="nsew")        
        self.bright_slider = tk.Scale(self.master, from_=0, to=255, orient="horizontal", command=self.on_value_change)
        self.bright_slider.grid(row=4, column=1, padx=10, pady=10, sticky="nsew")

        # Color Set Button
        self.c_set_label = tk.Label(self.master, text="Set Color:")
        self.c_set_label.grid(row=5, column=0, padx=5, pady=10, sticky="nsew")
        self.c_set_button = tk.Button(self.master, text="Set", command=self.on_c_set_click)
        self.c_set_button.grid(row=5, column=1, padx=10, pady=10, sticky="nsew")

        # Column 2 

        # IP Label
        self.ip_label = tk.Label(self.master, text="IP: ")
        self.ip_label.grid(row=0, column=3, padx=5, pady=10, sticky="nsew")
        self.ip_entry = tk.Entry(self.master)
        self.ip_entry.grid(row=0, column=4, padx=10, pady=10, sticky="nsew")

        # UID Label
        self.uid_label = tk.Label(self.master, text="UID: ")
        self.uid_label.grid(row=1, column=3, padx=5, pady=10, sticky="nsew")

        # MAC Label
        self.mac_label = tk.Label(self.master, text="MAC: ")
        self.mac_label.grid(row=2, column=3, padx=5, pady=10, sticky="nsew")

        # Connect Button
        self.connect_button = tk.Button(self.master, text="Connect", command=self.on_connect_click)
        self.connect_button.grid(row=3, column=4, padx=10, pady=10, sticky="nsew")

        self.debug_label = tk.Label(self.master, text="Nothing ... ", bg="gray")
        self.debug_label.grid(row=6, column=1, columnspan=4, rowspan=7, padx=10, pady=10, sticky="nsew")

        asyncio.run(self.modbus_daemon())

    def on_value_change(self, value):
        r_int = int(self.r_slider.get())
        b_int = int(self.b_slider.get())
        g_int = int(self.g_slider.get())

        c = f"#{r_int:02x}{b_int:02x}{g_int:02x}"

        self.c_set_button.config(bg=c)


    def on_en_click(self):
        if self.client.connected:
            self.en_bool = not self.en_bool
            if self.en_bool:
                self.en_button.config(text="On", bg=ModbusExample.ON_COLOUR)
                self.client.write_coil(address=ModbusExample.EN_COIL_ADDR, value=True)
            else:
                self.en_button.config(text="Off", bg=ModbusExample.OFF_COLOUR)
                self.client.write_coil(address=ModbusExample.EN_COIL_ADDR, value=False)

    def on_c_set_click(self):
        # Send over modbus
        # use r_int, b_int, g_int
        if self.client.connected:
            self.client.write_registers(ModbusExample.RED_CHAN_INPUT_ADDR, values=list([self.r_int, self.g_int, self.b_int]))

    def on_connect_click(self):
        self.ip_addr = self.ip_entry.get()
        self.mac = 0
        self.uid = 0
        if self.ip_addr:
            # connect to the device
            self.client = ModbusTcpClient(host=self.ip_addr, port=ModbusExample.DEFAULT_PORT)
            if(self.client.connect()):

                # update labels
                self.uid = self.client.read_holding_registers(address=ModbusExample.UID_HOLDING_REG, count= 1)
                self.mac = ModbusExample.MAC_FORMAT_STRING % self.client.read_holding_registers(address=ModbusExample.MAC_HOLDING_RED, count= 5 )

                self.uid_label.config(text=f"UID: {self.uid}")
                self.mac_label.config(text=f"MAC {self.mac}")

                self.connect_button.config(bg=ModbusExample.CONNECT_COLOR)

    async def modbus_daemon(self):
        if not self.client:
            if not self.client.connected:
                self.close()
                self.connect_button.config(bg=ModbusExample.DISCONNECT_COLOR)


if __name__ == "__main__":
    root = tk.Tk()
    app = ModbusExample(root)
    root.mainloop()