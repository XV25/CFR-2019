communication entre la carte arduino base roulante/rasp :

# important ! a chaque nouvelle fonction, �crire ici la commande utilis�e !

's'=115 : fonction ledOn => allume la led sur le pin 10
'z'=122 : fonction ledOff => �teind la led sur le pin 10
'l'=108 : fonction leftMotor => d�marre le moteur gauche, necessite de serial.write dir et pwm(dans le code python) et �crit dans le port s�rie 3 ligne : message + dir + vitesse
'r'=114 : fonction rightMotor => d�marre le moteur droit, necessite de serial.write dir et pwm(dans le code python) et �crit dans le port s�rie 3 ligne : message + dir + vitesse