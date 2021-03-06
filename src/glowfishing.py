"""
############################################################
Glowfish - A 3D game as variation of tic-tac-toe
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: 2014/05/07
:Status: This is a "work in progress"
:Home: `Labase <http://labase.selfip.org/>`__
:Copyright: 2014, `GPL <http://is.gd/3Udt>`__.

In GlowFish you combine the properties of blobs to win.
"""
__version__ = '0.1.0'
vec = color = None
L3, L2 = 6, 4
CS = 120
PD = 70
PO = 10


class Blob:

    def __init__(self, gui):
        def pc(inb, oub, tin, szi, tou, szo):
            return lambda ps: inb(tin, szi, ps) + oub(tou, szo, ps)
        self.jail = None
        cl = color
        M, N, G, Y, S, L = cl.magenta, cl.blue, cl.green, cl.yellow, 10, 0
        TIN, TOU, SZI = (cl.magenta, cl.blue), (cl.green, cl.yellow), (20, 0)
        INB, OUB, SZO = (self.dice, self.ball), (self.frame, self.ring), (15, 0)
        bpos = [(x*125 - 4*CS, y*125, 3*CS) for x in range(-4, 0) for y in range(-4, 4)]
        bpos += [(x*125 + 5*CS, y*125, 3*CS) for x in range(0, 4) for y in range(-4, 4)]
        self.bpos = bpos
        self.gui = gui
        #gui.scene.bind("click", self.click)
        self.blober = [
            pc(inb, oub, tin, szi, tou, szo)
            for inb in INB for oub in OUB for tin in TIN for szi in SZI for tou in TOU for szo in SZO]
        self.blob = [blob(pos) for pos, blob in zip(bpos, self.blober)]

    def dice(self, tint, size, ps):
        size += 20
        return [self.gui.box(pos=ps, size=(CS-PO-size, CS-PO-size, CS-PO-size), color=tint, opacity=1)]

    def ball(self, tint, size, ps):
        size -= 5
        return [self.gui.sphere(pos=ps, size=(CS-PO-size, CS-PO-size, CS-PO-size), color=tint, opacity=1)]

    def frame(self, tint, size, ps):
        return [
            self.gui.box(pos=ps, size=(CS, PO+size, CS), color=tint, opacity=1),
            self.gui.box(pos=ps, size=(CS, CS, PO+size), color=tint, opacity=1),
            self.gui.box(pos=ps, size=(PO+size, CS, CS), color=tint, opacity=1)]

    def ring(self, tint, size, ps):
        RCS = CS + 10
        return [
            self.gui.sphere(pos=ps, size=(RCS, PO+2*size, RCS), color=tint, opacity=1),
            self.gui.sphere(pos=ps, size=(RCS, RCS, PO+2*size), color=tint, opacity=1),
            self.gui.sphere(pos=ps, size=(PO+2*size, RCS, RCS), color=tint, opacity=1)]

    def click(self, event):
        obj = self.gui.scene.mouse.pick()
        objp = obj.pos
        pos = (objp.x, objp.y, objp.z)
        #print("blob click", event.type, event.which, pos)  # .x, obj.y, obj.z)
        if not pos in self.bpos:
            #print("click not in bpos", self.bpos)
            return
        for blob in self.blob:
            for part in blob:
                part.visible = False
        obind = self.bpos.index(pos)
        for part in self.blob[obind]:
            part.visible = True

        self.jail.toggle(self.blob[obind])

    def show(self, ablob):
        self.blob[self.blob.index(ablob)] = []
        for blob in self.blob:
            for part in blob:
                part.visible = True


class Jail:
    def __init__(self, gui, blob):

        self.gui = gui
        blob.jail = self
        gui.scene.bind("click", self.click)
        side = (-CS, 0, CS)
        side = (-3*CS, -CS, CS, 3*CS)
        self.hole = []
        self.obj = None
        self.cell = [[[(x, y, z) for x in side] for y in side] for z in side]
        self.loci = [(x, y, z) for x in side for y in side for z in side]
        self._click, self._next = blob.click, self.jail_click
        self.show = blob.show

    def draw(self):
        gui = self.gui
        #print (self.cell)
        self.hole = [gui.box(pos=cell, size=(CS-PD, CS-PD, CS-PD), color=color.gray(0.2), opacity=1)
                     for plane in self.cell for line in plane for cell in line]

        #print(color.blue, list(hole.opacity for hole in self.hole))

    def click(self, event):
        self._click(event)

    def toggle(self, obj):
        self.obj = obj
        self._click, self._next = self._next, self._click

    def jail_click(self, event):
        obj = self.gui.scene.mouse.pick()
        objp = obj.pos
        pos = (objp.x, objp.y, objp.z)
        #print(event.type, event.which, pos, objp, self.obj)  # .x, obj.y, obj.z)
        if not pos in self.loci:
            return
        #self.gui.sphere(pos=objp, size=(CS-PO, CS-PO, CS-PO), color=color.magenta, opacity=1)
        for part in self.obj:
            part.pos = vec(*pos)  # objp
        obj.visible = False
        self.loci[self.loci.index(pos)] = None
        self.show(self.obj)
        self.toggle(self.obj)


def main(gui, gvec, gcolor):
    global vec, color
    vec = gvec
    color = gcolor
    print('Fishing %s' % __version__)
    #Aquarium(gui).draw()

    Jail(gui, Blob(gui)).draw()
    #Peixe(bry, _cons).animate(0)