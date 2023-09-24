import os
from tkinter import Tk, Frame, Text, Label, PhotoImage, BitmapImage
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk as itk
from ksigner import open_and_hash_file, make_qr_code_image

class ksigner(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.wm_title("Ksigner")
        # self.option_add("*Foreground", "grey")
        # self.option_add("*Background", "black")
        self.main_container = Frame(self)
        self.main_container.pack(fill="both", expand=True)
        # Buttons
        self.buttons_panel = Frame(self.main_container)
        self.buttons_panel.grid(column=0, row=0, sticky='nsew')
        open_button = ttk.Button(
            self.buttons_panel,
            text='Open a File to Sign',
            command=self.open_file_to_hash
        )

        open_button.pack(side="right", fill="both", expand=True)

        # Info box
        self.info_panel = Frame(self.main_container)
        self.info_panel.grid(column=0, row=1, sticky='nsew')
        self.text = Text(self.info_panel, height=4)
        self.text.pack(side="right", fill="both", expand=True)

        # QRs and Camera panel
        self.qr_cam_panel = Frame(self.main_container)
        self.qr_cam_panel.grid(column=0, row=2, sticky='nsew')
        krux_logo_path = os.path.join( "assets", "krux.png")
        self.im = PhotoImage(file=krux_logo_path)
        self.label_qr = Label(self.qr_cam_panel, image=self.im)
        self.label_qr.pack(side="right", fill="both", expand=True)

    def open_file_to_hash(self):
        # file type
        filetypes = (
            ('All files', '*.*'),
            ('bin files', '*.bin')
        )
        # show the open file dialog
        to_sign_file = filedialog.askopenfilename(filetypes=filetypes)
        # shows the hash of the file
        hash_text = "File hash: " + open_and_hash_file(path=to_sign_file)
        self.text.insert("1.0", hash_text)
        qr_image = itk.PhotoImage(make_qr_code_image(data=hash_text))
        self.label_qr.config(image=qr_image)
        self.label_qr.image = qr_image

app = ksigner()
app.mainloop()
