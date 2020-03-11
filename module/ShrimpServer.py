import time
from mcpi.minecraft import Minecraft

class ShrimpServer:
    def __init__(self):
        self.old_t, self.new_t = int(round(time.time() * 1000)), int(round(time.time() * 1000))
        self.max_t = 300000 # ms

        self.mc    = None
        self.stats = False

        self.connect()
    
    def connect(self):
        try:
            self.mc = Minecraft.create(address = '34.64.235.46')
            self.stats = True
        except ConnectionRefusedError:
            self.mc = None
            self.stats = False
            
        return self.stats

    def getPlayerLen(self):
        if self.mc != None:
            return len(self.mc.getPlayerEntityIds())

if __name__ == "__main__":
    ss = ShrimpServer()