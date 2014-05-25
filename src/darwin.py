"""
############################################################
Darwin : A live book telling the voyage of the beagle
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: 2014/05/24
:Status: This is a "work in progress"
:Home: `Labase <http://labase.selfip.org/>`__
:Copyright: 2014, `GPL <http://is.gd/3Udt>`__.

The voyages of Charles Darwin on board of the clipper Beagle.
"""
__version__ = '0.1.0'
from math import sin, cos, radians
TIT, MAP, FIG, SCE, BIB = [None] * 5
vec = color = None
L3, L2 = 6, 4
FT = 8
PO = 4 * FT
CS = 25 * PO
DM = CS * 2
HERE = None
GLOBE = "../../lib/icon/MUNDI-novo-FINAL.jpg"
UBIB = dict(
    PLY=[
        (40.0, 1.1360197999999855), "PLYMOUTH",
        "http://www.tageo.com/get_map.php?lat=50.396&long=-4.139&name=Plymouth&tag=1",
        "http://farm4.static.flickr.com/3185/2502071514_8b93a13b3d.jpg",
        "http://www.infobritain.co.uk/Plymouth_Sound.jpg"
    ],
    HAM=[
        (-59.633333, -67.0), "PUERTO DEL HAMBRE",
        "http://www.tageo.com/get_map.php?lat=-53.633&long=-70.933&name=Puerto%20del%20hambre&tag=1",
        "http://dadaisforever.files.wordpress.com/2009/08/puerto-del-hambre-21.jpg?w=490",
        "http://upload.wikimedia.org/wikipedia/commons/1/14/Puerto_del_Hambre.jpg"
    ],
    RIO=[
        (-22.9035393, -43.20958689999998), "RIO DE JANEIRO",
        #"http://www.tageo.com/get_map.php?lat=-22.649&long=-43.659&name=Japeri&tag=1",
        "http://media.maps.com/magellan/Images/po00245_c.jpg",
        "http://www.itaipuacu.org/images/itaipuacudarwin/darwinrio.jpg",
        "http://darwin-online.org.uk/converted/published/1987_Insects_F1830/1987_Insects_F1830_fig13.jpg"
    ],
    GAL=[
        (-0.2292784, -98.5206679999998), "GALAPAGOS",
        "http://www.rtcc.org/files/2012/02/Galapagos_small1.jpg",
        "http://www.truthinscience.org.uk/tis2/images/stories/darwinsfinches.jpg",
        "http://www.aqua-firma.com/editorfiles/Image/Galapagos/Aggressor/Galapagos_Darwin_Arch350.jpg"
    ]
)


def spc(lat, lon):
    lat, lon = radians(lat), radians(-70-lon)
    #return int(CS*cos(lon)), int(sin(lat)*CS), int(CS*sin(lon))
    return int(CS*cos(lat)*cos(lon)), int(sin(lat)*CS), int(CS*cos(lat)*sin(lon))


class Location:

    def __init__(self, gui, place, title, satmap, picture, scene):
        #print ("place, satmap, picture, scene", place, satmap, picture, scene)
        gf = self.gui = gui
        self.place = place
        self.title, self.satmap, self.picture, self.scene = title, satmap, picture, scene
        loc = self.location = spc(*place)
        p = self.pl = gf.sphere(pos=loc, size=(PO, PO, PO), shininess=0, color=color.red, opacity=5e-1)
        #p.opacity = 0.5
        pass

    def route(self, to):
        dt = 8
        rx, ry = self.place
        fx, fy = rx, ry
        tx, ty = to.place
        dx, dy = (tx - fx) / dt, (ty - fy) / dt
        router = self.gui.curve(color=color.magenta, radius=2)
        arc = []  # [4*sin(i*pi/20) for i in range(21)]
        for a in range(dt+1):
            arc.append(1+0.1*sin(a*3.1416/(dt+0)))
        for i in arc:
            #print(spc(rx, ry), i)
            x, y, z = spc(rx, ry)
            point = (int(x * i), int(y * i), int(z * i))
            router.push(point)
            fx += dx
            fy += dy
            rx, ry = int(fx), int(fy)

    def click(self, event):
        if event == self.location:
            MAP.html = FIG.html = SCE.html = TIT.html = ""
            Globe.HERE.color = vec(1, 0, 0)
            self.pl.color = (0, 1, 0)  # color.green
            Globe.HERE = self.pl
            TIT.html = self.title
            MAP <= self.satmap
            FIG <= self.picture
            SCE <= self.scene


class Globe:
    HERE = None

    def __init__(self, gui):

        gf = self.gui = gui
        ''''''
        c = self.globe = gf.sphere(pos=(0, 0, 0), size=(DM, DM, DM), shininess=0, texture=GLOBE)
        c.rotate(angle=pi/2, axis=vec(0, 0, 1))
        c.rotate(angle=pi, axis=vec(0, 1, 0))
        ''''''
        #gf.scene.waitfor("textures", wait)
        gf.scene.visible = true
        gui.scene.bind("click", self.click)

        gf.scene.background = color.gray(.5)
        gf.scene.lights = []
        gf.scene.ambient = color.gray(.8)
        #gf.scene.forward = vec(-1, 0, 0)
        gf.scene.range = 120 * FT
        self.locations = {}
        for key, loc in BIB.items():
            self.locations[key] = Location(*loc)
        plymouth, rio, hambre = self.locations["PLY"], self.locations["RIO"], self.locations["HAM"]
        Globe.HERE = plymouth.pl
        plymouth.click(plymouth.location)
        plymouth.route(rio)
        rio.route(hambre)
        hambre.route(self.locations["GAL"])

    def draw(self):
        pass

    def click(self, event):
        obj = self.gui.scene.mouse.pick()
        objp = obj.pos
        pos = (objp.x, objp.y, objp.z)
        print("objp.x, objp.y, objp.z", pos)
        for loc in self.locations.values():
            loc.click(pos)


def main(gui, gvec, gcolor):
    global vec, color, TIT, MAP, FIG, SCE, BIB
    vec = gvec
    TIT, MAP, FIG, SCE = gui.doc["tit"], gui.doc["map"], gui.doc["fig"], gui.doc["sce"]
    BIB = {}
    for key, value in UBIB.items():
        vals = []
        for url in value[2:]:
            vals.append(gui.gui.IMG(src=url, width='100%'))
        BIB[key] = [gui, value[0], value[1]] + vals
    color = gcolor
    print('Darwin %s' % __version__)

    Globe(gui).draw()