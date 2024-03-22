import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
import numpy as np

# import Desnokretni_proces as Desnokretni_proces
# import stanja_za_plotiranje as stanja_za_plotiranje

import Metaklasa1 as Mk
import stanja_za_plotiranje_novo as szpn
import probna_graf as probna_graf
import Desnokretni_proces_novi as Dpn
from PIL import Image, ImageTk, Image


class TKINTERAPP(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplikacija s gumbovima i slikama")
        self.geometry("1600x1000")
        self.minsize(400,400)

        self.carnat()
        self.glavni_prozor()

    def glavni_prozor(self):
        Carnat=ttk.Button(self, text='Carnat', command = lambda: (self.obrisi_gumb(),self.carnat(),self.glavni_prozor()))
        Carnat.place(relx = 0.1, rely = 0.1, anchor = tk.CENTER)
        Raiken= ttk. Button(self, text= 'Raiken', command = lambda: (self.obrisi_gumb(),self.glavni_prozor(),self.raiken()))
        Raiken.place(relx = 0.17, rely = 0.1, anchor = tk.CENTER)

    def prikazi_ukloni_tablicu(self):
        # Provjeri postoji li već tablica
        if hasattr(self, 'tree') and self.tree is not None:
            # Ako postoji, ukloni je
            self.tree.destroy()
            self.tree = None
        else:
            # Ako ne postoji, stvori tablicu
            self.stvori_tablicu()

    def stvori_tablicu(self):
        # Stvaranje Treeviewa
        table_frame = ttk.Frame(self, width=400, height=180)
        table_frame.pack_propagate(False)  # Sprječava promjenu veličine okvira zbog djece
        table_frame.place(relx=0, rely=0.5)
        # Pozovite metodu za stvaranje tablice
        self.create_table(table_frame, self.lis[0].tolist())

    def gumbi(self):
        self.gumb_slika=[]
        
        gumbovi=["C:/FSB/cetvrta godina/Zavrsni rad/kod_slike_tabl/Kod/gumbi/okrugli gumb1.png",
      "C:/FSB/cetvrta godina/Zavrsni rad/kod_slike_tabl/Kod/gumbi/okrugli gimb2.png",
      "C:/FSB/cetvrta godina/Zavrsni rad/kod_slike_tabl/Kod/gumbi/okrugli gum 3.png",
      "C:/FSB/cetvrta godina/Zavrsni rad/kod_slike_tabl/Kod/gumbi/okrugli gumb 4.png",
      "C:/FSB/cetvrta godina/Zavrsni rad/kod_slike_tabl/slike i gumbi/okrugli_gumb5.png",
      "C:/FSB/cetvrta godina/Zavrsni rad/kod_slike_tabl/slike i gumbi/okrugli_gumb6.png"]

        for i in gumbovi:
            
            self.ikonica = PhotoImage(file=i)
            self.slika= Image.open(i)# Zamijenite "icon.png" sa stvarnom stazom do ikonice
            # Obrezivanje ikonice kako bi postala okrugla
            sirina = self.ikonica.width()  # Dobijemo širinu ikonice
            visina = self.ikonica.height()  # Dobijemo visinu ikonice

            r = min(sirina, visina) // 2  # Radijus okruglog gumba
            self.gumb_slika.append(self.ikonica.subsample(sirina // r, visina // r))
        return self.gumb_slika

    def prikazi_sliku(self):
        self.slika_label.config(image=self.moja_slika)
        self.slika_label.photo = self.moja_slika

    def stvori_objekt(self,a):
        self.objekat = szpn.Stanja_za_plotiranje(a[0])
        aha=self.objekat.lista_stanja()
        probna_graf.Stanja_plotiranje(aha)
        return self.objekat

    def stvori_Hs(self):
        self.objekt2=probna_graf.HS()
        return self.objekt2
    
    def stvori_Ts(self):
        self.objekt3=probna_graf.TS()
        return self.objekt3

    def obrisi_gumb(self):
    # Obriši sve postojeće gumbe
        for widget in self.winfo_children():
            widget.destroy()

    def zatvori_podprozor(self):
    # Funkcija za zatvaranje podprozora
        self.pod_prozor.destroy()


    def create_table(self,frame, data):
        # Stvaranje Treeviewaž
        j=0
        for i in data:
            combined_list = sum(i, [])
            data[j]=combined_list
            j+=1
    
        self.tree = ttk.Treeview(frame)
    
        # Definiranje stupaca
        self.tree["columns"] = ("Stanje", "Tlak", "Temp", "Entalpija", "Entropija", "Mas_ud")
    
        # Postavljanje naziva stupaca
        self.tree.column("#0", width=0, stretch=tk.NO)
        for col in ("Stanje", "Tlak", "Temp", "Entalpija", "Entropija", "Mas_ud"):
            self.tree.column(col, anchor= tk.W, width=20, stretch=tk.YES)
        # Postavljanje naziva zaglavlja
        self.tree.heading("#0", text="", anchor=tk.W)
        for col in ("Stanje", "Tlak", "Temp", "Entalpija", "Entropija", "Mas_ud"):
            self.tree.heading(col, text= col, anchor=tk.W)
    
        # Dodavanje podataka u tablicu
        for i, item in enumerate(data, start=1):
            self.tree.insert("", tk.END, values= [f"Stanje {i}"] + item)
    
        # Postavljanje tablice
        self.tree.pack(expand=tk.YES, fill=tk.BOTH)

    def open_number_window(self, button_name):
    # Create a new Toplevel window
        pod_prozor = tk.Toplevel(self)
        self.pod_prozor = pod_prozor
        pod_prozor.title(f"Stanja {button_name} ")
        frame1=ttk.Frame(pod_prozor)
        frame2=ttk.Frame(pod_prozor)
        frame3=ttk.Frame(pod_prozor)
        pod_prozor.maxsize(300,250)
        pod_prozor.minsize(300,250)
        pod_prozor.geometry("+800+500")

        save_button = ttk.Button(pod_prozor, text="Spremi", command=lambda: (self.save_numbers(button_name, entries), print(self.numbers_dict), self.zatvori_podprozor()))
        # save_button = ttk.Button(pod_prozor, text="Spremi", command=lambda: (self.save_numbers(button_name, entries), self.zatvori_podprozor()))
        save_button.pack(side='bottom')

        frame1.pack(side="left")
        frame3.pack(side='right')
        frame2.pack(side='right')

        # Check if there are previous numbers for this button
        # if self.numbers_dict[button_name]:
        #     numbers_str = ', '.join(map(str, self.numbers_dict[button_name]))
        #     label = tk.Label(pod_prozor, text=f"Previous Numbers: {numbers_str}")
        #     label.pack()

        # Entry widgets with labels
        entries = []
        labels1 = ['tlak', 'temperatura', 'entalpija', 'entropija', 'maseni udio', 'volumen']
        labels2 = ['bar', '°C', 'kJ/kg', 'kJ/kgK', 'kg/kg', 'm³/kg']

        for i in range(6):
            label1 = ttk.Label(frame1, text=labels1[i])
            label1.pack(padx=10, pady=5)

            label2 = ttk.Label(frame3, text = labels2[i])
            label2.pack(padx=10, pady=5)

            entry_var = tk.StringVar(value=str(self.numbers_dict[button_name][i][0]) if i < len(self.numbers_dict[button_name]) else '')
            entry = ttk.Entry(frame2, textvariable=entry_var)
            entry.pack(padx=10, pady=5)
            entries.append(entry_var)

        # Automatically copy entropija to gumb2 for gumb1
        # if button_name == 'gumb1':
        #     self.copy_entropija_to_gumb2(entries)

    def save_numbers(self, button_name, entries):

        # Get the entered numbers and convert them to integers
        try:
            numbers = [[str(entry.get())] if entry.get()[0][0].replace('.', '', 1).isdigit() else [''] for entry in entries]

        except IndexError:
            numbers = [[str(entry.get())] if entry.get().replace('.', '', 1).isdigit() else [''] for entry in entries]

        # Save the numbers for the specific button
        self.numbers_dict[button_name] = numbers
        
        self.svega[int(button_name[4])-1] = numbers

        # Automatically copy entropija to gumb2 for gumb1
        # if button_name == 'gumb1':
        #     self.copy_entropija_to_gumb2(entries)


    # def copy_entropija_to_gumb2(self, entries):
    #     # Copy entropija value from gumb1 to gumb2
    #     entropija_value = entries[3].get()  # index 3 corresponds to entropija
    #     if entropija_value.isdigit():
    #         self.numbers_dict['gumb2'] = ['', '', '', str(float(entropija_value)),'','']
    #     else:
    #         self.numbers_dict['gumb2'] = ['', '', '', '','']

    def toggle_mass_flow(self):
        if self.mass_flow_check_var.get() == 1:
            self.mass_flow_entry.config(state=tk.NORMAL)
        else:
            self.mass_flow_entry.config(state=tk.DISABLED)
            self.mas_protok = None  # Reset mass flow when disabled

    def prikaz_rjesenja(self):

        results_window = tk.Toplevel(self)
        results_window.title("Rezultati")

        frame1=ttk.Frame(results_window)
        frame2=ttk.Frame(results_window)
        frame3=ttk.Frame(results_window)

        frame1.pack(side="left")
        frame2.pack(side='right')
        frame3.pack(side='right')

        ekspanzija_label = tk.Label(frame1, text="Ekspanzija:")
        kondenzacija_label = tk.Label(frame1, text="Kondenzacija:")
        kompresija_label = tk.Label(frame1, text="Kompresija:")
        kotao_label = tk.Label(frame1, text="Kotao:")
        korisnost_label = tk.Label(frame1, text = 'Korisnost')
        pregrijavanje_label= tk.Label(frame1,  text = 'Pregrijavanje')
        mas_prot_label=tk.Label(frame1, text = 'Maseni protok')

        if self.mas_protok != None:
            tekst = 'kW'
        if self.mas_protok == None:
            tekst = 'kJ/kg'

        if int(np.shape(self.svega)[0]) == 4:

            ekspanzija_value = tk.Label(frame3, text=str(round(self.lis1[1],5)))
            kondenzacija_value = tk.Label(frame3, text=str(round(self.lis2[1],5)))
            kompresija_value = tk.Label(frame3, text=str(round(self.lis[1],5)))
            kotao_value = tk.Label(frame3, text=str(round(self.lis0[1],5)))
            korisnost_var = 100*(float(self.lis1[1]) + float(self.lis[1]))/float(self.lis0[1])
            korisnost_value=tk.Label(frame3, text=str(round(korisnost_var,5)))
            mas_prot_var = tk.Label(frame3, text=str(round(self.mas_protok,5) if self.mas_protok != None else None))

            mj_jed = tk.Label(frame2, text='kg/s')
            mj_jed.pack(padx=10, pady=5)
            mas_prot_label.pack(padx=10, pady=5)
            mas_prot_var.pack(padx=10,pady=5)

            mj_jed = tk.Label(frame2, text = tekst)
            mj_jed.pack(padx=10, pady=5)
            kotao_label.pack(padx=10, pady=5)
            kotao_value.pack(padx=10, pady=5)

            mj_jed = tk.Label(frame2, text = tekst)
            mj_jed.pack(padx=10, pady=5)
            ekspanzija_label.pack(padx=10, pady=5)
            ekspanzija_value.pack(padx=10, pady=5)

            kondenzacija_label.pack(padx=10, pady=5)
            kondenzacija_value.pack(padx=10, pady=5)
            mj_jed = tk.Label(frame2, text = tekst)
            mj_jed.pack(padx=10, pady=5)

            kompresija_label.pack(padx=10, pady=5)
            kompresija_value.pack(padx=10, pady=5)
            mj_jed = tk.Label(frame2, text = tekst)
            mj_jed.pack(padx=10, pady=5)

            korisnost_label.pack(padx=10, pady=5)
            korisnost_value.pack(padx=10, pady=5)
            mj_jed = tk.Label(frame2, text = '%')
            mj_jed.pack(padx=10, pady=5)


        if int(np.shape(self.svega)[0]) > 4:

            # kotao_value = tk.Label(frame3, text=str(round(self.lis[3],5)))
            ekspanzija_value = tk.Label(frame3, text=str(round(self.lis1[1],5)))
            pregrijavanje_value = tk.Label(frame3, text=str(round(self.lis2[1],5)))
            kondenzacija_value = tk.Label(frame3, text=str(round(self.lis4[1],5)))
            kompresija_value = tk.Label(frame3, text=str(round(self.lis[1],5)))
            korisnost_var = 100*(float(self.lis1[1]) +float(self.lis3[1])+ float(self.lis[1]))/(float(self.lis[3]) + float(self.lis2[1]))
            korisnost_value=tk.Label(frame3, text=str(round(korisnost_var,5)))

            mj_jed = tk.Label(frame2, text = tekst)
            mj_jed.pack(padx=10, pady=5)
            kotao_label.pack(padx=10, pady=5)
            kotao_value.pack(padx=10, pady=5)

            mj_jed = tk.Label(frame2, text = tekst)
            mj_jed.pack(padx=10, pady=5)
            ekspanzija_label.pack(padx=10, pady=5)
            ekspanzija_value.pack(padx=10, pady=5)

            mj_jed = tk.Label(frame2, text = tekst)
            mj_jed.pack(padx=10, pady=5)
            pregrijavanje_label.pack(padx=10, pady=5)
            pregrijavanje_value.pack(padx=10, pady=5)

            ekspanzija_value = tk.Label(frame3, text=str(round(self.lis3[1],5)))
            ekspanzija_label = tk.Label(frame1, text="Ekspanzija:")

            mj_jed = tk.Label(frame2, text = tekst)
            mj_jed.pack(padx=10, pady=5)
            ekspanzija_label.pack(padx=10, pady=5)
            ekspanzija_value.pack(padx=10, pady=5)

            kondenzacija_label.pack(padx=10, pady=5)
            kondenzacija_value.pack(padx=10, pady=5)
            mj_jed = tk.Label(frame2, text = tekst)
            mj_jed.pack(padx=10, pady=5)

            kompresija_label.pack(padx=10, pady=5)
            kompresija_value.pack(padx=10, pady=5)
            mj_jed = tk.Label(frame2, text = tekst)
            mj_jed.pack(padx=10, pady=5)

            korisnost_label.pack(padx=10, pady=5)
            korisnost_value.pack(padx=10, pady=5)
            mj_jed = tk.Label(frame2, text = '%')
            mj_jed.pack(padx=10, pady=5)

    def izracunaj(self, sve):
        sve = np.array(sve, dtype = '<U9')
        self.broj_stanja=int(np.shape(sve)[0])
        self.spremi_topl_tok()
        if int(np.shape(sve)[0]) == 4:

            obj=Dpn.Desnokretni_proces(sve, self.mas_protok)

            self.lis=obj.Kompresija(3,self.snaga_komp)
            self.lis0=obj.Kotao(0,self.topl_tok)
            self.lis1=obj.Ekspanzija(1,self.snaga_eksp)
            self.lis2=obj.Kondenzacija(2,self.kondenzacija)
            self.lis=obj.Kompresija(3,self.snaga_komp)

            obj.Provjeri(0, self.lis0)
            obj.Provjeri(1, self.lis1)
            obj.Provjeri(2, self.lis2)
            obj.Provjeri(3, self.lis)

        if int(np.shape(sve)[0]) > 4:
            obj=Dpn.Desnokretni_proces(sve,self.mas_protok)
            self.lis0=obj.Pocetno_stanje(0)
            self.lis1=obj.Ekspanzija(1)
            self.lis2=obj.Pregrijavanje(2)
            self.lis3=obj.Ekspanzija(3)
            self.lis4=obj.Kondenzacija(4)
            self.lis=obj.Kompresija(5)

        return self.lis

    def set_mass_flow(self):
        try:
            self.mas_protok = float(self.mass_flow_entry_var.get())
            print(f"Maseni protok set to: {self.mas_protok} kg/s")
        except ValueError:
            print("Invalid input for maseni protok")

    def spremi_topl_tok(self):

        self.topl_tok=float(self.topl_tok_kotao_entry_var.get()) if self.topl_tok_kotao_entry_var.get() != '' else None
        self.snaga_eksp=float(self.snaga_entry_var.get()) if self.snaga_entry_var.get() != '' else None
        self.kondenzacija=float(self.kondenzacija_entry_var.get()) if self.kondenzacija_entry_var.get() != '' else None
        self.snaga_komp=float(self.snaga_komp_entry_var.get()) if self.snaga_komp_entry_var.get() != '' else None

    def provjera_mas_prot(self):
         if self.broj_stanja == 4:

            razliciti_brojevi = set()
            lista=[self.lis1[2],self.lis2[2],self.lis[2]]

            for broj in lista:
                if lista.count(broj) > 1:
                    continue
                else:
                    razliciti_brojevi.add(broj)
            
            if not razliciti_brojevi:
                print("Svi brojevi su jednaki.")
            else:
                print("Različiti brojevi su:", list(razliciti_brojevi))
                self.mas_protok=float(list(razliciti_brojevi)[0]) if list(razliciti_brojevi)[0] != None else self.mas_protok
                self.izracunaj(self.svega)
            if self.lis1[1] == None:
                self.lis1[1] = self.lis2[3]
            else:
                pass

    def carnat(self):

        self.mas_protok = None
        #slika procesa:
        self.moja_slika = PhotoImage(file="C:/FSB/cetvrta godina/Zavrsni rad/kod_slike_tabl/slike i gumbi/carnatov proces bez tocaka.png")
        self.slika_label = tk.Label(self, image=self.moja_slika)
        self.slika_label.place(relx = 0.65, rely = 0.5, anchor = tk.CENTER)
        #stanja:

        self.numbers_dict = {'gumb1': np.array([['10'], ['400'], [''], [''], [''],['']]), 'gumb2':np.array([['0.5'], [''], [''], [''], [''],['']]),
                             'gumb3': np.array([[''], [''], [''], [''], ['0'],['']]), 'gumb4':np.array([['10'], [''], [''], [''], [''],['']])}
        #gumbovi:
        self.slike_gumbi=self.gumbi()

        okrugli_gumb1 = ttk.Button(self, image= self.slike_gumbi[0], command=lambda: (self.open_number_window('gumb1')))
        okrugli_gumb1.place(relx = 0.4, rely = 0.4, anchor = tk.CENTER)
    
        okrugli_gumb2 = ttk.Button(self, image= self.slike_gumbi[1],command=lambda: (self.open_number_window('gumb2')))
        okrugli_gumb2.place(relx = 0.62, rely = 0.4, anchor = tk.CENTER)
    
        okrugli_gumb3 = ttk.Button(self, image= self.slike_gumbi[2],command=lambda: (self.open_number_window('gumb3')))
        okrugli_gumb3.place(relx = 0.62, rely = 0.8, anchor = tk.CENTER)
    
        okrugli_gumb4 = ttk.Button(self, image= self.slike_gumbi[3],command=lambda: (self.open_number_window('gumb4')))
        okrugli_gumb4.place(relx = 0.4, rely = 0.8, anchor = tk.CENTER)

        self.svega = [ self.numbers_dict['gumb1'], self.numbers_dict['gumb2'],
                       self.numbers_dict['gumb3'], self.numbers_dict['gumb4']]
#------------------------------------------------------------------------------
        topl_tok_kotao=tk.Label(self, text='Toplinski tok [kW] \n kotao')
        topl_tok_kotao.place(relx = 0.28, rely = 0.5, anchor = tk.CENTER)

        self.topl_tok_kotao_entry_var = tk.StringVar(value=None)  # Inicijalna vrijednost None
        topl_tok_kotao_entry = ttk.Entry(self, textvariable=self.topl_tok_kotao_entry_var)
        topl_tok_kotao_entry.place(relx = 0.28, rely = 0.54, anchor = tk.CENTER)

        snaga_ekspanzija=tk.Label(self, text='Snaga eskpanzija [kW]')
        snaga_ekspanzija.place(relx = 0.65, rely = 0.22, anchor = tk.CENTER)

        self.snaga_entry_var = tk.StringVar(value=None)  # Inicijalna vrijednost None
        snaga_entry = ttk.Entry(self, textvariable=self.snaga_entry_var)
        snaga_entry.place(relx = 0.65, rely = 0.25, anchor = tk.CENTER)


        kondenzacija=tk.Label(self, text='Toplinski tok [kW] \n Kondenzacija')
        kondenzacija.place(relx = 0.68, rely = 0.48, anchor = tk.CENTER)

        self.kondenzacija_entry_var = tk.StringVar(value=None)  # Inicijalna vrijednost None
        kondenzacija_entry = ttk.Entry(self, textvariable=self.kondenzacija_entry_var)
        kondenzacija_entry.place(relx = 0.68, rely = 0.52, anchor = tk.CENTER)

        snaga_kompresija=tk.Label(self, text='Snaga kompresija [kW]')
        snaga_kompresija.place(relx = 0.52, rely = 0.73, anchor = tk.CENTER)

        self.snaga_komp_entry_var = tk.StringVar(value=None)  # Inicijalna vrijednost None
        snaga_komp_entry = ttk.Entry(self, textvariable=self.snaga_komp_entry_var)
        snaga_komp_entry.place(relx = 0.52, rely = 0.76, anchor = tk.CENTER)
#------------------------------------------------------------------------------
        self.lis = ['']
        self.lis[0] = np.array(self.svega)

        Izračunaj=ttk.Button(self, text= 'Izračunaj', command =  lambda : (self.set_mass_flow(),self.izracunaj(self.svega)
                           ,self.prikazi_ukloni_tablicu(),self.stvori_objekt(self.lis),self.prikaz_rjesenja()))
                            # print(self.lis0[2],self.lis1[2],self.lis2[2],self.lis[2])))

        Izračunaj.place(relx = 0.5, rely = 0.9, anchor = tk.CENTER)

        HS_dijagram=ttk.Button(self, text= 'HS-dijagram', command= lambda: (self.stvori_Hs(),self.objekt2.plotanje2()))
        HS_dijagram.place(relx=0.93, rely=1, anchor="se")
    
        TS_dijagram=ttk.Button(self, text= 'TS-dijagram', command =lambda: (self.stvori_Ts(),self.objekt3.plotanje()))
        TS_dijagram.place(relx=1, rely=1, anchor="se")
    
        tablica=ttk.Button(self, text='Tablica', command = lambda:(self.prikazi_ukloni_tablicu()))
        tablica.place(relx=0.1, rely=0.45, anchor = tk.CENTER)

        self.mass_flow_check_var = tk.IntVar()
        self.mass_flow_check = ttk.Checkbutton(self, text="Maseni protok", variable=self.mass_flow_check_var,
                                              command=self.toggle_mass_flow)
        self.mass_flow_check.place(relx=0.37, rely=0.12, anchor=tk.CENTER)

        # Entry field for mass flow
        self.mass_flow_label = tk.Label(self, text="kg/s")
        self.mass_flow_label.place(relx=0.535, rely=0.12, anchor=tk.CENTER)

        self.mass_flow_entry_var = tk.StringVar()
        self.mass_flow_entry = ttk.Entry(self, textvariable=self.mass_flow_entry_var, state=tk.DISABLED)
        self.mass_flow_entry.place(relx=0.47, rely=0.12, anchor=tk.CENTER)

    def raiken(self):

        self.mas_protok = None
        self.moja_slika = PhotoImage(file="C:/FSB/cetvrta godina/Zavrsni rad/kod_slike_tabl/slike i gumbi/Rainkenov_proces.png")
        self.slika_label = tk.Label(self, image=self.moja_slika)
        self.slika_label.place(relx = 0.5, rely = 0.5, anchor = tk.CENTER)
        #stanja:
        self.numbers_dict = {'gumb1': np.array([['30'], ['400'], [''], [''], [''],['']]), 'gumb2': np.array([['7.5'], [''], [''], [''], [''],['']]),
                             'gumb3': np.array([[''], ['350'], [''], [''], [''],['']]), 'gumb4': np.array([['0.2'], [''], [''], [''], [''],['']]),
                             'gumb5': np.array([[''], ['10'], [''], [''], [''],['']]), 'gumb6': np.array([['30'], [''], [''], [''], [''],['']])}

        #gumbovi:
        self.slike_gumbi=self.gumbi()
        okrugli_gumb1 = ttk.Button(self, image= self.slike_gumbi[0], command=lambda: (self.open_number_window('gumb1')))
        okrugli_gumb1.place(relx = 0.285, rely = 0.4, anchor = tk.CENTER)
    
        okrugli_gumb2 = ttk.Button(self, image= self.slike_gumbi[1],command=lambda: (self.open_number_window('gumb2')))
        okrugli_gumb2.place(relx = 0.5, rely = 0.35, anchor = tk.CENTER)
    
        okrugli_gumb3 = ttk.Button(self, image= self.slike_gumbi[2],command=lambda: (self.open_number_window('gumb3')))
        okrugli_gumb3.place(relx = 0.6, rely = 0.1, anchor = tk.CENTER)
    
        okrugli_gumb4 = ttk.Button(self, image= self.slike_gumbi[3],command=lambda: (self.open_number_window('gumb4')))
        okrugli_gumb4.place(relx = 0.71, rely = 0.4, anchor = tk.CENTER)

        okrugli_gumb5 = ttk.Button(self, image= self.slike_gumbi[4],command=lambda: (self.open_number_window('gumb5')))
        okrugli_gumb5.place(relx = 0.6, rely = 0.8, anchor = tk.CENTER)
        
        okrugli_gumb6 = ttk.Button(self, image= self.slike_gumbi[5],command=lambda: (self.open_number_window('gumb6')))
        okrugli_gumb6.place(relx = 0.4, rely = 0.8, anchor = tk.CENTER)

        #racunanje i crtanje grafova
        self.svega = [ self.numbers_dict['gumb1'], self.numbers_dict['gumb2'],
                       self.numbers_dict['gumb3'], self.numbers_dict['gumb4'],
                       self.numbers_dict['gumb5'], self.numbers_dict['gumb6']]

        self.lis = ['']
        self.lis[0] = np.array(self.svega)

        Izračunaj=ttk.Button(self, text= 'Izračunaj', command= lambda: (self.set_mass_flow(),self.izracunaj(self.svega),
                                        self.prikazi_ukloni_tablicu(),self.stvori_objekt(self.lis),self.prikaz_rjesenja()))

        Izračunaj.place(relx = 0.5, rely = 0.9, anchor = tk.CENTER)
    
        HS_dijagram=ttk.Button(self, text= 'HS-dijagram', command= lambda: (self.stvori_Hs(),self.objekt2.plotanje2()))
        HS_dijagram.place(relx=0.93, rely=1, anchor="se")
    
        TS_dijagram=ttk.Button(self, text= 'TS-dijagram', command =lambda: (self.stvori_Ts(),self.objekt3.plotanje()))
        TS_dijagram.place(relx=1, rely=1, anchor="se")

        tablica=ttk.Button(self, text='Tablica', command = lambda:(self.prikazi_ukloni_tablicu()))
        tablica.place(relx=0.1, rely=0.45, anchor = tk.CENTER)

        #maseni protok
        self.mass_flow_check_var = tk.IntVar()
        self.mass_flow_check = ttk.Checkbutton(self, text="Maseni protok", variable=self.mass_flow_check_var,
                                              command=self.toggle_mass_flow)
        self.mass_flow_check.place(relx=0.37, rely=0.12, anchor=tk.CENTER)

        self.mass_flow_label = tk.Label(self, text="kg/s")
        self.mass_flow_label.place(relx=0.535, rely=0.12, anchor=tk.CENTER)

        self.mass_flow_entry_var = tk.StringVar()
        self.mass_flow_entry = ttk.Entry(self, textvariable=self.mass_flow_entry_var, state=tk.DISABLED)
        self.mass_flow_entry.place(relx=0.47, rely=0.12, anchor=tk.CENTER)



if __name__=='__main__':
    TK = TKINTERAPP()
    TK.glavni_prozor()
    TK.mainloop()