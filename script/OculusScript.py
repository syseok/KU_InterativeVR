
class OculusScript(Actor.Actor):
    def __init__(self):
        self.LeftHandContainer = Container(0)
        self.RightHandContainer = Container(0)
        self.CameraContainer = Container(0)

        self._MainCamera = Camera(0)

        self._CameraTransform = None
        self._LeftHandTransform = None
        self._RightHandTransform = None
        self.tick = 0

        self.leftindexTrigger=0
        self.rightindexTrigger = 0

        self.lefthandTrigger = 0
        self.righthandTrigger = 0

        self.switchhandle = 0

        self.CarContainer = Container(0)

        return

    def OnCreate(self, uid):
        self._MainCamera = self.CameraContainer.FindComponentByType("Camera")
        self._CameraTransform = self.CameraContainer.FindComponentByType("TransformGroup")
        self._LeftHandTransform = self.LeftHandContainer.FindComponentByType("TransformGroup")
        self._RightHandTransform = self.RightHandContainer.FindComponentByType("TransformGroup")

        self.CarScriptComponent = self.CarContainer.FindComponentByType("ScriptComponent")
        self.CarScript = self.CarScriptComponent.GetActor()

        return 0 

    def OnDestroy(self):
        return 0 

    def OnEnable(self):
        return 0 

    def OnDisable(self):
        return 0

    def Update(self):
        doPrint = True;

        self.tick += 1
        
        if(self.tick <= 20):
            return
        
        self.tick = 0
        
        camPosition = self._CameraTransform.PropTransform.GetPosition()
        #camRotation = self._CameraTransform.PropTransform.GetRotation()

        #print(camPosition)
        

        hmdStatus = DeviceInput.GetHMDStatus("Oculus")
        hmdRot = DeviceInput.GetHMDOrientation("Oculus", False)
        hmdPos = DeviceInput.GetHMDPosition("Oculus", False)
        inputTime = DeviceInput.GetInputTime("Oculus")
        buttonInfo = DeviceInput.GetInputInfo("Oculus", 0)
        touchInfo = DeviceInput.GetInputInfo("Oculus", 1)
        controllerType = DeviceInput.GetControllerType("Oculus")

        #if doPrint:
            #print("hmd Stataus : " + str(hmdStatus))
            #print("Hmd Rot : " + str(hmdRot))
            #print("Hmd Pos : " + str(hmdPos))
            #print("Input Time : " + str(inputTime))
            #print("Button : " + str(buttonInfo))
            #print("Touch : " + str(touchInfo))
            #print("ControllerType : " + str(controllerType))

        #self.LPos = None
        #self.RPos = None

        for i in range(0,2):
            
            hand = i + 1

            handStatus = DeviceInput.GetHandStatus("Oculus", hand)



            if handStatus > 0:
                handRot = DeviceInput.GetHandOrientation("Oculus", hand)
                handPos = DeviceInput.GetHandPosition("Oculus", hand)
                tStick = DeviceInput.GetThumbStick("Oculus", hand, False);

                if hand == 1 :
                    self.lefthandTrigger = DeviceInput.GetTrigger("Oculus", hand, False, 0)
                    self.leftindexTrigger = DeviceInput.GetTrigger("Oculus", hand, False, 1)
                elif hand == 2 :
                    self.righthandTrigger = DeviceInput.GetTrigger("Oculus", hand, False, 0)
                    self.rightindexTrigger = DeviceInput.GetTrigger("Oculus", hand, False, 1)

                
                """if i == 0:
                    #LPos = handPos
                else:
                    #RPos = handPos"""

                if doPrint:
                    #if i == 0:
                    #    print("Left Hand >>")
                    #elif i == 1:
                    #    print("Right Hand >>")
                    #
                    #print("HandStatus : " + str(handStatus))
                             
                    if handStatus > 0 :
                        
                        print("HandRot : " + str(handRot))
                        print("HandPos : " + str(handPos))
                        #print("HandTrigger : " + str(handTrigger))
                        #print("IndexTrigger : " + str(indexTrigger))
                        #print("ThumbStick : " + str(tStick))

                #UpdatePosition
                nPos = camPosition + handPos
                nRot = handRot
                
                if hand == 1:
                    if self._LeftHandTransform!= None:
                        self._LeftHandTransform.PropTransform.SetPosition(nPos)
                        self._LeftHandTransform.PropTransform.SetRotation(nRot)
                elif hand == 2:
                    if self._RightHandTransform != None:
                        self._RightHandTransform.PropTransform.SetPosition(nPos)
                        self._RightHandTransform.PropTransform.SetRotation(nRot)

                #UseButton
                btnYCheck = buttonInfo & DeviceInput.ovrButton_Y
                btnXCheck = buttonInfo & DeviceInput.ovrButton_X
                btnBCheck = buttonInfo & DeviceInput.ovrButton_B
                btnACheck = buttonInfo & DeviceInput.ovrButton_A
                #if right hand's trigger pressed -> accel
                
                if self.leftindexTrigger > 0.8 :
                    self.CarScript.OnMessage("break_on",0,Math3d.Vector4(0,0,0,0),Math3d.Vector4(0,0,0,0))
                    self.CarScript.OnMessage("accel_off",0,Math3d.Vector4(0,0,0,0),Math3d.Vector4(0,0,0,0))
                elif self.rightindexTrigger > 0.8 :
                    self.CarScript.OnMessage("accel_on",0,Math3d.Vector4(0,0,0,0),Math3d.Vector4(0,0,0,0))
                    self.CarScript.OnMessage("break_off",0,Math3d.Vector4(0,0,0,0),Math3d.Vector4(0,0,0,0))
                
                if (self.righthandTrigger > 0.8 and (self.switchhandle==0 or self.switchhandle==1)):
                    self.CarScript.OnMessage("right_on",0,Math3d.Vector4(0,0,0,0),Math3d.Vector4(0,0,0,0))
                    self.switchhandle = 1
                else :
                    self.CarScript.OnMessage("right_off",0,Math3d.Vector4(0,0,0,0),Math3d.Vector4(0,0,0,0))
                    self.switchhandle = 0

                if (self.lefthandTrigger>0.8 and (self.switchhandle ==0 or self.switchhandle == 2)) :
                    self.CarScript.OnMessage("left_on",0,Math3d.Vector4(0,0,0,0),Math3d.Vector4(0,0,0,0))
                    self.switchhandle= 2
                else :
                    self.CarScript.OnMessage("left_off",0,Math3d.Vector4(0,0,0,0),Math3d.Vector4(0,0,0,0))   
                    self.switchhandle = 0
                
                



                if btnYCheck > 0:
                    #turn engine on
                    DeviceInput.SetVibration("Oculus", 1, 0.5, 0.5)
                    self.CarScript.OnMessage("start",0,Math3d.Vector4(0,0,0,0),Math3d.Vector4(0,0,0,0))
                    if doPrint :
                        print("btnYClick")

                if btnXCheck > 0:
                    DeviceInput.SetVibration("Oculus", 1, 0, 0)
                    self.CarScript.OnMessage("kill",0,Math3d.Vector4(0,0,0,0),Math3d.Vector4(0,0,0,0))
                    if doPrint :
                        print("btnXCheck")

                if btnBCheck > 0:
                    #B button for forward gear
                    self.CarScript.OnMessage("forward",0,Math3d.Vector4(0,0,0,0),Math3d.Vector4(0,0,0,0))
                    DeviceInput.SetVibration("Oculus", 2, 0.5, 0.5)
                    if doPrint :
                        print("btnBCheck")

                if btnACheck > 0:
                    #A button for rear gear
                    self.CarScript.OnMessage("rear",0,Math3d.Vector4(0,0,0,0),Math3d.Vector4(0,0,0,0))
                    DeviceInput.SetVibration("Oculus", 2, 0, 0)
                    if doPrint :
                        print("btnACheck")


        #hLength = (RPos - LPos).Length()
        #print("Dis = " + str(hLength))

        return

    def OnMessage(self, msg, number, Vector4_lparm, Vector4_wparam):
        return;
