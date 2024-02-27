import time
import serial
import pyfirmata
import keyboard
from pyfirmata import Arduino, util, STRING_DATA

ser = serial.Serial('COM8', 9600)
board = Arduino('COM7')


#led_pin = board.get_pin('d:9:o')
led_pin_1 = board.get_pin('d:8:o')
led_pin_2 = board.get_pin('d:9:o')
led_pin_3 = board.get_pin('d:10:o')

buzzer = board.get_pin('d:11:o')
servo = board.get_pin('d:{}:s'.format(12))
servo.write(180)

commandes_possible=['0','1','2','3','4','5','6','7','8','9','*','#','A','B','C','D']


code_utilisateur={('000'):['0','0','0','0'], ('001'):['1','1','1','1']}

code_public=['1','2','3','4']
code_installateur=['#','1','2','3','4','5','6']
liste_commandes=[]

mode_installateur = False
etat_alarme_sabotage = True
etat_alarme_verrouillage = True
MDP_et_carte = False
MDP_ou_carte = True
Modification_MDP_possible = True
temps_retard_alarme = 20
temps_verrouillage = 5

nb_refus_acces=0

def led(l1,l2,l3):
    led_pin_1.write(l1)
    led_pin_2.write(l2)
    led_pin_3.write(l3)


def list_a_str(s):
    if type(s)==list:
        str1 = " "
        response=str1.join(s)
    else:
        response=s
    return response

def list_a_str_cd(s):
    if type(s)==list:
        str1 = ""
        response=str1.join(s)
    else:
        response=s
    return response

def versLCD(text):
    board.send_sysex(STRING_DATA,util.str_to_two_byte_iter(list_a_str(text)))
    #print(text)


def chronometre(temps):
    while temps>0:
        print(temps)
        time.sleep(1)
        temps -= 1


