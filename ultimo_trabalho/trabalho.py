from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import pygame
import time
import random
import os

# ---------- CORES E CONFIGURAÇÕES ---------- #
co0 = "#000000"
co1 = "#FFFFFF"
co2 = "#4CAF50"  # Verde mais bonito para o botão "Sim"
co3 = "#F44336"  # Vermelho mais suave para o botão "Não"
co4 = "#000000"
co5 = "#000000"

caminho_fundo = r"C:\Users\davi emanuel passoni\Downloads\images (2).png" # Altere conforme necessário
credenciais = ['davi', 'game']

# ---------- FUNÇÃO PARA INICIAR O JOGO DA COBRINHA ---------- #
def iniciar_jogo():
    pygame.init()

    branco = (255, 255, 255)
    preto = (0, 0, 0)
    vermelho = (255, 0, 0)
    verde = (0, 255, 0)

    largura = 600
    altura = 400
    tamanho_bloco = 20
    velocidade = 15

    fonte = pygame.font.SysFont(None, 35)
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption('Jogo da Cobrinha')
    relogio = pygame.time.Clock()

    def desenhar_cobrinha(tamanho_bloco, lista_cobra):
        for x in lista_cobra:
            pygame.draw.rect(tela, verde, [x[0], x[1], tamanho_bloco, tamanho_bloco])

    def jogo():
        fim_de_jogo = False
        game_over = False

        x1 = largura / 2
        y1 = altura / 2
        x1_mudanca = 0
        y1_mudanca = 0
        lista_cobra = []
        comprimento_cobra = 1

        comida_x = round(random.randrange(0, largura - tamanho_bloco) / 20.0) * 20.0
        comida_y = round(random.randrange(0, altura - tamanho_bloco) / 20.0) * 20.0

        while not fim_de_jogo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    fim_de_jogo = True
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_LEFT:
                        x1_mudanca = -tamanho_bloco
                        y1_mudanca = 0
                    elif evento.key == pygame.K_RIGHT:
                        x1_mudanca = tamanho_bloco
                        y1_mudanca = 0
                    elif evento.key == pygame.K_UP:
                        y1_mudanca = -tamanho_bloco
                        x1_mudanca = 0
                    elif evento.key == pygame.K_DOWN:
                        y1_mudanca = tamanho_bloco
                        x1_mudanca = 0

            if x1 >= largura or x1 < 0 or y1 >= altura or y1 < 0:
                game_over = True

            x1 += x1_mudanca
            y1 += y1_mudanca
            tela.fill(preto)
            pygame.draw.rect(tela, vermelho, [comida_x, comida_y, tamanho_bloco, tamanho_bloco])

            cabeça_cobra = [x1, y1]
            lista_cobra.append(cabeça_cobra)

            if len(lista_cobra) > comprimento_cobra:
                del lista_cobra[0]

            for segmento in lista_cobra[:-1]:
                if segmento == cabeça_cobra:
                    game_over = True

            desenhar_cobrinha(tamanho_bloco, lista_cobra)
            pygame.display.update()

            if x1 == comida_x and y1 == comida_y:
                comida_x = round(random.randrange(0, largura - tamanho_bloco) / 20.0) * 20.0
                comida_y = round(random.randrange(0, altura - tamanho_bloco) / 20.0) * 20.0
                comprimento_cobra += 1

            relogio.tick(velocidade)

        pygame.quit()
        quit()

    jogo()

# ---------- INTERFACE DE LOGIN COM TKINTER ---------- #
janela = Tk()
janela.title("PYTHON")
janela.geometry("310x350")
janela.configure(bg=co1)
janela.resizable(False, False)

# Fundo
imagem_fundo_pil = Image.open(caminho_fundo).resize((600, 1000))
imagem_fundo = ImageTk.PhotoImage(imagem_fundo_pil)

# Frames
frame_cima = Frame(janela, width=310, height=50, bg=co1, relief="flat")
frame_cima.grid(row=0, column=0, pady=1, padx=0, sticky=NSEW)

frame_baixo = Frame(janela, width=310, height=300, bg=co1, relief="flat")
frame_baixo.grid(row=1, column=0, pady=1, padx=0, sticky=NSEW)

label_fundo = Label(frame_baixo, image=imagem_fundo)
label_fundo.place(x=0, y=0, relwidth=1, relheight=1)

# Labels de título
l_nome = Label(frame_cima, text="LOGIN THE GAME", height=1, anchor=NE, font=('Ivy', 25), bg=co1, fg=co4)
l_nome.place(x=5, y=5)

l_linha = Label(frame_cima, width=275, text="", height=1, anchor=NW, font=('Ivy', 1), bg=co5)
l_linha.place(x=10, y=45)

# Função de verificação
def verificar_senha():
    nome = e_nome.get()
    senha = str(e_pass.get())

    if nome == 'admin' and senha == 'admin' or (credenciais[0] == nome and credenciais[1] == senha):
        messagebox.showinfo('Login', f'Seja bem-vindo {nome}!')

        # Exibe a janela personalizada para confirmação de jogar
        janela_jogo = Toplevel(janela)
        janela_jogo.title("Você quer jogar?")
        janela_jogo.geometry("400x300")
        janela_jogo.configure(bg=co1)
        janela_jogo.resizable(False, False)

        # Adiciona o título bonito
        label = Label(janela_jogo, text="Você quer jogar o Jogo da Cobrinha?", font=("Arial", 15, "bold"), bg=co1, fg=co4)
        label.pack(pady=30)

        # Funções dos botões
        def sim_action():
            janela_jogo.destroy()  # Fecha a janela de confirmação
            iniciar_jogo()         # Inicia o jogo

        def nao_action():
            janela_jogo.destroy()  # Fecha a janela de confirmação
            janela.quit()          # Fecha o programa ou retorna ao login

        # Botões com novos estilos
        frame_botoes = Frame(janela_jogo, bg=co1)
        frame_botoes.pack(pady=20)

        botao_sim = Button(frame_botoes, text="Sim", width=15, height=2, bg=co2, fg=co4, font=("Arial", 12, "bold"), relief=RAISED, overrelief=RIDGE, command=sim_action)
        botao_sim.grid(row=0, column=0, padx=20)

        botao_nao = Button(frame_botoes, text="Não", width=15, height=2, bg=co3, fg=co4, font=("Arial", 12, "bold"), relief=RAISED, overrelief=RIDGE, command=nao_action)
        botao_nao.grid(row=0, column=1, padx=20)

    else:
        messagebox.showwarning('Erro', 'Usuário ou senha inválidos.')

# Campos de entrada
l_nome = Label(frame_baixo, text="NOME *", height=1, anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
l_nome.place(x=10, y=20)
e_nome = Entry(frame_baixo, width=25, justify='left', font=("", 15), relief="solid")
e_nome.place(x=14, y=50)

l_pass = Label(frame_baixo, text="SENHA *", height=1, anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
l_pass.place(x=10, y=90)
e_pass = Entry(frame_baixo, show='*', width=25, justify='left', font=("", 15), relief="solid")
e_pass.place(x=14, y=120)

botao_confirmar = Button(frame_baixo, text="ENTRAR", width=39, height=2, bg=co2, fg=co5, font=('Ivy 8 bold'), relief=RAISED, overrelief=RIDGE, command=verificar_senha)
botao_confirmar.place(x=15, y=180)

janela.imagem_fundo = imagem_fundo

janela.mainloop()


