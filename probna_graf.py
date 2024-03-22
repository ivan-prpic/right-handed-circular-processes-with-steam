import numpy as np

import matplotlib.pyplot as plt

from scipy import interpolate

import sys

sys.path.append(r'C:/FSB/cetvrta godina/Zavrsni rad/kod_slike_tabl/Kod/CSV_kod.py')
# sys.path.append(r'C:/FSB/cetvrta godina/Zavrsni rad/toplsinke tablice/Desnokretni_proces.py')
sys.path.append(r'C:/FSB/cetvrta godina/Zavrsni rad/kod_slike_tabl/Kod/stanja_za_plotiranje.py')
sys.path.append(r'C:/FSB/cetvrta godina/Zavrsni rad/kod_slike_tabl/Kod/stanja_za_plotiranje_novo.py')

import CSV_kod as CSV_kod
# import stanja_za_plotiranje as stanja_za_plotiranje

import stanja_za_plotiranje_novo as szpn

rijecnik1= CSV_kod.rijecnik1
rijecnik2= CSV_kod.rijecnik2
rijecnik3= CSV_kod.rijecnik3

nova_lista1= CSV_kod.nova_lista1
nova_lista2= CSV_kod.nova_lista2
nova_lista3= CSV_kod.nova_lista3

rijecnik1= CSV_kod.rijecnik1
rijecnik2= CSV_kod.rijecnik2
rijecnik3= CSV_kod.rijecnik3

nova_lista1= CSV_kod.nova_lista1
nova_lista2= CSV_kod.nova_lista2
nova_lista3= CSV_kod.nova_lista3



convert_to_floats=szpn.convert_to_floats


sara=np.array([[['30'],
        ['400'],
        ['3231.57'],
        ['6.9233'],
        ['1.2083215'],
        ['0.0994']],

       [['7.5'],
        ['215.18358'],
        ['2876.4842'],
        ['6.9233'],
        ['1.0512411'],
        ['0.2910405']],

       [['7.5'],
        ['300'],
        ['3058.21'],
        ['7.2669999'],
        ['1.1249142'],
        ['0.3478']],

       [['0.7'],
        ['89.93'],
        ['2582.4462'],
        ['7.2669999'],
        ['0.9662801'],
        ['2.2852873']],

       [['0.7'],
        ['10'],
        ['42.089999'],
        ['0.1511'],
        ['-0.165545'],
        ['0.001']],

       [['30'],
        ['10.020675'],
        ['45.026421'],
        ['0.1511'],
        ['-0.704621'],
        ['0.0009990']]], dtype='<U9')

# obj=szpn.Stanja_za_plotiranje(sara)
# y=obj.lista_stanja()
# pothlađena = y[0]
# pregrijana = y[1]
# stanje_izmedu = y[2]

# # objektica=stanja_za_plotiranje.Listiraj(sara)
# # 
# # pothlađena=objektica.pothlađena
# # pregrijana=objektica.pregrijana
# tlak_puna=sara[:,0]
# temperatura_puna=sara[:,1]
# entalpija_puna=sara[:,2]
# entropija_puna=sara[:,3]
# mas_ud_puna=sara[:,4]

# objektica = szpn.Stanja_za_plotiranje(sara)



class Stanja_plotiranje():
    def __init__(self, objektica):
        self.objektica=objektica

        global tlak_puna, temperatura_puna, entalpija_puna, entropija_puna, mas_ud_puna, pothlađena, pregrijana, stanje_izmedu
        tlak_puna =  self.objektica[3][:,0]
        temperatura_puna =self.objektica[3][:,1]
        entalpija_puna =self.objektica[3][:,2]
        entropija_puna =self.objektica[3][:,3]
        mas_ud_puna = self.objektica[3][:,4]
        

        pothlađena=self.objektica[0]
        pregrijana=self.objektica[1]
        stanje_izmedu = self.objektica[2]

# from stanja_za_plotiranje import convert_to_floats

#------------------------------------------------------------------------------p-v dijagram

#podaci za tlak i volumen iz tt
# tlak= nova_lista1[:,1]
# volumen1= nova_lista1[:,2]
# volumen2= nova_lista1[:,3]
# f1= interpolate.splrep(tlak, volumen1)
# f2= interpolate.splrep(tlak, volumen2)

