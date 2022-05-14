import wheels
import time

class Profile(object):
    def __init__(self,name="basic"):
        self.name = name
        self.rgb = wheels.COLORS["YELLOW"]

    def setRGB(self,rgb):
        self.rgb = rgb

    def colorController(self):
        pass

    def brightnessController(self,pixels):
        pass
    
    def display(self, pixels):
        self.colorController()
        self.brightnessController(pixels)
        pixels.fill(self.rgb)
        pixels.show()

    def __str__(self):
        return f"This is a {self.name} profile\nRGB current values : ({self.rgb}) "

class IndexProfile(Profile):
    def __init__(self):
        super().__init__("Index")
        self.index = [0] 
    
    def addToIndex(self,values):
        self.index.extend(values)
        print(self.index)

    def cleanArray(self,arr):
        indextopop = None
        for y in range(len(arr)):
            if arr[y]>150 or arr[y]<0:
                indextopop=y
        if indextopop != None:
            arr.pop(indextopop)
        return arr
    
    def display(self, pixels):

        for i in range(150):
            for y in range(len(self.index)):
                if i == self.index[y]:
                    pixels[self.index[y]] = (self.rgb)
    
            if i not in self.index:
                pixels[i] = (0,0,0)

        print(self.index)
        pixels.show()
        self.index = self.cleanArray(self.index)

    
class ColorFadeProfile(Profile):
    def __init__(self):
        super().__init__("ColorFade")
        super().setRGB(wheels.COLORS["RED"])
    def colorController(self):
        self.rgb = wheels.colorwheel(self.rgb)

class BreathingProfile(Profile):
    def __init__(self, refresh=0.02):
        super().__init__("Breathing")
        super().setRGB(wheels.COLORS["WHITE"])
        self.refresh = refresh
        self.x = 0.01

    def display(self, pixels):
        super().display(pixels)
        time.sleep(self.refresh)
        
    def brightnessController(self,pixels):
        if pixels.brightness >= 0.2:
            self.x = -self.x
        elif pixels.brightness <= 0:
            self.x = -self.x
            pixels.brightness = 0 
        pixels.brightness += self.x
        print(pixels.brightness)

class ColorBreathingProfile(BreathingProfile):
    def __init__(self):
        super().__init__()
        super().setRGB(wheels.COLORS["GREEN"])
        self.name = "ColorBreathing"
    def colorController(self):
        self.rgb = wheels.colorwheel(self.rgb,3)


class LoadingProfile(Profile):
    def __init__(self,cursor=0,refresh=0.5):
        self.cursor = cursor
        self.cursor2 = cursor
        self.refresh = refresh
        super().__init__("Loading")
        super().setRGB(wheels.COLORS["RED"])

    def display(self, pixels):
        pixels[self.cursor] = (self.rgb)
        pixels[self.cursor2] = (self.rgb)
        pixels.show()
        if self.cursor<150:
            self.cursor+=1
        if self.cursor2>0:
            self.cursor2-=1
        time.sleep(self.refresh)
    
    def resetCursor(self, cursor):
        self.cursor = cursor
        self.cursor2 = cursor

class SnakeProfile(IndexProfile):
    def __init__(self, refresh=0.05):
        super().__init__()
        super().setRGB(wheels.COLORS["WHITE"])
        self.refresh = refresh
        self.index=[]
        self.front=[]
        self.back=[]

    def addToIndex(self,values):
        self.front.extend(values)
        self.back.extend(values)
    
    
    
    def display(self, pixels):
        self.index = self.front + self.back
        super().display(pixels)
    
        for y in range(len(self.front)):
            self.front[y] += 1
        for y in range(len(self.back)):
            self.back[y] -= 1
        self.front=super().cleanArray(self.front)
        self.back=super().cleanArray(self.back)
        time.sleep(self.refresh)


def Factory(role):
    classes = {
        "BASIC": Profile,
        "INDEX": IndexProfile,
        "COLORFADE": ColorFadeProfile,
        "BREATH": BreathingProfile,
        "COLORBREATH": ColorBreathingProfile,
        "LOADING": LoadingProfile,
        "SNAKE": SnakeProfile
    }
    return classes[role]



    
