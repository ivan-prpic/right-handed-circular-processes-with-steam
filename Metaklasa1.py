import numpy as np
import copy
import sys

sys.path.append(r'C:/FSB/cetvrta godina/Zavrsni rad/kod_slike_tabl/Kod/CSV_kod.py')

import CSV_kod as CSV_kod


rijecnik1= CSV_kod.rijecnik1
rijecnik2= CSV_kod.rijecnik2
rijecnik3= CSV_kod.rijecnik3

nova_lista1= CSV_kod.nova_lista1
nova_lista2= CSV_kod.nova_lista2
nova_lista3= CSV_kod.nova_lista3


def interpol1(donja_vrijednost,gornja_vrijednost,s1,s2,s):
    donja_vrijednost=float(donja_vrijednost)
    gornja_vrijednost=float(gornja_vrijednost)
    s1=float(s1)
    s2=float(s2)
    s=float(s)
    y=donja_vrijednost+((gornja_vrijednost-donja_vrijednost)/(s2-s1))*(s-s1)
    return y

def interpolica1(donja_vrijednost,gornja_vrijednost,s1,s2,s):
    try:
        m,n=np.shape(donja_vrijednost)
        for j in range(n):
            for i in range(m):
                donja_vrijednost[i][j]=float(donja_vrijednost[i][j])
                gornja_vrijednost[i][j]=float(gornja_vrijednost[i][j])
    except ValueError:
        m=len(donja_vrijednost)
        for i in range(m):
            donja_vrijednost[i]=float(donja_vrijednost[i])
            gornja_vrijednost[i]=float(gornja_vrijednost[i])
            donja_vrijednost[i]=round(donja_vrijednost[i],6)
            gornja_vrijednost[i]=round(gornja_vrijednost[i],6)
    s1=float(s1)
    s2=float(s2)
    s=float(s)
    y=donja_vrijednost+((gornja_vrijednost-donja_vrijednost)/(s2-s1))*(s-s1)
    return y

def mas_udio(a,b,c): #prvo ide s pa s' pa s''
    a=float(a)
    b=float(b)
    c=float(c)
    y=(a-b)/(c-b)
    return y

def vel_stanja(a,b,c):
    a=float(a)
    b=float(b)
    c=float(c)
    y=a+c*(b-a)
    return y

def vrati_kljuc_po_indeksu(rjecnik, indeks):
    indeks_vrijednosti = 0

    for kljuc, vrijednost in rjecnik.items():
        if indeks_vrijednosti == indeks:
            return kljuc
        indeks_vrijednosti += 1

    return None  # Vraća None ako indeks nije pronađen u rječniku

def nadji_veći_i_manji(lista, moj_broj, rijecnik):
    prvi_veći = None
    indeks_većeg = None
    prvi_manji = None
    indeks_manjeg = None
    broj_jednak = None
    indeks_jednak = None

    lista = [float(num) for num in lista]
    moj_broj = float(moj_broj)

    for indeks, broj in enumerate(lista):
        if broj > moj_broj:
            if prvi_veći is None or broj < prvi_veći:
                prvi_veći = broj
                indeks_većeg = indeks
        elif broj < moj_broj:
            if prvi_manji is None or broj > prvi_manji:
                prvi_manji = broj
                indeks_manjeg = indeks
        elif broj == moj_broj:
            broj_jednak = broj
            indeks_jednak = indeks

    # If the number is equal to the given number
    if broj_jednak is not None:
        a = [vrati_kljuc_po_indeksu(rijecnik, indeks_jednak)]
        b = [broj_jednak]
        return a, b

    a = [vrati_kljuc_po_indeksu(rijecnik, indeks_većeg), vrati_kljuc_po_indeksu(rijecnik, indeks_manjeg)]
    b = [prvi_veći, prvi_manji]

    return a, b

sve=np.array([[['10'],
        ['179.89'],
        [''],
        [''],
        [''],
        ['']],

        [['8.2'],
        [''],
        [''],
        [''],
        [''],
        ['']],

        [['8.2'],
        ['350'],
        [''],
        [''],
        [''],
        ['']],

        [['0.22'],
        [''],
        [''],
        [''],
        [''],
        ['']],

        [[''],
        [''],
        [''],
        [''],
        ['0'],
        ['']],

        [['33'],
        [''],
        [''],
        [''],
        [''],
        ['']]],dtype='<U9')


