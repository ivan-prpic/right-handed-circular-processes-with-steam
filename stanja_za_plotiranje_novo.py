import numpy as np
import sys
from scipy import interpolate

sys.path.append(r'C:/FSB/cetvrta godina/Zavrsni rad/kod_slike_tabl/Kod/CSV_kod.py')
sys.path.append(r'C:/FSB/cetvrta godina/Zavrsni rad/kod_slike_tabl/Kod/Metaklasa1.py')

import CSV_kod as CSV_kod
import Metaklasa1 as Mk

rijecnik1= CSV_kod.rijecnik1
rijecnik2= CSV_kod.rijecnik2
rijecnik3= CSV_kod.rijecnik3

nova_lista1= CSV_kod.nova_lista1
nova_lista2= CSV_kod.nova_lista2
nova_lista3= CSV_kod.nova_lista3

def convert_to_floats(arr):
    # Use the map function to apply the float function to each element in the input list
    result = map(float, arr)
    # Return the resulting iterator as a list
    return list(result)
# svega=np.array([[['30'],
#           ['400'],
#           ['3231.57'],
#           ['6.9233'],
#           ['1.2083215'],
#           ['0.0994']],
 
#         [['7.5'],
#           ['215.18358'],
#           ['2876.4842'],
#           ['6.9233'],
#           ['1.0512411'],
#           ['0.2910405']],
 
#         [['7.5'],
#           ['350'],
#           ['3163.1400'],
#           ['7.44255'],
#           ['1.1625439'],
#           ['0.3801']],
 
#         [['0.2'],
#           ['60.06'],
#           ['2454.1223'],
#           ['7.44255'],
#           ['0.9343269'],
#           ['7.1457989']],
 
#         [['0.2'],
#           ['60.06'],
#           ['251.4'],
#           ['0.832'],
#           ['0.0'],
#           ['0.0010172']],
 
#         [['30'],
#           ['60.194174'],
#           ['254.47145'],
#           ['0.832'],
#           ['-0.512287'],
#           ['0.0010160']]], dtype='<U9')
svega= np.array([[['30'],
        ['233.86'],
        ['2803.26'],
        ['6.1858'],
        ['1.0'],
        ['0.066664']],

       [['0.23'],
        ['63.0'],
        ['2050.9649'],
        ['6.1858'],
        ['0.7604235'],
        ['5.1566758']],

       [['0.23'],
        ['63.0'],
        ['263.71500'],
        ['0.86866'],
        ['0.0'],
        ['0.0010188']],

       [['30'],
        ['63.160194'],
        ['266.86645'],
        ['0.86866'],
        ['-0.501932'],
        ['0.0010175']]], dtype='<U9')

