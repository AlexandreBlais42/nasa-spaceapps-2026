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
        height_meters = int(self.heightBar.get())
        coords = ((83.3362128, -141.00275), (41.6765597, -52.3237664))
        self.image = get_image_map(time, height_meters, coords, dimensions=[400, 300])

        if self.image == None:
            # display no data
            self.image = self.createNoDataImage()
        # udpate ui base on image
        self.updateDisplayFrame()

    def paramsFrameDef(self):
        # frame
        self.dataSelectionFrame = ctk.CTkFrame(self.mainFrame)
        self.dataSelectionFrame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # title
        self.paramsTitle = ctk.CTkLabel(
            self.dataSelectionFrame, text="Parameters", font=("Arial", 24, "bold")
        )
        self.paramsTitle.grid(row=0, column=0)

        # parameters
        #location
        self.locationFrame = ctk.CTkFrame(self.dataSelectionFrame)
        self.locationFrame.grid(row=2, column=0, sticky="ew")
        ctk.CTkLabel(self.locationFrame, text="Location", font=("Comic Sans MS", 18, "bold")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        ctk.CTkLabel(self.locationFrame, text="Region").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.region = ctk.CTkComboBox(self.locationFrame, values=["Montreal", "Sherbrooke", "Quebec", "Toronto"])
        self.region.set("Montreal")
        self.region.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(self.locationFrame, text="Latitude N/S").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.latitude1 = ctk.CTkEntry(self.locationFrame, placeholder_text="0.000")
        self.latitude2 = ctk.CTkEntry(self.locationFrame, placeholder_text="0.000")
        self.latitude1.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.latitude2.grid(row=2, column=2, padx=10, pady=5, sticky="w")
        
        ctk.CTkLabel(self.locationFrame, text="Longitude W/E").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.longitude1 = ctk.CTkEntry(self.locationFrame, placeholder_text="0.000")
        self.longitude2 = ctk.CTkEntry(self.locationFrame, placeholder_text="0.000")
        self.longitude1.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        self.longitude2.grid(row=3, column=2, padx=10, pady=5, sticky="w")
        
        ctk.CTkLabel(self.locationFrame, text="Sampling mode").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.coordsMode = ctk.StringVar(value="point")        
        def updateCoordsMode():
            if self.coordsMode.get() == "rectangle":
                self.coordsSwitch.configure(text="Rectangle")
            else:
                self.coordsSwitch.configure(text="Point")
        self.coordsSwitch = ctk.CTkSwitch(self.locationFrame,
            text="Point",
            variable=self.coordsMode,
            onvalue="rectangle",
            offvalue="point",
            command=updateCoordsMode
        )
        self.coordsSwitch.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        
        
        
        
        # height slider
        self.heightBar = ctk.CTkSlider(
            self.dataSelectionFrame,
            from_=0,
            to=10,
            number_of_steps=10,
            command=self.updateHeight,
        )
        self.heightBar.grid(row=1, column=0, padx=10, pady=10)
        self.heightBar.set(0)

        # send button
        self.sendRequestButton = ctk.CTkButton(
            self.dataSelectionFrame,
            text="Send Request",
            command=self.sendRequest,
            width=180,
            height=20,
        )
        self.sendRequestButton.grid(row=5, column=0, pady=5)

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

    def createNoDataImage(self):
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

    def updateHeight(self, value):
        self.heightBar.configure(text=f"Height: {int(value)}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
