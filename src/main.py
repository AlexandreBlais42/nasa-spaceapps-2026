from api import get_image_map
import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFont
import datetime
import regression
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

urbanDictionnary = {
    "Montreal"      : (45.50884, -73.58781),
    "Sherbrooke"    : (45.40008, -71.89908),
    "Quebec"        : (46.82985, -71.25403),
    "Toronto"       : (43.70011, -79.41630),
    "Vancouver"     : (49.24966, -123.1193),
    "Ottawa"        : (45.41117, -75.69812),
    "Edmonton"      : (53.55014, -113.4687),
    "Victoria"      : (48.43294, -123.3693),
    "Winnipeg"      : (49.88440, -97.14704),
    "Regina"        : (50.45008, -104.6178),
    "Bangkok"       : (13.75398, 100.50144),
    "Paris"         : (48.85341,   2.34880),
    "Rome"          : (41.89193,  12.51133),
    "Venice"        : (45.43713,  12.33265),
    "New York City" : (40.71427, -74.00597),
    "Boston"        : (42.35843, -71.05977),
    "Philadelphia"  : (39.95233, -75.16379),
    "Buenos Aires"  : (-34.6131, -58.37723),
    "Madrid"        : (40.41650,  -3.70256),
    "Barcelona"     : (41.38879,   2.15899),
    "Sydney"        : (-33.86785, 151.2073),
    "Lima"          : (-12.04318, -77.0282),
    "Wellington"    : (-32.55588, 148.9451),
    "Manila"        : (14.604200, 120.9822),
}

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
        self.columnconfigure(1, weight=1)
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
        """
        stuff a faire mais flemme pcq je suis seule
        time = timestart (les 6 boites)
        if timeSwitch is on, time = timestart -- timestop :P timeStep 
        
        les variables sont dans selected
        
        le coords c'est latitude1, latitude2
        if coordsMode is on faut donner aussi la résolution et prendre (lat1,lon1),(lat2,lon2)
        """
        
        time = datetime.datetime.now()
        height_meters = 2
        coords = ((self.latitude1.get(), self.longitude1.get()), (self.latitude1.get(), self.longitude2.get()))
        self.image = get_image_map(time, height_meters, coords, dimensions=[400, 300])

        if self.image == None:
            # display no data
            self.image = self.createNoDataImage()
        # udpate ui base on image
        self.updateDisplayFrame()

    def paramsFrameDef(self):
        
        self.time = datetime.datetime.now()
        self.selected = []
        self.coords = [[0,0],[0,0]]
        
        def setEntry(entry, text):
            entry.delete(0, "end")
            entry.insert(0, text)
        
        # frame
        self.dataSelectionFrame = ctk.CTkFrame(self.mainFrame)
        self.dataSelectionFrame.grid(row=0, column=0, sticky="nsw", padx=5, pady=5)

        # title
        self.paramsTitle = ctk.CTkLabel(
            self.dataSelectionFrame, text="Parameters", font=("Arial", 24, "bold")
        )
        self.paramsTitle.grid(row=0, column=0, sticky="w")
        # parameters
        self.regressionButton = ctk.CTkButton(
            self.dataSelectionFrame, text="Run Regression", command=self.testRegression
        )

        self.regressionButton.grid(row=6, column=0, pady=5)

        # variables
        self.variablesFrame = ctk.CTkScrollableFrame(self.dataSelectionFrame, width=300)
        self.variablesFrame.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        with open("src/variables.txt", "r") as f:
            self.variablesList = f.read().splitlines()
        self.variables = {}
        self.variablesText = ctk.CTkLabel(
            self.dataSelectionFrame, text="Variables selected : None"
        )
        self.variablesText.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        def updateVar(v):
            if self.variables[v].get() == 1:
                self.selected.append(v)
            else:
                self.selected.remove(v)
            self.variablesText.configure(
                text="Variables selected : " + ", ".join(self.selected)
            )

        for v in self.variablesList:
            var = ctk.BooleanVar(value=False)
            self.variables[v] = var
            ctk.CTkCheckBox(
                self.variablesFrame,
                text=v,
                variable=var,
                command=lambda v=v: updateVar(v),
            ).pack(anchor="w", padx=10, pady=5)

        # location
        self.locationFrame = ctk.CTkFrame(self.dataSelectionFrame)
        self.locationFrame.grid(row=3, column=0, sticky="ew")
        ctk.CTkLabel(
            self.locationFrame, text="Location", font=("Comic Sans MS", 18, "bold")
        ).grid(row=0, column=0, padx=10, pady=5, sticky="w")

        ctk.CTkLabel(self.locationFrame, text="Region").grid(
            row=1, column=0, padx=10, pady=5, sticky="w"
        )
        
        def regionChange(value):
            self.coords[0][0] = urbanDictionnary[value][0]
            self.coords[0][1] = urbanDictionnary[value][1]
            setEntry(self.latitude1,urbanDictionnary[value][0])
            setEntry(self.latitude2,urbanDictionnary[value][1])
            print(self.latitude1.get())
        
        self.region = ctk.CTkComboBox(
            self.locationFrame, command=regionChange, values=['Bangkok', 'Barcelona', 'Boston', 'Buenos Aires', 'Edmonton', 'Lima', 'Madrid', 'Manila', 'Montreal', 'New York City', 'Ottawa', 'Paris', 'Philadelphia', 'Quebec', 'Regina', 'Rome', 'Sherbrooke', 'Sydney', 'Toronto', 'Vancouver', 'Venice', 'Victoria', 'Wellington', 'Winnipeg']
        )
        
        self.region.set("Montreal")
        self.region.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(self.locationFrame, text="Latitude N/S").grid(
            row=2, column=0, padx=10, pady=5, sticky="w"
        )
        self.latitude1 = ctk.CTkEntry(self.locationFrame, placeholder_text="0.000")
        self.latitude2 = ctk.CTkEntry(self.locationFrame, placeholder_text="0.000")
        self.latitude1.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.latitude2.grid(row=2, column=2, padx=10, pady=5, sticky="w")

        ctk.CTkLabel(self.locationFrame, text="Longitude W/E").grid(
            row=3, column=0, padx=10, pady=5, sticky="w"
        )
        self.longitude1 = ctk.CTkEntry(self.locationFrame, placeholder_text="0.000")
        self.longitude2 = ctk.CTkEntry(self.locationFrame, placeholder_text="0.000")
        self.longitude1.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        self.longitude2.grid(row=3, column=2, padx=10, pady=5, sticky="w")
        
        self.latitude2.grid_remove()
        self.longitude2.grid_remove()

        # sampling mode
        ctk.CTkLabel(self.locationFrame, text="Sampling mode").grid(
            row=4, column=0, padx=10, pady=5, sticky="w"
        )
        self.coordsMode = ctk.StringVar(value="point")

        def updateCoordsMode():
            if self.coordsMode.get() == "rectangle":
                self.coordsSwitch.configure(text="rectangle")
                self.radiusFrame.grid_remove()
                self.latitude2.grid()
                self.longitude2.grid()
            else:
                self.coordsSwitch.configure(text="point")
                self.radiusFrame.grid()
                self.latitude2.grid_remove()
                self.longitude2.grid_remove()
                
        self.coordsSwitch = ctk.CTkSwitch(self.locationFrame,
            text="point",
            variable=self.coordsMode,
            onvalue="rectangle",
            offvalue="point",
            command=updateCoordsMode,
        )
        self.coordsSwitch.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        # largeur autour d'un point
        self.radiusFrame = ctk.CTkFrame(self.locationFrame, fg_color="transparent")
        self.radiusFrame.grid(row=2, column=2)
        ctk.CTkLabel(self.radiusFrame, text="Radius :").grid(
            row=4, column=0, padx=4, pady=5, sticky="e"
        )
        self.radius = ctk.CTkEntry(self.radiusFrame, placeholder_text="24", width=60)
        self.radius.grid(row=4, column=1, padx=4, pady=5, sticky="w")
        ctk.CTkLabel(self.radiusFrame, text="Km").grid(row=4, column=2, padx=4, pady=5, sticky="w")
        
        #Time
        self.timeFrame = ctk.CTkFrame(self.dataSelectionFrame)
        self.timeFrame.grid(row=4, column=0, sticky="ew")
        ctk.CTkLabel(self.timeFrame, text="Time", font=("Comic Sans MS", 18, "bold")).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(self.timeFrame, text="Start : ").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.timeStartFrame = ctk.CTkFrame(self.timeFrame)
        self.timeStartFrame.grid(row=1, column=1)
        
        self.timeStartYear = ctk.CTkEntry(self.timeStartFrame, placeholder_text="YYYY", width=50)
        self.timeStartYear.grid(row=0,column=0, padx=1,pady=5)
        self.timeStartMonth = ctk.CTkEntry(self.timeStartFrame, placeholder_text="MM", width=40)
        self.timeStartMonth.grid(row=0,column=1, padx=1,pady=5)
        self.timeStartDay = ctk.CTkEntry(self.timeStartFrame, placeholder_text="DD", width=40)
        self.timeStartDay.grid(row=0,column=2, padx=1,pady=5)
        
        self.timeStartHour = ctk.CTkEntry(self.timeStartFrame, placeholder_text="HH", width=40)
        self.timeStartHour.grid(row=0,column=3, padx=(10,1),pady=5)
        self.timeStartMin = ctk.CTkEntry(self.timeStartFrame, placeholder_text="MM", width=40)
        self.timeStartMin.grid(row=0,column=4, padx=1,pady=5)
        self.timeStartSec = ctk.CTkEntry(self.timeStartFrame, placeholder_text="SS", width=40)
        self.timeStartSec.grid(row=0,column=5, padx=1,pady=5)
        
        ctk.CTkLabel(self.timeFrame, text="Stop : ").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.timeStopFrame = ctk.CTkFrame(self.timeFrame)
        self.timeStopFrame.grid(row=2, column=1)
        
        self.timeStopYear = ctk.CTkEntry(self.timeStopFrame, placeholder_text="YYYY", width=50)
        self.timeStopYear.grid(row=0,column=0, padx=1,pady=5)
        self.timeStopMonth = ctk.CTkEntry(self.timeStopFrame, placeholder_text="MM", width=40)
        self.timeStopMonth.grid(row=0,column=1, padx=1,pady=5)
        self.timeStopDay = ctk.CTkEntry(self.timeStopFrame, placeholder_text="DD", width=40)
        self.timeStopDay.grid(row=0,column=2, padx=1,pady=5)
        
        self.timeStopHour = ctk.CTkEntry(self.timeStopFrame, placeholder_text="HH", width=40)
        self.timeStopHour.grid(row=0,column=3, padx=(10,1),pady=5)
        self.timeStopMin = ctk.CTkEntry(self.timeStopFrame, placeholder_text="MM", width=40)
        self.timeStopMin.grid(row=0,column=4, padx=1,pady=5)
        self.timeStopSec = ctk.CTkEntry(self.timeStopFrame, placeholder_text="SS", width=40)
        self.timeStopSec.grid(row=0,column=5, padx=1,pady=5)
        self.timeStopFrame.grid_remove()
        
        #time mode
        ctk.CTkLabel(self.timeFrame, text="Time mode").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.timeMode = ctk.StringVar(value="period")        
        def updateTimeMode():
            if self.timeMode.get() == "point":
                self.timeSwitch.configure(text="period")
                self.timeStopFrame.grid()
            else:
                self.timeSwitch.configure(text="point")
                self.timeStopFrame.grid_remove()
                
                
        self.timeSwitch = ctk.CTkSwitch(self.timeFrame,
            text="point",
            variable=self.timeMode,
            onvalue="point",
            offvalue="period",
            command=updateTimeMode
        )
        self.timeSwitch.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        
        self.timeStepFrame = ctk.CTkFrame(self.timeFrame)
        self.timeStepFrame.grid(row=3, column=1, columnspan=2, padx=10, pady=5, sticky="e")
        ctk.CTkLabel(self.timeStepFrame, text="Step :").grid(row=0, column=0, padx=0, pady=5, sticky="w")
        self.timeStep = ctk.CTkEntry(self.timeStepFrame, placeholder_text="1H", width=40)
        self.timeStep.grid(row=0,column=1, padx=10,pady=5, sticky="w")
        
        # # height slider
        # self.heightBar = ctk.CTkSlider(
        #     self.dataSelectionFrame,
        #     from_=0,
        #     to=10,
        #     number_of_steps=10,
        #     command=self.updateHeight,
        # )
        # self.heightBar.grid(row=1, column=0, padx=10, pady=10)
        # self.heightBar.set(0)

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
            row=0, column=1, sticky="nsew", padx=5, pady=5,
        )
        self.displayFrame.rowconfigure(1, weight=1)
        self.displayFrame.columnconfigure(0, weight=1)

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
        self.imageLabel.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

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

    def displayRegression(self, x, y):

        # Generate polynomial regression
        fig, model, degree, results = regression.polynomial_regression(x, y)

        # Clear previous graph
        if hasattr(self, "canvas"):
            self.canvas.get_tk_widget().destroy()

        # Display graph inside CustomTkinter
        self.canvas = FigureCanvasTkAgg(fig, master=self.displayFrame)
        self.canvas.draw()

        self.canvas.get_tk_widget().grid(row=2, column=0, padx=10, pady=10)

        # Store model
        self.regressionModel = model

        print("Best degree:", degree)
        print("R²:", model.score(np.array(x).reshape(-1, 1), y))

    def testRegression(self):
        x = [1, 2, 3, 4, 5, 6, 7, 8]
        y = [2, 5, 10, 17, 26, 37, 50, 65]

        self.displayRegression(x, y)

    def inference(self, x):
        if self.regressionModel is not None:
            return self.regressionModel.predict(x)


if __name__ == "__main__":
    app = App()
    app.mainloop()
