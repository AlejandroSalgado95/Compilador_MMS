from VirtualAddresses import VirtualAdresses

class EmptyTempMemoryInstantiator():
	def __init__(self):
		self.EmptyTempMemory = {
		"localInt" : VirtualAdresses(15300, 15399,"localInt"),
		"localFloat" : VirtualAdresses(15400, 15499,"localFloat"),
		"localChar" : VirtualAdresses(15500, 15599,"localChar"),
		"tempInt" : VirtualAdresses(15600, 15699,"tempInt"),
		"tempFloat" : VirtualAdresses(15700, 15799,"tempFloat"),
		"tempChar" : VirtualAdresses(15800, 15899,"tempChar"),
		"tempBool" : VirtualAdresses(15900, 15998,"tempBool")
		}
	
	def InstateEmptyTempMemory(self):
		newEmptyTempMemory = self.EmptyTempMemory
		return newEmptyTempMemory

