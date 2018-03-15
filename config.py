
class Parameters:

    def __init__(self, layer):
        self.layer = layer
        self.pixSizeX = None #Pixel size of X axis
        self.pixSizeY = None #Pixel size of Y axis
        self.topLeftX = None #Geo coordinate X of the Top Left pixel
        self.topLeftY = None #Geo coordinate Y of the Top Left pixel
        self.boundingboxSize = 25


    def readRasterConfig(self):
        self.pixSizeX = self.layer.rasterUnitsPerPixelX()
        self.pixSizeY = self.layer.rasterUnitsPerPixelY()
        self.topLeftX = self.layer.extent().xMinimum()
        self.topLeftY = self.layer.extent().yMaximum()