# #novi tlak
# tlak_new= arange(float(tlak[0]), float(tlak[-1]), 0.001)

# #novi volumen
# volumen1_new= interpolate.splev(tlak_new, f1)
# volumen2_new= interpolate.splev(tlak_new, f2)

# #plotiranje p-v
# plt.figure('p-v')

# plt.title("p-v", fontsize=20, fontweight='bold')
# plt.plot(volumen1_new, tlak_new, 'k', volumen2_new, tlak_new, 'k', linewidth=2)
# plt.xlim(-0, 0.75)
# plt.ylim(-10, 200)
# plt.ylabel("Tlak \n p [Pa]", fontweight='bold')
# plt.xlabel("Specifični volumen \n v [($m^3$)/kg]", fontweight='bold')
# plt.grid(True)
# plt.show()
# # plt.savefig('p-v.png', dpi=300)

#------------------------------------------------------------------------------T-s dijagram

class Pregrijanje:
    def __init__(self,i):
        self.i=i

    def pregrijaj(self):
        f_preg= interpolate.splrep(pregrijana[self.i][:,2][::2],pregrijana[self.i][:,0][::2])
        pregrijana_new= np.linspace(pregrijana[self.i][:,2][0],pregrijana[self.i][:,2][-1], 1000)
        pregrijana_new=pregrijana[self.i][:,2].tolist()+pregrijana_new[1:-1].tolist()
        pregrijana_new.sort()
        pregrijana_new=np.array(pregrijana_new, dtype='float64')
        temperatura_pregrijana_new= interpolate.splev(pregrijana_new, f_preg)
        return pregrijana_new, temperatura_pregrijana_new
    

    def pregrijaj2(self):
        f_preg2=interpolate.splrep(pregrijana[self.i][:,2][:],pregrijana[self.i][:,1][:])
        pregrijana_new2= np.linspace(pregrijana[self.i][:,2][0],pregrijana[self.i][:,2][-1], 1000)
        pregrijana_new2=pregrijana[self.i][:,2].tolist()+pregrijana_new2[1:-1].tolist()
        pregrijana_new2=sorted(pregrijana_new2)
        pregrijana_new2=np.array(pregrijana_new2, dtype='float64')
        entalpija_pregrijana_new=interpolate.splev(pregrijana_new2, f_preg2)
        return pregrijana_new2, entalpija_pregrijana_new

class Potlhladivanje:
    def __init__(self, i):
        self.i=i

    def pothladi(self):
        f_pot= interpolate.splrep(pothlađena[self.i][:,2], pothlađena[self.i][:,0])
        pothladena_new= np.linspace(pothlađena[self.i][:,2][0], pothlađena[self.i][:,2][-1], 1000 )
        pothladena_new=pothlađena[self.i][:,2].tolist()+pothladena_new.tolist()
        pothladena_new=sorted(pothladena_new)
        pothladena_new=np.array(pothladena_new, dtype='float64')
        temperatura_pothladena_new= interpolate.splev(pothladena_new, f_pot)
        return pothladena_new,temperatura_pothladena_new

    def pothladi2(self):
        f_pot2=interpolate.splrep(pothlađena[self.i][:,2],pothlađena[self.i][:,1])
        pothladena_new2=np.linspace(pothlađena[self.i][:,2][0],pothlađena[self.i][:,2][-1],1000)
        pothladena_new2=pothlađena[self.i][:,2].tolist()+pothladena_new2.tolist()
        pothladena_new2=sorted(pothladena_new2)
        pothladena_new2=np.array(pothladena_new2, dtype='float64')
        entalpija_pothladena_new=interpolate.splev(pothladena_new2,f_pot2)
        return pothladena_new2, entalpija_pothladena_new

