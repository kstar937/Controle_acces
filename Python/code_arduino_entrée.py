import serial
import time

ser = serial.Serial('COM8', 9600)   #Mettre en place un connexion avec la carte
commandes_possible=['0','1','2','3','4','5','6','7','8','9','*','#','A','B','C','D']    #Commandes acceptées
code_utilisateur={('000'):['0','0','0','0'], ('001'):['1','1','1','1']}                 #Codes des utilisateur
code_public=['1','2','3','4']                                                           #Code publis
code_installateur=['#','1','2','3','4','5','6']                                         #Code d'installateur
liste_commandes=[]                                     #Liste dans lequel s'inserera les commandes à executer
mode_installateur=False                                #Etat du mode programmateur
nb_refus_acces=0                                       #Nombre de refus
temps_verrouillage=5                                   #Temporisation de l'ouverture
temps_retard_alarme = 3                                #Temps pour activer l'alarme
def chronometre(temps):            #Fonction chronometre avec paramètre temps
    while temps>0:                 #Boucle while, marchera tant que le temps sera égale à 0
        print(temps)               #Afficher le temps
        time.sleep(1)              #Mettre en pause d'une seconde
        temps -= 1                 #Decrémentation du temps


#Cette fonction reste identique à celui de la simulation
def verfication_commande(liste):#Fonction qui permettra de vérifier si l'ensemble des caractères correspondent à une fonctionalité
    global mode_installateur;   #Généraliser les variables pour qu'elles utilisent dans tout le code
    global liste_commandes;
    global code_installateur;
    global temps_verrouillage;
    global code_public;
    global nb_refus_acces;
    global temps_retard_alarme;
    global code_utilisateur;

    try:                             #Forcer le code à fonctionner même lors d'une erreur
        if liste[0] != '#':          #Si le 1er caractère n'est pas un # 
            if len(liste) == 4:      #Si il y a 4 caractères
                if liste in code_utilisateur.values():  #Si le code inséré correspond à l'un des codes de la liste 
                    print('acces ouvert')               #Afficher "accès ouvert"
                    liste_commandes=[]                  #Rénitialiser la liste liste_commandes
                    a=chronometre(temps_verrouillage)   #Appel au chronometre en envoyant le temps de verrouillage
                    if a != 0:                          #Lorsque le compte est fini
                        print('acces ferme')            #Afficher "accès fermé"

                if liste == code_public:                #Si le code correspond au code_public
                    if verification_public():           #Appel à une fonction pour vérifier, Si elle reenvoie True
                        print('acces ouvert')               #Afficher "accès ouvert"
                        liste_commandes=[]                  #Rénitialiser la liste liste_commandes
                        a=chronometre(temps_verrouillage)   #Appel au chronometre en envoyant le temps de verrouillage
                        if a != 0:                          #Lorsque le compte est fini
                            print('acces ferme')            #Afficher "accès fermé"
                    else:
                        print("acces impossi.")

                else:                                   #Sinon
                    print('acces refuse')               #Afficher "accès refusé"
                    nb_refus_acces = nb_refus_acces + 1 #Incrémenter le nb_refus_acces
                    liste_commandes=[]
        else:                                           #Si le 1er caractère inséré est #
            if len(liste) == 7:                         #Si la commande inséré fait 7 caractères
                if liste == code_installateur:          #Si la commande correspond au code programmateur
                    liste_commandes=[]
                    mode_installateur = True            #Activé le mode installateur
                    print('prog. active')               #Afficher "prog. active"
                else:
                    mode_installateur = False           #Desactivé le mode installateur
                    print('prog. refuse')               #Afficher "prog. refuse"
                    liste_commandes=[]

    except:                                             #Le code sera forcé de fonctionner sauf
        pass                                            #pass signifier rien

def verification_public():
    t=time.localtime()                                  #Obtient l'heure locale par l'ordinateur
    temps_actuel = time.strftime("%H:%M:%S",t)          #Filtre les données qu'on veut afficher
    if "13:00:00"<temps_actuel<"16:00:00":              #Si l'heure actuel est entre 13h et 16h
        return True                                     #Retourne True
    else:                                               #Sinon
        return False                                    #Retourne False




while True:
    response = ser.readline().decode('ascii').rstrip() #Lecture des données envoyées par la carte
    if response in commandes_possible:                 #Si la réponse est une commande autorisé
        liste_commandes.append(response)               #Ajouter le caractère dans la liste

    try:
        if len(liste_commandes) > 1 and response=='#':
            liste_commandes=[]



    except:
        pass
