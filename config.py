class Config(object):

    pixSizeX = 1 #Pixel size of X axis
    pixSizeY = 1 #Pixel size of Y axis
    topLeftX = None #Geo coordinate X of the Top Left pixel
    topLeftY = None #Geo coordinate Y of the Top Left pixel

    @staticmethod
    def update(variable, value):
        if variable == 'pixSizeX':
            Config.pixSizeX = value
        elif variable == 'pixSizeY':
            Config.pixSizeY = value
        elif variable == 'topLeftX':
            Config.topLeftX = value
        elif variable == 'topLeftY':
            Config.topLeftY = value