def verfication_commande(liste):
    global mode_installateur;
    global etat_alarme_sabotage;
    global etat_alarme_verrouillage;
    global MDP_et_carte;
    global MDP_ou_carte;
    global Modification_MDP_possible;
    global temps_retard_alarme;
    global temps_verrouillage;
    global liste_commandes;
    global code_installateur;
    global code_public;
    global nb_refus_acces;

    versLCD(liste)

    try:
        if liste[0] != '#':
            if len(liste) == 4:
                if liste in code_utilisateur.values():
                    versLCD('acces ouvert')
                   # led_pin.write(1)
                    servo.write(90)
                    board.digital[8].write(1)
                    buzzer.write(1)
                    time.sleep(0.3)
                    buzzer.write(0)
                    liste_commandes=[]
                    a=chronometre(temps_verrouillage)
                    if a != 0:
                        versLCD('acces ferme')
                        servo.write(180)
                        board.digital[8].write(0)


                else:
                    versLCD('acces refuse')
                    nb_refus_acces = nb_refus_acces + 1
                    liste_commandes=[]
        else:
            if len(liste) == 7:
                if liste == code_installateur:
                    liste_commandes=[]
                    mode_installateur = True
                    versLCD('prog. active')
                else:
                    mode_installateur = False
                    versLCD('prog. refuse')
                    liste_commandes=[]

        if mode_installateur == True:

            if liste[0] == '0':
                versLCD("code de programmation")
                led(1,1,1)
                nouveau_code = ['#']
                liste_commandes=[]
                while len(nouveau_code) < 7:
                    response2 = ser.readline().decode('ascii').rstrip()
                    if response2 in commandes_possible:
                        nouveau_code.append(response2)
                        versLCD(nouveau_code)

                if len(nouveau_code) == 7:
                    versLCD("Code modifié")
                    led(1,1,1)
                    code_installateur=nouveau_code
                    liste_commandes=[]

            elif liste[0] == '1':
                led(1,0,0)
                if liste[1] == '0':
                    MDP_et_carte = False
                    MDP_ou_carte = True
                    versLCD("carte ou MDP")
                    liste_commandes=[]
                    led(1,1,1)

                elif liste[1] == '1':
                    MDP_et_carte = True
                    MDP_ou_carte = False
                    versLCD("carte et MDP")
                    liste_commandes=[]
                    led(1,1,1)

                elif liste[1] == '2':
                    Modification_MDP_possible = False
                    versLCD("modifi. desactive")
                    liste_commandes=[]
                    led(1,1,1)

                elif liste[1] == '3':
                    Modification_MDP_possible = True
                    versLCD("La modifi. active")
                    liste_commandes=[]
                    led(1,1,1)


            elif liste[0] == '2':
                versLCD("temporisation")
                led(0,1,0)
                nouveau_temps = []
                liste_commandes=[]
                while len(nouveau_temps) < 2:
                    response3 = ser.readline().decode('ascii').rstrip()
                    if response3 in commandes_possible:
                        nouveau_temps.append(response3)
                        versLCD(nouveau_temps)

                if len(nouveau_temps) == 2:
                    temps_verrouillage=float(list_a_str_cd(nouveau_temps))
                    versLCD("Temp. modifié :")
                    led(1,1,1)
                    liste_commandes=[]


            elif liste[0] == '3':
                versLCD("nouveau code")
                led(0,0,1)
                nouveau_CP = []
                liste_commandes=[]
                while len(nouveau_CP) < 4:
                    response4 = ser.readline().decode('ascii').rstrip()
                    if response4 in commandes_possible:
                        nouveau_CP.append(response4)
                        versLCD(nouveau_CP)

                if len(nouveau_CP) == 4:
                    versLCD("Code modifie")
                    code_public=nouveau_CP
                    liste_commandes=[]
                    led(1,1,1)



            elif liste[0] == '4':
                led(1,0,1)
                if liste[1] == '0':
                    etat_alarme_sabotage = False
                    versLCD("alarme dsact")
                    liste_commandes=[]
                    led(1,1,1)

                elif liste[1] == '1':
                    etat_alarme_sabotage = True
                    versLCD("alarme active")
                    liste_commandes=[]
                    led(1,1,1)




            elif liste[0] == '5':
                led(1,1,0)
                versLCD("num serie ")
                numero_serie = []
                liste_commandes=[]
                while len(numero_serie) < 3:
                    response4 = ser.readline().decode('ascii').rstrip()
                    if response4 in commandes_possible:
                        numero_serie.append(response4)
                        versLCD(numero_serie)

                if len(numero_serie) == 3:
                    versLCD("code usager")
                    code_nouv_util = []
                    while len(code_nouv_util) < 4:
                        response5 = ser.readline().decode('ascii').rstrip()
                        if response5 in commandes_possible:
                            code_nouv_util.append(response5)
                            versLCD(code_nouv_util)

                    if len(code_nouv_util) == 4:
                        versLCD("Utilisateur sauvegarde")
                        code_utilisateur[list_a_str_cd(numero_serie)]=code_nouv_util
                        led(1,1,1)




            elif liste[0] == '7':
                led(0,1,1)
                versLCD("N a supprimer")
                numero_serie_a_supprimer = []
                liste_commandes=[]
                while len(numero_serie_a_supprimer) < 3:
                    response5 = ser.readline().decode('ascii').rstrip()
                    if response5 in commandes_possible:
                        numero_serie_a_supprimer.append(response5)
                        versLCD(numero_serie_a_supprimer)

                if len(numero_serie_a_supprimer)==3:
                    code_utilisateur.pop(list_a_str_cd(numero_serie_a_supprimer))
                    versLCD('utilisateur Supprime')
                    led(1,1,1)



            elif liste[0] == 'A':
                mode_installateur = False
                led(0,0,0)
                versLCD('prog desact')
                liste_commandes=[]

    except:
        pass

while True:



    response = ser.readline().decode('ascii').rstrip()
    if response in commandes_possible:
        liste_commandes.append(response)


    try:
        if len(liste_commandes) > 1 and response=='#':
            liste_commandes=[]



    except:
        pass

    verfication_commande(liste_commandes)

    if nb_refus_acces >= 3:
        i=0
        while i < 10:
            buzzer.write(1)
            time.sleep(0.7)
            buzzer.write(0)
            i=i+1

'''


while True:
    response = input()
    if response in commandes_possible:
        liste_commandes.append(response)


    try:
        if len(liste_commandes) > 1 and response=='#':
            liste_commandes=[]
    except:
        pass

    verfication_commande(liste_commandes)
'''