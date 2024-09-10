import customtkinter 
import mysql.connector
from mysql.connector import Error
#config customTk
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

#conectando banco de dados
try:
    bd = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="teste"
    )
    if bd.is_connected():
        print("conectou")
except Error as err:
    print(f"erro ao conectar ao banco de dados {err}")


#criando janela
root = customtkinter.CTk()
root.title("Gestão")
root.geometry("400x400")
root.maxsize(400, 400)
root.minsize(400, 400)
fonte = customtkinter.CTkFont("gabriola", 14)
#fechar janela
def sair():
    root.destroy()

#exibir dados
dados_visivel = False
dados = None
def dados():
    global dados_visivel, dados
    global bt, btadicionar, fechar
    global nome1, preco1
    try:
            cursor = bd.cursor()
            #pegar dados
            query = "SELECT iid, nome, preco FROM Produtos"
            cursor.execute(query)
            resultados = cursor.fetchall()

            #exibir
            dados_text = ""
            for row in resultados:
                iid, nome, preco = row
                dados_text += f"ID: {iid}\nNome: {nome}\nPreço: {preco}\n----------------------------------------------------------------\n"
                
            if not dados_visivel:
                dados = customtkinter.CTkTextbox(root, height=330, width=400, font=fonte)
                dados.place(x="0", y="0") 
                dados.insert("1.0", dados_text)
                dados_visivel = True
                bt.configure(text="VOLTAR")
                fechar.destroy()
                btadicionar.destroy()
                nome1.destroy()
                preco1.destroy()
                
            else:
                if dados:
                    dados.destroy()
                    dados = None 
                dados_visivel = False
                bt.configure(text="DADOS")
                fechar = customtkinter.CTkButton(root, text="SAIR", command=sair, font=fonte)
                fechar.place(x="245", y="350")
                btadicionar = customtkinter.CTkButton(root, text="ADICIONAR", command=adicionar, font=fonte)
                btadicionar.place(x="155", y="350")
                nome = customtkinter.CTkEntry(root, placeholder_text="Nome", font=fonte)
                nome.place(relx="0.5", y="40", anchor="center")

                preco = customtkinter.CTkEntry(root, placeholder_text="Preço", font=fonte)
                preco.place(relx="0.5", y="80", anchor="center")
                                                
            
            

    except Error as err:
        print(f"Erro ao buscar dados: {err}")
        

        
def up():
    try:
            nome1.up = nome1.get()
            preco1.up = preco1.get()
            cursor = bd.cursor()
            idd.up = idd.get()
            if not idd.up:
                raise ValueError
                
            
            print(nome1.up, preco1.up, idd.up)
            query = "UPDATE Produtos SET nome = %s, preco = %s WHERE id = %s"
            values = (nome1.up, preco1.up, idd.up)
            cursor.execute(query, values)
            bd.commit()
            
            
    except ValueError:
        print("OS CAMPOS NÃO PODEM SER VAZIOS")
            
def adicionar():
    root2 = customtkinter.CTkToplevel()
    root2.title("Adicionar")
    root2.geometry("400x250")
    root2.maxsize(400, 250)
    root2.minsize(400, 250)
    
    def salvar():
        try:
            nome.up = nome.get()
            preco.up = preco.get()
            cursor = bd.cursor()
            print(nome.up, preco.up,)
            query = "INSERT INTO Produtos (nome, preco) VALUES (%s, %s)"
            values = (nome.up, preco.up)
            cursor.execute(query, values)
            bd.commit()
            
        except ValueError:
            print("OS CAMPOS NÃO PODEM SER VAZIOS")
        
    
    nome = customtkinter.CTkEntry(root2, placeholder_text="Nome", width=300, height=35)
    nome.place(relx="0.5", y="40", anchor="center")

    preco = customtkinter.CTkEntry(root2, placeholder_text="Preço", width=300, height=35)
    preco.place(relx="0.5", y="90", anchor="center")
    
    adicionar = customtkinter.CTkButton(root2, text="SALVAR", command=salvar, font=fonte)
    adicionar.place(relx="0.5", y="200", anchor="center")
    
    
    root2.mainloop()

#botoes
bt = customtkinter.CTkButton(root, text="DADOS", command=dados, font=fonte)
bt.place(x="20", y="350")

up = customtkinter.CTkButton(root, text="ATUALIZAR", command=up, corner_radius=10, font=fonte)
up.place(relx="0.5", y="250", anchor="center")

fechar = customtkinter.CTkButton(root, text="SAIR", command=sair, font=fonte)
fechar.place(x="245", y="350")

btadicionar = customtkinter.CTkButton(root, text="ADICIONAR", command=adicionar, font=fonte)
btadicionar.place(x="155", y="350")

#entry
idd = customtkinter.CTkEntry(root, placeholder_text="ID", font=fonte, width=60, height=35)
idd.place(relx="0.5", y="55", anchor="center")

nome1 = customtkinter.CTkEntry(root, placeholder_text="Nome", font=fonte,  width=300, height=35)
nome1.place(relx="0.5", y="100", anchor="center")

preco1 = customtkinter.CTkEntry(root, placeholder_text="Preço", font=fonte,  width=300, height=35)
preco1.place(relx="0.5", y="150", anchor="center")


root.mainloop()