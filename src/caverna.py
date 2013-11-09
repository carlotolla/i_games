"""
############################################################
Caverna - Principal
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: 2013/11/04
:Status: This is a "work in progress"
:Home: `Labase <http://labase.selfip.org/>`__
:Copyright: 2013, `GPL <http://is.gd/3Udt>`__.

Caverna é um jogo de aventuras em uma caverna.
"""
__version__ = '0.1.3'
SAIDAS_S = "Saidas%s"
CAVEX = "https://dl.dropboxusercontent.com/u/1751704/labase/caverna/img/cavernax.jpg"
CAVEY = "https://dl.dropboxusercontent.com/u/1751704/labase/caverna/img/cavernaz.jpg"
MUSH = "https://dl.dropboxusercontent.com/u/1751704/labase/caverna/img/cogumelo.png"
PACMAN = "https://dl.dropboxusercontent.com/u/1751704/labase/caverna/img/pacman.png"
TUNEIS = [(int(a), int(b)) for a, b in "01 02 03 14 15 25 26 36 34 47 57 67".split()]
CAMARAS = range(8)
TUNEL, CAMARA = "Tunel%s", "Camara%s"
MYID, MYPASS = 'private-pacman-cave', 'c4p6p7'


class Caverna:
    """Uma caverna com cameras tuneis e habitantes. :ref:`caverna`
    """
    def __init__(self, gui):
        """Inicializa Caverna. """
        def envia(channel='move', **kwargs):
            data = dict(to=MYID, CHANNEL_=channel, **kwargs)
            self.pusher.send(gui.JSON.dumps(data))

        def conecta():
            self.pusher.send('{"setID":"' + MYID + '","passwd":"' + MYPASS + '"}')
            self.send = envia
            self.pusher.send('{"to":"' + MYID + '","msg":"' + 'init' + '"}')

        def recebe(ev):
            data = gui.JSON.loads(ev.data)
            if 'SID' in data:
                self.sid = data['SID']
            if 'CHANNEL_' in data and data['sID'] != self.sid:
                self.event[data['CHANNEL_']](data)
            print('ev.data', ev.data)
        self.herois = {}
        self.send = self.cria_heroi = self.move_heroi = self.pega_item = lambda x: None
        self.event = dict(move=self.move_heroi, cria=self.cria_heroi, pega=self.pega_item)
        self.doc = gui.DOC
        self.html = gui.HTML
        self.sala = {}
        self.pusher = gui.WSK('ws://achex.ca:4010')
        self.pusher.on_open = conecta
        self.pusher.on_message = recebe

        self.heroi = self.caverna = self.ambiente = self.local = self.pontua = None
        self.main = self.doc['main']

    def cria_caverna(self):
        """Cria a caverna e suas partes."""
        self.caverna = self.html.DIV(Id="caverna", display='none')
        self.ambiente = self.html.DIV(Id="sala")
        self.pontua = self.html.DIV(Id="pontua", style=dict(width="100%", height=50))
        self.sala = {CAMARA % str(camara): Camara(self.html, self, camara) for camara in CAMARAS}
        self.sala.update({TUNEL % str(tunel): Tunel(self.html, self, tunel) for tunel in TUNEIS})
        self.local = self.sala[CAMARA % str(0)]
        estilo = dict(width=50, height=50, background='url(%s) 100%% 100%% / cover' % PACMAN, Float="left")
        self.heroi = self.html.DIV(Id='heroi_', style=estilo)
        self.ambiente <= self.local.camara
        self.local.camara <= self.heroi
        self.main <= self.pontua
        self.main <= self.ambiente

        return self

    def entra(self, destino):
        self.caverna <= self.local.camara
        self.local = self.sala[destino]
        self.local.camara <= self.heroi
        self.ambiente <= self.local.camara

    def pega(self, destino):
        self.pontua <= self.doc[destino]


class Sala:
    def monta_ambiente(self, nome):
        self.camara = self.cria_sala(nome=CAMARA % str(self.nome), cave=CAVEX)
        self.saida = [self.cria_saida(saida) for saida in TUNEIS if nome in saida]

    def __init__(self, gui, caverna, nome):
        """Inicializa Camara. """
        self.html, self.caverna, self.nome = gui, caverna, nome
        self.camara = self.saida = self.cogumelo = None
        self.saidas = self.html.DIV(Id=SAIDAS_S % str(nome))
        self.monta_ambiente(nome)
        self.camara <= self.saidas
        self.camara <= self.cogumelo

    def cria_sala(self, nome, cave):
        """Cria sala e suas partes."""
        def pega_objeto(evento):
            self.caverna.pega(evento.target.Id)
        nome = CAMARA % str(self.nome)
        estilo = dict(width=1000, height=800, background='url(%s)' % cave)
        self.camara = self.html.DIV(nome, Id=nome, style=estilo)
        estilo = dict(width=50, height=50, background='url(%s) 100%% 100%% / cover' % MUSH, Float="left")
        self.cogumelo = self.html.DIV(Id='mush_'+nome, style=estilo)
        self.cogumelo.onclick = pega_objeto
        self.camara.style.backgroundSize = 'cover'
        #self.caverna <= self.camara
        return self.camara

    def cria_saida(self, saida, tunel=TUNEL, width="33.33%"):
        """Cria tuneis ligados nesta caverna."""
        def entra_saida(evento):
            self.caverna.entra(evento.target.Id)
        nome = tunel % str(saida)
        #print('saida', nome)
        estilo = dict(
            width=width, height=550, Float="left")
        saida = self.html.DIV(nome, Id=nome, style=estilo)
        saida.onclick = entra_saida
        self.saidas <= saida
        return saida


class Camara(Sala):
    """Uma camara da caverna. :ref:`camara`
    """
    def monta_ambiente(self, nome):
        self.camara = self.cria_sala(nome=CAMARA % str(self.nome), cave=CAVEX)
        self.saida = [self.cria_saida(saida) for saida in TUNEIS if nome in saida]


class Tunel(Sala):
    """Uma camara da caverna. :ref:`camara`
    """
    def monta_ambiente(self, nome):
        self.camara = self.cria_sala(nome=TUNEL % str(self.nome), cave=CAVEY)
        self.saida = [self.cria_saida(saida, CAMARA, "50%") for saida in CAMARAS if saida in nome]


def main(gui):
    print('Caverna %s' % __version__)
    caverna = Caverna(gui).cria_caverna()
