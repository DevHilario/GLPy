from tkinter import *
from tkinter import messagebox
from tkinter import ttk

import sqlite3


class Library(Tk):
    def __init__(self):
        super().__init__()



        self.color_button_initial = '#629d6c'
        self.color_button_screens = '#00FFFF'
        self.background_space = '#BCBCBC'


        self.Banco_De_Dados = sqlite3.connect('Gerenciamento_Da_Biblioteca.db')
        self.Cursor = self.Banco_De_Dados.cursor()
        try:
            self.Cursor.execute('CREATE TABLE Biblioteca (Id INTEGER PRIMARY KEY AUTOINCREMENT'
                                ',Nome VARCHAR(30),'
                                'Autor VARCHAR(25),'
                                'Editor_a VARCHAR(25),' 
                                'Fisico_PDF text)')

        except:
            pass

        self.title('Gereciamento de Livros')
        self.resizable(False, False)

        self['bg'] = self.background_space
        self.geometry("+350+150")

        Label(self, text='Gerenciador de Livros', font=('Comic Sans MS', 50, 'bold'), bg=self.background_space).grid(row=0, column=0,
                                                                                           sticky='NEWS', padx=30,
                                                                                           pady=40)

        Adicionar_livros = Button(self, text='Adicionar Livro', font=('Verdana', 20), bd=5, relief=RAISED,
                                  bg=self.color_button_initial, command=self.Adicionar_algum_livro)
        Adicionar_livros.grid(row=1, column=0, sticky='NEWS', padx=7, pady=7)

        Todos_livros = Button(self, text='Todos os Livros', font=('Verdana', 20), bd=5, relief=RAISED,
                              bg=self.color_button_initial, command=self.Todos_livros_registrados)
        Todos_livros.grid(row=2, column=0, sticky='NEWS', padx=7, pady=7)

        Deletar_livros = Button(self, text='Deletar Livro', font=('Verdana', 20), bd=5, relief=RAISED,
                                bg=self.color_button_initial, command=self.Del_livro)
        Deletar_livros.grid(row=3, column=0, sticky='NEWS', padx=7, pady=7)

        Sair_livraria = Button(self, text='Sair da Livraria', font=('Verdana', 20), bd=5, relief=RAISED,
                               bg=self.color_button_initial, command=self.Sair_da_biblioteca)
        Sair_livraria.grid(row=4, column=0, sticky='NEWS', padx=7, pady=7)


    def Adicionar_algum_livro(self):
        self.withdraw()

        values = {'Livro Físico': '1',
                  'Livro PDF': '2'}

        self.Adicionar = Toplevel(self)
        self.Adicionar.resizable(False, False)
        self.Adicionar.geometry("+350+150")

        self.String = StringVar(self.Adicionar)

        Label(self.Adicionar, text='   Adicionar Livros   ', font=('Comic Sans MS', 50, 'bold')).grid(row=0, column=0,
                                                                                                      sticky='NEWS',
                                                                                                      padx=30, pady=40,
                                                                                                      columnspan=2)

        Label(self.Adicionar, text='Nome do Livro: ', font=('Verdana', 15)).grid(row=1, column=0, sticky='NES', padx=7,
                                                                                 pady=7)

        self.Nome_livro_entry = Entry(self.Adicionar, font=('Verdana', 15))
        self.Nome_livro_entry.grid(row=1, column=1, sticky='NEWS', padx=7, pady=7)

        Label(self.Adicionar, text='Autor(a) do Livro: ', font=('Verdana', 15)).grid(row=2, column=0, sticky='NES', padx=7,
                                                                                  pady=7)

        self.Autor_livro_entry = Entry(self.Adicionar, font=('Verdana', 15))
        self.Autor_livro_entry.grid(row=2, column=1, sticky='NEWS', padx=7, pady=7)

        Label(self.Adicionar, text='Editor(a) do Livro: ', font=('Verdana', 15)).grid(row=3, column=0, sticky='NES',
                                                                                      padx=7, pady=7)

        self.Editor_livro_entry = Entry(self.Adicionar, font=('Verdana', 15))
        self.Editor_livro_entry.grid(row=3, column=1, sticky='NEWS', padx=7, pady=7)

        for (text, value) in values.items():
            self.Tipo_livro = Radiobutton(self.Adicionar, text=text, variable=self.String, value=value, indicator=0,
                                          font=('Verdana', 15), bd=5, relief=RAISED)
            self.Tipo_livro.grid(row=4, column=int(value) - 1, sticky='NEWS', padx=7, pady=7)

        Salvar_Button = Button(self.Adicionar, text='Salvar Dados do Livro', font=('Arial Black', 20), bd=5,
                               relief=RAISED, bg=self.color_button_screens, command=self.Salvar_Livro)
        Salvar_Button.grid(row=5, column=0, columnspan=2, sticky='NEWS', padx=10, pady=10)

        Voltar_Button = Button(self.Adicionar, text='Voltar Para Página Inicial', font=('Arial Black', 20), bd=5,
                               relief=RAISED, bg=self.color_button_screens, command=self.Voltar_Inicial)
        Voltar_Button.grid(row=6, column=0, columnspan=2, sticky='NEWS', padx=10, pady=10)

    def Todos_livros_registrados(self):
        self.withdraw()

        Tabela = []

        self.Registros = Toplevel(self)
        self.Registros.resizable(False, False)
        self.Registros.geometry("+350+150")

        Voltar_Button = Button(self.Registros, text='Voltar Para Página Inicial', font=('Arial Black', 20), bd=5,
                               relief=RAISED, bg=self.color_button_screens, command=self.Voltar_Inicial)
        Voltar_Button.grid(row=0, column=0, columnspan=5, sticky='NEWS', padx=10, pady=10)

        list = self.Cursor.execute('SELECT * FROM Biblioteca  ORDER BY Nome ASC;')


        nomes_org = ['Livro', 'Autor(a)', 'Editor(a)', 'Formato']

        for f in list:
            Tabela.append(f[1:])

        style = ttk.Style()
        style.theme_use('alt')

        tree = ttk.Treeview(self.Registros, columns=nomes_org, show='headings')

        for nomes in nomes_org:
            tree.column(nomes, anchor='center')
            tree.heading(f'{nomes}', text=f'{nomes}')

        for table in Tabela:
            tree.insert('', END, values=table)

        tree.grid(row=1, column=0)

        Scroll_v = ttk.Scrollbar(self.Registros, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=Scroll_v.set)
        Scroll_v.grid(row=1, column=2, sticky='NS')


    def Del_livro(self):
        self.withdraw()


        Tabela_mostrar = []

        self.Del = Toplevel(self)
        self.Del.resizable(False, False)
        self.Del.geometry("+350+150")

        Voltar_Button = Button(self.Del, text='Voltar Para Página Inicial', font=('Arial Black', 20), bd=5,
                               relief=RAISED, bg=self.color_button_screens, command=self.Voltar_Inicial)
        Voltar_Button.grid(row=0, column=0, columnspan=5, sticky='NEWS', padx=10, pady=10)

        list = self.Cursor.execute('SELECT * FROM Biblioteca ORDER BY Nome ASC;')


        nomes_org = ['Livro', 'Autor(a)', 'Editor(a)', 'Formato']

        for f in list:
            Tabela_mostrar.append(f[1:])

        style = ttk.Style()
        style.theme_use('alt')

        style.map('Treeview', background=[('selected', 'green')])

        self.tree = ttk.Treeview(self.Del, columns=nomes_org, show='headings')

        for nomes in nomes_org:
            self.tree.column(nomes, anchor='center')
            self.tree.heading(f'{nomes}', text=f'{nomes}')

        for table in Tabela_mostrar:
            self.tree.insert('', END, values=table)

        self.tree.grid(row=1, column=0, columnspan=5)

        Scroll = ttk.Scrollbar(self.Del, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=Scroll.set)
        Scroll.grid(row=1, column=5, sticky='NS')

        self.tree.bind('<<TreeviewSelect>>', self.Jogar_livro_ao_limbo)

    def Sair_da_biblioteca(self):
        self.deiconify()
        self.destroy()

    def Salvar_Livro(self):
        Livro = self.Nome_livro_entry.get()
        Autor = self.Autor_livro_entry.get()
        Editor = self.Editor_livro_entry.get()
        Tipo = self.String.get()

        if Tipo == '1':
            Tipo = 'Físico'

        elif Tipo == '2':
            Tipo = 'PDF'

        if Livro == '' or Autor == '' or Editor == '' or Tipo == '':
            messagebox.showerror('Adicionamento de Livros', 'Por favor, preencha todos os espaços')

        else:
            self.Nome_livro_entry.delete('0', 'end')
            self.Autor_livro_entry.delete('0', 'end')
            self.Editor_livro_entry.delete('0', 'end')
            self.String.set(0)

            self.Cursor.execute(
                f'INSERT INTO Biblioteca (Nome, Autor, Editor_a, Fisico_PDF) VALUES ("{Livro}", "{Autor}", "{Editor}", "{Tipo}")')

            self.Banco_De_Dados.commit()

    def Jogar_livro_ao_limbo(self, event):
        for selected_item in self.tree.selection():

            T = messagebox.askquestion('Deletar',
                                       'Quer deletar esse item? (Os dados são perdidos\napós serem deletados)')

            if T == 'yes':
                lists = self.Cursor.execute('SELECT * FROM Biblioteca')

                G = self.tree.item(selected_item)
                values = list(G.values())

                for l in lists:
                    if l[1] == str(values[2][0]) and l[2] == str(values[2][1]) and l[3] == str(values[2][2]) and l[
                        4] == str(values[2][3]):
                        id_excluir = l[0]

                        self.Cursor.execute(f'DELETE from Biblioteca WHERE id = {id_excluir}')
                        self.Banco_De_Dados.commit()

                self.tree.delete(selected_item)

    def Voltar_Inicial(self):
        try:
            self.Adicionar.destroy()
            self.deiconify()

        except:
            pass

        try:
            self.Registros.destroy()
            self.deiconify()

        except:
            pass

        try:
            self.Del.destroy()
            self.deiconify()

        except:
            pass


if __name__ == '__main__':
    Library().mainloop()
