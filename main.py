from tkinter import *
import tkinter.font as tkFont
from tkinter import ttk
from Controller import Controller


#Because multiple functions can be defined as a single object and this is needed for the scrollbar.
def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func
    
def sortby(tree, col, descending):
    """sort tree contents when a column header is clicked on"""
    # grab values to sort
    data = [(tree.set(child, col), child) \
        for child in tree.get_children('')]
    # if the data to be sorted is numeric change to float
    #data =  change_numeric(data)
    # now sort the data in place
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    # switch the heading so it will sort in the opposite direction
    tree.heading(col, command=lambda col=col: sortby(tree, col, \
        int(not descending)))
        
def updateTableHeader(table, header, colWidths):
    for i in range(len(header)):
        table.heading(header[i], text=header[i].title(), command=lambda c=header[i]: sortby(table, c, 0))
        table.column(header[i], width=tkFont.Font().measure(header[i].title()))
        colWidths[i] = tkFont.Font().measure(header[i].title())
        
def AdjustColumnWidths(table, header, colWidths, newItem):
    for ix, val in enumerate(newItem):
        col_w = tkFont.Font().measure(val)
        if (colWidths[ix] < col_w):
            table.column(header[ix], width=col_w)
            colWidths[ix] = col_w
        

class Application(Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master, padding=(5, 0, 100, 5))
        
        self.master = master
        
        self.master.title("DB Stuff")
        self.master.geometry('1000x700')
        
        Controller.Setup()
        
        #Set up the grid for the Widgets
        self.grid(column=0, row=0, sticky=(N,W,E,S))
        self.master.grid_columnconfigure(0,weight=1)
        self.master.grid_rowconfigure(0,weight=1)
        
        self.productTable = None
        self.productHeader = ["name", "finish", "quantity"]
        self.productColWidth = [0, 0, 0]
        
        self.possibleProductIds, self.possibleProductNames = Controller.GetPossibleProducts()
        
        self.materialTable = None
        self.materialHeader = ["name", "vendor", "unit cost", "quantity"]
        self.materialColWidth = [0, 0, 0, 0]
        
        #A dictionary mapping the products' iids for the self.productTable TreeView to possibly several
        #   materials' iids in the self.materialTable TreeView.
        #{prodiid:[matiid, matiid, ...]}
        self.productToMaterials = {}
        
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        #Create all of the widgets that we will be using.
        productLbl = ttk.Label(self, text="Products")
        
        self.productTable = ttk.Treeview(self, columns=self.productHeader, show="headings")
        prodvsb = ttk.Scrollbar(self, orient="vertical", command=self.productTable.yview)
        prodhsb = ttk.Scrollbar(self, orient="horizontal", command=self.productTable.xview)
        self.productTable.configure(yscrollcommand=prodvsb.set, xscrollcommand=prodhsb.set)
        
        def removeProduct(*args):
            selitems = self.productTable.selection()
            for prodiid in selitems:
                #print(prodiid)
                #print(self.productTable.item(prodiid))
                #print(self.productTable.item(prodiid)["tags"][0])
                product = Controller.GetProduct(prodiid)
                
                for material in product.materials:
                    self.materialTable.delete(material.PK)
                
                self.productTable.delete(prodiid)
                #This just subtracts from the quantity if more than 1 exists.
                Controller.RemoveProduct(prodiid)
                
        def removeAllProducts(*args):
            for i in range(len(self.productTable.get_children())-1,-1,-1):
                self.productTable.delete(self.productTable.get_children()[i])
                
            for i in range(len(self.materialTable.get_children())-1,-1,-1):
                self.materialTable.delete(self.materialTable.get_children()[i])
        
        removeProductBtn = ttk.Button(self, text="Remove Product", command=removeProduct)
        removeAllProductsBtn = ttk.Button(self, text="Remove All Products", command=removeAllProducts)
        
        materialLbl = ttk.Label(self, text="Materials")
        self.materialTable = ttk.Treeview(self, columns=self.materialHeader, show="headings")
        matvsb = ttk.Scrollbar(self, orient="vertical", command=self.materialTable.yview)
        mathsb = ttk.Scrollbar(self, orient="horizontal", command=self.materialTable.xview)
        self.materialTable.configure(yscrollcommand=matvsb.set, xscrollcommand=mathsb.set)
        
        quitBtn = ttk.Button(self, text="QUIT", command=self.master.destroy)
        
        dropdownLbl = ttk.Label(self, text="Select a Product to Add!")
        
        selectedProductVar = StringVar(self.master)
        dropdown = ttk.OptionMenu(self, selectedProductVar, "<Product>", *self.possibleProductNames)
        
        def addProduct(*args):
            if (selectedProductVar.get() != "<Product>"):
                indx = self.possibleProductNames.index(selectedProductVar.get())
                product = Controller.AddProduct(self.possibleProductIds[indx], 1)
                
                newProd = (product.columnInfo["ProductDescription"], product.columnInfo["ProductFinish"], product.quantity)
                
                #First check to see if the product and its materials exist already!
                #There should only be 1 instance of each product and material in the tables.
                self.productTable.insert("", "end", iid=product.PK, values=newProd)
                
                AdjustColumnWidths(self.productTable, self.productHeader, self.productColWidth, newProd)
                
                for mat in product.materials:
                    newMat = (mat.name, mat.vendor, mat.unitCost, mat.quantity)
                    self.materialTable.insert("", "end", iid=mat.PK, values=newMat)
                    
                    AdjustColumnWidths(self.materialTable, self.materialHeader, self.materialColWidth, newMat)
                    
                    #materialList = self.productToMaterials.get(product.PK, [])
                    #materialList += mat.PK
                    #self.productToMaterials[product.PK] = materialList
                    
        addProductBtn = ttk.Button(self, text="Add Product", command=addProduct)
        
        #Set up the widget's location in the GUI
        productLbl.grid(column=0, row=0, pady=5)
        self.productTable.grid(column=0, row=1, columnspan=4, stick=(N,S,E,W))
        prodvsb.grid(column=2, row=1, sticky="ns")
        prodhsb.grid(column=0, row=2, columnspan=4, sticky="ew")
        
        removeProductBtn.grid(column=0, row=4)
        removeAllProductsBtn.grid(column=0, row=5)
        
        dropdownLbl.grid(column=1, row=3)
        dropdown.grid(column=1, row=4)
        addProductBtn.grid(column=1, row=5)
        
        materialLbl.grid(column=0, row=6, pady=6)
        self.materialTable.grid(column=0, row=7, columnspan=4, stick=(N,S,E,W))
        matvsb.grid(column=2, row=7, sticky="ns")
        mathsb.grid(column=0, row=8, columnspan=4, sticky="ew")
        
        quitBtn.grid(column=0, row=9, pady=10)
        
        self.columnconfigure(0, minsize=300)
        self.columnconfigure(1, minsize=300)
        
        updateTableHeader(self.productTable, self.productHeader, self.productColWidth)
        updateTableHeader(self.materialTable, self.materialHeader, self.materialColWidth)
        
def main():
    root = Tk()
    app = Application(master=root)
    app.mainloop()
    Controller.TearDown()
    
main()


