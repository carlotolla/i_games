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
from math import atan2 as at2
from math import sqrt, pi
__version__ = '0.1.0'

SCENE = None
RES = 40
PHI = (1+sqrt(5))/2
PHI2 = PHI**2
PHI3 = PHI**3
PHI4 = PHI**4
GRAUS_30 = pi/6.0
EIXO_Z = (0, 0, 1)
EIXO_NE = (1, 1, 0)
EIXO_SE = (1, -1, 0)
EIXO_SSE = (2, -1, 1)
EIXO_SSO = (2, -1, -1)
html4_names_to_hex = {'aqua': '#00ffff',
                      'black': '#000000',
                      'blue': '#0000ff',
                      'fuchsia': '#ff00ff',
                      'cyan': '#00ffff',
                      'green': '#008000',
                      'grey': '#808080',
                      'lime': '#00ff00',
                      'maroon': '#800000',
                      'navy': '#000080',
                      'olive': '#808000',
                      'purple': '#800080',
                      'red': '#ff0000',
                      'silver': '#c0c0c0',
                      'teal': '#008080',
                      'white': '#ffffff',
                      'yellow': '#ffff00'}


class Color:
    aqua = '#00ffff'
    black = '#000000'
    blue = '#0000ff'
    fuchsia = '#ff00ff'
    cyan = '#00ffff'
    green = '#008000'
    grey = '#808080'
    lime = '#00ff00'
    maroon = '#800000'
    navy = '#000080'
    olive = '#808000'
    purple = '#800080'
    red = '#ff0000'
    silver = '#c0c0c0'
    teal = '#008080'
    white = '#ffffff'
    yellow = '#ffff00'


class WGLVisual:
    def __init__(self, bry, _cons):
        global SCENE
        self.bry, self._cons, self._thr = bry, _cons, bry.THR

        SCREEN_WIDTH = bry.WIN.innerWidth
        SCREEN_HEIGHT = bry.WIN.innerHeight
        VIEW_ANGLE = 45
        ASPECT = 1  # SCREEN_WIDTH / SCREEN_HEIGHT
        NEAR = 1  # 0.1
        FAR = 10000
        self.camera = _cons(self._thr.PerspectiveCamera)(75, 1, 1, 10000)
        #self.camera = _cons(self._thr.PerspectiveCamera)(VIEW_ANGLE, ASPECT, NEAR, FAR)
        self.camera.position.z = 1000
        #self.camera.position.set(0, 150, 1000)

        SCENE = self.scene = _cons(self._thr.Scene)()
        #self.camera.lookAt(self.scene.position)
        #self.renderer = _cons(self._thr.CanvasRenderer)()
        self.renderer = _cons(self._thr.WebGLRenderer)({"antialias": True})
        self.renderer.setSize(444, 444)
        bry.DOC['main'].appendChild(self.renderer.domElement)
        #bry.DOC['main'].style.background = "black"
        self.draw()
        self.renderer.render(self.scene, self.camera)

    def draw(self):
        return None

    def frame(self, frame=SCENE):
        element = self._cons(self._thr.Object3D)()
        frame = frame or self.scene
        frame.add(element)
        return element

    def wglelement(self, geometry, pos=(0, 0, 0), sx=1.0, sy=1.0, sz=1.0, size=None, offrz=0.0,
                   color="#FFFFFF", opacity=1.0, wire = False, axis=(0, 0, 0), frame=SCENE):
        material = self._cons(self._thr.MeshBasicMaterial)({"color": color, "wireframe": wire, "opacity": opacity})
        #material = self._cons(self._thr.MeshPhongMaterial)(dict(
        #    ambient='#660000', color='#ff0000',
        #    specular='#ff8080', shininess=50))
        #material = self._cons(self._thr.MeshPhongMaterial)(dict(color=100, shininess=50))
        #material = self._cons(self._thr.MeshLambertMaterial)()  # ({"color": "rgb(250, 0,0)"})
        material.color = self._cons(self._thr.Color)(color)  # "#FF0000"

        element = self._cons(self._thr.Mesh)(geometry, material)

        def posit(x=0, y=0, z=0):
            element.position.x, element.position.y, element.position.z = int(x), int(y), int(z)
        posit(*pos)
        #raxis = lambda x, y, z: (at2(z, y), at2(z, x)+offrz, at2(y, x))
        #raxis = lambda y, x, z: (at2(y, z), at2(x, z)+offrz, at2(x, y))
        #raxis = lambda y, x, z: (at2(y, z), at2(z, x)+offrz, at2(x, y))
        #raxis = lambda y, x, z: (at2(y, z), at2(z, x)+offrz, at2(x, y))

        def raxis(y, x, z):
            return (at2(y, z), at2(z, x)+offrz, at2(x, y))
        print (raxis(*axis))
        element.rotation.x, element.rotation.y, element.rotation.z = raxis(*axis)
        element.scale = self._cons(self._thr.Vector3)(sx, sy, sz)
        frame = frame or self.scene
        frame.add(element)
        return element

    def vect(self, x, y, z):
        return self._cons(self._thr.Vector3)(x, y, z)

    def face(self, x, y, z):
        return self._cons(self._thr.Face3)(x, y, z)

    def box(self, length=100, width=100, height=100, **kwargs):
        geometry = self._cons(self._thr.CubeGeometry)(length, height, width)
        return self.wglelement(geometry, **kwargs)

    def ring(self, radius=100, thickness=10, hor=10, vert=RES, **kwargs):
        geometry = self._cons(self._thr.TorusGeometry)(radius, thickness, hor, vert)
        return self.wglelement(geometry, **kwargs)

    def pyramid(self, size=(100, 100, 100), base=4, top=0, **kwargs):
        a, b, c = size
        geometry = self._cons(self._thr.PyramidGeometry)(a, b, c)
        return self.wglelement(geometry, **kwargs)

    def npyramid(self, size=(100, 100, 100), base=4, top=0, **kwargs):
        geometry = self._cons(self._thr.CylinderGeometry)(top, size[0]/sqrt(2), size[1], base, false)
        aspect = size[2]/size[0]
        return self.wglelement(geometry, sx=aspect, sz=1/aspect, offrz=pi/4, **kwargs)

    def cone(self, radius=50, height=100, base=RES, top=0, **kwargs):
        geometry = self._cons(self._thr.CylinderGeometry)(top, radius, height, base, false)
        return self.wglelement(geometry, **kwargs)

    def sphere(self, radius=100, hor=RES, vert=RES, **kwargs):
        geometry = self._cons(self._thr.SphereGeometry)(radius, hor, vert)
        return self.wglelement(geometry, **kwargs)

    def ellipsoid(self, length=100, width=100, height=20, hor=RES, vert=RES, **kwargs):

        geometry = self._cons(self._thr.SphereGeometry)(length/2, hor, vert)
        return self.wglelement(geometry, sy=width/length, sz=height/length, **kwargs)


