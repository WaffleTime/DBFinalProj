from tkinter import *
from tkinter import ttk

#Because multiple functions can be defined as a single object and this is needed for the scrollbar.
def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func

class Application(Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master, padding=(5, 0, 100, 5))
        
        self.master = master
        
        self.master.title("DB Stuff")
        self.master.geometry('500x300')
        
        #Set up the grid for the Widgets
        self.grid(column=0, row=0, sticky=(N,W,E,S))
        self.master.grid_columnconfigure(0,weight=1)
        self.master.grid_rowconfigure(0,weight=1)
        
        self.products = ("table", "lamp", "tv", "car", "apple", "asdf", "book")
        self.productsString = StringVar(value=self.products)
        
        self.materials = ("plank", "hammer", "wood", "nail", "asdf", "hammer", "wood", "nail")
        self.materialsString = StringVar(value=self.materials)
        
        #self.selectedProduct = StringVar()
        #self.selectedProduct.set('')
        #self.selectedMaterial = StringVar()
        #self.selectedMaterial.set('')
        
        self.possibleProducts = ["table", "lamp", "tv", "car", "apple", "asdf", "book", "cake"]
        
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        #Create all of the widgets that we will be using.
        productLbl = ttk.Label(self, text="Products")
        self.productListBox = Listbox(self, listvariable=self.productsString, height=5)
        
        prodSB = ttk.Scrollbar(self, orient=VERTICAL, command=self.productListBox.yview)
        self.productListBox["yscrollcommand"] = prodSB.set
        
        def removeProduct(*args):
            idxs = self.productListBox.curselection()
            if (len(idxs) == 1):
                prods = list(self.products)
                del prods[idxs[0]]
                    
                prods = tuple(prods)
                self.productsString.set(prods)
                self.products = prods
                
                #Materials also need to be removed along with these products!
                
                self.updateListBoxes()
                
        def removeAllProducts(*args):
            prods = ()
            self.productsString.set(prods)
            self.products = prods

            mats = ()
            self.materialsString.set(mats)
            self.materials = mats
            
            self.updateListBoxes()
        
        removeProductBtn = ttk.Button(self, text="Remove Product", command=removeProduct)
        removeAllProductsBtn = ttk.Button(self, text="Remove All Products", command=removeAllProducts)
        
        materialLbl = ttk.Label(self, text="Materials")
        self.materialListBox1 = Listbox(self, listvariable=self.materialsString, height=5)
        self.materialListBox2 = Listbox(self, listvariable=self.materialsString, height=5)
        
        matSB = ttk.Scrollbar(self, orient=VERTICAL, command=combine_funcs(self.materialListBox1.yview, self.materialListBox2.yview))
        self.materialListBox1["yscrollcommand"] = matSB.set
        self.materialListBox2["yscrollcommand"] = matSB.set
        
        quitBtn = ttk.Button(self, text="QUIT", command=self.master.destroy)
        
        #selProd = ttk.Label(self, textvariable=self.selectedProduct)#, anchor="center")
        #selMat = ttk.Label(self, textvariable=self.selectedMaterial)#, anchor="center")
        
        dropdownLbl = ttk.Label(self, text="Select a Product to Add!")
        
        selectedProductVar = StringVar(self.master)
        dropdown = ttk.OptionMenu(self, selectedProductVar, "<Product>", *self.possibleProducts)
        
        def addProduct(*args):
            if (selectedProductVar.get() != "<Product>"):
                #Add a product to the product listbox
                prods = list(self.products) + [selectedProductVar.get()]
                prods = tuple(prods)
                self.productsString.set(prods)
                self.products = prods
                
                #Then add its materials to the material listbox
                mats = list(self.materials) + ["wood", "cardboard", "fire"]
                mats = tuple(mats)
                self.materialsString.set(mats)
                self.materials = mats
                
                self.updateListBoxes()
        
        addProductBtn = ttk.Button(self, text="Add Product", command=addProduct)
        
        #Set up the widget's location in the GUI
        productLbl.grid(column=0, row=0, pady=5)
        self.productListBox.grid(column=0, row=1, columnspan=2, stick=(N,S,E,W))
        prodSB.grid(column=2, row=1, sticky=(N,S))
        
        removeProductBtn.grid(column=0, row=2)
        removeAllProductsBtn.grid(column=1, row=2)
        
        materialLbl.grid(column=0, row=3, pady=5)
        self.materialListBox1.grid(column=0, row=4, stick=(N,S,E,W))
        self.materialListBox2.grid(column=1, row=4, stick=(N,S,E,W))
        matSB.grid(column=2, row=4, sticky=(N,S))
        
        quitBtn.grid(column=0, row=5, pady=10)
        
        dropdownLbl.grid(column=3, row=0)
        dropdown.grid(column=3, row=1)
        addProductBtn.grid(column=3, row=2)
        
        self.updateListBoxes()

        
            
        """   
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
        """
        
    def updateListBoxes(self):
        # Colorize alternating lines of the listboxes
        for i in range(0,len(self.products),2):
            self.productListBox.itemconfigure(i, background='#f0f0ff')
        for i in range(0,len(self.materials),2):
            self.materialListBox1.itemconfigure(i, background='#f0f0ff')
        for i in range(0,len(self.materials),2):
            self.materialListBox2.itemconfigure(i, background='#f0f0ff')
def main():
    root = Tk()
    app = Application(master=root)
    app.mainloop()
    
main()


