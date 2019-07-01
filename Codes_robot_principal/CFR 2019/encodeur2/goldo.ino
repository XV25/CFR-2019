





void catch_gold(float dist_a_mur, float dist_origine) // commande : 4
{ 
  // Attrape le goldenium placé à [dist_a_mur] du robot, sachant que le bras se trouve à la distance [dist_origine] de son point de départ.
  
  // Vérifie que le robot soit suffisamment proche du palet : si ce n'est pas le cas,
  // annule la commande (le bras sortirait trop loin et se bloquerait sinon)
  // La distance vérifiée est dist_a_mur + [épaisseur du mur détecté = 24-29 mm]
  if ( (dist_a_mur + 24 ) > 150)  
    {
    
    //Serial.println("Erreur : supérieur à la distance maximale d'avancement du bras. Commande annulée.\n ");
    
    }
 
 else{  

      // angles du servo1 : servomoteur pour monter / descendre le bras
      angle_preh = 89; // angle de préhension des palets
      float angle_attente =80; // angle après préhension des palets
    
      // angles du servo2 : servomoteur pour serrer la pince
      angle_ouv = 115;   //angle d'ouverture de la pince : peut varier entre 115-120
      angle_serr = 25; // angle de fermeture de la pince : peut varier entre 25-40
      
      int i = 0;
      float rapp_avancement = 0.1833; // distance parcourue pour un step commandé sur le 
                                      // moteur pas-à-pas. Déterminé via calibrage.
    
    
      // Détermination de la distance à parcourir par le bras pour récupérer le palet.
      // Correspond à la distance entre le robot et le mur + l'épaisseur du mur détecté [24-29mm]
      // - la distance actuelle du bras [dist_origine]
      float avancement_mm = dist_a_mur - dist_origine +29 ; 
      
      //Serial.println("Avancement pour palet : ");
      //Serial.print(avancement_mm);
     
      float conversion_step = avancement_mm/rapp_avancement;

    
      // étape 1 : mise en position pour préhension et rapprochement de la cible

      Servo2.write(angle_ouv);       
      Servo1.write(angle_preh);
      // ATTENTION : L'ARDUINO NE SEMBLE PLUS ETRE CAPABLE DE
      // REPONDRE PENDANT LE FONCTIONNEMENT DU STEPPER MOTOR!
      myStepper.step(conversion_step);
      
      // étape 2 : serrage progressif de la pince
      while (angle_serr - i>10)     // angle_serr -i doit être > 6
        {
          tps = millis();
          while ( (millis() - tps) < 25) // peut aller jusqu'à 100
            {
            Servo1.write(angle_preh);
            Servo2.write(angle_serr-i);
            }
          i++;
        }
      
      // étape 3 : relèvement du bras pour assurer la capture du goldenium
      int j = 0;
      while (angle_preh-j*0.8>angle_attente)
       // angle_preh - j*0.8 doit être > 73 : sinon, le bras se soulève trop
       // et le palet cogne la caméra.
       // On multiplie par 0.8 pour assurer un soulèvement lent du bras.
       {
          tps = millis();
          while ( (millis() - tps) < 25) 
              {
              Servo1.write(angle_preh-j*0.8); 
              Servo2.write(angle_serr-i);
              }
          j++;
       }
    
      // étape 4 : recul final du bras jusqu'à sa position d'origine.
      myStepper.step(-conversion_step);
      // sauvegarde des nouvelles valeurs pour les servomoteurs dans le
      // programme principal (angle_c_[1/2] étant des variables globales)
      angle_c_1 = angle_preh-i;
      angle_c_2 = angle_serr-j*0.8;
  
  }
}


void goldonium(){
  Serial.println("procedure goldonium");
  float dist = catch_dist(10);
  catch_gold(dist+25,dist_ori);
  Serial.println('f');
}
