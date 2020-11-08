import sys

sourceInputCode = sys.argv[1]
myParser = open("parser.py")
openedParser = myParser.read()
sys.argv = ["parser.py", sourceInputCode]
exec(openedParser)

myVirtualMachine = open("VirtualMachine.py")
openedVirtualMachine = myVirtualMachine.read()
exec(openedVirtualMachine)
