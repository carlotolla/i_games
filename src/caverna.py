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
CAVEX = "https://dl.dropboxusercontent.com/u/1751704/labase/caverna/img/cavernax.jpg"
CAVEY = "https://dl.dropboxusercontent.com/u/1751704/labase/caverna/img/cavernay.jpg"
TUNEIS = [(int(a), int(b)) for a, b in "01 02 03 14 15 25 26 36 34 47 57 67".split()]
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
        self.sala = {CAMARA % str(camara): Camara(self.html, self.caverna, camara) for camara in range(8)}
        self.sala.update({TUNEL % str(tunel): Tunel(self.html, self.caverna, tunel) for tunel in TUNEIS})
        self.local = self.sala[CAMARA % str(0)]
        self.ambiente <= self.local.camara
        self.main <= self.ambiente

        return self

    def entra(self, destino):
        self.caverna <= self.local
        self.local = self.camara[destino]
        self.sala <= self.local.camara


class Camara:
    """Uma camara da caverna. :ref:`camara`
    """
    def __init__(self, gui, caverna, nome):
        """Inicializa Camara. """
        self.html, self.caverna, self.nome = gui, caverna, nome
        self.camara = self.cria_sala(nome=CAMARA % str(self.nome), cave=CAVEX)
        self.saidas = self.html.DIV(Id="Saidas%s" % str(nome))
        self.camara <= self.saidas
        self.saida = [self.cria_saida(saida) for saida in TUNEIS if nome in saida]

    def cria_sala(self, nome, cave):
        """Cria sala e suas partes."""
        nome = CAMARA % str(self.nome)
        estilo = dict(
            width=1000, height=800,
            background='url(%s)' % cave)
        self.camara = self.html.DIV(nome, Id=nome, style=estilo)
        self.camara.style.backgroundSize = 'cover'
        self.caverna <= self.camara
        return self.camara

    def cria_saida(self, saida):
        """Cria tuneis ligados nesta caverna."""
        def entra_saida(evento):
            self.caverna.entra(evento.target.Id)
        nome = TUNEL % str(saida)
        print('tunel', nome)
        estilo = dict(
            width="33.33%", height=550, Float="left")
        saida = self.html.DIV(nome, Id=nome, style=estilo)
        self.saidas <= saida
        return saida


class Tunel:
    """Uma camara da caverna. :ref:`camara`
    """
    def __init__(self, gui, camara, nome):
        """Inicializa Tunel. """
        self.html, self.caverna, self.nome = gui, camara, nome
        self.camara = self.cria_sala(nome=TUNEL % str(self.nome), cave=CAVEY)

    def cria_sala(self, nome, cave):
        """Cria tunel e suas partes."""
        estilo = dict(
            width=1000, height=800,
            background='url(%s)' % cave)
        self.camara = self.html.DIV(nome, Id=nome, style=estilo)
        self.camara.style.backgroundSize = 'cover'
        self.caverna <= self.camara
        return self.camara

    def cria_saida(self, saida):
        """Cria tuneis ligados nesta caverna."""
        def entra_saida(evento):
            self.caverna.entra(evento.target.Id)
        nome = CAMARA % str(saida)
        print('tunel', nome)
        estilo = dict(
            width="50%", height=550, Float="left")
        saida = self.html.DIV(nome, Id=nome, style=estilo)
        self.saidas <= saida
        return saida


def main(gui):
    print('Caverna 0.1.0')
    caverna = Caverna(gui).cria_caverna()
