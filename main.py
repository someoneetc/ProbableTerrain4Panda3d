import CityBuilder

from direct.showbase.ShowBase import ShowBase

class Test(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        CityBuilder.generateBuilding('examples/map1.svg','output/test.egg')

        loader.loadModel('output/test.egg').reparentTo(render)


test = Test()
test.run()
