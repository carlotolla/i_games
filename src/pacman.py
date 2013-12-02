"""
############################################################
Pacman - O heroi faminto
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: 2013/12/02
:Status: This is a "work in progress"
:Home: `Labase <http://labase.selfip.org/>`__
:Copyright: 2013, `GPL <http://is.gd/3Udt>`__.

"""
__version__ = '0.1.0'
PAC = 20 


class Pacman:
    def __init__(self, bry):
        b = bry.DOC["main"]
        d = bry.HTML.DIV()
        d.style.backgroundColor = "blue"
        c = bry.SVG.svg(width=900, height=900)
        b <= d
        d <= c
        pac = bry.SVG.g()
        pac2 = (PAC, )*2
        pac4 = (PAC, )*5 + (PAC*2, )
        top = bry.SVG.path(d="M%d,%d h-%d a%d,%d 0 1,0 %d,0 z" % pac4, fill="yellow")
        bot = bry.SVG.path(d="M%d,%d h-%d a%d,%d 0 1,1 %d,0 z" % pac4, fill="yellow")
        c <= pac
        pac <= top
        pac <= bot
        self.rumo = 90
        pac2t = (self.rumo + 35, ) + pac2
        pac2b = (self.rumo + -35, ) + pac2
        pac2f = (self.rumo, ) + pac2
        re = bry.SVG.rect(x=200, y=100, width=100, height=100)
        tr = bry.SVG.animateTransform(
            attributeType="xml", attributeName="transform", begin="0s",
            type="rotate", to="%d %d %d" % pac2t, dur="0.4s", repeatCount="indefinite")
        tr.setAttribute("from", "%d %d %d" % pac2f)
        br = bry.SVG.animateTransform(attributeType="xml", attributeName="transform", begin="0s",
        type="rotate", to="%d %d %d" % pac2b, dur="0.4s", repeatCount="indefinite")
        br.setAttribute("from", "%d %d %d" % pac2f)
        waka = 'https://dl.dropboxusercontent.com/u/1751704/labase/pacman/fx/waka.ogg'
        w = bry.HTML.AUDIO(src=waka, type="audio/ogg")  # , autoplay="autoplay")
        self.here = (0, 0)
        self.step = (0, PAC*2)
        #pr = bry.SVG.animateTransform(attributeType="xml", attributeName="transform", begin="0s",
        #    type="translate", by= "%s,0"%here, dur="1s",repeatCount="indefinite")
        #pr = bry.SVG.animateTransform(attributeType="xml", attributeName="transform", begin="0s",
        #    type="translate", to="%d"%(here+100), dur="1s",repeatCount="indefinite")
        pr = bry.SVG.animateTransform(
            attributeType="xml", attributeName="transform", begin="0s",
            type="translate", by="%d %d" % self.step, dur="500ms", repeatCount="indefinite")
        pr.setAttribute("from", "%d %d" % self.here)
        pac <= pr

        def house(ev):
            x, y = self.here
            x = (x+self.step[0]) if x <= 900 - PAC*8 else 0
            y = (y+self.step[1]) if y <= 900 - PAC*8 else 0
            self.here = x, y
            #pr.From = "%d"%here
            pr.setAttribute("from", "%d %d" % self.here)
            #pr.to = "%d"%(here+100)
            w.play()
        d <= w
        pr.onrepeat = house
        #house(None)
        w.play()
            
        #pr.onend = house
        top <= tr
        bot <= br
        c <= re


def main(bry):
    print('Pacman %s' % __version__)
    Pacman(bry)