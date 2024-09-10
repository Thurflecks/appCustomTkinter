import customtkinter 
import mysql.connector
from mysql.connector import Error
#config customTk
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

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
def dados():
    try:
            cursor = bd.cursor()
            # Escreva sua consulta SQL para buscar os dados desejados
            query = "SELECT nome, preco FROM Produtos"
            cursor.execute(query)

            # Obter todos os resultados da consulta
            resultados = cursor.fetchall()

            # Iterar pelos resultados e exibir
            dados_text = ""
            for row in resultados:
                nome, preco = row
                dados_text += f"Nome: {nome}, Preço: {preco}\n"
                print(f"Nome: {nome}, Emailpreco: {preco}")
            dados = customtkinter.CTkTextbox(root)
            dados.place(relx="0.5", rely="0.5", anchor="center") 
            dados.insert("1.0", dados_text)
            
            

    except Error as err:
        print(f"Erro ao buscar dados: {err}")

#botoes
bt = customtkinter.CTkButton(root, text="Dados", command=dados)
bt.place(x="20", y="350")

fechar = customtkinter.CTkButton(root, text="SAIR", command=sair)
fechar.place(x="245", y="350")

root.mainloop()