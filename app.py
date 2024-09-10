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

#fechar janela
def sair():
    root.destroy()

#exibir dados
dados_visivel = False
dados = None
def dados():
    global dados_visivel, dados
    try:
            cursor = bd.cursor()
            #pegar dados
            query = "SELECT nome, preco FROM Produtos"
            cursor.execute(query)
            resultados = cursor.fetchall()

            #exibir
            dados_text = ""
            for row in resultados:
                nome, preco = row
                dados_text += f"Nome: {nome}, Preço: {preco}\n"
                print(f"Nome: {nome}, Emailpreco: {preco}")
            print("-------------------------------")
            if not dados_visivel:
                dados = customtkinter.CTkTextbox(root)
                dados.place(relx="0.5", rely="0.5", anchor="center") 
                dados.insert("1.0", dados_text)
                dados_visivel = True
            else:
                if dados:
                    dados.destroy()
                    dados = None 
                dados_visivel = False
            
            

    except Error as err:
        print(f"Erro ao buscar dados: {err}")
        

        
def up():
    try:
            nome.up = nome.get()
            preco.up = preco.get()
            cursor = bd.cursor()
            idd.up = idd.get()
            if not idd.up:
                raise ValueError
                
            
            print(nome.up, preco.up, idd.up)
            query = "UPDATE Produtos SET nome = %s, preco = %s WHERE id = %s"
            values = (nome.up, preco.up, idd.up)
            cursor.execute(query, values)
            bd.commit()
            
            
    except ValueError as err:
        print("OS CAMPOS NÃO PODEM SER VAZIOS")
            
    
    

#botoes
bt = customtkinter.CTkButton(root, text="DADOS", command=dados)
bt.place(x="20", y="350")

up = customtkinter.CTkButton(root, text="ATUALIZAR", command=up)
up.place(relx="0.5", y="250", anchor="center")

fechar = customtkinter.CTkButton(root, text="SAIR", command=sair)
fechar.place(x="245", y="350")

#entry
nome = customtkinter.CTkEntry(root, placeholder_text="Nome")
nome.place(relx="0.5", y="40", anchor="center")


preco = customtkinter.CTkEntry(root, placeholder_text="Preço")
preco.place(relx="0.5", y="80", anchor="center")


idd = customtkinter.CTkEntry(root, placeholder_text="ID")
idd.place(relx="0.5", y="160", anchor="center")

root.mainloop()