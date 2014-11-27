from tkinter import *
from tkinter import ttk

class Application(Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master, padding=(5, 0, 100, 5))
        
        self.master = master
        
        self.master.title("DB Stuff")
        
        #Set up the grid for the Widgets
        self.grid(column=0, row=0, sticky=(N,W,E,S))
        self.master.grid_columnconfigure(0,weight=1)
        self.master.grid_rowconfigure(0,weight=1)
        
        self.products = ("table", "lamp", "tv", "car", "apple", "asdf", "book")
        self.productsString = StringVar(value=self.products)
        
        self.materials = ("plank", "hammer", "wood", "nail", "asdf", "hammer", "wood", "nail")
        self.materialsString = StringVar(value=self.materials)
        
        self.selectedProduct = StringVar()
        self.selectedMaterial = StringVar()
        
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        #Create all of the widgets that we will be using.
        productLbl = ttk.Label(self, text="Products")
        products = Listbox(self, listvariable=self.productsString, height=5)
        
        prodSB = ttk.Scrollbar(self, orient=VERTICAL, command=products.yview)
        products["yscrollcommand"] = prodSB.set
        
        materialLbl = ttk.Label(self, text="Materials")
        materials = Listbox(self, listvariable=self.materialsString, height=5)
        
        matSB = ttk.Scrollbar(self, orient=VERTICAL, command=materials.yview)
        materials["yscrollcommand"] = matSB.set
        
        quitBtn = ttk.Button(self, text="QUIT", command=self.master.destroy)
        
        selProd = ttk.Label(self, textvariable=self.selectedProduct, anchor="center")
        selMat = ttk.Label(self, textvariable=self.selectedMaterial, anchor="center")
        
        #Set up the widget's location in the GUI
        productLbl.grid(column=0, row=0, pady=5)
        products.grid(column=0, row=1, stick=(N,S,E,W))
        prodSB.grid(column=1, row=1, sticky=(N,S))
        
        materialLbl.grid(column=0, row=2, pady=5)
        materials.grid(column=0, row=3, stick=(N,S,E,W))
        matSB.grid(column=1, row=3, sticky=(N,S))
        
        quitBtn.grid(column=0, row=4, pady=10)
        
        selProd.grid(column=2, row=1, padx=5, sticky=(W,E))
        selMat.grid(column=2, row=3, padx=5, sticky=(W,E))

        # Colorize alternating lines of the listboxes
        for i in range(0,len(self.products),2):
            products.itemconfigure(i, background='#f0f0ff')
        for i in range(0,len(self.materials),2):
            materials.itemconfigure(i, background='#f0f0ff')
            
            
        #Then bind some functions to the listboxes just cause
        def selectedProduct(*args):
            idxs = products.curselection()
            if len(idxs)==1:
                self.selectedProduct.set(self.products[idxs[0]])
            
        def selectedMaterial(*args):
            idxs = materials.curselection()
            if len(idxs)==1:
                self.selectedMaterial.set(self.materials[idxs[0]])
            
            
        products.bind('<<ListboxSelect>>', selectedProduct)
        materials.bind('<<ListboxSelect>>', selectedMaterial)
        
def main():
    root = Tk()
    app = Application(master=root)
    app.mainloop()
    
main()

