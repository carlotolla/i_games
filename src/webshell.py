"""
############################################################
WebShell - Um Gerenciador de Janelas ao estilo Gnome3
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: 2014/05/08
:Status: This is a "work in progress"
:Home: `Labase <http://labase.selfip.org/>`__
:Copyright: 2014, `GPL <http://is.gd/3Udt>`__.

"""
__version__ = '0.1.0'


class Window:

    def __init__(self, gui):
        pass


class Dash:

    def __init__(self, gui):
        self.gui = gui
        wall = gui.DOC["main"]
        blot = gui.HTML
        activ = blot.IMG(src='https://activufrj.nce.ufrj.br/static/favicon.ico')
        wall <= activ
        activ.onclick =self.activ
        pass

    def activ(self, event):
        self.gui().full()



def main(gui):
    gui().full()
    dash = Dash(gui)