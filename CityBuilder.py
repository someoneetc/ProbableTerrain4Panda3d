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

def generateBuilding():
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

    doc = minidom.parse('map.svg')  # parseString also exists
    #colorSet = set()
    #for path in doc.getElementsByTagName('polyline'):
    #    colorSet.add(path.getAttribute('stroke')) 




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
    data.writeEgg('test.egg')
    return None

    v1 = EggVertex()
    v1.setUv((0,0))
    v1.setPos(LPoint3d(-cell_scale/2,-cell_scale/2,0)),
    vp.addVertex(v1)

    """
    #ROOF
    v5 = EggVertex()
    v5.setUv((1 * tex_x,0))
    v5.setPos(LPoint3d(-cell_scale/2,-cell_scale/2,height)),
    vp.addVertex(v5)
    v6 = EggVertex()
    v6.setUv((1 * tex_x,1 * tex_y))
    v6.setPos(LPoint3d(cell_scale/2,-cell_scale/2,height)),
    vp.addVertex(v6)
    v7 = EggVertex()
    v7.setUv((1 * tex_x,2 * tex_y))
    v7.setPos(LPoint3d(cell_scale/2,cell_scale/2,height)),
    vp.addVertex(v7)
    v8 = EggVertex()
    v8.setUv((1 * tex_x,3 * tex_y))
    v8.setPos(LPoint3d(-cell_scale/2,cell_scale/2,height)),
    vp.addVertex(v8)
    
    roofHook = LVector3f(
                (-cell_scale/2 + cell_scale/2) / 2,
                (-cell_scale/2 + cell_scale/2) / 2,
                height,
            )

    data.addChild(vp)

    
    
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


    floor.addVertex(v1)
    floor.addVertex(v2)
    floor.addVertex(v3)
    floor.addVertex(v4)
    data.addChild(floor)
    floor.setNormal((0,0,1))
    floor.triangulateInPlace(True)

    facade1.addVertex(v1)
    facade1.addVertex(v2)
    facade1.addVertex(v6)
    facade1.addVertex(v5)
    facade1.setNormal((0,0,1))
    data.addChild(facade1)
    facade1.triangulateInPlace(True)

    facade2.addVertex(v2)
    facade2.addVertex(v3)
    facade2.addVertex(v7)
    facade2.addVertex(v6)
    facade2.setNormal((0,0,1))
    data.addChild(facade2)
    facade2.triangulateInPlace(True)

    facade3.addVertex(v3)
    facade3.addVertex(v4)
    facade3.addVertex(v8)
    facade3.addVertex(v7)
    facade3.setNormal((0,0,1))
    data.addChild(facade3)
    facade3.triangulateInPlace(True)

    facade4.addVertex(v4)
    facade4.addVertex(v1)
    facade4.addVertex(v5)
    facade4.addVertex(v8)
    facade4.setNormal((0,0,1))
    data.addChild(facade4)
    facade4.triangulateInPlace(True)

    roof.addVertex(v5)
    roof.addVertex(v6)
    roof.addVertex(v7)
    roof.addVertex(v8)
    roof.setNormal((0,0,1))
    data.addChild(roof)
    roof.triangulateInPlace(True)

    
    return data, roofHook
    """

