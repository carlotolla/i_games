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


class Pacman:
    def __init__(self, bry):
        b = bry.DOC["main"]
        d = bry.HTML.DIV()
        d.style.backgroundColor = "blue"
        c = bry.SVG.svg(width=900, height=900)
        b <= d
        d <= c
        pac = bry.SVG.g()
        top = bry.SVG.path(d="M50,50 h-50 a50,50 0 1,0 100,0 z", fill="yellow")
        bot = bry.SVG.path(d="M50,50 h-50 a50,50 0 1,1 100,0 z", fill="yellow")
        c <= pac
        pac <= top
        pac <= bot
        re = bry.SVG.rect(x=200, y=100, width=100, height=100)
        tr = bry.SVG.animateTransform(
            attributeType="xml", attributeName="transform", begin="0s",
            type="rotate", to="35 50 50", dur="0.4s", repeatCount="indefinite")
        tr.setAttribute("from", "0 50 50")
        br = bry.SVG.animateTransform(attributeType="xml", attributeName="transform", begin="0s",
        type="rotate", to="-35 50 50", dur="0.4s", repeatCount="indefinite")
        br.setAttribute("from", "0 50 50")
        waka = 'https://dl.dropboxusercontent.com/u/1751704/labase/pacman/fx/waka.ogg'
        w = bry.HTML.AUDIO(src=waka, type="audio/ogg")  # , autoplay="autoplay")
        self.here = 0
        #pr = bry.SVG.animateTransform(attributeType="xml", attributeName="transform", begin="0s",
        #    type="translate", by= "%s,0"%here, dur="1s",repeatCount="indefinite")
        #pr = bry.SVG.animateTransform(attributeType="xml", attributeName="transform", begin="0s",
        #    type="translate", to="%d"%(here+100), dur="1s",repeatCount="indefinite")
        pr = bry.SVG.animateTransform(
            attributeType="xml", attributeName="transform", begin="0s",
            type="translate", by=100, dur="1s", repeatCount="indefinite")
        pr.setAttribute("from", "%d" % self.here)
        pac <= pr

        def house(ev):
            self.here = (self.here+100) if self.here < 700 else 0
            #pr.From = "%d"%here
            pr.setAttribute("from", "%d" % self.here)
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