class container(Actor.Actor):
    
    G = 9.8
    fall = False
    height = 5
    red = False
    blue = False
    rot = False
    torot = 0.0
    total = 0.0
    kill = False
    tick = 0
    def __init__(self):
        self.redcon = Container(0)
        self.bluecon = Container(0)
        self.carcon = Container(0)
        self.carscriptcon = Container(0)
        self.switchcon = Container(0)
        return

    def OnCreate(self,uid): 
        self.redconTrans = self.redcon.FindComponentByType("TransformGroup")
        self.blueconTrans = self.bluecon.FindComponentByType("TransformGroup")

        self.redconSound = self.redcon.FindComponentByType("Sound")
        self.redconSound.PropSound.SetSoundFilePath("$project/Assets/sound/crash.wav")

        self.carTrans = self.carcon.FindComponentByType("TransformGroup")
        self.switchbox = self.switchcon.FindComponentByType("TransformGroup")
        self.switchboxtocollide = self.switchbox.GetWorldBox()

        self.carscriptcomponent = self.carscriptcon.FindComponentByType("ScriptComponent")
        self.carscript = self.carscriptcomponent.GetActor()


        self.redconTrans.PropTransform.SetShow(0)
        self.blueconTrans.PropTransform.SetShow(0)

        self.redconPos = self.redconTrans.GetPosition()
        self.redconPos = self.redconPos + Math3d.Vector3(0,10,0)
        self.blueconPos = self.blueconTrans.GetPosition()
        self.blueconPos = self.blueconPos + Math3d.Vector3(0,16,0)



        self.redconTrans.SetPosition(self.redconPos)
        self.blueconTrans.SetPosition(self.blueconPos)

        self.blueconPos = self.blueconTrans.GetPosition()
        return

    def OnDestroy(self):
        return

    def OnEnable(self):
        return

    def OnDisable(self):
        return

    def Update(self):
        self.carboxtocollide = self.carTrans.GetSumBox()
        if(self.tick<30):
            self.tick+=1
        if(self.carboxtocollide.OBBIntersect(self.switchboxtocollide)==True and self.kill==False and self.tick>20):
            self.fall=True
            self.kill=True
        #길을 바꿔야됨
            
    
        if(self.fall==True):
            self.carscript.OnMessage("Container",0,Math3d.Vector4(0,0,0,0),Math3d.Vector4(0,0,0,0))
            self.redconTrans.PropTransform.SetShow(1)
            self.blueconTrans.PropTransform.SetShow(1)
            self.redconPos = self.redconPos-Math3d.Vector3(0,1.414*3.3*self.height*0.06,0)
            self.blueconPos = self.blueconPos-Math3d.Vector3(0,1.414*3.3*self.height*0.06,0)
            if(self.redconPos.y<=0):
                self.redconPos.y=0
                if(self.red == False):
                    self.redconSound.Play()
                self.red=True
            if(self.blueconPos.y<5.550):
                self.blueconPos.y = 5.550
                if(self.blue==False):
                    self.redconSound.Play()
                    self.rot = True
                self.blue = True
                

            if(self.rot == True):
                self.torot=self.torot + 0.2
                self.total=self.total + self.torot
                print(self.total)
                if(self.total<=38):
                    self.blueconTrans.Rotate(0,self.torot,(0,1,0))
                else:
                    self.redconSound.Play()
                    self.rot=False

            if(self.red==True and self.blue == True and self.rot == False):
                self.fall=False
                self.red = False
                self.blue = False
            self.redconTrans.SetPosition(self.redconPos)
            self.blueconTrans.SetPosition(self.blueconPos)

        return
