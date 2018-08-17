import math

class crashing(Actor.Actor):
    speed = 0.0
    WA = 0.00 # Wheel Angle
    CA = 275.00 # Car Angle
    fric = 0.0004
    collchk = False
    colltimecnt=0
    crash = 0

    def R2A(self,R):
        return (180*R/math.pi)  # 라디안 -> 도 (PI -> 180)
    
    def A2R(self,A):
        return (A*math.pi/180)  # 도 -> 라디안 (180 -> PI)

    def __init__(self):
        self.car=Container(0)
        return
    def OnCreate(self,uid):
        self.cartrans = self.car.FindComponentByType("TransformGroup")
        self.carpos = self.cartrans.GetPosition()
        self.carrot = self.cartrans.GetRotation()
        return
    def OnDestory(self):
        return
    def OnEnable(self):
        return
    def OnDisable(self):
        return
    def Update(self):
        self.inkey()
        self.fricfunc()
        if(self.collchk):
            self.colliding()
        self.crash *= -1.02
        self.WA += self.crash
        self.move()
    
    def OnMessage(self, msg, number, Vector4_lparm, Vector4_wparam):

        if (msg == "LButtonDown"):
            self.speed=0.6
            self.crash = 0.01
        
       
                
        if(msg == "Coll_detect"):
            self.speed=self.speed*-1
            self.collchk=True


        return



    def fricfunc(self):
        if(self.speed>self.fric):
            self.speed-=self.fric
        elif(self.speed<0 and self.speed+self.fric<0):
            self.speed+=self.fric

    def inkey(self):

        if (self.speed != 0):
            if(self.WA<0):
                self.cartrans.Rotate(-10*self.speed,0,(0,1,0))
                self.CA -= 10*self.speed
            if(self.WA>0):
                self.cartrans.Rotate(10*self.speed,0,(0,1,0))
                self.CA += 10*self.speed
        #print(str(self.WA))

    def move(self):
        self.carpos.x += self.speed*(math.sin(self.A2R(self.WA+self.CA)))
        self.carpos.z += self.speed*(math.cos(self.A2R(self.WA+self.CA)))
        self.cartrans.SetPosition(self.carpos)

        
    def colliding(self):
        self.colltimecnt+=1
        if(self.colltimecnt==4):
            self.speed *= 0.2
            self.collchk=False
            self.colltimecnt=0

    def EulerToQuaternionFloat(self,euler):
        cosx2 = math.cos(euler.x / 2.0)
        sinx2 = math.sin(euler.x / 2.0)
        siny2 = math.sin(euler.y / 2.0)
        cosy2 = math.cos(euler.y / 2.0)
        sinz2 = math.sin(euler.z / 2.0)
        cosz2 = math.cos(euler.z / 2.0)
        
        x = siny2 * cosx2 * sinz2 + cosy2 * sinx2 * cosz2
        y = siny2 * cosx2 * cosz2 - cosy2 * sinx2 * sinz2
        z = cosy2 * cosx2 * sinz2 - siny2 * sinx2 * cosz2
        w = cosy2 * cosx2 * cosz2 + siny2 * sinx2 * sinz2
        
        r = Math3d.Vector4(x, y, z, w)

        return r
