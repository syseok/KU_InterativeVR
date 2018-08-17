class crashingcollision(Actor.Actor):
	def __init__(self):
		self.car=Container(0)
		self.carbox = Container(0)
		self.wall1=Container(0)

		self.crash1=Container(0)
		self.crash2=Container(0)
		self.crash3=Container(0)



		return
	def OnCreate(self,uid):
		self.cartrans = self.carbox.FindComponentByType("TransformGroup")
		self.carscriptcomponent = self.car.FindComponentByType("ScriptComponent")
		self.carscript = self.carscriptcomponent.GetActor()

		self.walltrans1 = self.wall1.FindComponentByType("TransformGroup")

		self.crashtrans1 = self.crash1.FindComponentByType("TransformGroup")
		self.crashtrans2 = self.crash2.FindComponentByType("TransformGroup")
		self.crashtrans3 = self.crash3.FindComponentByType("TransformGroup")

		self.wbox1=self.walltrans1.GetWorldBox()


		return
	def OnDestory(self):
		return
	def OnEnable(self):
		return
	def OnDisable(self):
		return
	def Update(self):
		carbox=self.cartrans.GetWorldBox()
		crashbox1 = self.crashtrans1.GetWorldBox()
		crashbox2 = self.crashtrans2.GetWorldBox()
		crashbox3 = self.crashtrans3.GetWorldBox()

		self.collide(carbox,self.wbox1)
		self.collide(carbox,crashbox1)
		self.collide(carbox,crashbox2)
		self.collide(carbox,crashbox3)

		return
	def OnMessage(self, msg, number, Vector4_lparm, Vector4_wparam):
		return
	def collide(self,box1,box2):
		if(box1.OBBIntersect(box2)==True):
			print("coll")
			self.carscript.OnMessage("Coll_detect",0,Math3d.Vector4(0,0,0,0),Math3d.Vector4(0,0,0,0))
