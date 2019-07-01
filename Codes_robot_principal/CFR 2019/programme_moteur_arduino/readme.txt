communication entre la carte arduino base roulante/rasp :

# important ! a chaque nouvelle fonction, écrire ici la commande utilisée !

's'=115 : fonction ledOn => allume la led sur le pin 10
'z'=122 : fonction ledOff => éteind la led sur le pin 10
'l'=108 : fonction leftMotor => démarre le moteur gauche, necessite de serial.write dir et pwm(dans le code python) et écrit dans le port série 3 ligne : message + dir + vitesse
'r'=114 : fonction rightMotor => démarre le moteur droit, necessite de serial.write dir et pwm(dans le code python) et écrit dans le port série 3 ligne : message + dir + vitesse