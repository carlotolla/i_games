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
IBASE = "../../lib/icon/%s.svg"
ICONS = [IBASE % icon for icon in "wiki blog mblog".split()]


class Window:

    def __init__(self, gui):
        pass


class Dash:

    def __init__(self, gui):
        self.gui = gui
        wall = self.wall = gui.DOC["main"]
        html = gui.HTML
        gui.DOC[html.HEAD][0] <= html.STYLE(
            ".launcher {position: relative; left:0; float:top;\
            padding:10; width:100%}")
        gui.DOC[html.HEAD][0] <= html.STYLE(
            ".dock {position: relative; left:0; float:top; width:50")

        activ = html.IMG(src='https://activufrj.nce.ufrj.br/static/favicon.ico')
        wall <= activ
        self.dash = html.DIV(Class="dock")
        self.hideout = html.DIV(Class="dock")
        self.dash_dock = html.DIV(Class="dock")
        #self.dash.style = "position: relative; left:0; float:top; width:50"
        #self.hideout.style = "position: relative; left:0; float:top; width:50; display:none"
        #self.dash.style = "position: absolute; left:0; top:50"
        self.wall <= self.dash_dock
        for icon in ICONS:
            self.dash <= self.gui.HTML.IMG(src=icon, Class="launcher")
        activ.onclick = self.activ

    def _activ(self, event):
        self.gui().full()
        self._activ = self.show_dash

    def activ(self, event):
        self._activ(None)

    def show_dash(self, event):
        self.dash_dock <= self.dash
        self._activ = self.hide_dash

    def hide_dash(self, event):
        self.hideout <= self.dash
        self._activ = self.show_dash


def main(gui):
    #gui().full()
    dash = Dash(gui)