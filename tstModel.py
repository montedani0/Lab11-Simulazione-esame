from model.model import Model

mym = Model()
mym.buildGraph(1)
n,e = mym.getGraphDetails()
print(n)
print(e)

