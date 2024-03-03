import time                         #importer la librairie

commandes_possible=['0','1','2','3','4','5','6','7','8','9','*','#','A','B','C','D']    #Commandes acceptées
code_utilisateur={('000'):['0','0','0','0'], ('001'):['1','1','1','1']}                 #Codes des utilisateur
code_public=['1','2','3','4']                                                           #Code publis
code_installateur=['#','1','2','3','4','5','6']                                         #Code d'installateur
liste_commandes=[]                                     #Liste dans lequel s'inserera les commandes à executer
mode_installateur=False                                #Etat du mode programmateur
nb_refus_acces=0                                       #Nombre de refus
temps_verrouillage=5                                   #Temporisation de l'ouverture
etat_alarme_sabotage = True                            #Etat de l'alarme anti-sabotage
MDP_et_carte = False                                   #Accès avec carte et code 
MDP_ou_carte = True                                    #Accès avec carte ou code
Modification_MDP_possible = True                       #Droit de modifier les codes
temps_retard_alarme = 3                                #Temps pour activer l'alarme

def chronometre(temps):            #Fonction chronometre avec paramètre temps
    while temps>0:                 #Boucle while, marchera tant que le temps sera égale à 0
        print(temps)               #Afficher le temps
        time.sleep(1)              #Mettre en pause d'une seconde
        temps -= 1                 #Decrémentation du temps