class Stanja_za_plotiranje:
    def __init__(self,sve):
        self.sve=sve[:]

        self.tlak=self.sve[:,0]
        self.temperatura=self.sve[:,1]
        self.entalpija=self.sve[:,2]
        self.entropija=self.sve[:,3]

        self.pregrijano = []
        self.pothladeno = []

        self.stanje_izmedu = [] 

    def tablica1(self, temperatura):
        temperatura=str(temperatura)
        try:
            stanje0=rijecnik1[temperatura]
        except KeyError:
            pomocna_temp= list(rijecnik1.keys())
            gornja_donja_temp=Mk.nadji_veći_i_manji(pomocna_temp, float(temperatura), rijecnik1)
            stanje0=Mk.interpolica1(rijecnik1[gornja_donja_temp[0][1]],rijecnik1[gornja_donja_temp[0][0]],
                                    gornja_donja_temp[0][1],gornja_donja_temp[0][0], temperatura)
        return stanje0
    def tablica2(self,tlak):
        tlak=str(tlak)
        try:
            stanje1=rijecnik2[tlak]
        except KeyError:
            pomocna_tlak= list(rijecnik2.keys())
            gornja_donja_tlak=Mk.nadji_veći_i_manji(pomocna_tlak, tlak, rijecnik2)
            stanje1=Mk.interpolica1(rijecnik2[gornja_donja_tlak[0][1]],rijecnik2[gornja_donja_tlak[0][0]],
                                gornja_donja_tlak[0][1],gornja_donja_tlak[0][0], tlak)
        return stanje1

    def tablica3(self, broj):
        tlak = self.tlak[broj][0]

        pom_stanje = self.tablica2(tlak)
        temp_kond = pom_stanje[0]
        pom_stanje_pot=[str(pom_stanje[i]) for i  in [0, 3, 6]]
        pom_stanje_preg = [str(pom_stanje[i]) for i in [0, 4, 7]]

        moje_tocke = [self.temperatura[broj][0], self.entalpija[broj][0], self.entropija[broj][0]]

        if self.tlak[broj] != self.tlak[broj-1]:
            self.s_pomocna = []
            self.h_pomocna =[]
            for i in range(0,11):
                self.h_pomocna.append(float(pom_stanje[3])+0.1*i*(float(pom_stanje[4]) - float(pom_stanje[3])))
                self.s_pomocna.append(float(pom_stanje[6])+0.1*i*(float(pom_stanje[7]) - float(pom_stanje[6])))
            self.stanje_izmedu.append([self.h_pomocna, self.s_pomocna])

        try:

            temperature=np.array(list(rijecnik3[tlak].keys()))
            stanje=np.array(list(rijecnik3[tlak].values()))
            stanje[:,0] = temperature

            temperatura = stanje[:,0].tolist()

            gornja_donja_temp=Mk.nadji_veći_i_manji(temperatura, temp_kond, rijecnik3[tlak])
            indeks_pot = temperatura.index(gornja_donja_temp[0][1])
            indeks_preg = temperatura.index(gornja_donja_temp[0][0])

            sve_pothladeno = stanje[:][:indeks_pot+1].tolist()
            sve_pregrijano = stanje[:][indeks_preg:].tolist()

            sve_pothladeno.append(pom_stanje_pot)
            sve_pregrijano.insert(0,pom_stanje_preg)
            # print(sve_pregrijano, sve_pothladeno)
            if float(moje_tocke[0]) > float(temp_kond):
                try: 
                    temperature.tolist().index(moje_tocke[0])
                    pass
                except ValueError:
                    sve_pregrijano.append(moje_tocke)
                    sve_pregrijano =sorted(sve_pregrijano, key = lambda x: float(x[0]))


            if float(moje_tocke[0]) < float(temp_kond):
                try:
                    temperature.tolist().index(moje_tocke[0])
                    pass
                except ValueError:
                    sve_pothladeno.append(moje_tocke)
                    sve_pothladeno = sorted(sve_pothladeno, key = lambda x: float(x[0]))



        except KeyError:
            pomocni_tlak=np.array(list(rijecnik3.keys()))
            gornji_donji_tlak=Mk.nadji_veći_i_manji(pomocni_tlak, tlak, rijecnik3)

            temp_kond1 = self.tablica2(gornji_donji_tlak[0][1])[0]
            temp_kond2 = self.tablica2(gornji_donji_tlak[0][0])[0]

            temperature=np.array(list(rijecnik3[gornji_donji_tlak[0][1]].keys()))

            gornja_donja1=Mk.nadji_veći_i_manji(temperature.tolist(), temp_kond1, rijecnik3[gornji_donji_tlak[0][1]])
            gornja_donja2=Mk.nadji_veći_i_manji(temperature.tolist(), temp_kond2, rijecnik3[gornji_donji_tlak[0][0]])

            stanje1=np.array(list(rijecnik3[gornji_donji_tlak[0][1]].values()))
            stanje2=np.array(list(rijecnik3[gornji_donji_tlak[0][0]].values()))
            stanje1[:,0] = temperature
            stanje2[:,0] = temperature

            stanje = Mk.interpolica1(stanje1,stanje2,
                     gornji_donji_tlak[0][1],gornji_donji_tlak[0][0],tlak)
            # stanje1 = np.array(stanje1, dtype = '<U9')

            # print(stanje, temp_kond)
            # print(gornja_donja1[0], gornja_donja2[0])
            if gornja_donja1[0] == gornja_donja2[0]:
                indeks_pot = temperature.tolist().index(gornja_donja1[0][1])
                indeks_preg = temperature.tolist().index(gornja_donja1[0][0])

                sve_pothladeno = stanje[:][:indeks_pot+1].tolist()
                sve_pregrijano = stanje[:][indeks_preg:].tolist()

                sve_pothladeno.append(pom_stanje_pot)
                sve_pregrijano.insert(0,pom_stanje_preg)

                if float(moje_tocke[0]) > float(temp_kond):
                    try: 
                        temperature.tolist().index(moje_tocke[0])
                        pass
                    except ValueError:
                        sve_pregrijano.append(moje_tocke)
                        sve_pregrijano =sorted(sve_pregrijano, key = lambda x: float(x[0]))

                if float(moje_tocke[0]) < float(temp_kond):
                    try:
                        temperature.tolist().index(moje_tocke[0])
                        pass
                    except ValueError:
                        sve_pothladeno.append(moje_tocke)
                        sve_pothladeno = sorted(sve_pothladeno, key = lambda x: float(x[0]))


            if gornja_donja1[0][0] == gornja_donja2[0][1]:

                indeks_pot = temperature.tolist().index(gornja_donja2[0][1])
                indeks_preg = temperature.tolist().index(gornja_donja2[0][0])

                sve_pothladeno = stanje[:][:indeks_pot].tolist()
                sve_pregrijano = stanje[:][indeks_preg:].tolist()

                sve_pothladeno.append(pom_stanje_pot)
                sve_pregrijano.insert(0,pom_stanje_preg)

                if float(moje_tocke[0]) > float(temp_kond):
                    try: 
                        temperature = np.array(temperature,  dtype = object)
                        temperature.tolist().index(moje_tocke[0])
                        pass
                    except ValueError:
                        sve_pregrijano.append(moje_tocke)
                        sve_pregrijano =sorted(sve_pregrijano, key = lambda x: float(x[0]))
                        # print('tu sam')

                if float(moje_tocke[0]) < float(temp_kond):
                    try:
                        temperature = np.array(temperature,  dtype = object)
                        temperature.tolist().index(moje_tocke[0])
                        pass
                    except ValueError:
                        sve_pothladeno.append(moje_tocke)
                        sve_pothladeno = sorted(sve_pothladeno, key = lambda x: float(x[0]))



            else:
                # print('?')
                indeks1=temperature.tolist().index(gornja_donja1[0][1])
                gornja_donja3 = Mk.nadji_veći_i_manji(temperature.tolist(), temp_kond, rijecnik3[gornji_donji_tlak[0][1]])
                indeks2 = temperature.tolist().index(gornja_donja3[0][1])
                stanje[:][indeks1+1:indeks2+1] = stanje2[:][indeks1+1:indeks2+1]

                indeks_pot= temperature.tolist().index(gornja_donja3[0][0])
                indeks_preg =temperature.tolist().index(gornja_donja2[0][0])

                sve_pothladeno = stanje[:][:indeks_pot].tolist()
                sve_pregrijano = stanje[:][indeks_preg:].tolist()

                pom_temp1 = self.tablica1(gornja_donja3[0][0])
                pom_temp2 = self.tablica1(gornja_donja2[0][1])
                
                indeks4= temperature.tolist().index(gornja_donja3[0][0])
                indeks5 =temperature.tolist().index(gornja_donja2[0][1])
                
                # print(gornja_donja2, gornja_donja3)
                pom_stanje1 = [pom_temp1[i] for i in [4,7]]
                pom_stanje2 = [pom_temp2[i] for i in [4,7]]
                
                # dodatne_tocke
                sve=np.array([[[tlak] for i in range(6)] for j in range(np.shape(gornja_donja3[0])[0])], dtype = '<U9')

                initial_obj= Mk.Trazi_tabl(None,None,None)
                pom_stanja = initial_obj.stanja_lista(sve)
    
                obj = Mk.Trazi_tabl(0, 'p', tlak)
                obj.interpol_tabl3(gornja_donja2[0][1])
                pom_stanje1 = [ pom_stanja[0][i][0] for i in [1,2,3]]
                sve_pregrijano.insert(0,pom_stanje1)
                obj.interpol_tabl3(gornja_donja3[0][0])
                pom_stanje1 = [ pom_stanja[0][i][0] for i in [1,2,3]]
                sve_pregrijano.insert(0,pom_stanje1)

                sve_pothladeno.append(pom_stanje_pot)
                sve_pregrijano.insert(0,pom_stanje_preg)

                if float(moje_tocke[0]) > float(temp_kond):
                    try: 
                        temperature = np.array(temperature,  dtype = object)
                        temperature.tolist().index(moje_tocke[0])
                        pass
                    except ValueError:
                        sve_pregrijano.append(moje_tocke)
                        sve_pregrijano.sort()

                if float(moje_tocke[0]) < float(temp_kond):
                    try:
                        temperature = np.array(temperature,  dtype = object)
                        temperature.tolist().index(moje_tocke[0])
                        pass
                    except ValueError:
                        sve_pothladeno.append(moje_tocke)
                        sve_pothladeno = sorted(sve_pothladeno)

        return sve_pothladeno, sve_pregrijano


    def lista_stanja(self):
        for i in range(np.shape(self.sve)[0]):

            x = self.tablica3(i)
            pot = list(map(lambda inner_list: list(map(float, inner_list)), x[0]))
            preg = list(map(lambda inner_list: list(map(float, inner_list)), x[1]))
            pot=np.array(pot,dtype=object)
            preg = np.array(preg, dtype=object)
            self.pregrijano.append(preg)
            self.pothladeno.append(pot)

        return  [self.pothladeno, self.pregrijano, self.stanje_izmedu, self.sve]

# obj=Stanja_za_plotiranje(svega)
# c=obj.lista_stanja()
