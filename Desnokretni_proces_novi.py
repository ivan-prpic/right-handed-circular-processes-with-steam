import numpy as np
import sys
import copy

sys.path.append(r'C:/FSB/cetvrta godina/Zavrsni rad/kod_slike_tabl/Kod/Metaklasa1.py')

import Metaklasa1 as Mk


svega=np.array([[['10'],
        ['400'],
        [''],
        [''],
        [''],
        ['']],

        [['0.5'],
        [''],
        [''],
        [''],
        [''],
        ['']],

        [['0.5'],
        [''],
        [''],
        [''],
        [''],
        ['']],

        [['10'],
        [''],
        [''],
        [''],
        [''],
        ['']]],dtype='<U9')

class Desnokretni_proces():
    def __init__(self, sve ,maseni_protok = None):

        self.sve=copy.copy(sve[:])
        self.maseni_protok = maseni_protok
        # self.maseni_protok = 1 if not self.maseni_protok else float(self.maseni_protok)

        global tlak, temperatura, entalpija, entropija, mas_ud, volumen, djeljeni_protok

        tlak=self.sve[:,0]
        temperatura=self.sve[:,1]
        entalpija=self.sve[:,2]
        entropija=self.sve[:,3]
        mas_ud=self.sve[:,4]
        volumen=self.sve[:,5]
        # djeljeni_protok=self.sve[:,6]

        initial_obj= Mk.Trazi_tabl(None,None,None)
        self.stanja = initial_obj.stanja_lista(self.sve)
        self.mas_prot_pom=maseni_protok

    def Pocetno_stanje(self, broj, topl_tok = None, mas_prot = None):


        if tlak[broj] and temperatura[broj]:

            poc_obj = Mk.Trazi_tabl(broj,'p', tlak[broj][0])
            poc_obj.interpol_tabl3(temperatura[broj][0])

        elif tlak[broj] and mas_ud[broj] and not temperatura[broj]:

              poc_obj = Mk.Trazi_tabl(broj,'p', tlak[broj][0], mas_ud[broj][0])
              poc_obj.interpol_tabl2()

        elif temperatura[broj] and mas_ud[broj] and not tlak[broj]:

              poc_obj = Mk.Trazi_tabl(broj,'T', temperatura[broj][0], mas_ud[broj][0])
              poc_obj.interpol_tabl1()

        elif tlak[broj] and temperatura[broj] and mas_ud[broj]:

              poc_obj = Mk.Trazi_tabl(broj,'p', tlak[broj][0], mas_ud[broj][0])
              poc_obj.interpol_tabl3(temperatura[broj][0])
 
        elif tlak[broj] and entalpija[broj] or temperatura[broj] and entalpija[broj]:

            poc_obj = Mk.Trazi_tabl(broj,'h', entalpija[broj][0])
            poc_obj.interpol_tabl2()

        elif tlak[broj] and entropija[broj] or temperatura[broj] and entropija[broj]:

            poc_obj = Mk.Trazi_tabl(broj,'s', entropija[broj][0])
            poc_obj.interpol_tabl2()

        else:
            pass

        return [self.stanja, topl_tok, mas_prot]
    def Kotao(self, broj, topl_tok = None, mas_prot = None):
        self.topl_tok_kotao = topl_tok

        if self.stanja[broj-1][0] and not self.stanja[broj][0]:
            self.stanja[broj][0] = self.stanja[broj-1][0]
            self.sve[broj-1][0] = self.stanja[broj-1][0]
            self.sve[broj][0] = self.stanja[broj-1][0]


        if self.stanja[broj][0] and not self.stanja[broj-1][0]:
            self.stanja[broj-1][0] = self.stanja[broj][0]
            self.sve[broj-1][0] = self.stanja[broj-1][0]
            self.sve[broj-1][0] = self.stanja[broj][0]

        if not entalpija[broj] and not entalpija[broj-1]:
            pass
        if not self.stanja[broj][2] and not self.stanja[broj-1][2]:
            pass

        self.izracunaj_stanje(broj)

        if self.stanja[broj-1][0] and not self.stanja[broj][0]:
            self.stanja[broj][0] = self.stanja[broj-1][0]
            self.sve[broj-1][0] = self.stanja[broj-1][0]
            self.sve[broj][0] = self.stanja[broj-1][0]


        if self.stanja[broj][0] and not self.stanja[broj-1][0]:
            self.stanja[broj-1][0] = self.stanja[broj][0]
            self.sve[broj-1][0] = self.stanja[broj-1][0]
            self.sve[broj-1][0] = self.stanja[broj][0]

        if not entalpija[broj] and not entalpija[broj-1]:
            pass
        if not self.stanja[broj][2] and not self.stanja[broj-1][2]:
            pass

        self.izracunaj_stanje(broj-1)

        if np.array_equal(self.stanja[broj],self.sve[broj]):
            if np.array_equal(self.stanja[broj-1],self.sve[broj-1]):
                print('Nemogu izracunati trenutno stanje, niti znam prošlo stanje')
                return [self.stanja, topl_tok, self.mas_prot_pom]
            else:
                if topl_tok:
                    if self.mas_prot_pom:
                        h1 = float(self.stanja[broj-1][2])
                        h2 = float(topl_tok)/float(self.mas_prot_pom)+h1
                        entalpija[broj][0] = str(h2)
                        self.izracunaj_stanje(broj)
                        return [self.stanja, topl_tok, self.mas_prot_pom]
                    if not self.mas_prot_pom:
                        print('nemam maseni protok, pretpostavaljam da je topl_tok u kJ/kg')
                        h1 = float(self.stanja[broj-1][2])
                        h2 = float(topl_tok)+h1
                        entalpija[broj][0] = str(h2)
                        self.izracunaj_stanje(broj)
                        return [self.stanja, topl_tok, self.mas_prot_pom]
                if not topl_tok:
                    print('Neznam sadasnje stanje, niti topl_tok')
                    return [self.stanja, topl_tok, self.mas_prot_pom]
        else:
            if np.array_equal(self.stanja[broj-1],self.sve[broj-1]):
                if topl_tok:
                    if self.mas_prot_pom:
                        h2 = float(self.stanja[broj][2])
                        h1 = h2 - float(topl_tok)/float(self.mas_prot_pom)
                        entalpija[broj-1][0] = str(h1)
                        self.izracunaj_stanje(broj-1)
                        self.Kompresija(broj-1,self.snaga_komp)
                        return [self.stanja,topl_tok, self.mas_prot_pom]
                    if not self.mas_prot_pom:
                        print('racunam proslo stanje, pretpostavljam da je topl_tok u kJ/kg')
                        h2 = float(self.stanja[broj][2])
                        h1 = h2 - float(topl_tok)
                        entalpija[broj-1][0] = str(h1)
                        self.izracunaj_stanje(broj-1)
                        self.Kompresija(broj-1,self.snaga_komp)
                        return [self.stanja, topl_tok, self.mas_prot_pom]
                if not topl_tok:
                    print('Neznam prošlo stanje, niti topl_tok')
                    return [self.stanja, topl_tok, mas_prot]
            else:
                if topl_tok:
                    if self.mas_prot_pom:
                        h2 = float(self.stanja[broj][2])
                        h1 = float(self.stanja[broj-1][2])
                        mas_prot_pom = float(topl_tok)/(h2-h1)
                        if mas_prot_pom == self.mas_prot_pom:
                            mas_prot=mas_prot_pom
                            return [self.stanja, topl_tok, mas_prot]
                        else:
                            print('ERROR maseni protoci nisu isti!!!!!, vjv je krivi topl_tok')
                            topl_tok = float(self.mas_prot_pom)*(h2-h1)
                            return [self.stanja, topl_tok, self.mas_prot_pom]
                    if not self.mas_prot_pom:
                        h2 = float(self.stanja[broj][2])
                        h1= float(self.stanja[broj-1][2])
                        mas_prot_pom = float(topl_tok)/(h2-h1)
                        self.mas_prot_pom = mas_prot_pom
                        mas_prot=mas_prot_pom
                        return [self.stanja, topl_tok, mas_prot]
                if not topl_tok:
                    if self.mas_prot_pom:
                        h2 = float(self.stanja[broj][2])
                        h1= float(self.stanja[broj-1][2])
                        topl_tok = float(self.mas_prot_pom)*(h2-h1)
                        return [self.stanja, topl_tok, self.mas_prot_pom]
                    if not self.mas_prot_pom:
                        print('topl_tok je u kJ/kg, jer neznam maseni protok')
                        h2 = float(self.stanja[broj][2])
                        h1= float(self.stanja[broj-1][2])
                        topl_tok = (h2-h1)
                        return [self.stanja, topl_tok, self.mas_prot_pom]

    def izracunaj_stanje(self,broj):

        if tlak[broj]:
            if temperatura[broj]:
                poc_obj = Mk.Trazi_tabl(broj,'p', tlak[broj][0])
                poc_obj.interpol_tabl3(temperatura[broj][0])

            if temperatura[broj] and mas_ud[broj]:
                poc_obj = Mk.Trazi_tabl(broj,'p', tlak[broj][0], mas_ud[broj][0])
                poc_obj.interpol_tabl3(temperatura[broj][0])

            if mas_ud[broj]:
                poc_obj = Mk.Trazi_tabl(broj,'p', tlak[broj][0], mas_ud[broj][0])
                poc_obj.interpol_tabl2()

            if entalpija[broj] and not entropija[broj]:
                poc_obj = Mk.Trazi_tabl(broj,'h', entalpija[broj][0])
                poc_obj.interpol_tabl2()

            if entropija[broj] and not entalpija[broj]:
                poc_obj = Mk.Trazi_tabl(broj,'s', entropija[broj][0])
                poc_obj.interpol_tabl2()

        if temperatura[broj]:
            if mas_ud[broj]:
                poc_obj = Mk.Trazi_tabl(broj,'T', temperatura[broj][0], mas_ud[broj][0])
                poc_obj.interpol_tabl1()

        return self.stanja[broj]

    def Ekspanzija(self,broj,snaga=None,mas_prot=None):

        self.snaga_eksp=snaga

        if self.stanja[broj-1][3] and not self.stanja[broj][3]:
            self.stanja[broj][3] = self.stanja[broj-1][3]
            self.sve[broj-1][3] = self.stanja[broj-1][3]
            self.sve[broj][3] = self.stanja[broj-1][3]


        if self.stanja[broj][3] and not self.stanja[broj-1][3]:
            self.stanja[broj-1][3] = self.stanja[broj][3]
            self.sve[broj-1][3] = self.stanja[broj-1][3]
            self.sve[broj-1][3] = self.stanja[broj][3]

        if not entropija[broj] and not entropija[broj-1]:
            pass
        if not self.stanja[broj][3] and not self.stanja[broj-1][3]:
            pass

        self.izracunaj_stanje(broj)

        if self.stanja[broj-1][3] and not self.stanja[broj][3]:
            self.stanja[broj][3] = self.stanja[broj-1][3]
            self.sve[broj-1][3] = self.stanja[broj-1][3]
            self.sve[broj][3] = self.stanja[broj-1][3]


        if self.stanja[broj][3] and not self.stanja[broj-1][3]:
            self.stanja[broj-1][3] = self.stanja[broj][3]
            self.sve[broj-1][3] = self.stanja[broj-1][3]
            self.sve[broj-1][3] = self.stanja[broj][3]

        if not entropija[broj] and not entropija[broj-1]:
            pass
        if not self.stanja[broj][3] and not self.stanja[broj-1][3]:
            pass

        self.izracunaj_stanje(broj-1)

        if np.array_equal(self.stanja[broj],self.sve[broj]):
            if np.array_equal(self.stanja[broj-1],self.sve[broj-1]):
                print('Nemogu izracunati trenutno stanje, niti znam prošlo stanje')
                return [self.stanja, snaga, self.mas_prot_pom]
            else:
                if snaga:
                    if self.mas_prot_pom:
                        h1 = float(self.stanja[broj-1][2])
                        h2 = h1 - float(snaga)/float(self.mas_prot_pom)
                        self.stanja[broj][2] = str(h2)
                        self.izracunaj_stanje(broj)
                        return [self.stanja, snaga, self.mas_prot_pom]
                    if not self.mas_prot_pom:
                        print('nemam maseni protok, pretpostavaljam da je snaga u kJ/kg')
                        h1 = float(self.stanja[broj-1][2])
                        h2 = h1 - float(snaga)
                        self.stanja[broj][2] = str(h2)
                        self.izracunaj_stanje(broj)
                        return [self.stanja, snaga, self.mas_prot_pom]
                if not snaga:
                    print('Neznam sadasnje stanje, niti snagu')
                    return [self.stanja, snaga, self.mas_prot_pom]
        else:
            if np.array_equal(self.stanja[broj-1],self.sve[broj-1]):
                if snaga:
                    if self.mas_prot_pom:
                        h2 = float(self.stanja[broj][2])
                        h1 = float(snaga)/float(self.mas_prot_pom) +h2
                        self.stanja[broj-1][2] = str(h1)
                        self.izracunaj_stanje(broj-1)
                        return [self.stanja, snaga, self.mas_prot_pom]
                    if not self.mas_prot_pom:
                        print('racunam proslo stanje, pretpostavljam da je snaga u kJ/kg')
                        h2 = float(self.stanja[broj][2])
                        h1 = float(snaga) + h2
                        self.stanja[broj-1][2] = str(h1)
                        self.izracunaj_stanje(broj-1)
                        return [self.stanja, snaga, self.mas_prot_pom]
                if not snaga:
                    print('Neznam prošlo stanje, niti snagu')
                    return [self.stanja, snaga, mas_prot]
            else:
                if snaga:
                    if self.mas_prot_pom:
                        h2 = float(self.stanja[broj][2])
                        h1 = float(self.stanja[broj-1][2])
                        mas_prot_pom = float(snaga)/(h1-h2)
                        if mas_prot_pom == self.mas_prot_pom:
                            mas_prot=mas_prot_pom
                            return [self.stanja, snaga, mas_prot]
                        else:
                            print('ERROR maseni protoci nisu isti!!!!!, vjv je kriva snaga')
                            snaga= float(self.mas_prot_pom)*(h1-h2)
                            return [self.stanja, snaga, self.mas_prot_pom]
                    if not self.mas_prot_pom:
                        h2 = float(self.stanja[broj][2])
                        h1= float(self.stanja[broj-1][2])
                        mas_prot_pom = float(snaga)/(h1-h2)
                        self.mas_prot_pom = mas_prot_pom
                        mas_prot=mas_prot_pom
                        return [self.stanja, snaga, mas_prot]
                if not snaga:
                    if self.mas_prot_pom:
                        h2 = float(self.stanja[broj][2])
                        h1= float(self.stanja[broj-1][2])
                        snaga = float(self.mas_prot_pom)*(h1-h2)
                        return [self.stanja, snaga,self.mas_prot_pom]
                    if not self.mas_prot_pom:
                        print('snaga je u kJ/kg, jer neznam maseni protok')
                        h2 = float(self.stanja[broj][2])
                        h1= float(self.stanja[broj-1][2])
                        snaga = (h1-h2)
                        return [self.stanja,snaga,self.mas_prot_pom]


    def Pregrijavanje(self, broj, topl_tok = None, mas_prot = None):

        if topl_tok:

            if mas_prot:
                h1 = self.stanja[broj-1][2]
                h2 = float(h1) + float(topl_tok)/float(mas_prot)
                eks_obj=Mk.Trazi_tabl(broj,'h', h2)
                eks_obj.interpol_tabl2()

            if not mas_prot:
                h1 = self.stanja[broj-1][2]
                h2 = float(h1) + float(topl_tok)/float(self.maseni_protok)
                mas_prot = float(topl_tok)/(float(h2) - float(h1))
                eks_obj=Mk.Trazi_tabl(broj,'h', h2)
                eks_obj.interpol_tabl2()

        if not topl_tok:

            tlak[broj] = self.stanja[broj-1][0]
            self.stanja[broj][0]=self.stanja[broj-1][0]
 
            if temperatura[broj]:

                preg_obj=Mk.Trazi_tabl(broj,'p', tlak[broj][0])
                preg_obj.interpol_tabl3(temperatura[broj][0])

            if entropija[broj] and not temperatura[broj]:

                preg_obj=Mk.Trazi_tabl(broj,'s', entropija[broj][0])
                preg_obj.interpol_tabl2()

            if entalpija[broj] and not temperatura[broj]:

                preg_obj=Mk.Trazi_tabl(broj,'h', entalpija[broj][0])
                preg_obj.interpol_tabl2()

            if mas_prot:
                topl_tok = float(mas_prot)*(float(self.stanja[broj][2]) - float(self.stanja[broj-1][2]))
            if not mas_prot:
                topl_tok = float(self.maseni_protok)*(float(self.stanja[broj][2]) - float(self.stanja[broj-1][2]))
                mas_prot = float(topl_tok)/(float(self.stanja[broj][2]) - float(self.stanja[broj-1][2]))

        return [self.stanja, topl_tok, mas_prot]

    def Kondenzacija(self, broj, topl_tok = None, mas_prot = None):

        self.topl_tok_kond = topl_tok
        if self.stanja[broj-1][0] and not self.stanja[broj][0]:
            self.stanja[broj][0] = self.stanja[broj-1][0]
            self.sve[broj-1][0] = self.stanja[broj-1][0]
            self.sve[broj][0] = self.stanja[broj-1][0]


        if self.stanja[broj][0] and not self.stanja[broj-1][0]:
            self.stanja[broj-1][0] = self.stanja[broj][0]
            self.sve[broj-1][0] = self.stanja[broj-1][0]
            self.sve[broj-1][0] = self.stanja[broj][0]

        if not entalpija[broj] and not entalpija[broj-1]:
            pass
        if not self.stanja[broj][2] and not self.stanja[broj-1][2]:
            pass

        self.izracunaj_stanje(broj)

        if self.stanja[broj-1][0] and not self.stanja[broj][0]:
            self.stanja[broj][0] = self.stanja[broj-1][0]
            self.sve[broj-1][0] = self.stanja[broj-1][0]
            self.sve[broj][0] = self.stanja[broj-1][0]


        if self.stanja[broj][0] and not self.stanja[broj-1][0]:
            self.stanja[broj-1][0] = self.stanja[broj][0]
            self.sve[broj-1][0] = self.stanja[broj-1][0]
            self.sve[broj-1][0] = self.stanja[broj][0]

        if not entalpija[broj] and not entalpija[broj-1]:
            pass
        if not self.stanja[broj][2] and not self.stanja[broj-1][2]:
            pass

        self.izracunaj_stanje(broj-1)

        if np.array_equal(self.stanja[broj],self.sve[broj]):
            if np.array_equal(self.stanja[broj-1],self.sve[broj-1]):
                print('Nemogu izracunati trenutno stanje, niti znam prošlo stanje')
                return [self.stanja, topl_tok, self.mas_prot_pom]
            else:
                if topl_tok:
                    if self.mas_prot_pom:
                        h1 = float(self.stanja[broj-1][2])
                        h2 = float(topl_tok)/float(self.mas_prot_pom)+h1
                        entalpija[broj][0] = str(h2)
                        self.izracunaj_stanje(broj)
                        return [self.stanja, topl_tok, self.mas_prot_pom]
                    if not self.mas_prot_pom:
                        print('nemam maseni protok, pretpostavaljam da je topl_tok u kJ/kg')
                        h1 = float(self.stanja[broj-1][2])
                        h2 = float(topl_tok)+h1
                        entalpija[broj][0] = str(h2)
                        self.izracunaj_stanje(broj)
                        return [self.stanja, topl_tok, self.mas_prot_pom]
                if not topl_tok:
                    print('Neznam sadasnje stanje, niti topl_tok')
                    return [self.stanja, topl_tok, self.mas_prot_pom]
        else:
            if np.array_equal(self.stanja[broj-1],self.sve[broj-1]):
                if topl_tok:
                    if self.mas_prot_pom:
                        h2 = float(self.stanja[broj][2])
                        h1 = h2 - float(topl_tok)/float(self.mas_prot_pom)
                        entalpija[broj-1][0] = str(h1)
                        self.izracunaj_stanje(broj-1)
                        self.Ekspanzija(broj-1,self.snaga_eksp)
                        return [self.stanja,topl_tok, self.mas_prot_pom]
                    if not self.mas_prot_pom:
                        print('racunam proslo stanje, pretpostavljam da je topl_tok u kJ/kg')
                        h2 = float(self.stanja[broj][2])
                        h1 = h2 - float(topl_tok)
                        entalpija[broj-1][0] = str(h1)
                        self.izracunaj_stanje(broj-1)
                        self.Ekspanzija(broj-1,self.snaga_eksp)
                        return [self.stanja, topl_tok, self.mas_prot_pom]
                if not topl_tok:
                    print('Neznam prošlo stanje, niti topl_tok')
                    return [self.stanja, topl_tok, mas_prot]
            else:
                if topl_tok:
                    if self.mas_prot_pom:
                        h2 = float(self.stanja[broj][2])
                        h1 = float(self.stanja[broj-1][2])
                        mas_prot_pom = float(topl_tok)/(h2-h1)
                        if mas_prot_pom == self.mas_prot_pom:
                            mas_prot=mas_prot_pom
                            return [self.stanja, topl_tok, mas_prot]
                        else:
                            print('ERROR maseni protoci nisu isti!!!!!, vjv je krivi topl_tok')
                            topl_tok = float(self.mas_prot_pom)*(h2-h1)
                            return [self.stanja, topl_tok, self.mas_prot_pom]
                    if not self.mas_prot_pom:
                        h2 = float(self.stanja[broj][2])
                        h1= float(self.stanja[broj-1][2])
                        mas_prot_pom = float(topl_tok)/(h2-h1)
                        self.mas_prot_pom = mas_prot_pom
                        mas_prot=mas_prot_pom
                        return [self.stanja, topl_tok, mas_prot]
                if not topl_tok:
                    if self.mas_prot_pom:
                        h2 = float(self.stanja[broj][2])
                        h1= float(self.stanja[broj-1][2])
                        topl_tok = float(self.mas_prot_pom)*(h2-h1)
                        return [self.stanja, topl_tok, self.mas_prot_pom]
                    if not self.mas_prot_pom:
                        print('topl_tok je u kJ/kg, jer neznam maseni protok')
                        h2 = float(self.stanja[broj][2])
                        h1= float(self.stanja[broj-1][2])
                        topl_tok = (h2-h1)
                        return [self.stanja, topl_tok, self.mas_prot_pom]


    def Kompresija(self, broj, snaga = None, mas_prot= None):

        self.snaga_komp=snaga

        if self.stanja[broj-1][3] and not self.stanja[broj][3]:
            self.stanja[broj][3] = self.stanja[broj-1][3]
            self.sve[broj-1][3] = self.stanja[broj-1][3]
            self.sve[broj][3] = self.stanja[broj-1][3]


        if self.stanja[broj][3] and not self.stanja[broj-1][3]:
            self.stanja[broj-1][3] = self.stanja[broj][3]
            self.sve[broj-1][3] = self.stanja[broj-1][3]
            self.sve[broj-1][3] = self.stanja[broj][3]

        if not entropija[broj] and not entropija[broj-1]:
            pass
        if not self.stanja[broj][3] and not self.stanja[broj-1][3]:
            pass

        self.izracunaj_stanje(broj)

        if self.stanja[broj-1][3] and not self.stanja[broj][3]:
            self.stanja[broj][3] = self.stanja[broj-1][3]
            self.sve[broj-1][3] = self.stanja[broj-1][3]
            self.sve[broj][3] = self.stanja[broj-1][3]


        if self.stanja[broj][3] and not self.stanja[broj-1][3]:
            self.stanja[broj-1][3] = self.stanja[broj][3]
            self.sve[broj-1][3] = self.stanja[broj-1][3]
            self.sve[broj-1][3] = self.stanja[broj][3]

        if not entropija[broj] and not entropija[broj-1]:
            pass
        if not self.stanja[broj][3] and not self.stanja[broj-1][3]:
            pass


        if np.array_equal(self.stanja[broj],self.sve[broj]):
            if np.array_equal(self.stanja[broj-1],self.sve[broj-1]):
                print('Nemogu izracunati trenutno stanje, niti znam prošlo stanje')
                return [self.stanja, snaga, self.mas_prot_pom]
            else:
                if snaga:
                    if self.mas_prot_pom:
                        h1 = float(self.stanja[broj-1][2])
                        h2 = h1 - float(snaga)/float(self.mas_prot_pom)
                        self.stanja[broj][2] = str(h2)
                        self.izracunaj_stanje(broj)
                        return [self.stanja, snaga, self.mas_prot_pom]
                    if not self.mas_prot_pom:
                        print('nemam maseni protok, pretpostavaljam da je snaga u kJ/kg')
                        h1 = float(self.stanja[broj-1][2])
                        h2 = h1 - float(snaga)
                        self.stanja[broj][2] = str(h2)
                        self.izracunaj_stanje(broj)
                        return [self.stanja, snaga, self.mas_prot_pom]
                if not snaga:
                    print('Neznam sadasnje stanje, niti snagu')
                    return [self.stanja, snaga, self.mas_prot_pom]
        else:
            if np.array_equal(self.stanja[broj-1],self.sve[broj-1]):
                if snaga:
                    if self.mas_prot_pom:
                        h2 = float(self.stanja[broj][2])
                        h1 = float(snaga)/float(self.mas_prot_pom) +h2
                        self.stanja[broj-1][2] = str(h1)
                        self.izracunaj_stanje(broj-1)
                        self.Kondenzacija(broj-1,self.topl_tok_kond)
                        return [self.stanja, snaga, self.mas_prot_pom]
                    if not self.mas_prot_pom:
                        print('racunam proslo stanje, pretpostavljam da je snaga u kJ/kg')
                        h2 = float(self.stanja[broj][2])
                        h1 = float(snaga) + h2
                        self.stanja[broj-1][2] = str(h1)
                        self.izracunaj_stanje(broj-1)
                        self.Kondenzacija(broj-1,self.topl_tok_kond)
                        return [self.stanja, snaga, self.mas_prot_pom]
                if not snaga:
                    print('Neznam prošlo stanje, niti snagu')
                    return [self.stanja, snaga, mas_prot]
            else:
                if snaga:
                    if self.mas_prot_pom:
                        h2 = float(self.stanja[broj][2])
                        h1 = float(self.stanja[broj-1][2])
                        mas_prot_pom = float(snaga)/(h1-h2)
                        if mas_prot_pom == self.mas_prot_pom:
                            mas_prot=mas_prot_pom
                            return [self.stanja, snaga, mas_prot]
                        else:
                            print('ERROR maseni protoci nisu isti!!!!!, vjv je kriva snaga')
                            snaga= float(self.mas_prot_pom)*(h1-h2)
                            return [self.stanja, snaga, self.mas_prot_pom]
                    if not self.mas_prot_pom:
                        h2 = float(self.stanja[broj][2])
                        h1= float(self.stanja[broj-1][2])
                        mas_prot_pom = float(snaga)/(h1-h2)
                        self.mas_prot_pom = mas_prot_pom
                        mas_prot=mas_prot_pom
                        return [self.stanja, snaga, mas_prot]
                if not snaga:
                    if self.mas_prot_pom:
                        h2 = float(self.stanja[broj][2])
                        h1= float(self.stanja[broj-1][2])
                        snaga = float(self.mas_prot_pom)*(h1-h2)
                        return [self.stanja, snaga,self.mas_prot_pom]
                    if not self.mas_prot_pom:
                        print('snaga je u kJ/kg, jer neznam maseni protok')
                        h2 = float(self.stanja[broj][2])
                        h1= float(self.stanja[broj-1][2])
                        snaga = (h1-h2)
                        return [self.stanja,snaga,self.mas_prot_pom]

    def Provjeri(self,broj,lista):
        if self.mas_prot_pom != None:
            pass
        else:
            self.mas_prot_pom = 1
        vrijednosti=[]
        vrijednosti_mas_prot=[]
        lista[1] = lista[1] if lista[1] != None else 0.0001
        for i in range(np.shape(self.stanja)[0]):
            pom_jed = self.mas_prot_pom*(float(self.stanja[i][2])-float(self.stanja[i-1][2]))
            vrijednosti.append(pom_jed)
        if abs(lista[1]) == abs(vrijednosti[broj]):
            pass
        else:
            if broj == 0:
                vrijednosti[broj] = abs(vrijednosti[broj])
            if broj == 1:
                vrijednosti[broj] = abs(vrijednosti[broj])
            if broj == 2:
                vrijednosti[broj] = -abs(vrijednosti[broj])
            if broj == 3:
                vrijednosti[broj] = -abs(vrijednosti[broj])
            lista[1] = float(vrijednosti[broj])

        if lista[2] != self.mas_prot_pom:
            lista[2]=self.mas_prot_pom

    def Prigusivanje(self,broj):
        entalpija[broj] = self.stanja[broj-1][2]

        if tlak[broj] and entalpija[broj]:

            prig_obj=Mk.Trazi_tabl(broj,'h', entalpija[broj][0])
            prig_obj.interpol_tabl2()

        if tlak[broj] and mas_ud[broj] and not entalpija[broj]:

            prig_obj=Mk.Trazi_tabl(broj,'p', tlak[broj][0], mas_ud[broj][0])
            prig_obj.interpol_tabl2()

        if tlak[broj] and temperatura[broj] and mas_ud[broj] and not entalpija[broj]:

            prig_obj=Mk.Trazi_tabl(broj,'p', tlak[broj][0], mas_ud[broj][0])
            prig_obj.interpol_tabl2(temperatura[broj][0])

        return self.stanja

    def Eskpanzija_s_trenjem(self,broj = None ,eta=None, h_2_stvarno = None, mas_prot = None):

        if eta != None and broj != None:
            stanje_idealno=self.Ekspanzija(broj)[broj][:]
            h_2_idealno=stanje_idealno[2]
            h_1 = self.stanja[broj-1][2]
            h_2_stvarno = str(float(h_1) - float(eta)*(float(h_1)-float(h_2_idealno)))
            eks_s_trenjem=Mk.Trazi_tabl(broj,'h', h_2_stvarno)
            eks_s_trenjem.interpol_tabl2()
            if mas_prot:
                snaga = float(mas_prot)*(float(self.stanja[broj-1][2]) - float(h_2_stvarno))
            if not mas_prot:
                snaga = float(self.maseni_protok)*(float(self.stanja[broj-1][2]) - float(h_2_stvarno))
                mas_prot = -float(snaga)/(float(h_2_stvarno) - float(self.stanja[broj-1][2]))
            return self.stanja, snaga, mas_prot

        if eta == None and h_2_stvarno != None and broj == None:
            h_1 = self.stanja[broj-1][2]
            h_2_idealno = self.stanje[broj][2]
            eta = (float(h_1) - float(h_2_stvarno))/(float(h_1) - float(h_2_idealno))
            eks_s_trenjem=Mk.Trazi_tabl(broj,'h', float(h_2_stvarno))
            eks_s_trenjem.interpol_tabl2()
            if mas_prot:
                snaga = float(mas_prot)*(float(self.stanja[broj-1][2]) - float(h_2_stvarno))
            if not mas_prot:
                snaga = float(self.maseni_protok)*(float(self.stanja[broj-1][2]) - float(h_2_stvarno))
                mas_prot = -float(snaga)/(float(h_2_stvarno) - float(self.stanja[broj-1][2]))
            return self.stanja, snaga, mas_prot, eta

    def Kompresija_s_trenjem(self, broj = None, eta = None, h_2_stvarno = None, mas_prot = None):

        if eta != None and broj != None:
            stanje_idealno=self.Kompresija(broj)[broj][:]
            h_2_idealno=stanje_idealno[2]
            h_1 = self.stanja[broj-1][2]
            h_2_stvarno = str(float(h_1) - (float(h_1)-float(h_2_idealno))/float(eta))
            kom_s_trenjem=Mk.Trazi_tabl(broj,'h', h_2_stvarno)
            kom_s_trenjem.interpol_tabl2()
            if mas_prot:
                snaga = float(mas_prot)*(float(self.stanja[broj-1][2]) - float(self.stanja[broj][2]))
            if not mas_prot:
                snaga = float(self.maseni_protok)*(float(self.stanja[broj-1][2]) - float(h_2_stvarno))
                mas_prot = float(snaga)/(float(self.stanja[broj-1][2]) - float(h_2_stvarno))
            return self.stanja

        if eta == None and h_2_stvarno != None and broj == None:
            h_1 = self.stanja[broj-1][2]
            h_2_idealno = self.stanje[broj][2]
            eta = (float(h_1) - float(h_2_idealno))/(float(h_1) - float(h_2_stvarno))
            kom_s_trenjem=Mk.Trazi_tabl(broj,'h', float(h_2_stvarno))
            kom_s_trenjem.interpol_tabl2()
            if mas_prot:
                snaga = float(mas_prot)*(float(self.stanja[broj-1][2]) - float(self.stanja[broj][2]))
            if not mas_prot:
                snaga = float(self.maseni_protok)*(float(self.stanja[broj-1][2]) - float(h_2_stvarno))
                mas_prot = float(snaga)/(float(self.stanja[broj-1][2]) - float(h_2_stvarno))
            return self.stanja, snaga, mas_prot, eta

    def Strujanje_s_trenjem(self, broj = None, h2 = None, topl_tok = None):

        if topl_tok != None and broj != None and h2 == None:
            if float(topl_tok) == 0:
                self.Pigusivanje(broj)

            if 0< float(topl_tok) or float(topl_tok) > 0:

                h1 = self.stanja[broj-1][2]
                h2 = str(float(topl_tok) - float(h1))
                struj_s_trenj_obj=Mk.Trazi_tabl(broj,'h', h2)
                struj_s_trenj_obj.interpol_tabl2()

            return self.stanja

        if topl_tok == None and h2 != None:
            topl_tok = self.maseni_protok*(float(h2) - float(h1))
            struj_s_trenj_obj=Mk.Trazi_tabl(broj,'h', float(h2))
            struj_s_trenj_obj.interpol_tabl2()
            return topl_tok

    # def Izmjenjivac_topl(self, broj_topl = None, broj_hlad = None, temperatura=None,
    #       mas_ud2 = None, topl_tok = None, maseni_protok1 = None, maseni_protok2 = None):
    #     broj1 = broj_topl
    #     broj2 = broj_hlad
        # slucaji:
            #1. Znam koji topl tok se izmjenjuje između struja
            #2. Znam mas_ud na koji se hladnija grije
            #3. Znam temperaturu na koju se toplija hladi, ali mi mora biti pothlađena kapljevina na izlazu
            #4. Znam temperaturu na koju se hladnija grije