def verfication_commande(liste):#Fonction qui permettra de vérifier si l'ensemble des caractères correspondent à une fonctionalité
    global mode_installateur;   #Généraliser les variables pour qu'elles utilisent dans tout le code
    global liste_commandes;
    global code_installateur;
    global temps_verrouillage;
    global code_public;
    global nb_refus_acces;
    global etat_alarme_sabotage;
    global MDP_et_carte;
    global MDP_ou_carte;
    global Modification_MDP_possible;
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

        if mode_installateur == True:                   #Si le mode_installateur est activé (True)
            if liste[0] == '0':                         #Si le 1er cactère est 0
                print("code de programmation")          
                liste_commandes=[]                      
                nouveau_code = ['#']                    #La liste nouveau_code débute avec un #
                while len(nouveau_code) < 7:            #Tant que la liste nouveau_code fait moins de 7 caractères
                    response2 = input()                 #Prendre la réponse de installateur dans une variable reponse2
                    if response2 in commandes_possible: #Si reponse2 est un caractres autorisé
                        nouveau_code.append(response2)  #ajouter le caractère dans la liste nouveau_code
                        print(nouveau_code)             

                if len(nouveau_code) == 7:              #Si il y a 7 caractère dans la liste nouveau_code
                    print("Code modifié")               
                    code_installateur=nouveau_code      #Le code_installateur sera remplacé par le code inséré dans le nouveau_code
                    liste_commandes=[]


            elif liste[0] == '1':                       #Si le 1er cactère est 1
                if liste[1] == '0':                     #Si le 2eme cactère est 0
                    MDP_et_carte = False                #Desactiver l'accès avec carte et code
                    MDP_ou_carte = True                 #Activer l'accès avec carte ou code
                    print("carte ou MDP")
                    liste_commandes=[]

                elif liste[1] == '1':                   #Si le 2eme cactère est 1
                    MDP_et_carte = True                 #Activer l'accès avec carte et code
                    MDP_ou_carte = False                #Désactiver l'accès avec carte ou code
                    print("carte et MDP")
                    liste_commandes=[]

                elif liste[1] == '2':                   #Si le 2eme cactère est 0
                    Modification_MDP_possible = False   #Ne pas permettre de modifier le code
                    print("modifi. desactive")
                    liste_commandes=[]

                elif liste[1] == '3':                   #Si le 2eme cactère est 3
                    Modification_MDP_possible = True   #Donner le droit de modifier le code
                    print("La modifi. active")
                    liste_commandes=[]


            elif liste[0] == '2':                       #Si le 1er cactère est 2
                print("temporisation")
                nouveau_temps = []
                liste_commandes=[]
                #Ici on insère un par un les 2 chiffres pour la temporisation
                while len(nouveau_temps) < 2:
                    response3 = input()
                    if response3 in commandes_possible:
                        nouveau_temps.append(response3)
                        print(nouveau_temps)

                if len(nouveau_temps) == 2:                 #Si il y a 2 caractère dans la liste nouveau_temps
                    temps_verrouillage=float(nouveau_temps) #Remplacer la temps_verrouillage par le nouvea_temps
                    print("Temp. modifié :")
                    liste_commandes=[]

            elif liste[0] == '3':                       #Si le 1er cactère est 3
                print("nouveau code")
                nouveau_CP = []
                liste_commandes=[]
                #Ici on insère un par un les 4 chiffres pour le code public
                while len(nouveau_CP) < 4:
                    response4 = input()
                    if response4 in commandes_possible:
                        nouveau_CP.append(response4)
                        print(nouveau_CP)

                if len(nouveau_CP) == 4:                #Si il y a 4 caractère dans la liste nouveau_CP
                    print("Code modifie")
                    code_public=nouveau_CP              #Remplacer la code_public par le code nouveau_CP
                    liste_commandes=[]

            elif liste[0] == '4':                       #Si le 1er cactère est 4
                if liste[1] == '0':                     #Si le 2eme cactère est 0
                    etat_alarme_sabotage = False        #Désactiver l'alarme anti-sabotage
                    print("alarme dsact")
                    liste_commandes=[]

                elif liste[1] == '1':                    #Si le 2eme cactère est 1
                    etat_alarme_sabotage = True         #Activer l'alarme anti-sabotage
                    print("alarme active")
                    liste_commandes=[]

            elif liste[0] == '5':                       #Si le 1er cactère est 5
                print("num serie ")
                numero_serie = []
                liste_commandes=[]
                #Ici on insère un par un les 3 chiffres pour le numéro de série d'utilisateur
                while len(numero_serie) < 3:
                    response4 = input()
                    if response4 in commandes_possible:
                        numero_serie.append(response4)
                        print(numero_serie)

                if len(numero_serie) == 3:
                    print("code usager")
                    code_nouv_util = []

                    #Ici on insère un par un les 4 chiffres du code d'utilisateur
                    while len(code_nouv_util) < 4:
                        response5 = input()
                        if response5 in commandes_possible:
                            code_nouv_util.append(response5)
                            print(code_nouv_util)

                    if len(code_nouv_util) == 4:
                        print("Utilisateur sauvegarde")
                        code_utilisateur[numero_serie]=code_nouv_util   #Ajouter le nouveau code associer à la clé comme le N° Série

            elif liste[0] == '7':                       #Si le 1er cactère est 7
                print("N a supprimer")
                numero_serie_a_supprimer = []
                liste_commandes=[]

                #Ici on insère un par un les 3 chiffres du N° Série à supprimer
                while len(numero_serie_a_supprimer) < 3:
                    response5 = input()
                    if response5 in commandes_possible:
                        numero_serie_a_supprimer.append(response5)
                        print(numero_serie_a_supprimer)

                if len(numero_serie_a_supprimer)==3:
                    code_utilisateur.pop(numero_serie_a_supprimer)#Supprimer l'utilisateur
                    print('utilisateur Supprime')


            elif liste[0] == 'A':                   #Si le 1er caractère est A 
                mode_installateur = False           #Quitter le mode programmation
                print('prog desact')
                liste_commandes=[]



    except:                                             #Le code sera forcé de fonctionner sauf
        pass                                            #pass signifier rien

while True:                                             #Boucle infini car vrai sera vrai comme 2==2
    response = input()                                  #Le caractère à insérer sera taper dans la boîte de dialogue
    if response in commandes_possible:                  #Si l'insertion correspond à une commande possible
        liste_commandes.append(response)                #Ajouter le caractère dans la liste_commandes

    try:
        if len(liste_commandes) > 1 and response=='#':  #Si après quelques appuies, on appuie # donc
            liste_commandes=[]                          #Vider la liste_commandes
    except:
        pass

    verfication_commande(liste_commandes)               #Appel à la fonction pour vérifier la liste_commandes

    if nb_refus_acces >= 3:                             #Si il refuse plus de 3 fois donc
        time.sleep(temps_retard_alarme)
        i=0                                             #Renitialisation de i
        while i < 5:                                    #Tant que i est inférieure à 5
            print("acces bloque")                       #Afficher "Accès bloqué"
            time.sleep(1)                               #Pause d'une seconde
            i = i + 1                                   #Incrémentation de i
        nb_refus_acces=0                                #Remettre à 0 le nombre de refus