# tlak=sve[:,0]
# temperatura=sve[:,1]
# entalpija=sve[:,2]
# entropija=sve[:,3]
# mas_ud=sve[:,4]
# volumen=sve[:,5]

class Trazi_tabl:
    def __init__(self, broj, stanja, vrijednost_stanje, maseni_ud=None):

        self.broj=broj
        self.stanja=stanja

        if maseni_ud != None:
            self.maseni_ud=float(maseni_ud)
        else:
            self.maseni_ud = maseni_ud

        self.vrijednost_stanje=str(vrijednost_stanje)

    def stanja_lista(self,lista):

        self.lista_stanja=copy.copy(lista[:])


        global tlak, temperatura, entalpija, entropija, mas_ud, volumen
        # print(self.lista_stanja)
        
        tlak=self.lista_stanja[:,0]
        temperatura=self.lista_stanja[:,1]
        entalpija=self.lista_stanja[:,2]
        entropija=self.lista_stanja[:,3]
        mas_ud=self.lista_stanja[:,4]
        volumen=self.lista_stanja[:,5]

        return self.lista_stanja

    def interpol_tabl1(self, pom_temp= None, pom_stanje=None):
        self.pom_temp= pom_temp
        self.pom_stanje= pom_stanje

        self.tlak= tlak
        self.temperatura= temperatura
        self.entalpija= entalpija
        self.entropija= entropija
        self.mas_ud= mas_ud
        self.volumen= volumen

        if self.pom_temp != None:
            self.pom_temp=str(self.pom_temp)

            try:
                self.pom_stanje=rijecnik1[self.pom_temp]
            except KeyError:
                pomocna_temp= list(rijecnik1.keys())
                gornja_donja_temp=nadji_veći_i_manji(pomocna_temp, float(self.pom_temp), rijecnik1)
                self.pom_stanje=interpolica1(rijecnik1[gornja_donja_temp[0][1]],rijecnik1[gornja_donja_temp[0][0]],
                                    gornja_donja_temp[0][1],gornja_donja_temp[0][0], self.pom_temp)

        if self.stanja == 'T': ##npr u zadatku znam tocno temperaturu i mas_ud za tocku
            self.temperatura[self.broj]=self.vrijednost_stanje
                
            try:
                stanje=rijecnik1[self.vrijednost_stanje]
                self.tlak[self.broj]= stanje[0]

            except KeyError:
                pomocna_temp= list(rijecnik1.keys())
                gornja_donja_temp=nadji_veći_i_manji(pomocna_temp, float(self.vrijednost_stanje), rijecnik1)
                stanje=interpolica1(rijecnik1[gornja_donja_temp[0][1]],rijecnik1[gornja_donja_temp[0][0]],
                                    gornja_donja_temp[0][1],gornja_donja_temp[0][0], self.vrijednost_stanje)

                self.tlak[self.broj]= stanje[0]


        if self.stanja == 'p':# npr znam tlak i mas_ud za tocku
            self.tlak[self.broj]=self.vrijednost_stanje

            try:

                pomocna_tlak=list(np.array(list(rijecnik1.values()))[:,0])
                indeks=pomocna_tlak.index(self.vrijednost_stanje)
                kljuc=vrati_kljuc_po_indeksu(rijecnik1, indeks)
                stanje=rijecnik1[kljuc]
                self.temperatura[self.broj]= str(kljuc)

            except ValueError or KeyError:

                pomocna_tlak1=np.array(list(rijecnik1.values()))[:,0]
                gornji_donji_tlak=np.array(nadji_veći_i_manji(pomocna_tlak1,self.vrijednost_stanje,rijecnik1))
                pomocno_stanje1=rijecnik1[gornji_donji_tlak[0][0]]
                pomocno_stanje2=rijecnik1[gornji_donji_tlak[0][1]]
                stanje=interpolica1(pomocno_stanje1,pomocno_stanje2,
                                    gornji_donji_tlak[1][0],gornji_donji_tlak[1][1], self.vrijednost_stanje)
                self.temperatura[self.broj]= interpol1(gornji_donji_tlak[0][0],gornji_donji_tlak[0][1],
                    gornji_donji_tlak[1][0],gornji_donji_tlak[1][1], self.vrijednost_stanje)

        if self.stanja == 'h' or self.stanja == 's': #npr znam temp na koju ekspandira i znam kolika mi je entalpija,
                                #a moram izracunati mas_ud da znam u kojem sam podrucju

            try:
                stanje= rijecnik1[self.temperatura[self.broj][0]]
            except KeyError:
                pomocna_temp= list(rijecnik1.keys())
                gornja_donja_temp=nadji_veći_i_manji(pomocna_temp, float(self.temperatura[self.broj][0]), rijecnik1)
                stanje=interpolica1(rijecnik1[gornja_donja_temp[0][1]],rijecnik1[gornja_donja_temp[0][0]],
                                    gornja_donja_temp[0][1],gornja_donja_temp[0][0], self.temperatura[self.broj][0])

        if self.maseni_ud == None:
            if self.stanja == 'h':
                self.mas_ud[self.broj] = mas_udio(self.vrijednost_stanje, stanje[3], stanje[4])
                self.entalpija[self.broj] = self.vrijednost_stanje

                if float(self.mas_ud[self.broj]) <0:
                    print('MORAM ICI U POTHLADENO')

                if float(self.mas_ud[self.broj]) >1:
                    print('MORAM ICI U PREGRIJANO')

                if float(self.mas_ud[self.broj])>0 and float(self.mas_ud[self.broj])<1:

                    self.entropija[self.broj]= vel_stanja(stanje[6], stanje[7], float(self.mas_ud[self.broj]))
                    self.volumen[self.broj]= vel_stanja(stanje[1], stanje[2], float(self.mas_ud[self.broj]))
                    self.tlak[self.broj] = stanje[0]

            if self.stanja == 's':
                self.mas_ud[self.broj] = mas_udio(self.vrijednost_stanje, stanje[6], stanje[7])
                self.entropija[self.broj]=self.vrijednost_stanje

                if float(self.mas_ud[self.broj]) <0:
                    print('MORAM ICI U POTHLADENO-metoda za pothađeno')

                if float(self.mas_ud[self.broj]) >1:
                    print('MORAM ICI U PREGRIJANO-zovem metodu za pregrijano')

                if float(self.mas_ud[self.broj])>0 and float(self.mas_ud[self.broj])<1:

                    self.entalpija[self.broj]= vel_stanja(stanje[3], stanje[4], float(self.mas_ud[self.broj]))
                    self.volumen[self.broj]= vel_stanja(stanje[1], stanje[2], float(self.mas_ud[self.broj]))
                    self.tlak[self.broj] = stanje[0]


        if self.maseni_ud != None:
            self.mas_ud[self.broj]=self.maseni_ud

            if self.maseni_ud == 0:
                self.entalpija[self.broj]= stanje[3]
                self.entropija[self.broj]= stanje[6]
                self.volumen[self.broj]= stanje[1]

            if self.maseni_ud == 1:
                self.entalpija[self.broj]= stanje[4]
                self.entropija[self.broj]= stanje[7]
                self.volumen[self.broj]= stanje[2]

            if self.maseni_ud > 0 and self.maseni_ud < 1:
                self.entalpija[self.broj]= vel_stanja(stanje[3], stanje[4], self.maseni_ud)
                self.entropija[self.broj]= vel_stanja(stanje[6], stanje[7], self.maseni_ud)
                self.volumen[self.broj]= vel_stanja(stanje[1], stanje[2], self.maseni_ud)

            if self.maseni_ud  < 0:
                pass
                #trebao biih dodati sta se desi kada si zadam automtski mas ud -1
        return stanje, self.pom_stanje

    def interpol_tabl2(self, pom_tlak=None,pom_stanje= None):
        self.pom_tlak=pom_tlak
        self.pom_stanje= pom_stanje

        self.tlak= tlak
        self.temperatura= temperatura
        self.entalpija= entalpija
        self.entropija= entropija
        self.mas_ud= mas_ud
        self.volumen= volumen

        if self.pom_tlak != None:
            self.pom_tlak = str(self.pom_tlak)
            try:
                self.pom_stanje=rijecnik2[self.pom_tlak]

            except KeyError:
                pomocna_tlak= list(rijecnik2.keys())
                gornja_donja_tlak=nadji_veći_i_manji(pomocna_tlak, float(self.pom_tlak), rijecnik2)
                self.pom_stanje=interpolica1(rijecnik2[gornja_donja_tlak[0][1]],rijecnik2[gornja_donja_tlak[0][0]],
                                    gornja_donja_tlak[0][1],gornja_donja_tlak[0][0], self.pom_tlak)

        if self.stanja == 'p': ##npr u zadatku znam tocno tlak i mas_ud za tocku
            self.tlak[self.broj]=self.vrijednost_stanje

            try:
                stanje=rijecnik2[self.vrijednost_stanje]
                self.temperatura[self.broj]= stanje[0]

            except KeyError:
                pomocna_tlak= list(rijecnik2.keys())
                gornja_donja_tlak=nadji_veći_i_manji(pomocna_tlak, float(self.vrijednost_stanje), rijecnik2)
                stanje=interpolica1(rijecnik2[gornja_donja_tlak[0][1]],rijecnik2[gornja_donja_tlak[0][0]],
                                    gornja_donja_tlak[0][1],gornja_donja_tlak[0][0], self.vrijednost_stanje)

                self.temperatura[self.broj]= stanje[0]


        if self.stanja == 'T':# npr znam temp i mas_ud za tocku
            self.temperatura[self.broj]=self.vrijednost_stanje

            try:

                pomocna_temp=list(np.array(list(rijecnik2.values()))[:,0])
                indeks=pomocna_temp.index(self.vrijednost_stanje)
                kljuc=vrati_kljuc_po_indeksu(rijecnik2, indeks)
                stanje=rijecnik2[kljuc]
                self.tlak[self.broj]= str(kljuc)

            except ValueError or KeyError:

                pomocna_temp1=np.array(list(rijecnik2.values()))[:,0]
                gornji_donji_temp=np.array(nadji_veći_i_manji(pomocna_temp1,self.vrijednost_stanje,rijecnik2))
                pomocno_stanje1=rijecnik2[gornji_donji_temp[0][0]]
                pomocno_stanje2=rijecnik2[gornji_donji_temp[0][1]]
                stanje=interpolica1(pomocno_stanje1,pomocno_stanje2,
                                    gornji_donji_temp[1][0],gornji_donji_temp[1][1], self.vrijednost_stanje)
                self.temperatura[self.broj]= interpol1(gornji_donji_temp[0][0],gornji_donji_temp[0][1],
                    gornji_donji_temp[1][0],gornji_donji_temp[1][1], self.vrijednost_stanje)

        if self.stanja == 'h' or self.stanja == 's':
            #npr znam temp na koju ekspandira i znam kolika mi je entalpija,
                                                                #a moram izracunati mas_ud da znam u kojem sam podrucju
            try:
                stanje= rijecnik2[self.tlak[self.broj][0]]
            except KeyError:
                pomocna_tlak= list(rijecnik2.keys())
                gornja_donja_tlak=nadji_veći_i_manji(pomocna_tlak, float(self.tlak[self.broj][0]), rijecnik2)
                stanje=interpolica1(rijecnik2[gornja_donja_tlak[0][1]],rijecnik2[gornja_donja_tlak[0][0]],
                                    gornja_donja_tlak[0][1],gornja_donja_tlak[0][0], self.tlak[self.broj][0])

        if self.maseni_ud == None:
            if self.tlak[self.broj] != self.vrijednost_stanje:
                if self.stanja == 'h':
                    self.mas_ud[self.broj] = mas_udio(self.vrijednost_stanje, stanje[3], stanje[4])
    
                    if float(self.mas_ud[self.broj]) >1 or float(self.mas_ud[self.broj]) <0:
                        print('MORAM ICI U PREGRIJANO ili POTHLAĐENO-tabl2-h')
                        try:
                            pomocna_entalpija=np.array(list(rijecnik3[self.tlak[self.broj][0]].values()))[:,1]
                            entalpija_gornja_donja=nadji_veći_i_manji(pomocna_entalpija, self.vrijednost_stanje, rijecnik3[self.tlak[self.broj][0]])
                        except KeyError:
                            pomocni_tlak=np.array(list(rijecnik3.keys()))
                            gornji_donji_tlak=nadji_veći_i_manji(pomocni_tlak, self.tlak[self.broj][0], rijecnik3)
                            stanje1=np.array(list(rijecnik3[gornji_donji_tlak[0][1]].values()))
                            stanje2=np.array(list(rijecnik3[gornji_donji_tlak[0][0]].values()))
                            pomocna_entalpija=interpolica1(stanje1,stanje2,
                                    gornji_donji_tlak[0][1],gornji_donji_tlak[0][0], self.tlak[self.broj][0])
                            entalpija_gornja_donja=nadji_veći_i_manji(pomocna_entalpija[:,1],
                                    self.vrijednost_stanje, rijecnik3[gornji_donji_tlak[0][0]])
                        
                        if np.size(entalpija_gornja_donja) == 4:
                            self.temperatura[self.broj]=interpol1(entalpija_gornja_donja[0][1],entalpija_gornja_donja[0][0],
                               entalpija_gornja_donja[1][1],entalpija_gornja_donja[1][0],self.vrijednost_stanje)
                        else:
                            self.temperatura[self.broj]=entalpija_gornja_donja[0][0]

                        self.entalpija[self.broj]=self.vrijednost_stanje

                        x=self.interpol_tabl3(self.temperatura[self.broj][0],self.tlak[self.broj][0])

                        self.volumen[self.broj]=x[0]
                        self.entropija[self.broj]=x[2]


                    if float(self.mas_ud[self.broj])>0 and float(self.mas_ud[self.broj])<1:
                            self.entalpija[self.broj] = self.vrijednost_stanje
                            self.entropija[self.broj]= vel_stanja(stanje[6], stanje[7], float(self.mas_ud[self.broj]))
                            self.volumen[self.broj]= vel_stanja(stanje[1], stanje[2], float(self.mas_ud[self.broj]))
                            self.temperatura[self.broj] = stanje[0]


            if self.tlak[self.broj] != self.vrijednost_stanje:
                if self.stanja == 's':
                    self.mas_ud[self.broj] = mas_udio(self.vrijednost_stanje, stanje[6], stanje[7])
    
                    if float(self.mas_ud[self.broj]) >1 or float(self.mas_ud[self.broj]) <0:
                        print('MORAM ICI U PREGRIJANO-tabl2-s')
                        try:
                            pomocna_entropija=np.array(list(rijecnik3[self.tlak[self.broj][0]].values()))[:,2]
                            entropija_gornja_donja=nadji_veći_i_manji(pomocna_entropija, self.vrijednost_stanje, rijecnik3[self.tlak[self.broj][0]])
                        except KeyError:
                            pomocni_tlak=np.array(list(rijecnik3.keys()))
                            gornji_donji_tlak=nadji_veći_i_manji(pomocni_tlak, self.tlak[self.broj][0], rijecnik3)
                            stanje1=np.array(list(rijecnik3[gornji_donji_tlak[0][1]].values()))
                            stanje2=np.array(list(rijecnik3[gornji_donji_tlak[0][0]].values()))
                            pomocna_entropija=interpolica1(stanje1,stanje2,
                                    gornji_donji_tlak[0][1],gornji_donji_tlak[0][0],self.tlak[self.broj][0])
                            entropija_gornja_donja=nadji_veći_i_manji(pomocna_entropija[:,2],
                                    self.vrijednost_stanje, rijecnik3[gornji_donji_tlak[0][0]])

                        if np.size(entropija_gornja_donja) == 4:
                            self.temperatura[self.broj]=interpol1(entropija_gornja_donja[0][1],entropija_gornja_donja[0][0],
                                  entropija_gornja_donja[1][1],entropija_gornja_donja[1][0],self.vrijednost_stanje)


                        else:
                            self.temperatura[self.broj]=entropija_gornja_donja[0][0]

                        self.entropija[self.broj] = self.vrijednost_stanje

                        x=self.interpol_tabl3(self.temperatura[self.broj][0],self.tlak[self.broj][0])

                        self.volumen[self.broj]=x[0]
                        self.entalpija[self.broj]=x[1]

                    if float(self.mas_ud[self.broj])>0 and float(self.mas_ud[self.broj])<1:
                            self.entropija[self.broj] = self.vrijednost_stanje
                            self.entalpija[self.broj]= vel_stanja(stanje[3], stanje[4], float(self.mas_ud[self.broj]))
                            self.volumen[self.broj]= vel_stanja(stanje[1], stanje[2], float(self.mas_ud[self.broj]))
                            self.temperatura[self.broj] = stanje[0]


        if self.maseni_ud != None:
            self.mas_ud[self.broj]=self.maseni_ud

            if self.maseni_ud == 0:
                self.entalpija[self.broj]= stanje[3]
                self.entropija[self.broj]= stanje[6]
                self.volumen[self.broj]= stanje[1]

            if self.maseni_ud == 1:
                self.entalpija[self.broj]= stanje[4]
                self.entropija[self.broj]= stanje[7]
                self.volumen[self.broj]= stanje[2]

            if self.maseni_ud > 0 and self.maseni_ud < 1:
                self.entalpija[self.broj]= vel_stanja(stanje[3], stanje[4], self.maseni_ud)
                self.entropija[self.broj]= vel_stanja(stanje[6], stanje[7], self.maseni_ud)
                self.volumen[self.broj]= vel_stanja(stanje[1], stanje[2], self.maseni_ud)

        return stanje, self.pom_stanje

    def interpol_tabl3(self,temp=None,tlak_pom=None):
        self.temp=temp
        self.tlak_pom=tlak_pom

        self.tlak= tlak
        self.temperatura= temperatura
        self.entalpija= entalpija
        self.entropija= entropija
        self.mas_ud= mas_ud
        self.volumen= volumen


        def tabl3(var):
            self.vrijednost_stanje=var

            if float(self.tlak[self.broj])<0.1 and float(self.mas_ud[self.broj])<0:
                stanje_za_pom1=self.interpol_tabl1(self.temp)[1]
                stanje=np.array([stanje_za_pom1[i] for i in [1,3,6]],dtype= object)

            if self.temp != None:

                if float(self.tlak[self.broj])<0.1 and float(self.mas_ud[self.broj])<0:
                    stanje_za_pom1=self.interpol_tabl1(self.temp)[1]
                    stanje=np.array([stanje_za_pom1[i] for i in [1,3,6]],dtype= object)

                if float(self.temp) == float(self.interpol_tabl2(self.vrijednost_stanje)[1][0]):
                    stanje=self.interpol_tabl2(self.vrijednost_stanje)[1]

                else:

                        try:
                            stanje=rijecnik3[self.vrijednost_stanje]
                            try:
                                stanje=rijecnik3[self.vrijednost_stanje][self.temp]
                            except KeyError:
                                pomocna_temp=np.array(list(rijecnik3[self.vrijednost_stanje].keys()))
                                gornja_donja_temperatura=np.array(nadji_veći_i_manji(pomocna_temp,self.temp,rijecnik3[self.vrijednost_stanje]))
                                stanje1=rijecnik3[self.vrijednost_stanje][gornja_donja_temperatura[0][1]]
                                stanje2=rijecnik3[self.vrijednost_stanje][gornja_donja_temperatura[0][0]]

                                if float(stanje1[1])*2<float(stanje2[1]) and float(stanje1[1])>100:
                                    if float(gornja_donja_temperatura[0][1])<float(self.interpol_tabl2(self.vrijednost_stanje)[1][0])<float(gornja_donja_temperatura[0][0]):
                                        stanje_za_pom2=self.interpol_tabl2(self.vrijednost_stanje)[1]

                                        if float(self.temp)<float(self.interpol_tabl2(self.vrijednost_stanje)[1][0]):
                                            stanje2=np.array([stanje_za_pom2[i] for i in [1,3,6]],dtype= object)
                                            stanje=interpolica1(stanje1,stanje2,
                                                                gornja_donja_temperatura[0][1],stanje_za_pom2[0],self.temp)
                                        if float(self.temp)>float(self.interpol_tabl2(self.vrijednost_stanje)[1][0]):
                                            stanje1=np.array([stanje_za_pom2[i] for i in [2,4,7]],dtype= object)
                                            stanje=interpolica1(stanje1,stanje2,
                                                                stanje_za_pom2[0],gornja_donja_temperatura[0][0],self.temp)
                                else:
                                    stanje=interpolica1(stanje2,stanje1,
                                                        gornja_donja_temperatura[0][0],gornja_donja_temperatura[0][1],self.temp)
            
                        except KeyError:
                            try:
                                pomocni_tlak=np.array(list(rijecnik3.keys()))
                                gornji_donji_tlak=nadji_veći_i_manji(pomocni_tlak, self.vrijednost_stanje, rijecnik3)
                                stanje1=rijecnik3[gornji_donji_tlak[0][1]][self.temp]
                                stanje2=rijecnik3[gornji_donji_tlak[0][0]][self.temp]
        
                                if float(stanje2[1])*1.5<float(stanje1[1]):
                                    if float(self.interpol_tabl2(gornji_donji_tlak[0][1])[1][0])< float(self.temp) < float(self.interpol_tabl2(gornji_donji_tlak[0][0])[1][0]):
                                        stanje_za_pom1=self.interpol_tabl1(self.temp)[1]
                
                                        if float(self.temp)<float(self.interpol_tabl2(self.vrijednost_stanje)[1][0]):
                                            stanje1=np.array([stanje_za_pom1[i] for i in [1,3,6]],dtype= object)
                                            stanje=interpolica1(stanje1,stanje2,
                                                                stanje_za_pom1[0],gornji_donji_tlak[0][0],self.vrijednost_stanje)
                                        if float(self.temp)>float(self.interpol_tabl2(self.vrijednost_stanje)[1][0]):
                                            stanje2=np.array([stanje_za_pom1[i] for i in [2,4,7]],dtype= object)
                                            stanje=interpolica1(stanje1,stanje2,
                                                                gornji_donji_tlak[0][1],stanje_za_pom1[0],self.vrijednost_stanje)
                                else:
                                    stanje=interpolica1(stanje1,stanje2,
                                                    gornji_donji_tlak[0][1],gornji_donji_tlak[0][0],self.vrijednost_stanje)
            
                            except KeyError:
            
                                pomocna_temp=np.array(list(rijecnik3[gornji_donji_tlak[0][0]].keys()))
                                gornja_donja_temp=nadji_veći_i_manji(pomocna_temp, self.temp, rijecnik3[gornji_donji_tlak[0][0]])
                                stanje1=interpolica1(rijecnik3[gornji_donji_tlak[0][1]][gornja_donja_temp[0][1]],rijecnik3[gornji_donji_tlak[0][1]][gornja_donja_temp[0][0]],
                                                    gornja_donja_temp[0][1],gornja_donja_temp[0][0],self.temp)
                                stanje2=interpolica1(rijecnik3[gornji_donji_tlak[0][0]][gornja_donja_temp[0][1]],rijecnik3[gornji_donji_tlak[0][0]][gornja_donja_temp[0][0]],
                                                    gornja_donja_temp[0][1],gornja_donja_temp[0][0],self.temp)
                                stanje=interpolica1(stanje2,stanje1,gornji_donji_tlak[0][0],
                                                    gornji_donji_tlak[0][1],self.vrijednost_stanje)
        
                            if float(stanje1[1])*1.5<stanje2[1]:
                                if float(self.temp)<float(self.interpol_tabl2(self.vrijednost_stanje)[1][0]):#ako mi je pothlađena kapljevina za neki glupi tlak i temp
                                    if float(self.temp)<float(self.interpol_tabl2(gornji_donji_tlak[0][0])[1][0]):
                                        stanje_za_pom2=self.interpol_tabl2(gornji_donji_tlak[0][0])[1]
                                        stanje2=np.array([stanje_za_pom2[i] for i in [1,3,6]],dtype= object)
                                        stanje2=interpolica1(rijecnik3[gornji_donji_tlak[0][0]][gornja_donja_temp[0][1]],stanje2,
                                                            gornja_donja_temp[0][1],stanje_za_pom2[0],self.temp)
                                        stanje_za_pom1=self.interpol_tabl1(self.temp)[1]
                                        stanje1=np.array([stanje_za_pom1[i] for i in [1,3,6]],dtype= object)
                                        stanje=interpolica1(stanje1,stanje2,
                                                            stanje_za_pom1[0],gornji_donji_tlak[0][0],self.vrijednost_stanje)
            
                                    if float(self.temp)>float(self.interpol_tabl2(gornji_donji_tlak[0][0])[1][0]):
                                        print('NEMOGUCE DA JE TEMPERATURA KONDENZACIJE VECA ZA TLAK %f OD TLAKA %f' %(self.vrijednost_stanje,gornji_donji_tlak[0][0]))
            
                                if float(stanje2[1])*1.5<stanje1[1]:
                                    if float(self.temp)>float(self.interpol_tabl2(self.vrijednost_stanje)[1][0]):
                                        #temp kondenzacje je manja od temperature interpolacije
                                        if float(self.interpol_tabl2(gornji_donji_tlak[0][1])[1][0])>float(gornja_donja_temp[0][1]):
                                            stanje_za_pom2=self.interpol_tabl2(gornji_donji_tlak[0][1])[1]
                                            stanje1=np.array([stanje_za_pom2[i] for i in [2,4,7]],dtype= object)
                                            stanje1=interpolica1(stanje1,rijecnik3[gornji_donji_tlak[0][1]][gornja_donja_temp[0][0]],
                                                                  stanje_za_pom2[0],gornja_donja_temp[0][0],self.temp)
                                            stanje_za_pom1=self.interpol_tabl1(self.temp)[1]
                                            stanje2=np.array([stanje_za_pom1[i] for i in [2,4,7]],dtype= object)
                                            stanje=interpolica1(stanje1,stanje2,
                                                                stanje_za_pom1[0],gornji_donji_tlak[0][1],self.vrijednost_stanje)
                
                                        #temp kond npr za tlak 1 je manja od temp koju trazimo
                                        if float(self.interpol_tabl2(gornji_donji_tlak[0][0])[1][0])<float(self.temp):
                                            stanje_za_pom2=self.interpol_tabl2(gornji_donji_tlak[0][0])[1]
                                            stanje2=np.array([stanje_za_pom2[i] for i in [2,4,7]],dtype= object)
                                            stanje2=interpolica1(stanje2,rijecnik3[gornji_donji_tlak[0][0]][gornja_donja_temp[0][0]],
                                                                stanje_za_pom2[0],gornja_donja_temp[0][0],self.temp)
                                            stanje=interpolica1(stanje1,stanje2,
                                                                gornji_donji_tlak[0][1],gornji_donji_tlak[0][0],self.vrijednost_stanje)
                
                                        #temp.kondenzacije je veca od temp koju trazimo
                                        if float(self.interpol_tabl2(gornji_donji_tlak[0][0])[1][0])>float(self.temp):
                                            stanje_za_pom1=self.interpol_tabl1(self.temp)[1]
                                            stanje2=np.array([stanje_za_pom1[i] for i in [2,4,7]],dtype= object)
                                            stanje=interpolica1(stanje2,stanje1,
                                                                stanje_za_pom1[0],gornji_donji_tlak[0][1],self.vrijednost_stanje)

                        return stanje

        if self.stanja == 'p' and self.temp != None:

            self.temp=str(self.temp)

            self.tlak[self.broj]=self.vrijednost_stanje

            x=tabl3(self.vrijednost_stanje)


            try: 

                if x.all() != None:
                    y=self.interpol_tabl2(self.vrijednost_stanje)[0]#provjera pregrijano ili pothladeno za neki tlak
                    self.volumen[self.broj]= x[0]
                    self.entalpija[self.broj]= x[1]
                    self.entropija[self.broj]= x[2]
                    self.temperatura[self.broj]=self.temp
                    self.mas_ud[self.broj] = mas_udio(x[2],y[6],y[7])

            except AttributeError:
                    pass
            else:
                pass


        elif self.tlak_pom != None and self.temp != None:
                x=tabl3(self.tlak_pom)
                return x

    # def vrati_stanje(self):

    #     return self.lista_stanja

#upisujem sta mi je konstantno, ako imam kondenzaciju onda ako je pothladeno upisujem za tabl 3 tlak i temp
#ako mi ide kond do mas ud=0 upisujem za tabl 2 tlak koji je konst
# obj0=Trazi_tabl(None,None,None)
# lis=obj0.stanja_lista(sve)

# obj=Trazi_tabl(0,'s',3.4)
# obj.interpol_tabl2()

# # 
# obj1=Trazi_tabl(1,'s',7.05395)
# obj1.interpol_tabl2()

# obj2=Trazi_tabl(0,'p',0.23,0.5)
# obj2.interpol_tabl3(70)
# # # 
# obj3=Trazi_tabl(3,'s',7.39924)
# obj3.interpol_tabl2()

# obj4=Trazi_tabl(4,'p', 0.22,0)
# obj4.interpol_tabl2()

# obj5=Trazi_tabl(5,'s', 0.85644)
# obj5.interpol_tabl2()


# print(lis)
# print(sve)

