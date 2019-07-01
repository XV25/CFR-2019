void catch_buck(float dist_a_mur, float dist_origine)
{
  // Attrape le palet placé à [dist_a_mur] du robot, sachant que le bras se trouve à la distance [dist_origine] de son point de départ.
  
  
  // Vérifie que le robot soit suffisamment proche du palet : si ce n'est pas le cas,
  // annule la commande (le bras sortirait trop loin et se bloquerait sinon)
  // La distance vérifiée est dist_a_mur + [épaisseur du mur détecté = 24-29 mm]
  if ( (dist_a_mur + 25) > 150)
    {
    //Serial.println("Erreur : supérieur à la distance maximale d'avancement du bras. Commande annulée.\n ");
    }
  
  else
    {
    
    // angles du servo1 : servomoteur pour monter / descendre le bras
    float angle_attente =95; // angle après préhension des palets
    angle_preh = 115; // angle de préhension des palets. Compris entre 115-105.
    
    // angles du servo2 : servomoteur pour serrer la pince
    angle_ouv = 105;   //angle d'ouverture de la pince : peut varier entre 105-120
    angle_serr = 40; // angle de fermeture de la pince : peut varier entre 25-40
    
     
    float rapp_avancement = 0.1833; // distance parcourue pour un step commandé sur le 
                                      // moteur pas-à-pas. Déterminé via calibrage.
    

    // Détermination de la distance à parcourir par le bras pour récupérer le palet.
    // Correspond à la distance entre le robot et le mur + l'épaisseur du mur détecté [25-38mm]
    // - la distance actuelle du bras [dist_origine]
    float avancement_mm = dist_a_mur - dist_origine + 38; 
    
    //Serial.println("Avancement pour palet : ");
    //Serial.print(avancement_mm);
    
    float conversion_step = avancement_mm/rapp_avancement;

  
    // étape 1 : mise en position pour préhension du palet
    Servo2.write(angle_serr);   
    delay(30);
    Servo1.write(angle_preh);
    delay(30);
    Servo2.write(angle_ouv);
    
    // étape 2 : rapprochement de la cible
    
    // ATTENTION : L'ARDUINO NE SEMBLE PLUS ETRE CAPABLE DE
    // REPONDRE PENDANT LE FONCTIONNEMENT DU STEPPER MOTOR!
    
    myStepper.step(conversion_step);
  
     // étape 3 : serrage progressif de la pince
     int i = 0;
     while (angle_serr - i>20)     // angle_serr -i doit être > 6
        {
          tps = millis();
          while ( (millis() - tps) < 25) // peut aller jusqu'à 100
            {
              Servo1.write(angle_preh);
              Servo2.write(angle_serr-i);
            }
          i++;
        }
      
    // étape 4 : relèvement du bras pour assurer la capture tout en effectuant
    // un recul progressif pour éviter de se cogner contre le bord du support du palet.
    int j = 0;
    float dist_recul = 0; // sauvegarde de la distance totale de recul
    while (angle_preh - j > angle_attente)
     {
        
        tps = millis();
        while ( (millis() - tps) < 25) // possible d'aller jusqu'à 100 au besoin
            {
              Servo2.write(angle_serr-i);
              Servo1.write(angle_preh-j); 
            }
            
        if (j < 10)
            {
              // Recul du bras, sauvegarde de la distance reculée (exprimée en steps)
              // Correspond environ à 1mm reculé par étape.
              myStepper.step(-6); 
            }
        j++;
     }
  
    // étape 5 : recul final du bras jusqu'à sa position d'origine.
    Servo2.write(angle_serr-i);
    Servo1.write(angle_preh-j); 
    myStepper.step(-conversion_step+dist_recul);
    // sauvegarde des nouvelles valeurs pour les servomoteurs dans le
    // programme principal (angle_c_[1/2] étant des variables globales)
    angle_c_1 = angle_preh-i;
    angle_c_2 = angle_serr-j;
    }
}

void palet(){
  Serial.println("procedure palet");
  float dist = catch_dist(10);
  
  catch_buck(dist,dist_ori);
  Serial.println('f');
}
