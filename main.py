import CityBuilder

from direct.showbase.ShowBase import ShowBase

class Test(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        buildings = CityBuilder.generateBuilding()

        loader.loadModel('test.egg').reparentTo(render)


test = Test()
test.run()
