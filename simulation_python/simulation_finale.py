import time
import serial
import pyfirmata
import keyboard
from pyfirmata import Arduino, util, STRING_DATA

board = Arduino('COM7')


#led_pin = board.get_pin('d:9:o')
led_pin_r = board.get_pin('d:8:o')
led_pin_b = board.get_pin('d:10:o')
led_pin_g = board.get_pin('d:9:o')

buzzer = board.get_pin('d:11:o')
servo = board.get_pin('d:{}:s'.format(12))
servo.write(60)

commandes_possible=['0','1','2','3','4','5','6','7','8','9','*','#','A','B','C','D']
code_utilisateur=[['1','2','3','4'],['0','0','0','0'],['4','4','4','4'],]
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


def rgb_led(r,g,b):
    led_pin_r.write(r)
    led_pin_g.write(g)
    led_pin_b.write(b)


def list_a_str(s):
    if type(s)==list:
        str1 = " "
        response=str1.join(s)
    else:
        response=s
    return response


def versLCD(text):
    board.send_sysex(STRING_DATA,util.str_to_two_byte_iter(list_a_str(text)))


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

    versLCD(liste)

    try:
        if liste[0] != '#':
            if len(liste) == 4:
                if liste == code_utilisateur[0] or liste == code_utilisateur[1] or liste == code_utilisateur[2]:
                    versLCD('accès ouvert')
                   # led_pin.write(1)
                    rgb_led(1,0,0)
                    servo.write(110)
                    buzzer.write(1)
                    time.sleep(0.3)
                    buzzer.write(0)
                    liste_commandes=[]
                    a=chronometre(temps_verrouillage)
                    if a != 0:
                        versLCD('accès fermé')
                        rgb_led(0,0,0)
                        servo.write(60)
                        buzzer.write(0)

                else:
                    versLCD('accès refusé')
                    liste_commandes=[]
        else:
            if len(liste) == 7:
                if liste == code_installateur:
                    liste_commandes=[]
                    mode_installateur = True
                    versLCD('mode programateur activé')
                    rgb_led(0,1,0)
                else:
                    mode_installateur = False
                    versLCD('mode programateur refusé')
                    rgb_led(0,0,0)
                    liste_commandes=[]

        if mode_installateur == True:

            if liste[0] == '1':
                if liste[1] == '0':
                    MDP_et_carte = False
                    MDP_ou_carte = True
                    versLCD("Nécéssité de la carte ou MDP pour rentrer")
                    liste_commandes=[]

                elif liste[1] == '1':
                    MDP_et_carte = True
                    MDP_ou_carte = False
                    versLCD("Nécéssité de la carte et MDP pour rentrer")
                    liste_commandes=[]

                elif liste[1] == '2':
                    Modification_MDP_possible = False
                    versLCD("La modification des MDP utilisateur est impossible")
                    liste_commandes=[]

                elif liste[1] == '3':
                    Modification_MDP_possible = True
                    versLCD("La modification des MDP utilisateur est possible")
                    liste_commandes=[]

            elif liste[0] == '8':
                if liste[1] == '0':
                    etat_alarme_verrouillage = False
                    versLCD("L’alarme de verrouillage est desactivée")
                    liste_commandes=[]

                elif liste[1] == '1':
                    etat_alarme_verrouillage = True
                    versLCD("L’alarme de verrouillage est activée")
                    liste_commandes=[]

            elif liste[0] == '4':
                if liste[1] == '0':
                    etat_alarme_sabotage = False
                    versLCD("L’alarme anti-sabotage désactivée")
                    liste_commandes=[]

                elif liste[1] == '1':
                    etat_alarme_sabotage = True
                    versLCD("L’alarme anti-sabotage sactivée")
                    liste_commandes=[]

            if liste[0] == '0':
                versLCD("Insérer le nouveau code de programmation")
                nouveau_code = ['#']
                liste_commandes=[]
                while len(nouveau_code) < 7:
                    response2 = input("mdp nv")
                    if response2 in commandes_possible:  # Vérifie si la réponse est une commande possible
                        versLCD(response2)
                        nouveau_code.append(response2)

                if len(nouveau_code) == 7:
                    versLCD("Code de programmation modifié :")
                    code_installateur=nouveau_codeq
                    liste_commandes=[]

            elif liste[0] == 'A':
                mode_installateur = False
                rgb_led(0,0,0)
                versLCD('mode programateur desactivé')
                liste_commandes=[]

    except:
        pass



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