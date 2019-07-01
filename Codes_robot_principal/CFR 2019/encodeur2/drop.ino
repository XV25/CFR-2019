

double drop_buck(float dist_ori)
{
  // Programme permettant de déposer le palet dans la balance
  
   dist_ori = move_arm(150,dist_ori);
   angle_c_2 = 120;
   Servo2.write(angle_c_2);
   delay(1000);
   dist_ori = move_arm(-150,dist_ori);
}


float move_arm(float dist_avancement,float dist_ori)
{
  // Déplace le bras de [dist_avancement] mm. 
  //Renvoie ensuite la distance d'avancement effectuée.
  // dist_ori : distance à laquelle le bras se trouve actuellement. Permet de vérifier
  // que la commande entrée ne provoquera pas de problèmes.
  
  float rapp_avancement = 0.1833; // distance parcourue pour un step commandé sur le 
                                  // moteur pas-à-pas. Déterminé via calibrage.

  
  // Si la distance commandée fait que le bras serait placé à une distance supérieure
  // à 150mm (distance maximale pour le périmètre du bras), bloque cette commande 
  // pour que le bras s'arrête à 150mm.
  
  if (avancement_mm + dist_ori > 150)
    {
      avancement_mm = 150-dist_ori;
      float conversion_step = avancement_mm/rapp_avancement;
      myStepper.step(conversion_step);
      return(150);
      
    }
    
 // Si la distance commandée fait que le bras serait placé à une distance inférieure
 // à 0mm (distance de recul maximale), bloque cette commande pour que le bras s'arrête à 0mm.
 
  else if (avancement_mm + dist_ori <0)
    {
      avancement_mm = -dist_ori;
     float conversion_step = avancement_mm/rapp_avancement;
     myStepper.step(conversion_step);
     return(0);
    }

  else
    {
      float avancement_mm = dist_avancement;
      float conversion_step = avancement_mm/rapp_avancement;
      myStepper.step(conversion_step);
      return( avancement_mm);
    }

}


void balance(){
  Serial.println("procedure balance");
  drop_buck(dist_ori);
  Serial.println('f');
}
