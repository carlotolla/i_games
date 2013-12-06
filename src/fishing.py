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


class Aquarium:
    def __init__(self, bry, _cons):
        self.bry = bry
        #print(bry, dir(bry))
        cameraC = _cons(bry.THR.PerspectiveCamera)
        self.camera = cameraC(75, 1, 1, 10000)
        self.camera.position.z = 1000

        sceneC = _cons(bry.THR.Scene)
        self.scene = sceneC()

        geometry = _cons(bry.THR.CubeGeometry)(200, 200, 200)
        material = _cons(bry.THR.MeshBasicMaterial)({"color": "#FF0000", "wireframe": True})
        geometry = _cons(bry.THR.SphereGeometry)(200, 15, 15)
        a = _cons(bry.THR.Vector3)(1, 1.2, 1.5)
        scale = _cons(bry.THR.Matrix4)().makeScale(a)
        geometry.applyMatrix(scale)
        material = _cons(bry.THR.MeshBasicMaterial)({"color": "#FF0000", "wireframe": True})

        meshC = _cons(bry.THR.Mesh)
        self.mesh = meshC(geometry, material)
        self.scene.add(self.mesh)

        rendererC = _cons(bry.THR.CanvasRenderer)
        self.renderer = rendererC()
        self.renderer.setSize(444, 444)
        bry.DOC['main'].appendChild(self.renderer.domElement)
        self.renderer.render(self.scene, self.camera)

    def animate(self, i):
        # note: bry.THR.js includes requestAnimationFrame shim
        self.bry.WIN.requestAnimationFrame(self.animate)

        self.mesh.rotation.x += 0.01
        self.mesh.rotation.y += 0.02

        self.renderer.render(self.scene, self.camera)


def main(bry, _cons):
    print('Fishing %s' % __version__)
    Aquarium(bry, _cons).animate(0)