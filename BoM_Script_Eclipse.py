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
#!/usr/bin/env python
import urllib2
from bs4 import BeautifulSoup
import sys
import re

def digikey_part_is_reeled(html_tree):
    '''Returns True if this Digi-Key part is reeled or Digi-reeled.'''
    qty_tiers = list(get_digikey_price_tiers(html_tree).keys())
    if len(qty_tiers) > 0 and min(qty_tiers) >= 100:
        return True
    if html_tree.find('table',
                      id='product-details-reel-pricing') is not None:
        return True
    return False

    
def get_digikey_price(pnumber, quantity):
    page = urllib2.urlopen( \
    "http://search.digikey.ca/scripts/DkSearch/dksus.dll?Detail?name=" + pnumber)

    soup = BeautifulSoup(page,'lxml')

    '''Get the pricing tiers from the parsed tree of the Digikey product page.'''
    price_tiers = {}
    try:
        for tr in soup.find('table', id='product-dollars').find_all('tr'):
            try:
                td = tr.find_all('td')
                qty = int(re.sub('[^0-9]', '', td[0].text))
                price_tiers[qty] = float(re.sub('[^0-9\.]', '', td[1].text))
            except (TypeError, AttributeError, ValueError,
                    IndexError):  # Happens when there's no <td> in table row.
                continue
    except AttributeError:
        # This happens when no pricing info is found in the tree.
        print 'No Digikey pricing information found!'
        return 0  # Return empty price tiers.
    if min(price_tiers) >= 100:
        print "reel"
    else:
        while (price_tiers.get(quantity, None) == None):
            quantity -= 1
        print pnumber 
        print price_tiers.get(quantity, None)
        return price_tiers.get(quantity, None)
    


# File path du fichier
# Todo: Inclure un file path
fp = '/home/jean-francois/Git/Eclipse Solar Car/Template_Hardware/Project_Template/Project_Template_bom2.csv'


# Lit le Bom genere par KiBom
#get_digikey_price('535-13445-2-ND', 10)
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

#df4['Price'] = get_digikey_price(pnumber, quantity)

df4['Unit price'] = df4.apply(lambda df4: get_digikey_price(df4['Supplier Part Number'], df4['Quantity Per PCB']), axis=1)
df4['Ext price'] = df4['Unit price'] * df4['Quantity Per PCB']
#print df4.values
    
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
