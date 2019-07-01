
void poussePalet(float dist_a_faire, float dist_origine){
   // Sors le bras de dist_a_faire pour pouvoir pousser le palet,
   // sachant que le bras se trouve initialement à dist_origine
   
   // Met le bras au bon angle et avec la pince fermée (via respectivement
   // servo1 et servo2)
   Servo1.write(81);
   angle_c_2 = 20;
   Servo2.write(angle_c_2);
   
   // Avance le bras de la distance nécessaire, met à jour la position du bras
   // via dist_ori (sauvegardée car dist_ori est une variable globale)
   dist_ori= move_arm(dist_a_faire,dist_origine);
   
   
}

void retour(float dist_a_faire, float dist_origine){

  // Rentre le bras à l'intérieur du robot

  angle_c_2 = 90;
  Servo2.write(angle_c_2); // ouverture de la pince
  Servo1.write(70);  // soulèvement du bras pour confirmer le glissement du palet 
                     // dans l'accélérateur
                     
  // remise en position initiale du bras
  
  // A noter : dist_a_faire doit être négatif pour faire reculer le bras.
  // dist_origine correspond à la position actuelle du bras, dist_ori à la 
  // position à la fin du déplacement (qui sera sauvegardée)
  
  dist_ori = move_arm(dist_a_faire,dist_origine); 
  Servo1.write(90);
  }

void pousse(){
  Serial.println("procedure pousse palet");
  dist = catch_dist(10);
  dist = dist + 5;
  poussePalet(dist,dist_ori);
  Serial.println('f');
}


void retour(){
  Serial.println("procedure retour");
  retour(-dist,dist_ori);
  Serial.println('f');
}
