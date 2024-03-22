# import pandas as pd

import numpy as np

import csv

# podaci=pd.read_csv(r"C:\FSB\cetvrta godina\Zavrsni rad\toplsinke tablice\topltabl.csv",delimiter=';')

def ucitavanje(*dat): #def funkcije

    velicina= np.shape(dat)[0] #broj ulaznih podataka#stvaranje lista za podatke
    lista= [[]for i in range( velicina)]
    j= 0

    for datoteke in dat: #ulazni podatci
        with open( datoteke) as brojevi: #raspakiravanje ulaznih podataka
            podatci= csv.reader(brojevi, delimiter=';') #csv čitač podatak
            next(podatci)
            for redak in podatci: #za redove unutar padatka
                lista[j].append(redak) #puni mi listu s redovima
            j+=1
            
    return lista
# def main():
global nova_lista1, nova_lista2, rijecnik1, rijecnik2,rijecnik3

nova_lista1= ucitavanje('C:/FSB/cetvrta godina/Zavrsni rad/kod_slike_tabl/Toplinske tablice/topltabl.csv','C:/FSB/cetvrta godina/Zavrsni rad/kod_slike_tabl/Toplinske tablice/topltabl2.csv')
nova_lista3 =ucitavanje('C:/FSB/cetvrta godina/Zavrsni rad/kod_slike_tabl/Toplinske tablice/topltabl3+.csv')


rijecnik1= {}
rijecnik2= {}
rijecnik3= {}


# zamjena ","sa "." zato što glupi excel to nemože
for i in range(np.shape(nova_lista1)[0]):
    for j in range(len(nova_lista1[i])):
        for k in range(len(nova_lista1[i][i])):
            nova_lista1[i][j][k]= nova_lista1[i][j][k].replace(',','.').replace('â€“','-')


for l in range(len(nova_lista3[0])):
    for m in range(len(nova_lista3[0][0])):
        nova_lista3[0][l][m]= nova_lista3[0][l][m].replace(',','.')


nova_lista1= np.array(nova_lista1, dtype= object)
nova_lista3= np.array(nova_lista3, dtype= object)


nova_lista3= np.reshape(nova_lista3,(45,30,4))
nova_lista2= np.array(nova_lista1[1], dtype= object)
nova_lista1= np.array(nova_lista1[0], dtype= object)


tlakovi= np.array([0.1,0.5,1,1.5,2,3,4,5,6,7,8,9,10,12.5,15,17.5,20,25,30,35,40,45,50,60,70,80,90,100,120,140],dtype=object)
tlakovi= [str(element).replace('.0','') for element in tlakovi]
temperatura= nova_lista3[:,0][:,0]


kljucevi1= nova_lista1.T[0]
kljucevi2= nova_lista2.T[0]
kljucevi3= tlakovi


vrjednosti1= nova_lista1[:,1:]
vrjednosti2= nova_lista2[:,1:]
vrjednosti3= nova_lista3

for i in range(len(kljucevi1)):
    rijecnik1[kljucevi1[i]]= vrjednosti1[i]

for i in range(len(kljucevi2)):
    rijecnik2[kljucevi2[i]]= vrjednosti2[i]

for i in range(len(kljucevi3)):
    pomocni= {}
    for j in range(np.shape(nova_lista3)[0]):
        pomocni[temperatura[j]]= nova_lista3[:,i][j][1:]
    rijecnik3[kljucevi3[i]]= pomocni
