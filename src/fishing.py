"""
############################################################
Fishing - An adventure in the deep sea
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: 2013/11/29
:Status: This is a "work in progress"
:Home: `Labase <http://labase.selfip.org/>`__
:Copyright: 2013, `GPL <http://is.gd/3Udt>`__.

Fishing is a photo safari in the deeps of the ocean.
"""
__version__ = '0.1.0'

SCENE = None


class Aquarium:
    def __init__(self, bry, _cons):
        global SCENE
        self.bry, self._cons, self._thr = bry, _cons, bry.THR
        #print(bry, dir(bry))
        cameraC = _cons(self._thr.PerspectiveCamera)
        self.camera = cameraC(75, 1, 1, 10000)
        self.camera.position.z = 1000

        sceneC = _cons(self._thr.Scene)
        SCENE = self.scene = sceneC()

        geometry = _cons(self._thr.CubeGeometry)(200, 200, 200)
        material = _cons(self._thr.MeshBasicMaterial)({"color": "#FF0000", "wireframe": True})
        geometry = _cons(self._thr.SphereGeometry)(200, 20, 20)
        svect = _cons(self._thr.Vector3)(1, 1.2, 1.5)
        #svect = _cons(self._thr.Vector3)(1, 1, 1)
        scale = _cons(self._thr.Matrix4)().makeScale(1, 1.2, 1.5)
        #geometry.applyMatrix(scale)
        material = _cons(self._thr.MeshBasicMaterial)({"color": "#FF0000", "wireframe": False})
        self.box(pos=(300, -100, 200))
        self.ellipsoid(pos=(-300, 100, 200), length=300, width=170, height=150, color='#FFFF00', opacity=0.5)

        meshC = _cons(self._thr.Mesh)
        self.mesh = meshC(geometry, material)
        self.scene.add(self.mesh)
        self.mesh.scale = svect
        rendererC = _cons(self._thr.CanvasRenderer)
        self.renderer = rendererC()
        self.renderer.setSize(444, 444)
        bry.DOC['main'].appendChild(self.renderer.domElement)
        bry.DOC['main'].style.background = "black"
        self.renderer.render(self.scene, self.camera)

    def frame(self):
        return self._cons(self._thr.Object3D)()

    def box(self, pos=(0, 0, 0), length=100, width=100, height=100,
            color="#000000", opacity=1, wire = False, axis=(0, 0, 0), frame=SCENE):
        geometry = self._cons(self._thr.CubeGeometry)(length, width, height)
        material = self._cons(self._thr.MeshNormalMaterial)({"color": color, "wireframe": wire, "opacity": opacity})
        element = self._cons(self._thr.Mesh)(geometry, material)
        element.position.x, element.position.y, element.position.z = pos
        element.rotation.x, element.rotation.y, element.rotation.z = axis
        frame = frame or self.scene
        frame.add(element)
        return element

    def sphere(self, pos=(0, 0, 0), length=100, hor=20, vert=20,
               color="#000000", opacity=1, wire = False, axis=(1, 0, 0), frame=SCENE):
        geometry = self._cons(self._thr.SphereGeometry)(length, hor, vert)
        material = self._cons(self._thr.MeshBasicMaterial)({"color": color, "wireframe": wire, "opacity": opacity})
        element = self._cons(self._thr.Mesh)(geometry, material)
        element.position.x, element.position.y, element.position.z = pos
        element.rotation.x, element.rotation.y, element.rotation.z = axis
        frame = frame or self.scene
        frame.add(element)
        return element

    def ellipsoid(self, pos=(0, 0, 0), length=100, width=20, height=20, hor=20, vert=20,
                  color="#000000", opacity=1, wire = False, axis=(1, 0, 0), frame=SCENE):
        geometry = self._cons(self._thr.SphereGeometry)(length/2, hor, vert)
        material = self._cons(self._thr.MeshBasicMaterial)({"color": color, "wireframe": wire, "opacity": opacity})
        element = self._cons(self._thr.Mesh)(geometry, material)
        element.position.x, element.position.y, element.position.z = pos
        element.rotation.x, element.rotation.y, element.rotation.z = axis
        element.scale = self._cons(self._thr.Vector3)(1, width/length, height/length)
        frame = frame or self.scene
        frame.add(element)
        return element

    def animate(self, i):
        # note: self._thr.js includes requestAnimationFrame shim
        self.bry.WIN.requestAnimationFrame(self.animate)

        self.mesh.rotation.x += 0.01
        self.mesh.rotation.y += 0.02

        self.renderer.render(self.scene, self.camera)


def main(bry, _cons):
    print('Fishing %s' % __version__)
    Aquarium(bry, _cons).animate(0)