class TS():
    def __init__(self):
        self.temperatura1= nova_lista2[:,1]
        self.temperatura2= nova_lista2[:,1][::-1]
        self.entropija1= nova_lista2[:,7]
        self.entropija2= nova_lista2[:,8][::-1]

        
        self.f3= interpolate.splrep(self.entropija1, self.temperatura1)
        self.f4= interpolate.splrep(self.entropija2, self.temperatura2)
        
        self.entropija1=convert_to_floats(self.entropija1)
        self.entropija2=convert_to_floats(self.entropija2)
        self.temperatura1=convert_to_floats(self.temperatura1)
        self.temperatura2=convert_to_floats(self.temperatura2)
        
        self.entropija1_new= np.linspace(float(self.entropija1[0]), float(self.entropija1[-1]), 1000)
        self.entropija1_new= self.entropija1+ self.entropija1_new.tolist()
        self.entropija1_new.sort()
        self.entropija1_new=np.array(self.entropija1_new)

        self.entropija2_new= np.linspace(float(self.entropija2[0]), float(self.entropija2[-1]), 1000)
        self.entropija2_new= self.entropija2+ self.entropija2_new.tolist()
        self.entropija2_new.sort()
        self.entropija2_new=np.array(self.entropija2_new)

        self.temperatura1_new= interpolate.splev(self.entropija1_new, self.f3)
        self.temperatura2_new= interpolate.splev(self.entropija2_new, self.f4)
        
        
        plt.figure('T-s',figsize=(20,10))
        
        plt.title('T-s', fontsize=20, fontweight='bold')
        plt.plot(self.entropija1,self.temperatura1)
        plt.plot(self.entropija2,self.temperatura2)
        plt.plot(self.entropija1_new, self.temperatura1_new, 'k', self.entropija2_new, self.temperatura2_new, 'k', linewidth=2)
        plt.plot(self.entropija1_new[-1],self.temperatura1_new[-1],'ko',label="točke procesa")

    def plotanje(self):

        for i in range(np.shape(pregrijana)[0]):

            plt.plot(float(entropija_puna[i]),float(temperatura_puna[i]),'ko')
            plt.text(float(entropija_puna[i])+0.1*i,float(temperatura_puna[i]), f'{i+1}', fontsize=15, fontweight='bold')

            const_entropija=np.linspace(pothlađena[i][:,2][-1],pregrijana[i][:,2][0],100)
            const_temperatura=[pothlađena[i][-1][0]]*np.size(const_entropija)

            if float(entropija_puna[i-1]) == float(entropija_puna[i]):
                plt.plot([float(entropija_puna[i-1]), float(entropija_puna[i])], [float(temperatura_puna[i-1]),float(temperatura_puna[i])], 'k', linewidth= 3)
            
            if float(mas_ud_puna[i])>1:
                if tlak_puna[i-1] != tlak_puna[i-2] and float(entropija_puna[i-1])==float(entropija_puna[i-2]):
                    if tlak_puna[i-1] == tlak_puna[i] and float(mas_ud_puna[i-1])>1 and float(mas_ud_puna[i])>1:
                        pass
                    else:
                        obj=Pregrijanje(i)
                        liste=obj.pregrijaj()
                        pregrijana_new=liste[0]
                        temperatura_pregrijana_new=liste[1]
                        entro_indeks=pregrijana_new.tolist().index(float(entropija_puna[i]))
                        plt.plot(pregrijana_new[:entro_indeks+1], temperatura_pregrijana_new[:entro_indeks+1],'k', linewidth= 3)
                        plt.plot(const_entropija, const_temperatura, 'k', linewidth=3)
                        plt.plot(pregrijana_new, temperatura_pregrijana_new, 'r', linewidth=1)

                if tlak_puna[i-1] == tlak_puna[i-2] and float(temperatura_puna[i-1])>float(temperatura_puna[i-2]):
                    if np.shape(pregrijana)[0]>4:
                        obj=Pregrijanje(i)
                        liste=obj.pregrijaj()
                        pregrijana_new=liste[0]
                        temperatura_pregrijana_new=liste[1]
                        temperatura_pregrijana_new=temperatura_pregrijana_new.tolist()
                        temperatura_pregrijana_new.append(float(temperatura_puna[i+1]))

                        pregrijana_new=pregrijana_new.tolist()
                        pregrijana_new.append(float(entropija_puna[i+1]))
    
                        pregrijana_new.sort()
                        temperatura_pregrijana_new.sort()

                        entro_indeks1= pregrijana_new.index(float(entropija_puna[i]))
                        entro_indeks2= pregrijana_new.index(float(entropija_puna[i+1]))
                        pregrijana_new=np.array(pregrijana_new,dtype=object)
                        temperatura_pregrijana_new=np.array(temperatura_pregrijana_new,dtype=object)
                        plt.plot(pregrijana_new[entro_indeks1:entro_indeks2+1], temperatura_pregrijana_new[entro_indeks1:entro_indeks2+1],'k', linewidth= 3)
                        plt.plot(pregrijana_new, temperatura_pregrijana_new, 'r', linewidth=1)

                    else:
                        obj=Pregrijanje(i)
                        liste=obj.pregrijaj()
                        pregrijana_new=liste[0]
                        temperatura_pregrijana_new=liste[1]
                        entro_indeks=pregrijana_new.tolist().index(float(entropija_puna[i]))
                        plt.plot(pregrijana_new[:entro_indeks+1], temperatura_pregrijana_new[:entro_indeks+1],'k', linewidth= 3)
                        plt.plot(const_entropija, const_temperatura, 'k', linewidth=3)
                        plt.plot(pregrijana_new, temperatura_pregrijana_new, 'r', linewidth=1)

                # plt.fill([float(entropija_puna[i]),float(entropija_puna[i+1]),float(pregrijana[i][:,2][0])],
                #                     [float(temperatura_puna[i]),float(temperatura_puna[i+1]),float(pregrijana[i][:,0][0])],facecolor='lightblue',label="$q_{uk}$")
                # plt.fill([float(entropija_puna[i+1]),float(pregrijana[i][:,2][0]),float(pothlađena[i][:,2][-1]),float(pothlađena[i+1][:,2][-1])],
                #                     [float(temperatura_puna[i+1]),float(pregrijana[i][:,0][0]),float(pothlađena[i][:,0][-1]),float(pothlađena[i+1][:,0][-1])],facecolor='lightblue')

            if 0<float(mas_ud_puna[i])<=1:
                obj=Pregrijanje(i)
                liste=obj.pregrijaj()
                pregrijana_new=liste[0]
                temperatura_pregrijana_new=liste[1]
                plt.plot([pothlađena[i][:,2][-1], float(entropija_puna[i])],
                          [float(temperatura_puna[i]), float(temperatura_puna[i])], 'k', linewidth= 3)
                plt.plot(pregrijana_new, temperatura_pregrijana_new, 'r', linewidth=1)

            if float(mas_ud_puna[i])<0:
                obj1=Potlhladivanje(i)
                liste1=obj1.pothladi()
                pothladena_new=liste1[0]
                temperatura_pothladena_new=liste1[1]
                entro_indeks=pothladena_new.tolist().index(float(entropija_puna[i]))
                plt.plot(pothladena_new[entro_indeks:], temperatura_pothladena_new[entro_indeks:],'k', linewidth= 3)
                plt.plot(pothladena_new, temperatura_pothladena_new, 'r', linewidth=1)
    
            if float(tlak_puna[i-1]) != float(tlak_puna[i]):
                plt.plot(const_entropija, const_temperatura, 'r', linewidth=1)
                plt.text(pothlađena[i][:,2][-1]+((pregrijana[i][:,2][0] - pothlađena[i][:,2][-1])/2) - 0.45, pregrijana[i][:,0][0]+5, ' %0.2f bara i %0.3f °C' %(tlak_puna[i], pregrijana[i][:,0][0]),fontsize=10, fontweight='light')


        plt.text(self.entropija1_new[-1],self.temperatura1_new[-1]+10, 'K', fontsize=15, fontweight='light')
        plt.xlabel("Specifična entropija \n s [kJ/kgK]", fontweight='bold')
        plt.ylabel("Temperatura \n T [K]", fontweight='bold')
        plt.ylim(-10,400)
        plt.grid(True)
        plt.legend()
        plt.show()
        plt.savefig('T-s.png', dpi=300)