# obj=Desnokretni_proces(svega,2)

# lis3=obj.Kompresija(3)
# lis=obj.Kotao(0,6000)
# lis1=obj.Ekspanzija(1)
# lis2=obj.Kondenzacija(2)
# lis3=obj.Kompresija(3)

# obj.Provjeri(0,lis)
# obj.Provjeri(1,lis1)
# obj.Provjeri(2,lis2)
# obj.Provjeri(3,lis3)


# lis=obj.Pocetno_stanje(0)
# lis2=obj.Ekspanzija(1,600)
# # lis2=obj.Eskpanzija_s_trenjem(1,0.7)
# lis3=obj.Pregrijavanje(2)
# lis4=obj.Ekspanzija(21)
# print(lis4)
# lis5=obj.Kondenzacija(2,-1000)
# # print(lis5)
# lis6=obj.Kompresija(3)



    # def Ekspanzija(self, broj, snaga = None, mas_prot = None):

    #     self.snaga_eks=snaga

    #     if self.stanja[broj-1][3]:
    #         entropija[broj] = self.stanja[broj-1][3]

    #     if tlak[broj] and entropija[broj] and not mas_ud[broj]:
    
    #             eks_obj=Mk.Trazi_tabl(broj,'s', entropija[broj][0])
    #             eks_obj.interpol_tabl2()
    
    #     if tlak[broj] and mas_ud[broj] and not entropija[broj]:
    #         if 0<float(mas_ud[broj])<=1:
    #             eks_obj=Mk.Trazi_tabl(broj,'p', tlak[broj][0], mas_ud[broj][0])
    #             eks_obj.interpol_tabl2()
    #         else:
    #             print('trebam znati entropiju da mi ekspanidra u homogoeno podrucije')
    
    #     if tlak[broj] and temperatura[broj] and not entropija[broj]:
    #         eks_obj=Mk.Trazi_tabl(broj,'p', tlak[broj][0])
    #         eks_obj.interpol_tabl3(temperatura[broj][0])

    #     if tlak[broj] and mas_ud[broj] and not entropija[broj]:
    #         if 0<float(mas_ud[broj])<=1 and temperatura[broj]:
    #             eks_obj=Mk.Trazi_tabl(broj,'p', tlak[broj][0] , mas_ud[broj][0])
    #             eks_obj.interpol_tabl3(temperatura[broj][0])
    #         else:
    #             eks_obj=Mk.Trazi_tabl(broj,'p', tlak[broj][0],mas_ud[broj][0])
    #             eks_obj.interpol_tabl3()

    #     if tlak[broj] and entalpija[broj]:
    #             eks_obj=Mk.Trazi_tabl(broj,'h', entalpija[broj][0])
    #             eks_obj.interpol_tabl2()

    #     if self.stanja[broj][3] and tlak[broj-1] and not entropija[broj-1]:
    #         self.stanja[broj-1][3] = self.stanja[broj][3]
    #         eks_obj=Mk.Trazi_tabl(broj-1,'s', float(self.stanja[broj][3][0]))
    #         eks_obj.interpol_tabl2()

    #     if snaga:
    #         if mas_prot:
    #             pass

    #         if not mas_prot:
    #             try:
    #                 h1 = self.stanja[broj-1][2]
    #                 h2 = self.stanja[broj][2]
    #                 mas_prot = float(snaga)/(float(h1) - float(h2))
    #                 self.mas_prot_pom=mas_prot
    #             except ValueError:
    #                 print('lalala')

    #     if not snaga:
    #         if mas_prot:
    #             try:
    #                 snaga = float(mas_prot)*(float(self.stanja[broj-1][2]) - float(self.stanja[broj][2]))
    #             except ValueError:
    #                 pass
    #         if not mas_prot:
    #             try:
    #                 snaga = float(self.maseni_protok)*(float(self.stanja[broj-1][2]) - float(self.stanja[broj][2]))
    #                 mas_prot = -float(snaga)/(float(self.stanja[broj][2]) - float(self.stanja[broj-1][2]))
    #             except ValueError:
    #                 pass
    #     else:
    #         pass

    #     return [self.stanja, snaga, mas_prot]

    # def Kondenzacija(self, broj, topl_tok = None, mas_prot = None):
    #     mas_prot=self.mas_prot_pom if mas_prot == None else mas_prot
    #     x = None

    #     if self.stanja[broj-1][0] and not self.stanja[broj][0]:
    #         self.stanja[broj][0] = self.stanja[broj-1][0]
    #         tlak[broj] = self.stanja[broj-1][0]

    #     if self.stanja[broj][0] and not self.stanja[broj-1][0]:
    #         self.stanja[broj-1][0] = self.stanja[broj][0]
    #         tlak[broj-1] = self.stanja[broj][0]

    #     if tlak[broj] and mas_ud[broj] and not temperatura[broj]:

    #         kond_obj=Mk.Trazi_tabl(broj,'p', tlak[broj][0], mas_ud[broj][0])
    #         kond_obj.interpol_tabl2()

    #     if tlak[broj] and temperatura[broj] and not mas_ud[broj]:

    #         kond_obj=Mk.Trazi_tabl(broj,'p', tlak[broj][0])
    #         kond_obj.interpol_tabl3(temperatura[broj][0])

    #     if tlak[broj] and temperatura[broj] and mas_ud[broj]:

    #         if float(mas_ud[broj])<0:
    #             kond_obj=Mk.Trazi_tabl(broj,'p', tlak[broj][0])
    #             kond_obj.interpol_tabl3(temperatura[broj][0])
    #         else:
    #             kond_obj=Mk.Trazi_tabl(broj,'T', temperatura[broj][0], mas_ud[broj][0])
    #             kond_obj.interpol_tabl1()

    #     if topl_tok:

    #         if self.stanja[broj][2] and not self.stanja[broj-1][2]:

    #             if mas_prot:
    #                 h2=self.stanja[broj][2]
    #                 h1 = float(h2) - (float(topl_tok)/float(mas_prot))
    #                 self.stanja[broj-1][2]=str(h1)
    #                 entalpija[broj-1] = str(h1)
    #                 x=self.Ekspanzija(broj-1)

    #             if not mas_prot:
    #                 h2=self.stanja[broj][2]
    #                 h1 = float(h2) - (float(topl_tok)/float(self.maseni_protok))
    #                 self.stanja[broj-1][2]=str(h1)
    #                 entalpija[broj-1] = str(h1)
    #                 mas_prot = float(topl_tok)/(float(h2) - float(h1))
    #                 x=self.Ekspanzija(broj-1)


    #         if self.stanja[broj-1][2] and not self.stanja[broj][2] or not entalpija[broj]:
    #             if mas_prot:
    #                 h1=self.stanja[broj-1][2]
    #                 h2 = (float(topl_tok)/float(mas_prot)) + float(h1)
    #                 kond_obj=Mk.Trazi_tabl(broj,'h', h2)
    #                 kond_obj.interpol_tabl2()

    #             if not mas_prot:
    #                 h1=self.stanja[broj-1][2]
    #                 h2 = (float(topl_tok)/float(self.maseni_protok)) + float(h1)
    #                 self.stanja[broj][2]=str(h2)
    #                 entalpija[broj] = str(h2)
    #                 kond_obj=Mk.Trazi_tabl(broj,'h', entalpija[broj][0])
    #                 kond_obj.interpol_tabl2()
    #                 mas_prot = float(topl_tok)/(float(h2) - float(h1))

    #         # if self.stanja[broj-1][2] and self.stanja[broj][2]:
    #         #     if mas_prot:
    #         #         pass
    #         #     if not mas_prot:
    #         #         h1=self.stanja[broj-1][2]
    #         #         h2 = self.stanja[broj][2]
    #         #         mas_prot = float(topl_tok)/(float(h2) - float(h1))



    #     if not topl_tok:

    #         if mas_prot:
    #             topl_tok = float(mas_prot)*(float(self.stanja[broj][2]) - float(self.stanja[broj-1][2]))
    #         if not mas_prot:
    #             topl_tok = float(self.maseni_protok)*(float(self.stanja[broj][2]) - float(self.stanja[broj-1][2]))
    #             mas_prot = float(topl_tok)/(float(self.stanja[broj][2]) - float(self.stanja[broj-1][2]))

    #     return [self.stanja, topl_tok, mas_prot, x[1] if x != None else None]

    # def Kompresija(self, broj, snaga = None, mas_prot= None):

    #     if snaga:

    #         if mas_prot:
    #             h1 = self.stanja[broj-1][2]
    #             h2 = float(h1) - float(snaga)/float(mas_prot)
    #             # eks_obj=Mk.Trazi_tabl(broj,'h', h2)
    #             # eks_obj.interpol_tabl2()

    #         if not mas_prot:
    #             h1 = self.stanja[broj-1][2]
    #             h2 = float(h1) - float(snaga)/float(self.maseni_protok)
    #             mas_prot = float(snaga)/(float(h1) - float(h2))
    #             # eks_obj=Mk.Trazi_tabl(broj,'h', h2)
    #             # eks_obj.interpol_tabl2()

    #     if not snaga:

    #         entropija[broj] = self.stanja[broj-1][3]
    
    #         if tlak[broj] and entropija[broj]:
    
    #             komp_obj=Mk.Trazi_tabl(broj,'s', entropija[broj][0])
    #             komp_obj.interpol_tabl2()
    
    #         if tlak[broj] and temperatura[broj] and not entropija[broj] and not mas_ud[broj]:
    
    #             komp_obj=Mk.Trazi_tabl(broj,'p', tlak[broj][0])
    #             komp_obj.interpol_tabl3(temperatura[broj][0])
    
    #         if tlak[broj] and temperatura[broj] and mas_ud[broj] and not entropija[broj]:
    
    #             komp_obj=Mk.Trazi_tabl(broj,'p', tlak[broj][0], mas_ud[broj][0])
    #             komp_obj.interpol_tabl3(temperatura[broj][0])
    
    #         if tlak[broj] and mas_ud[broj] and not entropija[broj] and not temperatura[broj]:
    
    #             komp_obj=Mk.Trazi_tabl(broj,'p', tlak[broj][0], mas_ud[broj][0])
    #             komp_obj.interpol_tabl2()

    #         if mas_prot:
    #             snaga = float(mas_prot)*(float(self.stanja[broj-1][2]) - float(self.stanja[broj][2]))
    #             kotao = float(mas_prot)*(float(self.stanja[0][2]) - float(self.stanja[broj][2]))
    #         if not mas_prot:
    #             snaga = float(self.maseni_protok)*(float(self.stanja[broj-1][2]) - float(self.stanja[broj][2]))
    #             mas_prot = float(snaga)/(float(self.stanja[broj-1][2]) - float(self.stanja[broj][2]))
    #             kotao = float(mas_prot)*(float(self.stanja[0][2]) - float(self.stanja[broj][2]))

    #     return  [self.stanja, snaga, mas_prot, kotao]