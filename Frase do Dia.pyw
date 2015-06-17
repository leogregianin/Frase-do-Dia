# -*- coding: utf-8 -*-

import time, re, webbrowser
import wikipedia
from Tkinter import *

__version__ = '0.4'

class FrasedoDia(object):

    def __init__(self, parent):
        meses = ('Janeiro', 'Fevereiro', u'Março', 'Abril', 'Maio', 'Junho', 'Julho',
                 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro')
        now = time.localtime()
        year = time.strftime('%Y',now)
        month = meses[now.tm_mon - 1]
        day = now.tm_mday
        self.today = '%s de %s' % (day, month)
        self._today = '%s de %s de %s' % (day, month, year)
        menubar = Menu(root)
        root.config(menu=menubar)
        root.title('Frase do dia %s' % self._today)
        root.geometry('450x320')
        root.resizable(0,0)

        filemenu1 = Menu(menubar)
        filemenu2 = Menu(menubar)
        filemenu3 = Menu(menubar)

        menubar.add_cascade(label='Arquivo', menu=filemenu1)
        menubar.add_cascade(label='Links da Citação', menu=filemenu3)
        menubar.add_cascade(label='Ajuda', menu=filemenu2)

        filemenu1.add_command(label='Sair', command=self.Quit)
        filemenu2.add_command(label='Abrir wikiquote.org', command=self.Quote)
        filemenu2.add_command(label='Sobre', command=self.About)

        filemenu3.add_command(label=u'Endereço da citação', command=self.LinkQuote)
        filemenu3.add_command(label=u'Autor da citação', command=self.LinkAuthor)

        self.frame1 = Frame(root)
        self.frame1.pack()
        
        self.frame2 = Frame(root)
        self.frame2.pack()
        
        self.frame4 = Frame(root)
        self.frame4.pack()
        Label(self.frame4, width=60).pack(side=LEFT)

        self.frame5 = Frame(root)
        self.frame5.pack()

        self.frame6 = Frame(root)
        self.frame6.pack()
        Label(self.frame6, width=60).pack(side=LEFT)

        self.getQuote()

    def getQuote(self):

        colchetes = {"["  : "",
                     "[[" : "",
                     "]"  : "",
                     "]]" : "",
                     }
        def converte(s): #closure
            for original, plain in colchetes.items():
                s = s.replace(original, plain)
            return s

        site = wikipedia.getSite('pt', 'wikiquote')
        self.template = 'Template:Frase do dia/%s' % self.today
        page = wikipedia.Page(site, self.template)
        text = page.get()
    
        r = re.search('(?<=frase=)(.+)', text)
        m = re.search('(?<=autor=)(.+)', text)
        quote = """\n%s \n\n%s \n""" % (converte(r.group(0)), converte(m.group(0)))
        self.autor = converte(m.group(0)).strip()

        text = Text(self.frame2, font=('Verdana, 12'))
        text.pack()
        text.insert('insert', quote)
        text.config(state=DISABLED)

    def LinkQuote(self):
        webbrowser.open(("http://pt.wikiquote.org/wiki/%s" % self.template), 1)

    def LinkAuthor(self):
        webbrowser.open(("http://pt.wikiquote.org/wiki/%s" % self.autor), 1)

    def Quote(self):
        webbrowser.open("http://pt.wikiquote.org", 1)

    def Quit(self):
        root.destroy()

    def About(self):
        import tkMessageBox
        tkMessageBox.showinfo('Frase do Dia %s' % __version__,
                              u"""\
Citação do dia pelo site wikiquote.org

Wikiquote é um compêndio de citações livres
das mais diversas fontes provenientes de
pessoas notáveis e obras criativas em todas
as línguas. Wikiquote é um projeto da Wikimedia
Foundation onde também faz parte a Wikipedia.

Autores:
Leonardo Gregianin <leogregianin@gmail.com>
Walter Cruz <@waltercruz>
""")

if __name__ == "__main__":
    root = Tk()
    app = FrasedoDia(root)
    root.mainloop()
