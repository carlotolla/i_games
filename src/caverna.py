"""
############################################################
Caverna - Principal
############################################################

:Author: *Carlo E. T. Oliveira*
:Contact: carlo@nce.ufrj.br
:Date: 2013/11/04
:Status: This is a "work in progress"
:Revision: 0.1.3
:Home: `Labase <http://labase.selfip.org/>`__
:Copyright: 2013, `GPL <http://is.gd/3Udt>`__.

Caverna é um jogo de aventuras em uma caverna.
"""
SAIDAS_S = "Saidas%s"
CAVEX = "https://dl.dropboxusercontent.com/u/1751704/labase/caverna/img/cavernax.jpg"
CAVEY = "https://dl.dropboxusercontent.com/u/1751704/labase/caverna/img/cavernaz.jpg"
MUSH = "https://dl.dropboxusercontent.com/u/1751704/labase/caverna/img/cogumelo.png"
TUNEIS = [(int(a), int(b)) for a, b in "01 02 03 14 15 25 26 36 34 47 57 67".split()]
CAMARAS = range(8)
TUNEL, CAMARA = "Tunel%s", "Camara%s"


class Caverna:
    """Uma caverna com cameras tuneis e habitantes. :ref:`caverna`
    """
    def __init__(self, gui):
        """Inicializa Caverna. """
        self.doc = gui.DOC
        self.html = gui.HTML
        self.sala = {}
        self.heroi = self.caverna = self.ambiente = self.local = None
        self.main = self.doc['main']

    def cria_caverna(self):
        """Cria a caverna e suas partes."""
        self.caverna = self.html.DIV(Id="caverna", display='none')
        self.ambiente = self.html.DIV(Id="sala")
        self.sala = {CAMARA % str(camara): Camara(self.html, self, camara) for camara in CAMARAS}
        self.sala.update({TUNEL % str(tunel): Tunel(self.html, self, tunel) for tunel in TUNEIS})
        self.local = self.sala[CAMARA % str(0)]
        self.ambiente <= self.local.camara
        self.main <= self.ambiente

        return self

    def entra(self, destino):
        self.caverna <= self.local.camara
        self.local = self.sala[destino]
        self.ambiente <= self.local.camara


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
        nome = CAMARA % str(self.nome)
        estilo = dict(width=1000, height=800, background='url(%s)' % cave)
        self.camara = self.html.DIV(nome, Id=nome, style=estilo)
        estilo = dict(width=50, height=50, background='url(%s) 100%% 100%% / cover' % MUSH, Float="left")
        self.cogumelo = self.html.DIV(Id='mush_'+nome, style=estilo)
        self.camara.style.backgroundSize = 'cover'
        #self.caverna <= self.camara
        return self.camara

    def cria_saida(self, saida, tunel=TUNEL, width="33.33%"):
        """Cria tuneis ligados nesta caverna."""
        def entra_saida(evento):
            self.caverna.entra(evento.target.Id)
        nome = tunel % str(saida)
        print('saida', nome)
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
    print('Caverna 0.1.0')
    caverna = Caverna(gui).cria_caverna()
