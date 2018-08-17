import math
import random
from collections import namedtuple
class car(Actor.Actor):
    map_size=7
    simple_map=[[0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 1, 1, 1, 1, 1, 0, 0, 0],[0, 1, 0, 1, 0, 1, 1, 1, 0],[0, 1, 1, 1, 1, 1, 0, 1, 0],[0, 1, 0, 1, 0, 0, 0, 1, 0],[0, 1, 0, 1, 1, 1, 1, 1, 0],[0, 1, 0, 1, 0, 0, 0, 1, 0],[0, 1, 1, 1, 1, 1, 1, 1, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0]]
    d_map=[[[False]*4 for i in range(9)] for j in range(9)]
    loc_struct=namedtuple("loc_struct", "x y direc cost")
    direction=[[1,0],[0,1],[-1,0],[0,-1]] #+1은 우회전 -1 좌회전 +2는 반대
    speed = 0.0
    Aflag = 0
    Dflag = 0
    Wflag = 0
    Sflag = 0
    Rflag = 1 # 후진 기어 키면 -1
    WA = 0.00 # Wheel Angle
    CA = 0.00 # Car Angle
    fric = 0.0004
    handlefric = 1
    grabhandle = False
    collchk = False
    colltimecnt=0
    start = False
    chkk=True
    sx=0
    sy=1
    prex=0
    prey=1
    mydir=0
    path=list()
    pathleng=0
    naviprog=0
    nextx=0
    nexty=0
    mat_no=0
    navibool = False
    dx=0
    dy=0
    def R2A(self,R):
        return (180*R/math.pi)  # 라디안 -> 도 (PI -> 180)
    
    def A2R(self,A):
        return (A*math.pi/180)  # 도 -> 라디안 (180 -> PI)

    def R2S(self,rx,ry,angle):
        return (int)((rx+10)/20),(int)((ry+30)/20),(int)(((angle+45)%360)/90)
    def __init__(self):
        self.car=Container(0)
        
        self.fMeshContainer = Container(0)
        self.directCon = Container(0)
        
        self.directsoundCon = Container(0)
        self.metersoundcon = Container(0)
        self.tire1=Container(0)
        self.tire2=Container(0)
        for i in range(1,self.map_size+1):
            for j in range(1,self.map_size+1):
                for k,direc in enumerate(self.direction):
                    if(self.simple_map[i][j]==1 and self.simple_map[i+direc[0]][j+direc[1]]==1):
                        self.d_map[i][j][k]=True
        self.d_map[0][1][0]=True
        self.d_map[1][1][2]=True
        return
    def OnCreate(self,uid):
        self.cartrans = self.car.FindComponentByType("TransformGroup")
        self.carpos = self.cartrans.GetPosition()
        self.carrot = self.cartrans.GetRotation()
        self.tiretrans1 = self.tire1.FindComponentByType("TransformGroup")
        self.tiretrans2 = self.tire2.FindComponentByType("TransformGroup")
        
        self._fbxMesh = self.fMeshContainer.FindComponentByType("Cube")
        self.directMesh = self.directCon.FindComponentByType("Cube")
        self.Sound = self.metersoundcon.FindComponentByType("Sound")
        self.directSound = self.directsoundCon.FindComponentByType("Sound")
        return
    def OnDestory(self):
        return
    def OnEnable(self):
        return
    def OnDisable(self):
        return
    def Update(self):
        if(self.chkk==True):
            self.chkk=False
            while(1):
                self.dx=random.randint(1,7)
                self.dy=random.randint(1,7)
                if(self.simple_map[self.dx][self.dy]==1 and (self.dx!=self.sx or self.dy!=self.sy)):
                    break
            self.path=self.navi(self.sx,self.sy,self.mydir,self.dx,self.dy)
            print(self.path)
            self.nextx,self.nexty=self.navimsg(self.naviprog)
        self.inkey()
        self.fricfunc()
        if(self.collchk):
            self.colliding()
        self.move()
        if(self.prex!=self.sx or self.prey!=self.sy):
            print(self.sx,self.sy)
            if(self.sx==self.path[self.naviprog+1].x and self.sy==self.path[self.naviprog+1].y):
                self.naviprog+=1
            else:
                print("You have wrong path, new path calulating")
                self.path=self.navi(self.sx,self.sy,self.mydir,self.dx,self.dy)
                print(self.path)
                self.nextx,self.nexty=self.navimsg(self.naviprog)
            if(self.naviprog==self.pathleng-1):
                print("arrived")
                self.chkk=True;
            elif(self.sx==self.nextx and self.sy==self.nexty):
                self.nextx,self.nexty=self.navimsg(self.naviprog)
        if (self.navibool==True):
            #self.mat_no += 1
            print("doyouhearme")
            if((self.mat_no)==1):
                self._fbxMesh.PropMaterial.SetTextureDiffuse("$project/Assets/navi/100.png")
                self.Sound.PropSound.SetSoundFilePath("$project/Assets/navi/100.wav")
                self.Sound.Play()
                print("print1")
                self.navibool=False
            elif((self.mat_no)==2):
                self._fbxMesh.PropMaterial.SetTextureDiffuse("$project/Assets/navi/200.png")
                self.Sound.PropSound.SetSoundFilePath("$project/Assets/navi/200.wav")
                self.Sound.Play()
                print("print2")
                self.navibool=False
            elif((self.mat_no)==3):
                self._fbxMesh.PropMaterial.SetTextureDiffuse("$project/Assets/navi/300.png")
                self.Sound.PropSound.SetSoundFilePath("$project/Assets/navi/300.wav")
                self.Sound.Play()
                print("print3")
                self.navibool=False
            elif((self.mat_no)==4):
                self._fbxMesh.PropMaterial.SetTextureDiffuse("$project/Assets/navi/400.png")
                self.Sound.PropSound.SetSoundFilePath("$project/Assets/navi/400.wav")
                self.Sound.Play()
                print("print4")
                self.navibool=False
            elif((self.mat_no)==5):
                self._fbxMesh.PropMaterial.SetTextureDiffuse("$project/Assets/navi/500.png")
                self.Sound.PropSound.SetSoundFilePath("$project/Assets/navi/500.wav")
                self.Sound.Play()
                print("print5")
                self.navibool=False
        return
    
    def OnMessage(self, msg, number, Vector4_lparm, Vector4_wparam):
        
        if(msg=="Container"):
            self.simple_map[1][3]=0
            for i,dr in enumerate(self.direction):
                self.d_map[1][3][i]=False
                self.d_map[1+dr[0]][3+dr[1]][(i+2)%4]=False
            self.path=self.navi(self.sx,self.sy,self.mydir,self.dx,self.dy)
            print(self.path)
            self.nextx,self.nexty=self.navimsg(self.naviprog)
        
        if (msg == "KeyDown"):

            if(self.start == True) :
            
                if( number == 0x41): #"A" : 핸들 좌로 꺾기
                    self.Aflag = 1
                elif( number == 0x44): #"D" : 핸들 우로 꺾기
                    self.Dflag = 1
                elif( number == 0x57): #"W" : 엑셀
                    self.Wflag = 1
                elif( number == 0x53): #"S" : 브레이크
                    self.Sflag = 1
                elif( number == 0x51) : #"Q" : 드라이브 기어
                    self.Rflag = 1
                elif( number == 0x45) : #"E" : 후진 기어
                    self.Rflag = -1
                elif( number == 0x0D) : #"ENTER" : 시동 끄기
                    self.start = False
                    
            elif(self.start == False) :

                if(number == 0X0D) : #"ENTER" : 시동 켜기
                    self.start = True
                    
        if (msg == "KeyUp"):
            
            if( number == 0x41): #"A"
                self.Aflag = 0
            elif( number == 0x44): #"D"
                self.Dflag = 0
            elif( number == 0x57): #"W"
                self.Wflag = 0
            elif( number == 0x53): #"S"
                self.Sflag = 0
                
        if(msg == "Coll_detect"):
            #print("coll")
            self.speed=self.speed*-1
            self.collchk=True


        if(msg == "break_on"):
            self.Sflag = 1
        if(msg=="break_off"):
            self.Sflag = 0
        if(msg=="accel_on"):
            self.Wflag = 1
        if(msg=="accel_off"):
            self.Wflag= 0
        if(msg=="right_on"):
            self.Dflag =1
        if(msg=="right_off"):
            self.Dflag=0
        if(msg=="left_on"):
            self.Aflag = 1
        if(msg=="left_off"):
            self.Aflag = 0
        if(msg=="start"):
            self.start = True
        if(msg=="kill"):
            self.start = False
        if(msg == "forward"):
            self.Rflag= 1
        if(msg == "rear"):
            self.Rflag=-1
        return

    def fricfunc(self):
        if(self.speed>self.fric):
            self.speed-=self.fric
        elif(self.speed<0 and self.speed+self.fric<0):
            self.speed+=self.fric
        if(self.grabhandle == False):
            if(self.WA>0):
                self.WA-=self.handlefric
            elif(self.WA<0):
                self.WA+=self.handlefric

    def inkey(self):
        self.grabhandle=False
        if (self.Wflag == 1):
            self.speed += 0.001*self.Rflag
        if (self.Sflag == 1):
            if (self.speed*self.Rflag  > 0):
                self.speed -= 0
        if (self.Aflag == 1 ):
            self.grabhandle=True
            
            if(self.WA>-45):
                self.WA  -= 0.5
        if (self.Dflag == 1 ):
            self.grabhandle=True
            if(self.WA<45):
                self.WA += 0.5
        if (self.speed != 0):
            if(self.WA<0):
                self.cartrans.Rotate(-10*self.speed,0,(0,1,0))
                #self.cameraTrans.Rotate(-10*self.speed,0,(0,1,0))
                self.CA -= 10*self.speed
            if(self.WA>0):
                self.cartrans.Rotate(10*self.speed,0,(0,1,0))
                #self.cameraTrans.Rotate(10*self.speed,0,(0,1,0))
                self.CA += 10*self.speed
            self.CA=self.CA%360
        self.tiretrans1.SetLocalRotation(self.EulerToQuaternionFloat(Math3d.Vector3(0,self.A2R(self.WA),0))) #tire rotate
        self.tiretrans2.SetLocalRotation(self.EulerToQuaternionFloat(Math3d.Vector3(0,self.A2R(self.WA),0))) #tire rotate

    def move(self):
        self.carpos.x += self.speed*(math.sin(self.A2R(self.WA+self.CA)))
        self.carpos.z += self.speed*(math.cos(self.A2R(self.WA+self.CA)))
        #self.cameraPos.x +=self.speed*(math.sin(self.A2R(self.WA+self.CA)))
        #self.cameraPos.z +=self.speed*(math.cos(self.A2R(self.WA+self.CA)))
        self.cartrans.SetPosition(self.carpos)
        #self.cameraTrans.SetPosition(self.cameraPos)
        self.prex=self.sx
        self.prey=self.sy
        self.sx,self.sy,self.mydir=self.R2S(self.carpos.z,self.carpos.x,self.CA)
    def colliding(self):
        self.colltimecnt+=1
        if(self.colltimecnt==4):
            self.speed *= 0.02
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

    def queue_get(self,a):
        return a.x,a.y,a.direc,a.cost

    def bfs(self,q,chk,via,fx,fy):
        rear=0
        while(rear<len(q)):
            x,y,direc,cost=self.queue_get(q[rear])
            if(x==fx and y==fy):
                return rear
            for i,dr in enumerate(self.direction):
                rev=(i+2)%4
                if(self.d_map[x][y][i]==True and self.d_map[x+dr[0]][y+dr[1]][rev]==True and chk[x+dr[0]][y+dr[1]]==False):
                    q.append(self.loc_struct(x+dr[0],y+dr[1],i,cost+1))
                    via.append(rear)
                    chk[x+dr[0]][y+dr[1]]=True
            rear+=1
        fail=-1
        return fail

    def via_func(self,q,w,via):
        bfspath=[self.loc_struct(0,0,0,0) for i in range(q[w].cost+1)]
        prev=w
        while(w!=-1):
            bfspath[q[w].cost]=self.loc_struct(q[w].x,q[w].y,q[prev].direc,q[w].cost)
            prev=w
            w=via[w]
        return bfspath

    def navi(self,x,y,direc,fx,fy):
        print("hi navi")
        chk=[[False for i in range(self.map_size+2)] for j in range(self.map_size+2)]
        curr=self.loc_struct(x,y,direc,0)
        chk[curr.x][curr.y]=True
        q=list()
        q.append(curr)
        via=list()
        via.append(-1)
        v=self.bfs(q,chk,via,fx,fy)
        if(v==-1):
            bfspath=list()
            print("no path")
        else:
            bfspath=self.via_func(q,v,via)
            self.pathleng=q[v].cost+1
            print("path finded cost :",self.pathleng)
            self.naviprog=0
        return bfspath

    def navimsg(self,prog):
        prevdir=self.path[prog].direc
        straightcnt=0
        if((prevdir+2)%4==self.mydir):
            print("U Turn and")
        if((prevdir+1)%4==self.mydir):
            print("Turn Left and")
        if((prevdir-1)%4==self.mydir):
            print("Turn Right and")
        for i in range(prog+1,self.pathleng):
            straightcnt+=1
            if(prevdir!=self.path[i].direc):
                print("Go straight",straightcnt*100,"meter and")
                if((prevdir+1)%4==self.path[i].direc):
                    print("Turn Right")
                    self.directSound.PropSound.SetSoundFilePath("$project/Assets/navi/right.wav")
                    self.directMesh.PropMaterial.SetTextureDiffuse("$project/Assets/navi/right.png")
                    self.directSound.Play()
                else:
                    print("Turn Left")
                    self.directSound.PropSound.SetSoundFilePath("$project/Assets/navi/left.wav")
                    self.directMesh.PropMaterial.SetTextureDiffuse("$project/Assets/navi/left.png")
                    self.directSound.Play()
                self.mat_no=straightcnt
                self.navibool=True
                return self.path[i].x,self.path[i].y
        print("Go straight",straightcnt*100,"meter and arrive")
        self.directSound.PropSound.SetSoundFilePath("$project/Assets/navi/finish.wav")
        self.directMesh.PropMaterial.SetTextureDiffuse("$project/Assets/navi/straight.png")
        self.directSound.Play()
        self.mat_no=straightcnt
        self.navibool=True
        return self.path[self.pathleng-1].x,self.path[self.pathleng-1].y