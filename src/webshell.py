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
STYLE = dict(
    launcher=".launcher {position: relative; left:0; float:top;"
             "padding:10; width:100%; max-width:50px;}",
    acti=".acti {position: absolute; left:0; float:left; width:16;}",
    topb=".topb {position: absolute; top:0; height:20; margin-bottom:30;}",
    midp=".midp {position: absolute; top:0; width:98%; height:100%; overflow:hidden;}",
    dash=".dash {position: absolute; left:0; float:left; width:100%; padding-top:15;"
         " transition: 0.1s linear left; max-width:80px;}",
    dock=".dock {position: absolute; left:0; float:left; width:8%; padding-top:15;"
         " transition: 0.1s linear left;}",
    over=".over {position: relative; left:10%; top:30;  float:left; width:74%;"
         " background-color: #b0b0b0;}",
    work=".work {position: relative; left:0; float:right; width:15%; overflow:hidden;}",
    windock=".windock {position: relative; left:0; float:left; width:40%; height:40%;"
         " margin:1%; overflow:hidden; border: 2px solid black; border-radius:4px;}",  # background-color:black")
    workwin=".workwin {position: relative; left:0; float:left; width:auto; height:auto"
         " margin:1%; overflow:hidden; border: 2px solid black; border-radius:4px;}",  # background-color:black")
    workdock=".workdock {position: relative; left:0; float:left; width:90%; height:20%;"
         " margin:1%; overflow:hidden; border: 2px solid black; border-radius:4px;}",  # background-color:black")
    nwindow=".nwindow {position: absolute; left:0; float:left; width:100%;"
         " background-color: white; height:100%; margin:10px; overflow:scroll;}",
    window=".window {margin:5px; width:auto; height:auto;"
         " background-color: white; overflow:inherit;}",
    desktop=".desktop {position: absolute; left:0; top:0; width:100%; height:100%; opacity:1;"
         " background-color: white; overflow:inherit; transition: 0.4s linear left;}"

)
DOCKSIZES = [94, 94, 46, 30, 22, 17, 14, 11, 10]


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


class Tool(Window):

    def __init__(self, gui, parent, class_name, html='', action=lambda x: None):
        #Pane.__init__(self, gui, parent, class_name)
        self.element = html
        parent and parent <= self.element
        self.element.onclick = action  # self.select

    def select(self, event):
        print("select")
        self.action(self)


class Window_Pool(Pane):

    def __init__(self, gui, parent, class_name, action=lambda x: None, dock_class="workdock"):
        Pane.__init__(self, gui, parent, class_name)
        self.pool = []
        self.action, self.dock_class = action, dock_class

    def adjust_pool(self):
        side = int(len(self.pool) ** 0.5 + 0.999) % 9
        width = "%d%%" % DOCKSIZES[side]
        hside = int(len(self.pool) / side + 0.999) % 9
        height = "%d%%" % (DOCKSIZES[hside] - 2)
        #print (side, width, height, hside)
        for win in self.pool:
            win.element.style.width = width
            win.element.style.height = height

    def append(self, window):
        len_pool = len(self.pool)
        if len_pool >= 36:
            return True
        self.pool.append(window)
        self.adjust_pool()

    def new(self, html):
        window = Window_Dock(self.gui, self, self.dock_class, html, self.action)
        self.append(window)


class Work_Pool(Window_Pool):

    def __init__(self, gui, parent, class_name, action=lambda x: None, dock_class="windock"):
        Window_Pool.__init__(self, gui, parent, class_name, action, dock_class)

    def adjust_pool(self):
        pass

    def new(self, html):
        window = Window_Pool(self.gui, self, self.dock_class, html, self.action)
        self.append(window)


class Dash:

    def dynamic_css_configuraion(self, gui):
        html, header = gui.HTML, gui.DOC[gui.HTML.HEAD][0]
        [header <= html.STYLE(style) for style in STYLE.values()]
        return html

    def build(self, gui, pool, wall):
        wall.style.width = '100%'
        wall.style.overflow = 'hidden'
        for icon in ICONS:
            #self.dash <= self.gui.HTML.IMG(src=icon, Class="launcher")
            Tool(gui, self.dash, "launcher", self.gui.HTML.IMG(src=icon, Class="launcher"), self.tool)
        self.hide_dash(None)
        #self.load(HOME)
        ct = loads(HOME_CONTS)
        for ind in range(4):
            #pool.new(ct["result"])
            self.work_dock.new(ct["result"])
        activ = html.IMG(src='https://activufrj.nce.ufrj.br/static/favicon.ico', Class="acti")
        self.top_dock <= activ
        activ.onclick = self.activ

    def change_workspace(self, workspace):
        self.desk <= workspace

    def icons(self, dock):
        self.window_pool.new(loads(HOME_CONTS)["result"])

    def all(self, dock):
        self.window_pool.new(loads(HOME_CONTS)["result"])

    def tool(self, dock):
        self.window_pool.new(loads(HOME_CONTS)["result"])

    def select(self, dock):
        self.dock = dock
        self.desktop <= dock.content
        self.hide_dash(None)

    def __init__(self, gui):
        self.gui = gui
        self.dock = None
        wall = self.wall = gui.DOC["main"]
        html = self.dynamic_css_configuraion(gui)

        mid = self.mid_pannel = Pane(gui, wall, "midp")
        #hide = self.hideout = Pane(gui)
        dock = self.dash_dock = Pane(gui, mid, "dock")
        self.dash = Pane(gui, dock, "dash")
        desk = self.desk = Window(gui, mid, "over")
        pool = self.window_pool = Window_Pool(gui, desk, "winwork", self.select)
        work = self.work_dock = Work_Pool(gui, mid, "work", self.change_workspace)
        work.adjust_pool = lambda x=0: None
        self.desktop = Window(gui, wall, "desktop")
        self.top_dock = Pane(gui, wall, "topb")
        self.build(gui, pool, wall)

    def _activ(self, event):
        #self.gui().full()
        self._activ = self.show_dash

    def activ(self, event):
        self._activ(None)

    def show_dash(self, event):
        #self.dash_dock <= self.dash
        print("show_dash", self.dock)
        self.desktop.element.style.display = "none"
        self.dash.element.style.left = 0
        self._activ = self.hide_dash
        self.dock and self.dock.refit()

    def hide_dash(self, event):
        #self.hideout <= self.dash
        self.dash.element.style.left = -80
        self._activ = self.show_dash
        self.desktop.element.style.display = "block"

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
