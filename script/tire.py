import math
import QuaternionMath

class tire(Actor.Actor):
	tireAngle = 0.0
	def __init__(self):
		self.tire=Container(0)
		return
	def OnCreate(self,uid):
		self.tiretrans = self.tire.FindComponentByType("TransformGroup")
		return

	def OnDestroy(self):
		return

	def OnEnable(self):
		return

	def OnDisable(self):
		return

	def Update(self):
		#self.tiretrans.SetRotation(QuaternionMath.EulerToQuaternionFloat(0,self.tireAngle,0)) 

		return
	def OnMessage(self, msg, number, Vector4_lparm, Vector4_wparm):
		if(msg=="angle"):
			self.tireAngle = Vector4_lparm.x
			print("message ok")
                        
