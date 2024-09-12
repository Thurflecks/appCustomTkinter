import customtkinter 
import mysql.connector
from mysql.connector import Error
from tkinter import PhotoImage
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
        print("conectado")
except Error as err:
    print(f"erro ao conectar ao banco de dados {err}")


#criando janela
root = customtkinter.CTk()
root.title("Gestão")
root.geometry("400x400")
root.maxsize(400, 400)
root.minsize(400, 400)
icone = PhotoImage(file="/home/two/Documentos/work/appCustomTkinter/ico.png")
root.iconphoto(True, icone)
fonte = customtkinter.CTkFont("gabriola", 14)

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
            btadicionar.destroy()
            nome1.destroy()
            preco1.destroy()
            
        else:
            if dados:
                dados.destroy()
                dados = None 
            dados_visivel = False
            bt.configure(text="DADOS")
            btadicionar = customtkinter.CTkButton(root, text="ADICIONAR", command=adicionar, font=fonte)
            btadicionar.place(x="245", y="350")
            nome1 = customtkinter.CTkEntry(root, placeholder_text="Nome", font=fonte,  width=300, height=35)
            nome1.place(relx="0.5", y="115", anchor="center")
            preco1 = customtkinter.CTkEntry(root, placeholder_text="Preço", font=fonte,  width=300, height=35)
            preco1.place(relx="0.5", y="160", anchor="center")
                                                                
            
            

    except Error as err:
        print(f"Erro ao buscar dados: {err}")
        

#atualizar dados      
def up():
    global ids
    try:
        nome1.up = nome1.get()
        preco1.up = preco1.get()
        cursor = bd.cursor()
        idd_up = idd.get()
        if not idd_up or idd_up == " ":
            raise ValueError("OS VALORES NÃO PODEM SER VAZIOS")
        query = "UPDATE Produtos SET nome = %s, preco = %s WHERE iid = %s"
        values = (nome1.up, preco1.up, idd_up)
        cursor.execute(query, values)
        bd.commit()
        nome1.delete(0, "end")
        preco1.delete(0, "end")
        var.set(ids[ids.__len__() - 1])
        aviso2.configure(text=" ")
            
            
    except ValueError as e:
        aviso2.configure(text=str(e), text_color="red")
            
#adicionando abrindo outra janela
def adicionar():
    root2 = customtkinter.CTkToplevel() 
    root2.title("Adicionar")
    root2.geometry("400x300")
    root2.maxsize(400, 300)
    root2.minsize(400, 300)
    
    aviso = customtkinter.CTkLabel(root2, text=" ", font=fonte)
    aviso.place(relx="0.5", y="260", anchor="center")
    

    def sair2():
        root2.destroy()
    
    def salvar():
        
        try:
            nome2.ad = nome2.get()
            preco2.ad = preco2.get()
            cursor = bd.cursor()
            if not nome2.ad or not preco2.ad:
                raise ValueError("OS VALORES NÃO PODEM SER VAZIOS")
            query = "INSERT INTO Produtos (nome, preco) VALUES (%s, %s)"
            values = (nome2.ad, preco2.ad)
            cursor.execute(query, values)
            bd.commit()
            nome2.delete(0, "end")
            preco2.delete(0, "end")
            aviso.configure(text=" ")
            
            
        except ValueError as e:
            aviso.configure(text=str(e), text_color="red")
       
    
    nome2 = customtkinter.CTkEntry(root2, placeholder_text="Nome", width=300, height=35, font=fonte)
    nome2.place(relx="0.5", y="80", anchor="center")

    preco2 = customtkinter.CTkEntry(root2, placeholder_text="Preço", width=300, height=35, font=fonte)
    preco2.place(relx="0.5", y="130", anchor="center")
    
    adicionar2 = customtkinter.CTkButton(root2, text="SALVAR", command=salvar, font=fonte)
    adicionar2.place(relx="0.5", y="230", anchor="center")
    
    fechar2 = customtkinter.CTkButton(root2, text="VOLTAR", command=sair2, font=fonte)
    fechar2.place(x="250", y="10")
    
    root2.wait_visibility()
    root2.grab_set()
    root2.mainloop()
    

    
def pegarid():
    cursor = bd.cursor()
    query = "SELECT iid FROM Produtos"
    cursor.execute(query)
    resultados = cursor.fetchall()
    ids.clear()
    for row in resultados:
        iid = str(row[0])
        ids.append(iid)
    idd.configure(values=ids)
    if ids:
        ids.append(" ")
        var.set(ids[ids.__len__()- 1])
        
#vars   
ids = []
var = customtkinter.StringVar(root)
#botoes

bt = customtkinter.CTkButton(root, text="DADOS", command=dados, font=fonte, image=icone)
bt.place(x="20", y="350")

up = customtkinter.CTkButton(root, text="ATUALIZAR", command=up, corner_radius=10, font=fonte)
up.place(relx="0.5", y="250", anchor="center")

btadicionar = customtkinter.CTkButton(root, text="ADICIONAR", command=adicionar, font=fonte)
btadicionar.place(x="245", y="350")


#entry
idd = customtkinter.CTkOptionMenu(root, variable=var, values=ids)
idd.place(relx="0.5", y="70", anchor="center")

nome1 = customtkinter.CTkEntry(root, placeholder_text="Novo Nome", font=fonte,  width=300, height=35)
nome1.place(relx="0.5", y="115", anchor="center")

preco1 = customtkinter.CTkEntry(root, placeholder_text="Novo Preço", font=fonte,  width=300, height=35)
preco1.place(relx="0.5", y="160", anchor="center")

#LABEL
aviso2 = customtkinter.CTkLabel(root, text=" ", font=fonte)
aviso2.place(relx="0.5", y="290", anchor="center")

#defs

pegarid()

root.mainloop()