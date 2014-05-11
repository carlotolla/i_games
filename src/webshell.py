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
from json import loads
__version__ = '0.1.0'
IBASE = "../../lib/icon/%s.svg"
ICONS = [IBASE % icon for icon in "wiki blog mblog".split()]
HOME = "https://activufrj.nce.ufrj.br/rest/wiki/carlo/home"


class Pane:

    def __init__(self, gui, parent=None, class_name=''):
        self.gui = gui
        self.element = html.DIV(Class=class_name)
        parent and parent <= self.element
        pass

    def __le__(self, other):
        element = isinstance(other, Pane) and other.element or other
        print (self.element, element, other)
        self.element <= element


class Window(Pane):

    def __init__(self, gui, parent, class_name, html=''):
        Pane.__init__(self, gui, parent, class_name)
        self.element.html = html


class Window_Dock(Pane):

    def __init__(self, gui, parent, class_name, html='', action=lambda x: None):
        Pane.__init__(self, gui, parent, class_name)
        shutter = self.shutter = Pane(gui, self.element, "desktop")
        shutter.element.style.backgroungColor = "white"
        shutter.element.style.opacity = 0.6
        shutter.element.onclick = self.select
        self.content = Window(gui, self, "window", html)
        self.action = action

    def select(self, event):
        print("select")
        self.action(self)

    def refit(self):
        self.element <= self.content.element

    def __le__(self, other):
        element = isinstance(other, Pane) and other.element or other
        self.element <= element
        self.element <= self.shutter.element


class Tool_Dock(Window_Dock):
    pass


class Window_Pool(Pane):

    def __init__(self, gui, parent, class_name, action=lambda x: None):
        Pane.__init__(self, gui, parent, class_name)
        self.pool = []
        self.action = action

    def append(self, window):
        self.pool.append(window)

    def new(self, html):
        window = Window_Dock(self.gui, self, "windock", html, self.action)
        self.append(window)


