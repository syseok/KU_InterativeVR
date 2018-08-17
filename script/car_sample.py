class car_sample(Actor.Actor):
	def __init__(self):
		self.car = Container(0)
		return

	def OnCreate(self,uid):		 
		self.cartrans = self.car.FindComponentByType("TransformGroup")
		self.carpos = self.cartrans.GetPosition()
		return

	def OnDestroy(self):
		return

	def OnEnable(self):
		return

	def OnDisable(self):
		return

	def Update(self):
		self.carpos.z += 0.05 
		self.cartrans.SetPosition(self.carpos)
		return
	
	


