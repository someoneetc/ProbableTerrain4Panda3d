import random
from xml.dom import minidom
from panda3d.egg import *
from panda3d.core import CSZupRight, LPoint3d


def _createFaces(data,floor_points,roof_points):
    floor = EggPolygon('floor')
    facade1 = EggPolygon('facade1')
    facade2 = EggPolygon('facade2')
    facade3 = EggPolygon('facade3')
    facade4 = EggPolygon('facade4')
    roof = EggPolygon('roof')

    material = EggMaterial('BaseMaterial')
    material.setBase((.05,.05,.05,.05))
    material.setEmit((0,0,0,0))
    material.setRoughness(0)
    material.setMetallic(1)
    data.addChild(material)

    floor.setMaterial(material)
    facade1.setMaterial(material)
    facade2.setMaterial(material)
    facade3.setMaterial(material)
    facade4.setMaterial(material)
    roof.setMaterial(material)


    for (fpt,rpt) in zip(floor_points,roof_points):
        floor.addVertex(fpt)
        roof.addVertex(rpt)
    data.addChild(floor)
    data.addChild(roof)
    floor.setNormal((0,0,1))

    #Facades should be number of points + 1
    for i in range(len(floor_points) + 1):
        facade = EggPolygon()
        facade.addVertex(floor_points[i % len(floor_points)])
        facade.addVertex(floor_points[(i + 1) % len(floor_points)])
        facade.addVertex(roof_points[(i + 1) % len(floor_points)])
        facade.addVertex(roof_points[i % len(floor_points)])
        data.addChild(facade)


def _parsePoints(pointsSvg):
    return list(map(lambda pt : list(map(lambda x: float(x), pt.split(','))), pointsSvg.split(' ')))

def generateBuilding(filePath,outputPath):
    z_up = EggCoordinateSystem()
    z_up.setValue(CSZupRight)

    data = EggData()
    data.addChild(z_up)
    vp = EggVertexPool('vertexPool')
    data.addChild(vp)



    #FLOOR
    colorSet = {
            'major-roads': 0xfafa7a,
            'minor-road': 0xf8f8f8,
            'buildings': {
                'stroke': 0x282828,
                'fill': 0xece5db
                },
            'water': 0xa9d9fe,
            #TODO other colors
        }

    doc = minidom.parse(filePath)  # parseString also exists


    for line in doc.getElementsByTagName('polyline'):
        if (line.getAttribute('fill') != '' and
            int(line.getAttribute('stroke').replace('#',''),16) == colorSet['buildings']['stroke'] and 
            int(line.getAttribute('fill').replace('#',''),16) == colorSet['buildings']['fill']):
            points = _parsePoints(line.getAttribute('points'))
            polygon = EggPolygon()
            data.addChild(polygon)
            height = random.uniform(10.0,30.0)
            floor_points = []
            roof_points = []
            for pt in list(reversed(points)):
                v = EggVertex()
                v.setPos(LPoint3d(pt[0],pt[1],0))
                vp.addVertex(v)
                floor_points.append(v)

                v2 = EggVertex()
                v2.setPos(LPoint3d(pt[0],pt[1],height))
                vp.addVertex(v2)
                roof_points.append(v2)


            _createFaces(data,floor_points,roof_points)


    
    doc.unlink()
    data.writeEgg(outputPath)
