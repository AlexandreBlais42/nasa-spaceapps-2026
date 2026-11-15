from api import get_image_map
import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFont
import datetime


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("NASA space app")
        self.geometry("900x600")
        self.minsize(600, 400)

        # Appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # variables
        self.image = None

        self.build()

    def build(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Title
        self.title = ctk.CTkLabel(
            self, text="NASA space app", font=("Arial", 24, "bold")
        )
        self.title.grid(row=0, column=0, pady=25)

        # Main frame
        self.mainFrame = ctk.CTkFrame(self, corner_radius=15)
        self.mainFrame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.mainFrame.columnconfigure(0, weight=1)

        self.paramsFrameDef()
        self.initDisplayFrame()

    def sendRequest(self):
        time = datetime.datetime.now()
        height_meters = 10
        coords = ((83.3362128, -141.00275), (41.6765597, -52.3237664))
        self.image = get_image_map(time, height_meters, coords, dimensions=[400, 300])

        if self.image == None:
            # display no data
            self.image = self.create_no_data_image()
        # udpate ui base on image
        self.updateDisplayFrame()

    def paramsFrameDef(self):
        # frame
        self.dataSelectionFrame = ctk.CTkFrame(self.mainFrame)
        self.dataSelectionFrame.grid(row=0, column=0, sticky="wn", padx=5, pady=5)

        # title
        self.paramsTitle = ctk.CTkLabel(
            self.dataSelectionFrame, text="Parameters", font=("Arial", 24, "bold")
        )
        self.paramsTitle.grid(row=0, column=0)

        # parmeters

        # send button
        self.sendRequestButton = ctk.CTkButton(
            self.dataSelectionFrame,
            text="Send Request",
            command=self.sendRequest,
            width=180,
            height=20,
        )
        self.sendRequestButton.grid(row=1, column=0, pady=5)

    def initDisplayFrame(self):
        # frame
        self.displayFrame = ctk.CTkFrame(self.mainFrame)
        self.displayFrame.grid(
            row=0, column=1, sticky="w", padx=5, pady=5, columnspan=2
        )

        # display image
        if self.image:
            image = self.image
        else:
            image = Image.open("src/images/terre.png")

        # Create CTkImage
        self.displayImage = ctk.CTkImage(
            light_image=image, dark_image=image, size=(400, 300)
        )
        # Display image
        self.imageLabel = ctk.CTkLabel(
            self.displayFrame, image=self.displayImage, text=""
        )
        self.imageLabel.grid(row=1, column=0, pady=20)

    def updateDisplayFrame(self):
        self.imageLabel.configure(image=None)
        self.displayImage = ctk.CTkImage(
            light_image=self.image, dark_image=self.image, size=(400, 300)
        )
        self.imageLabel.configure(image=self.displayImage)

    def create_no_data_image(self):
        width, height = 400, 300

        image = Image.new("RGB", (width, height), "#242424")
        draw = ImageDraw.Draw(image)

        text = "NO DATA"
        font = ImageFont.truetype("arial.ttf", 32)

        bbox = draw.textbbox((0, 0), text, font=font)
        x = (width - (bbox[2] - bbox[0])) / 2
        y = (height - (bbox[3] - bbox[1])) / 2

        draw.text((x, y), text, fill="#888888", font=font)

        return image


if __name__ == "__main__":
    app = App()
    app.mainloop()
