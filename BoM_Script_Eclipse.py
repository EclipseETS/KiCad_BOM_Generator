# -*- coding: utf-8 -*-
"""
Created on Mon May 15 18:21:18 2017

@author: Jul

#==============================================================================

Description:
1- Ouvrir le BOM generer par KiBom.
2- Lire le fichier
3- Generer le csv Project_MasterBom
4- Ecrire dans le Project_MasterBom
5- Generer les csv Digikey_MasterBom, Wurth_MasterBom, autre_MasterBom
6- Parser le csv pour les différents suppliers
7- Ecrire dans les csv des suppliers respectifs

Option: Generer les noms des supliers automatiquement

#==============================================================================
"""


# Import modules
import pandas as pd

# Todo: Modifier en fonction
# Todo: Faire une interface graphique

# Todo: Inclure le nom du responsable de la commande


# File path du fichier
# Todo: Inclure un file path
fp = 'C:\Eclipse\KiCad_BoM_Eclipse\\Project_Template_bom.csv'


# Lit le Bom genere par KiBom
df1=pd.read_csv(fp)


# Lit les colonnes standards a Eclipse
df2 = pd.DataFrame(df1, columns = ['Component', 'References', 'Value', 'Footprint', 'Quantity Per PCB', 'Description', 'Manufacturer', 'Manufacturer Part Number', 'Supplier', 'Supplier Part Number'])

# Ecrit dans un nouveau fichier le Master Bom
# Todo: Renommer le nom de fichier
df2.to_csv('MasterBom.csv', index = False)

# Scan pour les colonnes pertinente a la commande
df3 = pd.DataFrame(df1, columns = ['Manufacturer', 'Manufacturer Part Number', 'Supplier', 'Supplier Part Number', 'Quantity Per PCB'])

# Scan pour le supplier Digikey
df4 = df3[df3['Supplier'].notnull() & (df3['Supplier'] == "Digikey")& (df3['Manufacturer'] != "Wurth Electronics Inc.")]
# Remet l'index a zero
df4 = df4.reset_index(drop=True)
# Fait commencer l'index a 1
df4.index =  df4.index + 1  
# Ecrit dans un fichier csv les pieces chez digikey 
df4.to_csv('DigikeyBom.csv')

# Scan pour le supplier Wurth
df5 = df3[df3['Supplier'].notnull() & (df3['Manufacturer'] == "Wurth Electronics Inc.")]
# Remet l'index a zero
df5 = df5.reset_index(drop=True)
# Fait commencer l'index a 1
df5.index =  df5.index + 1 
# Ecrit dans un fichier csv les pieces chez digikey 
# Todo: Ajouter le nom du projet
df5.to_csv('WurthBom.csv')

# Scan pour les autres supplier que Wurth et digikey
df6 =  df3[df3['Supplier'].notnull() & (df3['Manufacturer'] != "Wurth Electronics Inc.") & (df3['Supplier'] != "Digikey")]
# Remet l'index a zero
df6 = df6.reset_index(drop=True)
# Fait commencer l'index a 1
df6.index =  df6.index + 1
# Ecrit dans un fichier csv les autres pieces a commander
df6.to_csv('OtherBom.csv')



#==============================================================================
# import tkinter
# from tkinter.filedialog import askopenfilename
# 
#==============================================================================







#==============================================================================
# def browse():
#     global infile
#     infile=askopenfilename()
#     
# def newfile();:
#     global oufile
#     outfine=askopenfilename()
#     
# def BomFunction(outfile=outfile)
#     df = pandas.read_csv(infile)
#     
# 
# 
#==============================================================================



#==============================================================================
# 
# root=tkinter.Tk()
# 
# root.title("Bom Generator")
# 
# 
# label=tkinter.Label(root, text="Bom Generator for Eclipse")
# label.pack()
# 
# 
# browseButton=tkinter.Button(root,text="Browse", command=browse)
# browseButton.pack()
# 
# 
# 
# root.mainloop()
# 
# 
#==============================================================================



# For windows installer
# pip install pyinstaller
# pyinstaller --onefile --windoed "name.py"
