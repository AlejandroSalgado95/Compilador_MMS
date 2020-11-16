class Operand():
    def __init__(self, oName, oValue ,oType, oVAddress):
        self.name = oName
        self.value = oValue
        self.type = oType
        self.vAddress = oVAddress
        self.fakeAddress = ""