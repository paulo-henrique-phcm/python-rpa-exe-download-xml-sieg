from customtkinter import (
    CTkToplevel,
    CTkButton,
    CTkLabel,
    CTkScrollableFrame,
    CTkFrame,
    CTkTextbox,
)
import customtkinter, time


class ToplevelWindow(CTkToplevel):
    def __init__(
        self,
        *args,
        TITULO: str = "",
        SUBTITULO: str = "",
        MENSAGEM: str = "",
        TEXTO_BOTAO: str = "Fechar",
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.tamanho_horizontal = 700
        self.limite_largura_quebra_palavra = 30

        # REMOVE AS BORDAS, FICANDO UMA JANELA MAIS BONITA, POREM SEM A OPCAO DE ARRASTAR
        # if MODO_SEM_BORDA:
        #     self.overrideredirect(True)
        #     self.configure(fg_color='#333F57')

        self.title("Caixa de mensagens")
        
        self.geometry(f"{self.tamanho_horizontal}x400")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(2, weight=0)

        # 0 ELEMENTO
        if TITULO:
            fonte_grande = ("", 30, "bold")
            self.label_titulo = CTkLabel(
                self,
                text=TITULO,
                font=fonte_grande,
                wraplength=self.tamanho_horizontal - self.limite_largura_quebra_palavra,
                text_color="#0082FF",
            )
            self.label_titulo.grid(
                row=0, column=0, padx=(10, 10), pady=10, sticky="new"
            )

        # 1 ELEMENTO (FRAME ROLAVEL CONTENDO SUBTITULO E TEXTO)
        self.frame_scrool = CTkFrame(self)
        self.frame_scrool.grid(row=1, column=0, padx=(10, 10), pady=0, sticky="nsew")
        # self.frame_scrool.configure(fg_color="transparent")
        self.frame_scrool.grid_columnconfigure(0, weight=1)
        self.frame_scrool.grid_rowconfigure(1, weight=2)

        if SUBTITULO:
            fonte_grande = ("", 25, "bold")
            self.label_subtitulo = CTkLabel(
                self.frame_scrool,
                text=SUBTITULO,
                font=fonte_grande,
                wraplength=self.tamanho_horizontal - self.limite_largura_quebra_palavra,
            )
            self.label_subtitulo.grid(
                row=0, column=0, padx=(10, 10), pady=10, sticky="new"
            )

        if MENSAGEM:
            fonte_grande = ("", 16)
            # self.label_mensagem = CTkLabel(
            #     self.frame_scrool,
            #     text=MENSAGEM,
            #     font=fonte_grande,
            #     wraplength=self.tamanho_horizontal - self.limite_largura_quebra_palavra
            # )
            self.label_mensagem = CTkTextbox(
                master=self.frame_scrool,
                corner_radius=0,
                wrap="word",
                font=fonte_grande,
                bg_color="transparent",
                fg_color="transparent",
            )
            self.label_mensagem.insert("1.0", MENSAGEM)
            self.label_mensagem.configure(state="disabled")
            self.label_mensagem.grid(
                row=1, column=0, padx=(10, 10), pady=10, sticky="nsew"
            )

        # 2 ELEMENTO VOTAO
        # Botão personalizado para fechar a janela
        self.botao_fechar = CTkButton(
            self, text=TEXTO_BOTAO, command=self.fechar_janela, font=("", 20, "bold")
        )
        # self.botao_fechar.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
        self.botao_fechar.grid(
            row=2, column=0, padx=(10, 10), pady=(10, 10), sticky="s"
        )

        # Centralizar a janela na tela
        self.centralizar_janela()

        # PERMITE CLICAR E ARRASTAR A TELA CLICANDO EM QUALQUER LUGAR DELA
        # self.bind("<ButtonPress-1>", self.iniciar_arraste)
        # self.bind("<B1-Motion>", self.arrastar_janela)

    def iniciar_arraste(self, event):
        self.x_pos = event.x
        self.y_pos = event.y

    def arrastar_janela(self, event):
        nova_pos_x = self.winfo_x() + (event.x - self.x_pos)
        nova_pos_y = self.winfo_y() + (event.y - self.y_pos)
        self.geometry(f"+{nova_pos_x}+{nova_pos_y}")

    def centralizar_janela(self):
        self.update_idletasks()
        largura = self.winfo_width()
        altura = self.winfo_height()
        pos_x = (self.winfo_screenwidth() - largura) // 2
        pos_y = (self.winfo_screenheight() - altura) // 2
        self.geometry(f"+{pos_x}+{pos_y}")
        self.lift()

    def fechar_janela(self):
        self.destroy()

    @classmethod
    def exibir_popup(cls):
        # time.sleep(1)
        popup = cls()
        popup.lift()  # Garante que a janela fique em primeiro plano
        popup.mainloop()
