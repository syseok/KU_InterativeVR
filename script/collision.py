class collision(Actor.Actor):
	def __init__(self):
		self.car=Container(0)

		self.wall1=Container(0)
		self.wall2=Container(0)
		self.wall3=Container(0)
		self.wall4=Container(0)
		self.wall5=Container(0)
		self.wall6=Container(0)
		self.wall7=Container(0)
		self.wall8=Container(0)
		self.wall9=Container(0)

		return
	def OnCreate(self,uid):
		self.cartrans = self.car.FindComponentByType("TransformGroup")
		self.carscriptcomponent = self.car.FindComponentByType("ScriptComponent")
		self.carscript = self.carscriptcomponent.GetActor()

		self.walltrans1 = self.wall1.FindComponentByType("TransformGroup")
		self.walltrans2 = self.wall2.FindComponentByType("TransformGroup")
		self.walltrans3 = self.wall3.FindComponentByType("TransformGroup")
		self.walltrans4 = self.wall4.FindComponentByType("TransformGroup")
		self.walltrans5 = self.wall5.FindComponentByType("TransformGroup")
		self.walltrans6 = self.wall6.FindComponentByType("TransformGroup")
		self.walltrans7 = self.wall7.FindComponentByType("TransformGroup")
		self.walltrans8 = self.wall8.FindComponentByType("TransformGroup")
		self.walltrans9 = self.wall9.FindComponentByType("TransformGroup")

		self.wbox1=self.walltrans1.GetSumBox()
		self.wbox2=self.walltrans2.GetSumBox()
		self.wbox3=self.walltrans3.GetSumBox()
		self.wbox4=self.walltrans4.GetSumBox()
		self.wbox5=self.walltrans5.GetSumBox()
		self.wbox6=self.walltrans6.GetSumBox()
		self.wbox7=self.walltrans7.GetSumBox()
		self.wbox8=self.walltrans8.GetSumBox()
		self.wbox9=self.walltrans9.GetSumBox()

		return
	def OnDestory(self):
		return
	def OnEnable(self):
		return
	def OnDisable(self):
		return
	def Update(self):
		carbox=self.cartrans.GetSumBox()
		self.collide(carbox,self.wbox1)
		self.collide(carbox,self.wbox2)
		self.collide(carbox,self.wbox3)
		self.collide(carbox,self.wbox4)
		self.collide(carbox,self.wbox5)
		self.collide(carbox,self.wbox6)
		self.collide(carbox,self.wbox7)
		self.collide(carbox,self.wbox8)
		self.collide(carbox,self.wbox9)
		return
	def OnMessage(self, msg, number, Vector4_lparm, Vector4_wparam):
		return
	def collide(self,box1,box2):
		if(box1.OBBIntersect(box2)==True):
			print("coll")
			self.carscript.OnMessage("Coll_detect",0,Math3d.Vector4(0,0,0,0),Math3d.Vector4(0,0,0,0))