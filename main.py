#coding: utf-8

from ScreenRes import ScreenRes
from HighContrastManager import HighContrastManager
from ScreenOrien import ScreenOrien
from Luminosity import Luminosity
from Police import Police
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo


#Resolution
default_resolution=f"{ScreenRes.get()[0]} x {ScreenRes.get()[1]}"
lis_resolution=[ f"{element[0]} x {element[1]}" for element in ScreenRes.get_modes()]
#Orientation
lis_orientation=ScreenOrien.get_modes()
default_orientation=ScreenOrien.get()

#HighContrast
current_contrast_settings = HighContrastManager.get_high_contrast_settings()
default_contrast_enable=HighContrastManager.is_high_contrast_enabled()
default_contrast_theme=current_contrast_settings.lpszDefaultScheme
lis_contrast=HighContrastManager.get_modes()

#police
lis_police=Police.get_modes()

def setResolution(*arg):
    new_resol=var_resolution.get()
    new_resol=new_resol.split(" x ")
    ScreenRes.set(int(new_resol[0]), int(new_resol[1]))
    """ handle the resolution changed event """
    showinfo(
        title='Result',
        message=f'Vous avez choisir  "{var_resolution.get()}"!'
    )
def setOrientation(*arg):
    new_orien=cmbx_orientation.current()
    if new_orien==0:
        ScreenOrien.set(1)
    elif new_orien == 1:
        ScreenOrien.set(90)
    elif new_orien==2 :
        ScreenOrien.set(180)
    elif new_orien==3:
        ScreenOrien.set(270)
    showinfo(
        title='Result',
        message=f'Vous avez choisir "{var_orientation.get()}" !'
    )

def setContrast():
    new_contrast=var_contrast_list.get()
    HighContrastManager.toggle_high_contrast(True, new_contrast)
    showinfo(
            title='Result',
            message=f'Vous avez choisir "{new_contrast}" !'
        )
def activer_combobox_contrast():
    cmbx_contrast['state']="active"
    btn_contrast['state']="active"
def desactiver_combobox_contrast():
    cmbx_contrast["state"]="disabled"
    btn_contrast['state']="disabled"

def on_radio_change_contrast():
    selected=var_contrast.get()
    if selected==1:
        activer_combobox_contrast()
        if HighContrastManager.is_high_contrast_enabled():
            return
        HighContrastManager.toggle_high_contrast(True)
        showinfo(
            title='Result',
            message='Vous avez activer Le contraste !'
        )
    else:
        desactiver_combobox_contrast()
        HighContrastManager.toggle_high_contrast(False)

def setLuminosity():
    # print(scl_lumi.get())
    Luminosity.set(scl_lumi.get())
    showinfo(
            title='Result',
            message=f'La luminosite est "{scl_lumi.get()}" !'
        )
    
     

