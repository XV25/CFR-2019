
void boutonPoussoir(float dist_a_palet, float dist_origine){
    
   float p_sc;
   angle_c_2 = 20;
   Servo2.write(angle_c_2);
   Servo1.write(83);
   dist= move_arm(dist_a_palet,dist_ori);
}


void pousseBouton(){
  Serial.println("procedure pousse palet");
  dist = catch_dist(10);
  dist = dist +12;
  boutonPoussoir(dist,dist_ori);
  Serial.println('f');
}
