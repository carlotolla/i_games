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
ARESTAS = [[a, b] for a, b in "01 02 03 14 15 25 26 36 34 47 57 67".split()]


class Caverna:
    """Uma caverna com cameras tuneis e habitantes. :ref:`caverna`
    """
    def __init__(self, gui):
        """Initializes builder and gui. """
        self.doc = gui.DOC
        self.html = gui.HTML
        self.camara = {}
        self.tunel = {}
        self.heroi = self.caverna = self.sala = None
        self.main = self.doc['main']

    def cria_caverna(self):
        """Cria a caverna e suas partes."""
        self.caverna = self.html.DIV(Id="caverna", display='none')
        self.sala = self.html.DIV(Id="sala")
        self.camara = {camara: Camara(self.html, self.caverna, camara) for camara in range(8)}
        self.sala <= self.camara[0].camara
        self.main <= self.sala

        return self


class Camara:
    """Uma camara da caverna. :ref:`camara`
    """
    def __init__(self, gui, caverna, nome):
        """Initializes builder and gui. """
        self.html, self.caverna, self.nome = gui, caverna, nome
        self.camara = self.cria_sala()

    def cria_sala(self):
        """Cria a camara e suas partes."""
        nome = "camara%d" % self.nome
        estilo = dict(
            width=1000, height=800,
            background='url(%s)' % CAVEX)
        self.camara = self.html.DIV(nome, Id=nome, style=estilo)
        self.camara.style.backgroundSize = 'cover'
        self.caverna <= self.camara
        return self.camara


def main(gui):
    print('Caverna 0.1.0')
    caverna = Caverna(gui).cria_caverna()
