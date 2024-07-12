import tkinter
from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
import pymysql
root = Tk()

class WindowDraggable():
    def __init__(self, label):
        self.label = label
        label.bind('<ButtonPress-1>', self.StartMove)
        label.bind('<ButtonRelease-1>', self.StopMove)
        label.bind('<B1-Motion>', self.OnMotion)
    def StartMove(self, event):
        self.x = event.x
        self.y = event.y
    def StopMove(self, event):
        self.x = None
        self.y = None
    def OnMotion(self, event):
        x = (event.x_root - self.x - self.label.winfo_rootx() + self.label.winfo_rootx())
        y = (event.y_root - self.y - self.label.winfo_rooty() + self.label.winfo_rooty())
        root.geometry("+%s+%s" %(x,y))
        
judul_kolom = ("ID", "Nama", "Deskripsi", "Harga", "Stok")
                
class Produk:
    def __init__(self, parent):
        self.parent = parent
        self.parent.protocol("WM_DELETE_WINDOWS", self.keluar)
        lebar=750
        tinggi=500
        setTengahX = (self.parent.winfo_screenwidth()-lebar)//2
        setTengahY = (self.parent.winfo_screenheight()-tinggi)//2
        self.parent.geometry("%ix%i+%i+%i" %(lebar, tinggi, setTengahX, setTengahY))
        self.parent.overrideredirect(1)
        self.aturKomponen()
        self.auto()
        
    def auto(self):
        con = pymysql.connect(db="test", user='root', passwd='', host="localhost", port=3306, autocommit=True)
        cur = con.cursor()
        cuv = con.cursor()
        sqlid = "SELECT max(id) FROM produk"
        sql = "SELECT id FROM produk"
        cur.execute(sqlid)
        cuv.execute(sql)
        maxkode = cur.fetchone()
        
        if cuv.rowcount > 0:
            autohit = int(maxkode[0]) + 1
            self.entID.insert(0, autohit)
            self.entNama.focus_set()
        else:
            hit = "1"
            self.entID.insert(0, hit)
            self.entNama.focus_set()
            
        self.entID.config(state="readonly")
        
    def keluar(self, event=None):
        self.parent.destroy()
        
    def aturKomponen(self):
        frameWin = Frame(self.parent, bg="#666")
        frameWin.pack(fill=X,side=TOP)
        WindowDraggable(frameWin)
        Label(frameWin, text='PRODUK', bg='#666', fg="white").pack(side=LEFT, padx=20)
        buttonx = Button(frameWin, text="X", fg="white", bg="#FA8072", width=6, height=2, bd=0, \
                         activebackground="#FB8072", activeforeground="white", \
                         command=self.onClose, relief=FLAT)
        buttonx.pack(side=RIGHT)
        
        mainFrame = Frame(self.parent)
        mainFrame.pack(side=TOP, fill=X)
        btnFrame = Frame(self.parent)
        btnFrame.pack(side=TOP, fill=X)
        tabelFrame = Frame(self.parent)
        tabelFrame.pack(expand=YES, side=TOP, fill=Y)

        Label(mainFrame, text='  ').grid(row=0, column=0)
        Label(btnFrame, text='  ').grid(row=1, column=0)
        
        Label(mainFrame, text='ID').grid(row=1, column=0, sticky=W, padx=20)
        Label(mainFrame, text=':').grid(row=1, column=1, sticky=W, pady=5, padx=10)
        self.entID = Entry(mainFrame, width=20)
        self.entID.grid(row=1, column=2, sticky=W)
        
        Label(mainFrame, text='Nama').grid(row=2, column=0, sticky=W, padx=20)
        Label(mainFrame, text=':').grid(row=2, column=1, sticky=W, pady=5, padx=10)
        self.entNama = Entry(mainFrame, width=20)
        self.entNama.grid(row=2, column=2, sticky=W)
        
        Label(mainFrame, text='Deskripsi').grid(row=3, column=0, sticky=W, padx=20)
        Label(mainFrame, text=':').grid(row=3, column=1, sticky=W, pady=5, padx=10)
        self.entDesc = ScrolledText(mainFrame, height=2, width=30)
        self.entDesc.grid(row=3, column=2, sticky=W)
        
        Label(mainFrame, text='Harga').grid(row=4, column=0, sticky=W, padx=20)
        Label(mainFrame, text=':').grid(row=4, column=1, sticky=W, pady=5, padx=10)
        self.entHarga = Entry(mainFrame, width=20)
        self.entHarga.grid(row=4, column=2, sticky=W)
        
        Label(mainFrame, text='Stok').grid(row=5, column=0, sticky=W, padx=20)
        Label(mainFrame, text=':').grid(row=5, column=1, sticky=W, pady=5, padx=10)
        self.entStok = Entry(mainFrame, width=20)
        self.entStok.grid(row=5, column=2, sticky=W)
        
        self.btnSave = Button(btnFrame, text='Save', width=10, relief=FLAT, bd=2, bg="#666", fg="white",\
                        activebackground="#444", activeforeground="white", command=self.onSave)
        self.btnSave.grid(row=0, column=1, padx=5)
        
        self.btnUpdate = Button(btnFrame, text='Update', state="disable", width=10, relief=FLAT, bd=2, bg="#666", fg="white",\
                        activebackground="#444", activeforeground="white" , command=self.onUpdate)
        self.btnUpdate.grid(row=0, column=2, pady=10, padx=5)
        
        self.btnClear = Button(btnFrame, text='Clear', width=10, relief=FLAT, bd=2, bg="#666", fg="white",\
                        activebackground="#444", activeforeground="white" , command=self.onClear)
        self.btnClear.grid(row=0, column=3, pady=10, padx=5)
        
        self.btnDelete = Button(btnFrame, text='Delete', state="disable", width=10, relief=FLAT, bd=2, bg="#FC6042", fg="white",\
                        activebackground="#444", activeforeground="white", command=self.onDelete)
        self.btnDelete.grid(row=0, column=4, pady=10, padx=5)
        
        self.fr_data = Frame(tabelFrame, bd=10)
        self.fr_data.pack(fill=BOTH, expand=YES)
        
        self.trvTabel = ttk.Treeview(self.fr_data, columns=judul_kolom, show='headings')
        self.trvTabel.bind("<Double-1>", self.OnDoubleClick)
        sbVer = Scrollbar(self.fr_data, orient='vertical', command=self.trvTabel.yview)
        sbVer.pack(side=RIGHT, fill=Y)
        self.trvTabel.pack(side=TOP, fill=BOTH)
        self.trvTabel.configure(yscrollcommand=sbVer.set)
        self.table()
        
    def OnDoubleClick(self, event):
        self.entID.config(state="normal")
        self.entID.delete(0, END)
        self.entNama.delete(0, END)
        self.entDesc.delete('1.0', 'end')
        self.entHarga.delete(0, END)
        self.entStok.delete(0,END)
        
        it = self.trvTabel.selection()[0]
        ck = str(self.trvTabel.item(it, "values"))[2:3]
        self.entID.insert(END,ck)
        cID = self.entID.get()
        
        con = pymysql.connect(db="test", user="root", passwd="", host="localhost", port=3306, autocommit=True)
        cur = con.cursor()
        sql = "SELECT nama, deskripsi, harga, stok FROM produk WHERE id = %s"
        cur.execute(sql, cID)
        data = cur.fetchone()
        
        self.entNama.insert(END, data[0])
        self.entDesc.insert(END, data[1])
        self.entHarga.insert(END, data[2])
        self.entStok.insert(END, data[3])
        
        self.entID.config(state="disable")
        self.btnSave.config(state="disable")
        self.btnUpdate.config(state="normal")
        self.btnDelete.config(state="normal")
        
    def table(self):
        con = pymysql.connect(db="test", user="root", passwd="", host="localhost", port=3306, autocommit=True)
        cur = con.cursor()
        cur.execute("SELECT id, nama, deskripsi, harga, stok FROM produk")
        data_table = cur.fetchall()
        
        for kolom in judul_kolom:
            self.trvTabel.heading(kolom, text=kolom)
            self.trvTabel.column("ID", width=10, anchor="w")
            self.trvTabel.column("Nama", width=150, anchor="w")
            self.trvTabel.column("Deskripsi", width=350, anchor="w")
            self.trvTabel.column("Harga", width=100, anchor="w")
            self.trvTabel.column("Stok", width=100, anchor="w")
        
        i=0
        for dat in data_table:
            if(i%2):
                baris="genap"
            else:
                baris="ganjil"

            self.trvTabel.insert('', 'end', values=dat, tags=baris)
            i+=1
            
        self.trvTabel.tag_configure("ganjil", background="#FFFFFF")
        self.trvTabel.tag_configure("genap", background="whitesmoke")
        cur.close()
        con.close()
        
    def onClose(self, event=None):
        self.parent.destroy()
        
    def onSave(self):
        con = pymysql.connect(db="test", user='root', passwd='', host="localhost", port=3306, autocommit=True)

        cID = self.entID.get()
        cNama = self.entNama.get()
        cDesc = self.entDesc.get('1.0','end')
        cHarga = self.entHarga.get()
        cStok = self.entStok.get()
        
        if len(cNama) == 0:
            tkinter.messagebox.showwarning(title="Peringatan", message="Nama tidak boleh kosong")
        else:
            cur = con.cursor()
            sql = "INSERT INTO produk(id, nama, deskripsi, harga, stok) VALUES(%s, %s, %s, %s, %s)"
            cur.execute(sql, (cID, cNama, cDesc, cHarga, cStok))
            self.onClear()
            tkinter.messagebox.showinfo(title="Informasi", message="Data sudah disimpan")
            cur.close()
            con.close()
    
    def onClear(self):
        self.btnSave.config(state="normal")
        self.btnUpdate.config(state="disable")
        self.btnDelete.config(state="disable")
        
        self.entID.config(state="normal")
        self.entID.delete(0, END)
        self.entNama.delete(0, END)
        self.entDesc.delete('1.0', 'end')
        self.entHarga.delete(0, END)
        self.entStok.delete(0, END)
        
        self.trvTabel.delete(*self.trvTabel.get_children())
        self.fr_data.after(0, self.table())
        self.auto()
        self.entNama.focus_set()
        
    def onUpdate(self):
        cID = self.entID.get()
        if len(cID) == 0:
            tkinter.messagebox.showwarning(title="Peringatan", message="ID Kosong")
            self.entID.focus_set()
        else:
            con = pymysql.connect(db="test", user='root', passwd='', host="localhost", port=3306, autocommit=True)
            cur = con.cursor()
            cID = self.entID.get()
            cNama = self.entNama.get()
            cDesc = self.entDesc.get('1.0','end')
            cHarga = self.entHarga.get()
            cStok = self.entStok.get()
        
            sql = "UPDATE produk SET nama = %s, deskripsi=%s, harga=%s, stok=%s " +\
                  "WHERE id = %s"
            cur.execute(sql, (cNama, cDesc, cHarga, cStok, cID))
            self.onClear()
            
            tkinter.messagebox.showinfo(title="Informasi", message="Data sudah terupdate")
            cur.close()
            con.close()
        
    def onDelete(self):
        con = pymysql.connect(db="test", user='root', passwd='', host="localhost", port=3306, autocommit=True)
        cur = con.cursor()
        self.entID.config(state="normal")
        cID = self.entID.get()
        sql = "DELETE FROM produk WHERE id=%s"
        cur.execute(sql,cID)
        self.onClear()

        tkinter.messagebox.showinfo(title="Informasi", message="Data sudah dihapus")
        cur.close()
        con.close()
        
def main():
    Produk(root)
    root.mainloop()
main()