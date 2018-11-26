# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 17:11:23 2018

@author: Enzin
"""

import requests, time
#user='enzo.vieira@reseau.eseo.fr'
#pas='MDPProjetSi2018'        surement a utiliser plus tard pour refresh les cookie (possibilité d'automatiser)
# avec from requests.auth import HTTPDigestAuth
#from requests.auth import HTTPDigestAuth


urlmeteo='http://www.prevision-meteo.ch/services/json/savigny-sur-orge'
urlbus385='https://api-lab-trone-stif.opendata.stif.info/service/tr-vianavigo/departures?line_id=100100385%3A385&stop_point_id=StopPoint%3A59%3A6195778'

#liste des condition météo ---------------------------------------------------------
Ensoleillé = ['Ensoleillé', 
              'Nuit bien dégagée', 
              'Eclaircies', 
              'Faibles passages nuageux',
              'Faiblement nuageux',
              'Nuit légèrement voilée',
              'Nuit claire et stratus',
              'Nuit claire'
              ]

Nuageux = ['Ciel voilé',
           'Brouillard',
           'Nuit nuageuse',
           'Fortement nuageux',
           'Développement nuageux',
           'Nuit avec développement nuageux'
           ]

Pluvieux = ['Stratus',
            'Stratus se dissipant',
            'Averses de pluie faible',
            'Averses de pluie modérée',
            'Averses de pluie forte',
            'Couvert avec averses',
            'Pluie faible',
            'Pluie forte',
            'Pluie modérée',
            'Faiblement orageux',
            'Nuit faiblement orageuse',
            'Orage modéré',
            'Fortement orageux',
            'Pluie et neige mêlée faible',
            'Pluie et neige mêlée modérée',
            'Pluie et neige mêlée forte'
            ]

Neige = ['Averses de neige faible',
         'Nuit avec averses de neige faible',
         'Neige faible',
         'Neige forte',
         ]

#----------------------------------------------------------------------------------------

#nuit ou non ?--------------------------------------------------------------------------

def jour(temp_réel,sunrise,sunset):
    heuretemps = int(temp_réel[:2])
    minutetemps = int(temp_réel[3:])
    heuredébut = int(sunrise[:2])
    minutedébut = int(sunrise[3:])
    heurefin = int(sunset[:2])
    minutefin = int(sunset[3:])
    
    if (((heuretemps<=heuredébut) and (minutetemps<minutedébut)) or ((heuretemps>=heurefin) and (minutetemps>minutefin))):
        etatjour=False
    elif(heuretemps<heuredébut or heuretemps>heurefin):
        etatjour=False
    else:
        etatjour=True

    return etatjour
        

#--------------------------------------------------------------------------------------

#choix de la condition a afficher---------------------------------------------------
def choixtemps(condi):
    
    if condi in Nuageux :
        print ('Nuageux')
    if condi in Pluvieux :
        print('Pluvieux')
    if condi in Ensoleillé :
        print('Ensoleillé')
    if condi in Neige :
        print('Neige')  
        
#-------------------------------------------------------------------------------------------
def takedata():
    Databrut = requests.get(urlmeteo) 
    datameteo = Databrut.json()
    jar = requests.cookies.RequestsCookieJar()
    jar.set('sessionid','eqj7aszlxj9ucsb55dzcedpyxugd7wod',domain='api-lab-trone-stif.opendata.stif.info',path='/')
    busdatabrut = requests.get(urlbus385, cookies=jar)
    databus = busdatabrut.json()

#-----------------------------------------------------------------------------------------------
    sunrise = datameteo['city_info']['sunrise']
    sunset = datameteo['city_info']['sunset']
    temp_réel = time.strftime('%H:%M')
#condition météorologique

    condi = datameteo['current_condition']['condition']


    tempé =  datameteo['current_condition']['tmp']
    
   
    return condi,sunrise,sunset,temp_réel,datameteo,Databrut,tempé,databus

def afficherjour(etatjour):
    
    if etatjour == True:
        print("jour")
    else:
        print("nuit")
        
def horairebus(databus):
    direction = databus[0]['lineDirection']
    if direction == 'Suivant a + De' :
        print('--')
    
    elif direction == 'Savigny Toulouse-Lautrec' or direction == 'Epinay-Sur-Orge RER' :
        code = databus[0]['code']
        if code == 'duration' :
            dirgaresav = databus[0]['time']
            print(dirgaresav+ " minutes")
        else :
            print("0 minute")
    else :
        direction = databus[1]['lineDirection']
        if direction == 'Savigny Toulouse-Lautrec' or direction == 'Epinay-Sur-Orge RER' :
            code = databus[1]['code']
            if code == 'duration' :
                dirgaresav = databus[1]['time']
                print(dirgaresav+ " minutes")
            else:
                print("0 minute")
        else:
            direction = databus[2]['lineDirection']
            if direction == 'Savigny Toulouse-Lautrec' or direction == 'Epinay-Sur-Orge RER' :
                code = databus[2]['code']
            if code == 'duration' :
                dirgaresav = databus[2]['time']
                print(dirgaresav+ " minutes")
            else:
                print("0 minute")
            

def main():
    
#while méteo
    
    while True:
        
        condi,sunrise,sunset,temp_réel,data,Databrut,tempé,databus = takedata()
        print("sunrise :",sunrise)   
        print(time.strftime('%H:%M'))
        print("sunset :",sunset)
        etatjour=jour(temp_réel, sunrise, sunset)
        afficherjour(etatjour)       
        choixtemps(condi)     
        print(tempé,"°C")  
        print(' ')
        horairebus(databus)
        print('----------------------------')
    
    #if étatjour== True pas allumé led 
    #sinon allumé led ( il fait nuit)
    
        time.sleep(60)
        
if __name__=="__main__":main()