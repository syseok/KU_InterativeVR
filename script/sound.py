class sound(Actor.Actor):
    engine = False
    def __init__(self):
        self.SoundCon1 = Container(0)
        self.SoundCon2 = Container(0)
        self.SoundCon3 = Container(0)
        return
    def OnCreate(self,uid):
        self.soundcom1 = self.SoundCon1.FindComponentByType("Sound")
        self.soundcom2 = self.SoundCon2.FindComponentByType("Sound")
        self.soundcom3 = self.SoundCon3.FindComponentByType("Sound")
        self.soundcom1.PropSound.SetSoundFilePath("$project/Assets/sound/start.wav")
        self.soundcom2.PropSound.SetSoundFilePath("$project/Assets/sound/turnoff.wav")
        self.soundcom3.PropSound.SetSoundFilePath("$project/Assets/sound/horn.wav")
        return
    def OnDestory(self):
        return
    def OnEnable(self):
        return
    def OnDisable(self):
        return
    def Update(self):
        return
    def OnMessage(self, msg, number, Vector4_lparm, Vector4_wparam):
        if (msg == "KeyDown"):
            if( number == 0x0D) :
                if(self.engine == False):
                    self.soundcom1.Play()
                    self.engine = True
                else :
                    self.soundcom2.Play()
                    self.engine = False
        if (msg == "LButtonDown"):
            self.soundcom3.Play()
        return