''' '''


class Peixe(WGLVisual):
    def __init__(self, bry, _cons):
        """Construtor do ser marinho, definindo um esqueleto(frame) e desenhando"""
        WGLVisual.__init__(self, bry, _cons)
        self.esqueleto = self.frame()
        self.tamanho = t = 400
        #self.ellipsoid(frame=self.esqueleto, pos=(0, 0), length=PHI*t, width=t, height=t/PHI, color='#00ffff')
        self.cor_do_corpo = '#00ffff'  # Color.cyan
        self.cor_cauda = cor_cauda = '#FF0000'  # Color.red
        #self.desenha_o_corpo(self.cor_do_corpo, l=t)
        self.cauda_superior = self.desenha_o_corpo(cor_cauda, l=t*1/PHI**2, d=(t*1.5/PHI, t*1/PHI4))
        self.cauda_inferior = self.desenha_o_corpo(cor_cauda, l=t*1/PHI**2, d=(t*1.5/PHI, t*-1/PHI4))
        #self.cauda_superior.rotate(angle=GRAUS_30, axis=EIXO_Z)
        #self.cauda_inferior.rotate(angle=-GRAUS_30, axis=EIXO_Z)
        self.labio_superior = self.desenha_o_labio(eixo=EIXO_NE)
        self.labio_inferior = self.desenha_o_labio(eixo=EIXO_SE)
        self.olho_esquerdo = self.desenha_o_olho(l=t, d=(-t*0.7/PHI, t*1/PHI4, t*1.2/PHI4))
        self.olho_direito = self.desenha_o_olho(l=t, d=(-t*0.7/PHI, t*1/PHI4, -t*1.2/PHI4))
        self.barbatana_dorsal = self.desenha_a_barbatana(l=t, d=(-t*0.1/PHI, t*1/PHI4), eixo = EIXO_NE)
        #self.nadadeira_direita = self.desenha_a_nadadeira(l=t, d=(-t*0.2/PHI, -t*0.1/PHI4), eixo = EIXO_SSE)
        #self.nadadeira_esquerda = self.desenha_a_nadadeira(l=t, d=(-t*0.2/PHI, -t*0.1/PHI4), eixo = EIXO_SSO)
    
    def desenha_a_barbatana(self, l=1, eixo=(0, 0, 0), d=(0, 0, 300)):
        return self.pyramid(
            frame=self.esqueleto, size=(l, int(l/PHI), int(l/PHI4)), pos=d, color=self.cor_cauda  # ,  axis=eixo
        )
    
    def desenha_a_nadadeira(self, l=1, eixo=(0, 0, 0), d=(0, 0)):
        return self.pyramid(
            frame=self.esqueleto, size=(l, l/PHI4, l/PHI), pos=d, color=self.cor_cauda,  axis=eixo
        )
    
    def desenha_o_labio(self, eixo):
        t = self.tamanho
        return self.ring(
            frame=self.esqueleto, pos=(t*-1.1/PHI, 0),  axis=eixo,
            radius=t*0.15,  thickness=t*0.07, color = self.cor_cauda
        )
    
    def desenha_o_corpo(self, cor, l=1, d=(0, 0)):
        return self.ellipsoid(
            frame=self.esqueleto, length=PHI*l, width=l, height=l/PHI, pos=d, color=cor
        )
    
    def desenha_o_olho(self, l=1, d=(0, 0, 0)):
        globo = l/PHI3
        return self.ellipsoid(
            frame=self.esqueleto, length=globo, width=globo, height=globo, pos=d, color=Color.blue
        )

    def animate(self, i):
        # note: self._thr.js includes requestAnimationFrame shim
        self.bry.WIN.requestAnimationFrame(self.animate)

        self.esqueleto.rotation.x += 0.01
        self.esqueleto.rotation.y += 0.02

        self.renderer.render(self.scene, self.camera)
