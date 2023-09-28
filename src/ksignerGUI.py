"""
ksignerGUI.py

A simple Graphical User Interface version
of ksigner-cli.py based o tkinter.

TODO: rebuild to kivy?    
"""

####################
# Standard libraries
####################
import os
import base64
from tkinter import Tk
from tkinter import Frame
from tkinter import Text
from tkinter import Label
from tkinter import PhotoImage
#from tkinter import BitmapImage
from tkinter import ttk
from tkinter import filedialog

#######################
# Third party libraries
#######################
import cv2
from PIL import ImageTk, Image

#################
# Local libraries
#################
from hashutils import open_and_hash_file
from qrutils import make_qr_code_image

# Scanned object types
SIGNATURE = 0
PUB_KEY = 1

class KSignerTk(Tk):
    """
    class KSignerTk

    an implementation of ksigner-cli in Tk GUI
    """

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.wm_title("Ksigner")
        # self.option_add("*Foreground", "grey")
        # self.option_add("*Background", "black")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=4)
        # self.main_container = Frame(self)
        # self.main_container.pack(fill="both", expand=True)

        # Variables
        self.file_to_sign = None
        self.qr_object = SIGNATURE

        # Buttons
        self.buttons_panel = Frame()
        self.buttons_panel.grid(column=0, row=0, sticky="nsew")
        open_button = ttk.Button(
            self.buttons_panel,
            text="Open a File to Sign",
            command=self.open_file_to_hash,
        )
        open_button.pack(side="left", fill="both", expand=True)

        self.scan_sig_button = ttk.Button(
            self.buttons_panel,
            text="Scan and Save Signature",
            command=self.capture_signature,
            state="disabled",
        )
        self.scan_sig_button.pack(side="left", fill="both", expand=True)

        scan_pb_key_button = ttk.Button(
            self.buttons_panel,
            text="Scan and Save Private Key",
            # command=self.open_file_to_hash,
            state="disabled",
        )
        scan_pb_key_button.pack(side="left", fill="both", expand=True)

        # Info box
        self.info_panel = Frame()
        self.info_panel.grid(column=0, row=1, sticky="nsew")
        self.text = Text(self.info_panel, height=4)
        self.text.pack(side="right", fill="both", expand=True)

        # QRs and Camera panel
        self.qr_panel = Frame()
        self.qr_panel.grid(column=0, row=2, sticky="nsew")
        krux_logo_path = os.path.join("assets", "krux.png")
        self.krux_logo_image = PhotoImage(file=krux_logo_path)
        self.label_qr = Label(self.qr_panel, image=self.krux_logo_image)
        self.label_qr.pack(side="right", fill="both", expand=True)

        self.cam_panel = Frame()
        self.cam_panel.grid(column=0, row=2, sticky="nsew")
        self.cam_panel.grid_remove()
        self.cap = None
        self.detector = cv2.QRCodeDetector()
        self.cam_label = Label(self.cam_panel)
        self.cam_label.pack(side="left", fill="both", expand=True)

    def open_file_to_hash(self):
        """
        open_file_to_hash

        Open a file and create a hash for it
        """
        
        # file type
        filetypes = (("All files", "*.*"), ("bin files", "*.bin"))
        # show the open file dialog
        self.file_to_sign = filedialog.askopenfilename(filetypes=filetypes)
        if not isinstance(self.file_to_sign, str):
            return
        # shows the hash of the file
        hash_text = "File hash: " + open_and_hash_file(path=self.file_to_sign)
        self.text.insert("1.0", hash_text + "\n")
        qr_image = ImageTk.PhotoImage(make_qr_code_image(data=hash_text))
        self.label_qr.config(image=qr_image)
        self.label_qr.image = qr_image
        self.scan_sig_button["state"] = "normal"

    def capture_qr_code(self):
        """
        capture_qr_code

        capture QRCode from camera
        """
        _, frame = self.cap.read()
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        cam_image = ImageTk.PhotoImage(image=img)
        self.cam_label.config(image=cam_image)
        self.label_qr.image = cam_image
        qr_data, _bbox, _straight_qrcode = self.detector.detectAndDecode(frame)

        if len(qr_data) > 0:
            if self.qr_object == SIGNATURE:
                self.save_signature(qr_data)
            elif self.qr_object == PUB_KEY:
                self.save_pub_key(qr_data)
            self.cap.release()
            return
        self.after(1, self.capture_qr_code)

    def detach_cam(self):
        """
        detach_cam

        detachs camera to avoid new capture 
        """
        self.cam_panel.grid_remove()
        self.label_qr.config(image=self.krux_logo_image)
        self.label_qr.image = self.krux_logo_image

    def capture_signature(self):
        """
        capture_signature

        capture the qrcode from the krux device
        """
        self.cam_panel.grid()
        self.qr_object = SIGNATURE
        self.cap = cv2.VideoCapture(0)
        self.capture_qr_code()

    def save_signature(self, signature):
        """
        save_signature

        gets signature generated from qrcode
        and create a text file on computer
        """
        # Encode data
        binary_signature = base64.b64decode(signature.encode())
        # Saves a signature
        signature_file = f"{self.file_to_sign}.sig"
        with open(signature_file, "wb") as sig_file:
            sig_file.write(binary_signature)
        self.text.insert("1.0", f"Saved signature file: {signature_file}\n")
        self.detach_cam()

    def save_pub_key(self, pubkey):
        """
        save_pubkey

        TODO
        """
        pass


app = KSignerTk()
app.mainloop()