if __name__ == '__main__':
    window=tk.Tk()
    window.title("Accessibilite sur windows")
    window.geometry("750x750")


    frm_resolution=tk.Frame(master=window)
    frm_orientation=tk.Frame(master=window)
    frm_luminosity=tk.Frame(master=window)
    frm_contrast=tk.Frame(master=window)
    frm_police=tk.Frame(master=window)


    #  Screen resolution
    lbl_resolution=ttk.Label(master=frm_resolution, text="Resolution de l'écran", font=("Algerian",  15))
    lbl_resolution.configure(anchor="center")

    var_resolution=tk.StringVar(master=frm_resolution)
    cmbx_resolution=ttk.Combobox(master=frm_resolution, textvariable=var_resolution)
    cmbx_resolution['values']=lis_resolution
    cmbx_resolution['state']='readonly'
    cmbx_resolution.current(lis_resolution.index(default_resolution))

    btn_resolution=tk.Button(master=frm_resolution, text="Appliquer", command=setResolution)

    lbl_resolution.grid(row=0, column=0, padx=6, pady=10, sticky="NW")
    cmbx_resolution.grid(column=0, row=1, sticky='NW', padx=10)
    btn_resolution.grid(column=0, row=1, padx=5, sticky="NE")

    # Screen Orientation
    lbl_orientation=tk.Label(master=frm_orientation, text="Orientation de l'écran", font=("Algerian",  15))

    var_orientation=tk.StringVar(master=frm_orientation)
    cmbx_orientation=ttk.Combobox(master=frm_orientation, textvariable=var_orientation)
    cmbx_orientation['values']=lis_orientation
    cmbx_orientation['state']='readonly'
    cmbx_orientation.current(lis_orientation.index(default_orientation))

    btn_orientation=tk.Button(master=frm_orientation, text="Appliquer", command=setOrientation)

    lbl_orientation.grid(row=0, column=0, padx=6, pady=10, sticky="NW")
    cmbx_orientation.grid(column=0, row=1, sticky='NW', padx=20)
    btn_orientation.grid(column=0, row=1, padx=5, sticky="NE")

    # Luminosity
    lbl_lumi=ttk.Label(master=frm_luminosity, text="Luminosité", font=("Algerian",  15))
    scl_lumi=tk.Scale(master=frm_luminosity, from_=0, to=100, orient=tk.HORIZONTAL)
    scl_lumi.set(Luminosity.get())

    btn_lumi=tk.Button(master=frm_luminosity, text="Appliquer", command=setLuminosity)
    # scl_lumi.pack()

    lbl_lumi.grid(row=0, column=0, padx=6, pady=10, sticky="NW")
    scl_lumi.grid(column=0, row=1, sticky='NE', padx=5)
    btn_lumi.grid(column=1, row=1, pady=15, sticky="NE")


    #High Contrast
    lbl_contrast=ttk.Label(master=frm_contrast, text="High Contrast", font=("Algerian",  15))

    var_contrast=tk.IntVar(master=frm_contrast, value=default_contrast_enable)
    # values={"Active":True, "Desactiver":False}
    rdbtn_active=ttk.Radiobutton(master=frm_contrast, text="Active", variable=var_contrast, value=1, command=on_radio_change_contrast)
    rdbtn_desactive=ttk.Radiobutton(master=frm_contrast, text="Desactiver", variable=var_contrast, value=0, command=on_radio_change_contrast)

    lbl_contrast_list=ttk.Label(master=frm_contrast, text="Choisir un theme", font=("Algerian",  10))
    var_contrast_list=tk.StringVar(master=frm_contrast)
    cmbx_contrast=ttk.Combobox(master=frm_contrast, textvariable=var_contrast_list)
    cmbx_contrast['values'] = lis_contrast
    # cmbx_contrast['state']='readonly'
    # cmbx_contrast['state']='disabled'
    cmbx_contrast.current(lis_contrast.index(default_contrast_theme))
    btn_contrast=tk.Button(master=frm_contrast, text="Appliquer", command=setContrast)
    # btn_contrast['state']="disabled"

    lbl_contrast.grid(column=0, row=0, padx=6, pady=10, sticky="NW")
    rdbtn_active.grid(row=1, column=0, padx=10, sticky="NW")
    rdbtn_desactive.grid(row=1, column=1, padx=5, sticky="NW")


    lbl_contrast_list.grid(column=0, row=2, padx=10, sticky="NW")
    cmbx_contrast.grid(row=3, column=0, sticky="NW", padx=10)
    btn_contrast.grid(row=3, column=1)

    #Police
    lbl_police=ttk.Label(master=frm_police, text="Police", font=("Algerian",  15))
    var_police=tk.StringVar(master=frm_police)
    cmbx_police=ttk.Combobox(master=frm_police, textvariable=var_police)
    cmbx_police['values']=lis_police
    cmbx_police['state']='readonly'
    btn_police=tk.Button(master=frm_police, text="Appliquer")

    lbl_police.grid(column=0, row=0, padx=10, sticky="NW")
    cmbx_police.grid(row=1, column=0, sticky="NW", padx=10)
    btn_police.grid(row=1, column=1)


    frm_contrast.grid(row=2, column=1, sticky="NW")
    frm_orientation.grid(row=1, column=1, sticky="NW")
    frm_resolution.grid(row=0, column=1, sticky="NW")
    frm_luminosity.grid(row=4, column=1, sticky="NW")
    frm_police.grid(row=3, column=1, sticky="NW")





    on_radio_change_contrast()


    window.mainloop()