# objekt1=TS()
# objekt1.plotanje()
#------------------------------------------------------------------------------h-s dijagram
class HS():
    def __init__(self):
        self.entalpija1= nova_lista2[:,4]
        self.entropija1= nova_lista2[:,7]
        self.entalpija2= nova_lista2[:,5][::-1]
        self.entropija2= nova_lista2[:,8][::-1]
        
        
        f5= interpolate.splrep(self.entropija1, self.entalpija1)
        f6= interpolate.splrep(self.entropija2, self.entalpija2)
        
        
        self.entropija1_new= np.linspace(float(self.entropija1[0]), float(self.entropija1[-1]), 1000)
        self.entropija2_new= np.linspace(float(self.entropija2[0]), float(self.entropija2[-1]), 1000)
        
        self.entalpija1_new= interpolate.splev(self.entropija1_new, f5)
        self.entalpija2_new= interpolate.splev(self.entropija2_new, f6)

        plt.figure('h-s', figsize=(20,10))
        
        plt.title("h-s", fontsize=20, fontweight='bold')
        plt.plot(self.entropija1_new, self.entalpija1_new, 'k', self.entropija2_new, self.entalpija2_new, 'k', linewidth=2)
        plt.plot(self.entropija1_new[-1], self.entalpija1_new[-1],'ko')

    def plotanje2(self):

        for i in range(np.shape(pregrijana)[0]):
        
            plt.plot(float(entropija_puna[i]),float(entalpija_puna[i]),'ko')
            plt.text(float(entropija_puna[i])+0.07*i,float(entalpija_puna[i])+75, f'{i+1}', fontsize=15, fontweight='bold')

            if float(entropija_puna[i-1]) == float(entropija_puna[i]):
                plt.plot([float(entropija_puna[i-1]), float(entropija_puna[i])], [float(entalpija_puna[i-1]),float(entalpija_puna[i])], 'k', linewidth= 3)
                plt.plot([float(pothlađena[i][:,2][-1]),float(pregrijana[i][:,2][0])],
                      [float(pothlađena[i][:,1][-1]),float(pregrijana[i][:,1][0])],'r', linewidth=1,zorder=2)

            if float(mas_ud_puna[i])>1:
                if tlak_puna[i-1] != tlak_puna[i-2] and float(entropija_puna[i-1])==float(entropija_puna[i-2]):
                    if tlak_puna[i-1] == tlak_puna[i] and float(mas_ud_puna[i-1])>1 and float(mas_ud_puna[i])>1:
                        pass

                    else:
                        obj=Pregrijanje(i)
                        liste=obj.pregrijaj2()
                        pregrijana_new=liste[0]
                        entalpija_pregrijana_new=liste[1]
                        entro_indeks=pregrijana_new.tolist().index(float(entropija_puna[i]))
                        plt.plot(pregrijana_new[:entro_indeks+1], entalpija_pregrijana_new[:entro_indeks+1],'k', linewidth= 3)
                        plt.plot([float(pothlađena[i][:,2][-1]),float(pregrijana[i][:,2][0])],
                                [float(pothlađena[i][:,1][-1]),float(pregrijana[i][:,1][0])],'k', linewidth=3, zorder=1)
                        plt.plot(pregrijana_new, entalpija_pregrijana_new, 'r', linewidth=1)
                        plt.text(pothlađena[i][:,2][-1]+(float(entropija_puna[i]) - pothlađena[i][:,2][-1])/2,
                                 pothlađena[i][:,1][-1]+(float(entalpija_puna[i]) - pothlađena[i][:,1][-1])/2+15,
                                 ' %s bara i %s °C' %(float(tlak_puna[i]), pregrijana[i][:,0][0]), rotation=30, rotation_mode='anchor',fontsize=10, fontweight='light')

                if tlak_puna[i-1] == tlak_puna[i-2] and float(temperatura_puna[i-1])>float(temperatura_puna[i-2]):
                    if np.shape(pregrijana)[0]>4:
                        obj=Pregrijanje(i)
                        liste=obj.pregrijaj2()
                        pregrijana_new=liste[0]
                        entalpija_pregrijana_new=liste[1]

                        pregrijana_new=pregrijana_new.tolist()
                        pregrijana_new.append(float(entropija_puna[i+1]))
                        pregrijana_new.sort()

                        entalpija_pregrijana_new=entalpija_pregrijana_new.tolist()
                        entalpija_pregrijana_new.append(float(entalpija_puna[i+1]))
                        entalpija_pregrijana_new.sort()

                        entro_indeks1= pregrijana_new.index(float(entropija_puna[i]))
                        entro_indeks2= pregrijana_new.index(float(entropija_puna[i+1]))

                        pregrijana_new=np.array(pregrijana_new,dtype=object)
                        entalpija_pregrijana_new=np.array(entalpija_pregrijana_new,dtype=object)

                        plt.plot(pregrijana_new[entro_indeks1:entro_indeks2+1], entalpija_pregrijana_new[entro_indeks1:entro_indeks2+1],'k', linewidth= 3)
                        plt.plot(pregrijana_new, entalpija_pregrijana_new, 'r', linewidth=1)

                        plt.text(pothlađena[i][:,2][-1]+(float(entropija_puna[i]) - pothlađena[i][:,2][-1])/2,
                                      pothlađena[i][:,1][-1]+(float(entalpija_puna[i]) - pothlađena[i][:,1][-1])/2+15,
                                      ' %s bara i %s °C' %(float(tlak_puna[i]), pregrijana[i][:,0][0]), rotation=30, rotation_mode='anchor',fontsize=10, fontweight='light')

                    else:
                        obj=Pregrijanje(i)
                        liste=obj.pregrijaj2()
                        pregrijana_new=liste[0]
                        entalpija_pregrijana_new=liste[1]
                        entro_indeks=pregrijana_new.tolist().index(float(entropija_puna[i]))
                        plt.plot(pregrijana_new[:entro_indeks+1], entalpija_pregrijana_new[:entro_indeks+1],'k', linewidth= 3)
                        plt.plot([float(pothlađena[i][:,2][-1]),float(pregrijana[i][:,2][0])],
                              [float(pothlađena[i][:,1][-1]),float(pregrijana[i][:,1][0])],'k', linewidth=3, zorder=1)
                        plt.plot(pregrijana_new, entalpija_pregrijana_new, 'r', linewidth=1)
                        plt.text(pothlađena[i][:,2][-1]+(float(entropija_puna[i]) - pothlađena[i][:,2][-1])/2,
                                 pothlađena[i][:,1][-1]+(float(entalpija_puna[i]) - pothlađena[i][:,1][-1])/2+15,
                                 ' %s bara i %s °C' %(float(tlak_puna[i]), pregrijana[i][:,0][0]), rotation=30, rotation_mode='anchor',fontsize=10, fontweight='light')

            if 0<float(mas_ud_puna[i])<=1:
                obj=Pregrijanje(i)
                liste=obj.pregrijaj2()
                pregrijana_new=liste[0]
                entalpija_pregrijana_new=liste[1]
                plt.plot(pregrijana_new, entalpija_pregrijana_new, 'r', linewidth=1)
                plt.plot([pothlađena[i][:,2][-1],float(entropija_puna[i])],
                      [pothlađena[i][:,1][-1],float(entalpija_puna[i])],'k', linewidth=3)
                plt.text(pothlađena[i][:,2][-1]+(float(entropija_puna[i]) - pothlađena[i][:,2][-1])/2,
                         pothlađena[i][:,1][-1]+(float(entalpija_puna[i]) - pothlađena[i][:,1][-1])/2+15,
                         ' %s bara i %s °C' %(float(tlak_puna[i]), pregrijana[i][:,0][0]), rotation=26, rotation_mode='anchor',fontsize=10, fontweight='light')
                                                 
            
            if float(mas_ud_puna[i])<0:
                obj=Potlhladivanje(i)
                liste=obj.pothladi2()
                pothladena_new=liste[0]
                entalpija_pothladena_new=liste[1]
                entro_indeks=pothladena_new.tolist().index(float(entropija_puna[i]))
                plt.plot(pothladena_new[entro_indeks:], entalpija_pothladena_new[entro_indeks:],'k', linewidth= 3)
                plt.plot(pothladena_new, entalpija_pothladena_new, 'r', linewidth=1)

        plt.text(self.entropija1_new[-1]-0.2, self.entalpija1_new[-1]+10, 'K', fontsize=15, fontweight='light')
        plt.ylabel("Specifična entalpija \n h [kJ/kg]",fontweight='bold')
        plt.xlabel("Specifična entropija \n s [kj/kgK]",fontweight='bold')
        plt.grid(True)
        plt.show()

# objekt2=HS()
# objekt2.plotanje2()
