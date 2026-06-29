from model.model import Model

mym = Model()
mym.buildGraph("Brazil")
n,e = mym.graphDetails()
print(n)
print(e)