''' '''


class Aquarium(WGLVisual):
    def __init__(self, bry, _cons):
        WGLVisual.__init__(self, bry, _cons)

    def draw(self):
        frame = self.frame()
        floorMaterial = self._cons(self._thr.MeshBasicMaterial)({"color": Color.yellow, "wireframe": False})
        floorGeometry = self._cons(self._thr.PlaneGeometry)(10000, 10000, 10, 10)
        floor = self._cons(self._thr.Mesh)(floorGeometry, floorMaterial)
        #floor.position.y = -1
        floor.rotation.x = pi / 2
        self.scene.add(floor)
        self.box(frame=frame, pos=(0, 0, 0), length=200, width=200, height=200, color= Color.red)
        self.pyramid(frame=frame, pos=(300, 0, 0), size=(300, 200, 200), color= Color.red, axis=(1, 0, 0))
        self.pyramid(frame=frame, pos=(300, 300, 0), size=(300, 200, 200), color= Color.lime, axis=(1, 1, 0))
        self.pyramid(frame=frame, pos=(0, 300, 0), size=(300, 200, 200), color= Color.cyan, axis=(0, 1, 0))
        self.pyramid(frame=frame, pos=(-300, 300, 0), size=(300, 200, 200), color= Color.blue, axis=(-1, 1, 0))
        self.pyramid(frame=frame, pos=(-300, 0, 0), size=(300, 200, 200), color= Color.navy, axis=(-1, 0, 0))
        self.pyramid(frame=frame, pos=(0, -300, 0), size=(300, 200, 200), color= Color.green, axis=(0, -1, 0))
        '''
        self.pyramid(frame=frame, pos=(0, 0, -300), size=(300, 200, 200), color= Color.yellow, axis=(0, 0, -1))
        self.pyramid(frame=frame, pos=(0, 0, 300), size=(300, 200, 200), color= Color.fuchsia, axis=(0, 0, 1))
        '''
        #self.pyramid(frame=frame, pos=(0, 200, 200), size=(300, 200, 250), color= Color.blue, axis=(1, 0, 0))
        #self.pyramid(frame=frame, pos=(-400, 400, 200), size=(300, 200, 250), color= Color.green, axis=(1, 1, 0))
        #self.pyramid(frame=frame, pos=(-200, 400, 200), size=(300, 200, 250), color= Color.green, axis=(1, 0, 1))
        #self.pyramid(frame=frame, pos=(200, 400, 200), size=(300, 200, 250), color= Color.green, axis=(0, 1, 1))
        #self.ring(frame=frame, pos=(-100, -300, 200))
        #self.cone(frame=frame, pos=(200, -300, -200), radius=200, height=400)
        #self.ellipsoid(frame=frame, pos=(-300, 100, 200), length=300, width=170, height=150, color='#FFFF00', opacity=0.5)
        #self.mesho = self.ellipsoid(frame=frame, length=200, width=240, height=300, color='#FF0000')
        self.mesh = frame

    def animate(self, i):
        # note: self._thr.js includes requestAnimationFrame shim
        self.bry.WIN.requestAnimationFrame(self.animate)

        self.mesh.rotation.x += 0.01
        self.mesh.rotation.y += 0.02

        self.renderer.render(self.scene, self.camera)


def main(bry, _cons):
    print('Fishing %s' % __version__)
    #Aquarium(bry, _cons).animate(0)
    Aquarium(bry, _cons)
    #Peixe(bry, _cons).animate(0)