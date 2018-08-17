import math
import random
from collections import namedtuple
class AI(Actor.Actor):
	map_size=7
	ai_num=6
	loc_struct=namedtuple("loc_struct", "x y direc cost")
	xy_struct=namedtuple("xy_struct","x y angle")
	simple_map=[[0, 0, 0, 0, 0, 0, 0, 0, 0],[0, 1, 1, 1, 1, 1, 0, 0, 0],[0, 1, 0, 1, 0, 1, 1, 1, 0],[0, 1, 1, 1, 1, 1, 0, 1, 0],[0, 1, 0, 1, 0, 0, 0, 1, 0],
	[0, 1, 0, 1, 1, 1, 1, 1, 0],[0, 1, 0, 1, 0, 0, 0, 1, 0],[0, 1, 1, 1, 1, 1, 1, 1, 0],[0, 0, 0, 0, 0, 0, 0, 0, 0]]
	map_type=[[0,1,0,0,0,0,0,0,0],[0,3,2,3,2,7,0,0,0],[0,1,0,1,0,3,2,7,0],[0,3,2,3,2,4,0,1,0],[0,1,0,1,0,0,0,1,0],
	[0,1,0,3,2,2,2,3,0],[0,1,0,1,0,0,0,1,0],[0,5,2,3,2,2,2,4,0],[0,0,0,0,0,0,0,0,0]]
	d_map=[[[False]*4 for i in range(9)] for j in range(9)]
	spot=[[[[0,0,0] for i in range(100)] for j in range(4)] for k in range(8)]
	direction=[[1,0],[0,1],[-1,0],[0,-1]] #+1은 우회전 -1 좌회전 +2는 반대
	speed = [0.0 for i in range(ai_num)]
	Aflag = [0 for i in range(ai_num)]
	Dflag = [0 for i in range(ai_num)]
	Wflag = [0 for i in range(ai_num)]
	Sflag = [0 for i in range(ai_num)]
	WA = [0.00 for i in range(ai_num)] # Wheel Angle
	CA = [0.00 for i in range(ai_num)] # Car Angle
	grabhandle = [False for i in range(ai_num)]
	fric = 0.0004
	handlefric = 1
	sx = [0 for i in range(ai_num)]
	sy = [0 for i in range(ai_num)]
	rx = [0 for i in range(ai_num)]
	ry = [0 for i in range(ai_num)]
	mydirec = [0 for i in range(ai_num)]
	chk_dest = [False for i in range(ai_num)]
	path = [list() for i in range(ai_num)]
	spath= [list() for i in range(ai_num)]
	prog=[0 for i in range(ai_num)]
	progleng=[0 for i in range(ai_num)]
	naviprog = [0 for i in range(ai_num)]
	pathleng = [0 for i in range(ai_num)]
	rotchk = [False for i in range(ai_num)]
	cntt=0
	spotn=0

	def R2A(self,R):
		return (180*R/math.pi)  # 라디안 -> 도 (PI -> 180)
	def A2R(self,A):
		return (A*math.pi/180)  # 도 -> 라디안 (180 -> PI)
	def R2S(self,rx,ry,angle):
		return (int)((rx+10)/20),(int)((ry+30)/20),(int)(((angle+45)%360)/90)
	def S2R(self,x,y):
		return x*20,y*20-20
	def __init__(self):
		self.ai1 = Container(0)
		self.lefttire1 = Container(0)
		self.righttire1 = Container(0)
		self.ai2 = Container(0)
		self.lefttire2 = Container(0)
		self.righttire2 = Container(0)
		self.ai3 = Container(0)
		self.lefttire3 = Container(0)
		self.righttire3 = Container(0)
		self.ai4 = Container(0)
		self.lefttire4 = Container(0)
		self.righttire4 = Container(0)
		self.ai5 = Container(0)
		self.lefttire5 = Container(0)
		self.righttire5 = Container(0)
		self.ai6 = Container(0)
		self.lefttire6 = Container(0)
		self.righttire6 = Container(0)

		for i in range(1,self.map_size+1):
			for j in range(1,self.map_size+1):
				for k,direc in enumerate(self.direction):
					if(self.simple_map[i][j]==1 and self.simple_map[i+direc[0]][j+direc[1]]==1):
						self.d_map[i][j][k]=True
		self.simple_map[0][1]=0
		self.d_map[0][1][0]=True
		self.d_map[1][1][2]=True

		for i in range(self.ai_num):
			self.speed[i]=0.1

		#type1 세로길
		inner=6
		outer=15
		nspot=10
		self.spotn=nspot
		angs=90/nspot
		for i in range(nspot):
			self.spot[1][0][i][0]=20/(nspot)*(i+1)
			self.spot[1][0][i][1]=outer-1
			self.spot[1][0][i][2]=0
			self.spot[1][2][i][0]=20/(nspot)*((nspot-1)-i)
			self.spot[1][2][i][1]=inner
			self.spot[1][2][i][2]=180
		#type2 가로길
		for i in range(nspot):
			self.spot[2][1][i][0]=inner
			self.spot[2][1][i][1]=20/(nspot)*(i+1)
			self.spot[2][1][i][2]=90
			self.spot[2][3][i][0]=outer-1
			self.spot[2][3][i][1]=20/(nspot)*((nspot-1)-i)
			self.spot[2][3][i][2]=270
		#type4
		for i in range(nspot):
			self.spot[4][2][i][0]=inner*math.sin(self.A2R(angs*((nspot-1)-i)))
			self.spot[4][2][i][1]=inner*math.cos(self.A2R(angs*((nspot-1)-i)))
			self.spot[4][2][i][2]=90+angs*(i+1)
			self.spot[4][3][i][0]=outer*math.sin(self.A2R(angs*(i+1)))
			self.spot[4][3][i][1]=outer*math.cos(self.A2R(angs*(i+1)))
			self.spot[4][3][i][2]=360-angs*(i+1)
		#type5
		for i in range(nspot):
			self.spot[5][1][i][0]=inner*math.sin(self.A2R(angs*(1+i)))
			self.spot[5][1][i][1]=20-inner*math.cos(self.A2R(angs*(1+i)))
			self.spot[5][1][i][2]=angs*(i+1)
			self.spot[5][2][i][0]=outer*math.sin(self.A2R(angs*((nspot-1)-i)))
			self.spot[5][2][i][1]=20-outer*math.cos(self.A2R(angs*((nspot-1)-i)))
			self.spot[5][2][i][2]=270-angs*(i+1)
		#type6
		for i in range(nspot):
			self.spot[6][0][i][0]=20-inner*math.sin(self.A2R(angs*((nspot-1)-i)))
			self.spot[6][0][i][1]=20-inner*math.cos(self.A2R(angs*((nspot-1)-i)))
			self.spot[6][0][i][2]=(270+angs*(i+1))%360
			self.spot[6][1][i][0]=20-outer*math.sin(self.A2R(angs*(i+1)))
			self.spot[6][1][i][1]=20-outer*math.cos(self.A2R(angs*(i+1)))
			self.spot[6][1][i][2]=180-angs*(i+1)
		#type7
		for i in range(nspot):
			self.spot[7][3][i][0]=20-inner*math.sin(self.A2R(angs*(1+i)))
			self.spot[7][3][i][1]=inner*math.cos(self.A2R(angs*(1+i)))
			self.spot[7][3][i][2]=180+angs*(i+1)
			self.spot[7][0][i][0]=20-outer*math.sin(self.A2R(angs*((nspot-1)-i)))
			self.spot[7][0][i][1]=outer*math.cos(self.A2R(angs*((nspot-1)-i)))
			self.spot[7][0][i][2]=90-angs*(i+1)

					
		return
	def OnCreate(self,uid):
		self.aitrans1 = self.ai1.FindComponentByType("TransformGroup")
		self.aipos1 = self.aitrans1.GetPosition()
		self.airot1 = self.aitrans1.GetRotation()
		self.lefttiretrans1 = self.lefttire1.FindComponentByType("TransformGroup")
		self.righttiretrans1 = self.righttire1.FindComponentByType("TransformGroup")

		self.aitrans2 = self.ai2.FindComponentByType("TransformGroup")
		self.aipos2 = self.aitrans2.GetPosition()
		self.airot2 = self.aitrans2.GetRotation()
		self.lefttiretrans2 = self.lefttire2.FindComponentByType("TransformGroup")
		self.righttiretrans2 = self.righttire2.FindComponentByType("TransformGroup")

		self.aitrans3 = self.ai3.FindComponentByType("TransformGroup")
		self.aipos3 = self.aitrans3.GetPosition()
		self.airot3 = self.aitrans3.GetRotation()
		self.lefttiretrans3 = self.lefttire3.FindComponentByType("TransformGroup")
		self.righttiretrans3 = self.righttire3.FindComponentByType("TransformGroup")

		self.aitrans4 = self.ai4.FindComponentByType("TransformGroup")
		self.aipos4 = self.aitrans4.GetPosition()
		self.airot4 = self.aitrans4.GetRotation()
		self.lefttiretrans4 = self.lefttire4.FindComponentByType("TransformGroup")
		self.righttiretrans4 = self.righttire4.FindComponentByType("TransformGroup")

		self.aitrans5 = self.ai5.FindComponentByType("TransformGroup")
		self.aipos5 = self.aitrans5.GetPosition()
		self.airot5 = self.aitrans5.GetRotation()
		self.lefttiretrans5 = self.lefttire5.FindComponentByType("TransformGroup")
		self.righttiretrans5 = self.righttire5.FindComponentByType("TransformGroup")

		self.aitrans6 = self.ai6.FindComponentByType("TransformGroup")
		self.aipos6 = self.aitrans6.GetPosition()
		self.airot6 = self.aitrans6.GetRotation()
		self.lefttiretrans6 = self.lefttire6.FindComponentByType("TransformGroup")
		self.righttiretrans6 = self.righttire6.FindComponentByType("TransformGroup")
		return
	def OnDestory(self):
		return
	def OnEnable(self):
		return
	def OnDisable(self):
		return
	def Update(self):
		self.AI_Update(self.aitrans1,self.aipos1,self.airot1,self.lefttiretrans1,self.righttiretrans1,0)
		self.AI_Update(self.aitrans2,self.aipos2,self.airot2,self.lefttiretrans2,self.righttiretrans2,1)
		self.AI_Update(self.aitrans3,self.aipos3,self.airot3,self.lefttiretrans3,self.righttiretrans3,2)
		self.AI_Update(self.aitrans4,self.aipos4,self.airot4,self.lefttiretrans4,self.righttiretrans4,3)
		self.AI_Update(self.aitrans5,self.aipos5,self.airot5,self.lefttiretrans5,self.righttiretrans5,4)
		self.AI_Update(self.aitrans6,self.aipos6,self.airot6,self.lefttiretrans6,self.righttiretrans6,5)
		return
	def OnMessage(self, msg, number, Vector4_lparm, Vector4_wparam):
		return

	def AI_Update(self,cartrans,carpos,carrot,tiretrans1,tiretrans2,n):
		self.move(cartrans,carpos,carrot,n)
		self.inkey(cartrans,carpos,carrot,tiretrans1,tiretrans2,n)
		#self.fricfunc(n)
		if(self.chk_dest[n]==True and self.dist(self.rx[n],self.ry[n],self.spath[n][self.prog[n]].x,self.spath[n][self.prog[n]].y)<(float)(20/self.spotn)):
			self.prog[n]+=1
			self.rotchk[n]=False
			#if(self.prog[n]==self.progleng[n]-1-self.spotn):
			#	self.chk_dest[n]=False
		if(self.CA[n]%90==0 and self.chk_dest[n]==True and self.sx[n]==self.path[n][self.pathleng[n]-1].x and self.sy[n]==self.path[n][self.pathleng[n]-1].y):
			self.chk_dest[n]=False
		if(self.chk_dest[n]==False):
			self.set_destination(n)
		self.order(carpos,cartrans,n)
		return

	def inkey(self,cartrans,carpos,carrot,tiretrans1,tiretrans2,n):
		self.grabhandle[n]=False
		if (self.Wflag[n] == 1):
			self.speed[n] += 0.001
		if (self.Sflag[n] == 1 and self.speed[n] > -0.03):
			self.speed[n] -= 0.005
		if (self.Aflag[n] == 1):
			self.grabhandle[n]=True
			if(self.WA[n]>=-45):
				self.WA[n] -= 0.5
		if (self.Dflag[n] == 1 ):
			self.grabhandle[n]=True
			if(self.WA[n]<=45):
				self.WA[n] += 0.5
		#if (self.speed[n] != 0):
		#	if(self.WA[n]<0):
				#cartrans.Rotate(-10*self.speed[n],0,(0,1,0))
				#self.CA[n] -= 10*self.speed[n]
		#	if(self.WA[n]>0):
				#cartrans.Rotate(10*self.speed[n],0,(0,1,0))
				#self.CA[n] += 10*self.speed[n]
			self.CA[n]=self.CA[n]%360
		tiretrans1.SetLocalRotation(self.EulerToQuaternionFloat(Math3d.Vector3(0,self.A2R(self.WA[n]),0))) #tire rotate
		tiretrans2.SetLocalRotation(self.EulerToQuaternionFloat(Math3d.Vector3(0,self.A2R(self.WA[n]),0))) #tire rotate
		return

	def fricfunc(self,n):
		if(self.speed[n]>self.fric):
			self.speed[n]-=self.fric
		elif(self.speed[n]<0 and self.speed[n]+self.fric<0):
			self.speed[n]+=self.fric
		if(self.grabhandle[n] == False):
			if(self.WA[n]>0):
				self.WA[n]-=self.handlefric
			elif(self.WA[n]<0):
				self.WA[n]+=self.handlefric
		return

	def move(self,cartrans,carpos,carrot,n):
		#carpos.x += self.speed[n]*(math.sin(self.A2R(self.WA[n]+self.CA[n])))
		#carpos.z += self.speed[n]*(math.cos(self.A2R(self.WA[n]+self.CA[n])))
		#self.cntt+=1
		#if(self.cntt%10==1 and self.cntt>5):
		#	carpos.z=self.spath[n][self.prog[n]].x
		#	carpos.x=self.spath[n][self.prog[n]].y
		#	print(self.spath[n][self.prog[n]].angle)
		#	self.prog[n]+=1
		#	if(self.prog[n]==self.progleng[n]):
		#		self.prog[n]=0
		#cartrans.SetPosition(carpos)
		#print(self.sx[n],self.sy[n],self.mydirec[n])
		self.sx[n],self.sy[n],self.mydirec[n]=self.R2S(carpos.z,carpos.x,self.CA[n])
		self.rx[n]=carpos.z
		self.ry[n]=carpos.x
		return

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

	def set_destination(self,n):
		self.chk_dest[n]=True
		fx,fy=self.random_dest(n)
		#print("ai path")
		self.path[n]=self.navi(self.sx[n],self.sy[n],self.mydirec[n],fx,fy,n)
		self.spath[n]=self.calcul_spath(n)
		#print(self.path[n])
		return

	def random_dest(self,n):
		while(1):
			newx=random.randint(1,7)
			newy=random.randint(1,7)
			if((self.map_type[newx][newy]==1 or self.map_type[newx][newy]==2) and (newx!=self.sx[n] or newy!=self.sy[n])):
				return newx,newy

	def queue_get(self,a):
		return a.x,a.y,a.direc,a.cost
	def bfs(self,q,chk,via,fx,fy):
		rear=0
		while(rear<len(q)):
			x,y,direc,cost=self.queue_get(q[rear])
			if(x==fx and y==fy):
				return rear
			for i,dr in enumerate(self.direction):
				if(rear==0 and direc!=i):
					continue
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
	def navi(self,x,y,direc,fx,fy,n):
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
			#print("no path")
		else:
			bfspath=self.via_func(q,v,via)
			self.pathleng[n]=q[v].cost+1
			#print("path finded cost :",self.pathleng[n])
			self.naviprog[n]=0
		return bfspath

	def calcul_spath(self,n):
		#first spath
		spot_path=list()
		for i in range(0,self.pathleng[n]):
			road_type=self.map_type[self.path[n][i].x][self.path[n][i].y]
			if(road_type==3):
				if(self.path[n][i-1].direc==self.path[n][i].direc):
					if(self.path[n][i].direc%2==0):
						road_type=1
					else:
						road_type=2
				elif(self.path[n][i-1].direc==0):
					if(self.path[n][i].direc==3):
						road_type=4
					else:
						road_type=5
				elif(self.path[n][i-1].direc==1):
					if(self.path[n][i].direc==2):
						road_type=4
					else:
						road_type=7
				elif(self.path[n][i-1].direc==2):
					if(self.path[n][i].direc==3):
						road_type=7
					else:
						road_type=6
				elif(self.path[n][i-1].direc==3):
					if(self.path[n][i].direc==2):
						road_type=5
					else:
						road_type=6
			if(i==0):
				spot_path.append(self.real_loc(road_type,self.path[n][i].x,self.path[n][i].y,self.path[n][i].direc,self.spotn-1))
			else:
				for j in range(self.spotn):
					spot_path.append(self.real_loc(road_type,self.path[n][i].x,self.path[n][i].y,self.path[n][i].direc,j))
		self.prog[n]=0
		self.progleng[n]=len(spot_path)
		return spot_path
	
	def real_loc(self,tp,x,y,direc,num):
		temp=self.spot[tp][direc][num]
		rtn=self.xy_struct(x*20-10+temp[0],y*20-30+temp[1],temp[2])
		return rtn
	def order(self,carpos,cartrans,n):
		x1=self.rx[n]
		y1=self.ry[n]
		x2=self.spath[n][self.prog[n]].x
		y2=self.spath[n][self.prog[n]].y
		dx=(x2-x1)/self.dist(x1,y1,x2,y2)
		dy=(y2-y1)/self.dist(x1,y1,x2,y2)
		nowangle=self.spath[n][self.prog[n]].angle
		prevangle=self.spath[n][self.prog[n]].angle
		if(self.prog[n]>0):
			prevangle=self.spath[n][self.prog[n]-1].angle
			if(self.rotchk[n]==False):
				self.rotchk[n]=True
				self.CA[n]=nowangle
				cartrans.Rotate(nowangle-prevangle,0,(0,1,0))
		carpos.z+=dx*self.speed[n]
		carpos.x+=dy*self.speed[n]
		cartrans.SetPosition(carpos)
		if(self.speed[n]<0.2):
			self.Wflag[n]=1
		else:
			self.Wflag[n]=0
		if(nowangle-prevangle<0):
			self.Aflag[n]=1
			self.Dflag[n]=0
		elif(nowangle-prevangle>0):
			self.Dflag[n]=1
			self.Aflag[n]=0
		else:
			self.Aflag[n]=0
			self.Dflag[n]=0
		return
	def dist(self,x1,y1,x2,y2):
		return math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))
	def ccw(self,x0,y0,x1,y1,x2,y2):
		result=x1*y2-x2*y1
		if(result<0):
			return 1
		else:
			return 0
	def relf(self,angle):
		return angle/5