class Dash:

    def dynamic_css_configuraion(self, gui):
        html, header = gui.HTML, gui.DOC[gui.HTML.HEAD][0]
        header <= html.STYLE(
            ".launcher {position: relative; left:0; float:top;\
            padding:10; width:100%;}")
        header <= html.STYLE(".acti {position: absolute; left:0; float:left; width:16;}")
        header <= html.STYLE(".topb {position: absolute; top:0; width:100%; height:20; margin-bottom:30;}")
        header <= html.STYLE(".dock {position: absolute; left:0; float:left; width:60; padding-top:15;"
                             " transition: 0.1s linear left;}")
        header <= html.STYLE(".over {position: relative; left:80; top:30;  float:left; width:80%;"
                             " background-color: #b0b0b0;}")
        header <= html.STYLE(".wlist {position: relative; left:0; float:left; width:20%;}")
        header <= html.STYLE(".windock {position: relative; left:0; float:left; width:40%; height:40%;"
                             " margin:10px; overflow:hidden; border: 2px solid black; border-radius:4px;}")  # background-color:black")
        header <= html.STYLE(".nwindow {position: absolute; left:0; float:left; width:100%;"
                             " background-color: white; height:100%; margin:10px; overflow:scroll;}")
        header <= html.STYLE(".window {margin:5px; width:auto; height:auto;"
                             " background-color: white; overflow:inherit;}")
        header <= html.STYLE(".desktop {position: absolute; left:0; top:0; width:100%; height:100%; opacity:1;"
                             " background-color: white; overflow:inherit; transition: 0.4s linear left;}")
        return html

    def build(self, gui, pool, wall):
        for icon in ICONS:
            self.dash <= self.gui.HTML.IMG(src=icon, Class="launcher")
        self.hide_dash(None)
        #self.load(HOME)
        ct = loads(HOME_CONTS)
        for ind in range(4):
            pool.new(ct["result"])
        activ = html.IMG(src='https://activufrj.nce.ufrj.br/static/favicon.ico', Class="acti")
        self.top_dock <= activ
        activ.onclick = self.activ

    def select(self, dock):
        self.dock = dock
        self.desktop <= dock.content
        self.hide_dash(None)

    def __init__(self, gui):
        self.gui = gui
        self.dock = None
        wall = self.wall = gui.DOC["main"]
        wall.style.width = '100%'
        html = self.dynamic_css_configuraion(gui)

        mid = self.mid_pannel = Pane(gui, wall, "topb")
        mid.element.style.height = '100%'
        #hide = self.hideout = Pane(gui)
        dock = self.dash_dock = Pane(gui, mid, "dock")
        self.dash = Pane(gui, dock, "dock")
        pool = self.window_pool = Window_Pool(gui, mid, "over", self.select)
        self.desktop = Window(gui, wall, "desktop")
        self.top_dock = Pane(gui, wall, "topb")
        self.build(gui, pool, mid)

    def _activ(self, event):
        #self.gui().full()
        self._activ = self.show_dash

    def activ(self, event):
        self._activ(None)

    def show_dash(self, event):
        #self.dash_dock <= self.dash
        print("show_dash", self.dock)
        self.desktop.element.style.left = 2000
        self.dash.element.style.left = 0
        self._activ = self.hide_dash
        self.dock and self.dock.refit()

    def hide_dash(self, event):
        #self.hideout <= self.dash
        self.dash.element.style.left = -80
        self._activ = self.show_dash
        self.desktop.element.style.left = 0

    def on_json_complete(self, req):
        if req.status == 200 or req.status == 0:
            self.content.html = req.text
        else:
            self.content.html = "error "+req.text

    def on_complete(self, req):
        if req.status == 200 or req.status == 0:
            self.content.html = req.text
        else:
            self.content.html = "error "+req.text

    def load(self, url=IBASE % "icons"):
        req = self.gui.AJAX.ajax()
        req.bind('complete', self.on_complete)
        req.open('GET', url, True)
        req.set_header('content-type', 'application/x-www-form-urlencoded')
        req.send()


def main(gui):
    #gui().full()
    dash = Dash(gui)

HOME_CONTS=r'''{"status": 0, "result": {"pagina": "indice", "wikidata": {"data_cri": "2011-12-14 14:54:19.888003", "comentar": true, "tags": [], "registry_id": "carlo", "alterar": true, "apagar": false, "nomepag_id": "indice", "ler": true, "alterado_por": "carlo", "pag": "carlo/indice", "owner": "carlo", "conteudo": "<p><a href=\"/wiki/carlo/home\">P&aacute;gina Inicial<\/a><\/p>\r\n\r\n<p><a href=\"/wiki/carlo/Atividades\">Atividades<\/a><\/p>\r\n\r\n<p><a href=\"/wiki/carlo/Redes_Sociais\">Redes Sociais<\/a><\/p>\r\n\r\n<p><a href=\"/wiki/carlo/Ideias\">Ideias<\/a><\/p>\r\n\r\n<hr />\r\n<p><a href=\"/wiki/carlo/Pessoal\">Pessoal (privado)<\/a><\/p>\r\n\r\n<p><a href=\"/wiki/carlo/Game_Design\">Game Design<\/a><\/p>\r\n\r\n<p><a href=\"/wiki/carlo/Livros_no_Dominio_Publico\">Livros<\/a><\/p>\r\n\r\n<p><a href=\"/wiki/carlo/Jogos_Python\">Jogos<\/a><\/p>", "data_alt_fmt": "31/03/2014 \u00e0s 17:11", "data_alt": "2014-03-31 17:11:49.721490", "comentarios": [], "nomepag": "\u00cdndice", "data_cri_fmt": "14/12/2011 \u00e0s 14:54"}, "path": "/<a href='/wiki/carlo'>carlo<\/a>/"}}'''
