// Include the Servo library 
#include <Servo.h> 
#include <Stepper.h>
#define sensor A0 // Sharp IR GP2Y0A41SK0F (4-30cm, analog)


const int stepsPerRevolution = 203;//203; //202 // change this to fit the number of steps per revolution
//float rapp_avancement = 11/60;  //ici, en mm/step 0.1833mm par step
// for your motor

// initialize the stepper library on pins 8 through 11:
Stepper myStepper(stepsPerRevolution, 8, 9, 10, 11);//include <Stepper.h>


unsigned long tps;
// Declare the Servo pin 
int servoPin1 = 5; // servo pour monter / descendre le bras
int servoPin2 = 6; //servo pour serrer la pince
int tst = 0;
int k = 0;
Servo Servo1; 
Servo Servo2; 
double angle_preh = 0;
double angle_serr = 0;
double angle_ouv = 0;
double dist_ori = 0; // distance à laquelle le bras doit être placé initialement
float * p_cs; // contient le nombre de steps de déplacement par rapport à l'origine.

double angle_c_1 = 75;
double angle_c_2 = 90;
//char Instructions;
char Instructions[6];
char * commande;
size_t taille;
//String str_brs;
//String str_ang;
float arm_depl = 0;

void setup() { 
   // set the speed at 60 rpm:
  myStepper.setSpeed(70); // ou 60
  // initialize the serial port:
  Serial.begin(9600);
  analogReference(EXTERNAL);
  // We need to attach the servo to the used pin number 
  Servo1.attach(servoPin1); 
  Servo2.attach(servoPin2); 
}

void loop(){ 
// ATTENTION : LE BRAS NE PEUT S'AVANCER DE PLUS DE 150 MM! TOUTE COMMANDE
// DEPASSANT CETTE DISTANCE SERA ANNULEE!
// ATTENTION : L'UTILISATION DU MOTEUR PAS A PAS SEMBLE MOBILISER TOUTE LA
// CARTE ARDUINO : AUCUNE AUTRE COMMANDE SUR LES PINS NE SEMBLE POSSIBLE
// PENDANT SON UTILISATION!

while (Serial.available() > 0) 
 {
 taille = Serial.readBytes(Instructions,12);
 Serial.print(Instructions);
 if (Instructions[0] == '1')
   {
    //Commande 1 : déplace le bras jusqu'à une distance demandée, et le maintient à cette distance. 
    String str_brs(Instructions);
    str_brs = str_brs.substring(1);
   arm_depl = str_brs.toFloat();
   Serial.println("Moving about : ");
   Serial.print(arm_depl);
   Serial.println(" mm.");
   p_cs= move_arm(arm_depl,dist_ori);
   Serial.print(*p_cs);
   dist_ori += *p_cs;
   
   if (dist_ori < 0)
      {
      dist_ori = 0;
      }
   else if (dist_ori > 150)
      {
      dist_ori = 150;
      }

   Serial.print(dist_ori);
   }
 else if (Instructions[0] == '2')
   {
   //Commande 2 : déplace le bras suivant un angle donné.
   Serial.println("Raise_arm activated \n");
      String str_ang(Instructions);
    str_ang = str_ang.substring(1);
    Serial.println(str_ang);
   angle_preh = str_ang.toFloat();
   Serial.println("Moving to : ");
   Serial.print(angle_preh);
   Serial.println(" degrees.");
   angle_c_1 = angle_preh;
   Servo1.write(angle_c_1);
   }

 else if (Instructions[0] == '3')
   {
   //Commande 3 : ouvre la pince
   Serial.println("Open_arm activated \n");
   angle_c_2 = 115;
   Servo2.write(angle_c_2);
   }

   else if (Instructions[0] == '6')
   {
   //Commande 6 : déplace pince d'un angle donné
   Serial.println("Move_grip activated \n");
    String str_ang(Instructions);
    str_ang = str_ang.substring(1);
    Serial.println(str_ang);
   angle_preh = str_ang.toFloat();
   Serial.println("Moving to : ");
   Serial.print(angle_preh);
   Serial.println(" degrees.");
   angle_c_2 = angle_preh;
   Servo2.write(angle_c_2);
   }


 else if (Instructions[0] == '4')
   {
   //Commande 4 : attrape le goldenium, placé suivant une distance donnée par arm_depl.
   Serial.println("Get_gold activated \n");
       String str_brs(Instructions);
    str_brs = str_brs.substring(1);
   arm_depl = str_brs.toFloat();
   Serial.println("Robot to gold is : ");
   Serial.print(arm_depl);
   Serial.println(" mm.");
   Serial.println("Distance from the bottom of robot : ");
   Serial.print(dist_ori);
   Serial.println(" mm.");
   catch_gold(arm_depl,dist_ori);
   angle_c_1= 89 - 10; // à modifier si valeur max de i change
   angle_c_2 = 20;         // à modifier si valeur max de i change
   Servo2.write(angle_c_1);
   Servo2.write(angle_c_2);
   }

 else if (Instructions[0] == '5')
   {
   //Commande 5 : attrape un autre palet, placé suivant une distance donnée par arm_depl.
   Serial.println("Get_buck activated \n");
       String str_brs(Instructions);
    str_brs = str_brs.substring(1);
   arm_depl = str_brs.toFloat();
   Serial.println("Robot to buck is : ");
   Serial.print(arm_depl);
   Serial.println(" mm.");
   catch_buck(arm_depl,dist_ori);
   angle_c_1= 115 - 19; // à modifier si valeur max de i change
   angle_c_2 = 20;         // à modifier si valeur max de i change
   Servo2.write(angle_c_1);
   Servo2.write(angle_c_2);
   }

 else if (Instructions[0] == '7')
   {
   //Commande 7 : mesure la distance entre le goldenium et le bras
   // avec le télémètre, puis l'attrape
   Serial.println("Get_auto_gold activated \n");
  float med = catch_dist(10);
   Serial.println("Robot to buck is : ");
   Serial.print(med);
   Serial.println(" mm.");
   catch_gold(med,dist_ori);
   angle_c_1= 89 - 10; // à modifier si valeur max de i change
   angle_c_2 = 20;         // à modifier si valeur max de i change
   Servo2.write(angle_c_1);
   Servo2.write(angle_c_2);
   }

 else if (Instructions[0] == '8')
   {
   //Commande 8 : mesure la distance entre le palet et le bras
   // avec le télémètre, puis l'attrape
   Serial.println("Get_auto_buck activated \n");
  float med = catch_dist(10);
   Serial.println("Robot to buck is : ");
   Serial.print(med);
   Serial.println(" mm.");
   catch_buck(med,dist_ori);
   angle_c_1= 115 - 19; // à modifier si valeur max de i change
   angle_c_2 = 20;         // à modifier si valeur max de i change
   Servo2.write(angle_c_1);
   Servo2.write(angle_c_2);
   }

    else if (Instructions[0] == '9')
   {
   //Commande 9 : prend une mesure avec le télémètre
   Serial.println("Get_measure activated \n");
  float med = catch_dist(10);
   Serial.println("Robot to buck is : ");
   Serial.print(med);
   Serial.println(" mm.");
   }

 // si aucune commande n'est donnée, maintient les servo-moteurs à leurs positions.
 Servo1.write(angle_c_1);
 
 Servo2.write(angle_c_2);

   
 }


}



float * move_arm(float dist_avancement,float dist_ori)
{
  // Déplace le bras de [dist_avancement] mm.
  float rapp_avancement = 0.1833;
  float avancement_mm = dist_avancement;
//  if (dist_ori < 10)
//  {
//    avancement_mm += 5;
//  }
  float conversion_step = avancement_mm/rapp_avancement;
  float * p_cs = &avancement_mm;
  myStepper.step(conversion_step);
  return( p_cs);
}

void catch_buck(float dist_a_palet, float dist_origine)
{
  // Attrape le palet placé à [dist_a_palet] du robot, sachant que le bras se trouve à la distance [dist_origine] de son point de départ.
  int i = 0;
  angle_ouv = 105;   
  angle_preh = 115; ///105
  angle_serr = 40;
  float dist_recul = 0;
  float  angle_attente =90; 
  float rapp_avancement = 0.1906;
//  float avancement_mm = dist_a_palet - dist_origine +5;
//
//  if ( (dist_a_palet) > 150)
//    {
//    Serial.println("Erreur : supérieur à la distance maximale d'avancement du bras. Commande annulée.\n ");
//    }

  // si la distance est bien prise avec un capteur ultrason en bas : 
   float avancement_mm = dist_a_palet - dist_origine + 25+10+3; //(+10?)

  if ( (dist_a_palet + 25) > 150)
    {
    Serial.println("Erreur : supérieur à la distance maximale d'avancement du bras. Commande annulée.\n ");
    }

  else
    {
    float conversion_step = avancement_mm/rapp_avancement;
    float vit = 56.62; // 3.11s / 100mm environ pour 60 rpm (32.15) ; 1.766 / 100 mm env à 90 rpm (56.62)
    float tps_deplacement = avancement_mm / vit;
    // étape 1 : rapprochement de la cible
    Servo1.write(angle_attente+5); // étape utile
    Servo2.write(angle_serr);       // étape utile
    myStepper.step(conversion_step/2); 
    // ATTENTION : L'ARDUINO NE SEMBLE PLUS ETRE CAPABLE DE
    // REPONDRE PENDANT LE FONCTIONNEMENT DU STEPPER MOTOR!
  
    // étape 2 : mise en position pour préhension du palet
    Servo1.write(angle_preh);
    Servo2.write(angle_ouv);
    myStepper.step(conversion_step/2);
  
     // étape 3 : serrage progressif de la pince
    while (i<20)                   //40   // possible de réduire i?
      {
        tps = millis();
        while ( (millis() - tps) < 25) // 100 : sécurité
          {
          Servo2.write(angle_serr-i); //i/2
          }
        i++;
      }
      
    // étape 4 : recul progressif du bras, relèvement de celui-ci pour assurer la capture. 
    i = 0;
    while (i<20)
     {
        if (i < 10)
        {
        myStepper.step(-5); // réduction de la distance de recul : Etape vraiment utile
        dist_recul += 5;
        }

        tps = millis();
        while ( (millis() - tps) < 25) //100 //possible de réduire encore : peut-être
            {
                        if ( (i%2 == 0) )
          {
            Servo2.write(angle_serr-20);
          }
          else
          {
            Servo2.write(angle_serr-39/2);
          }
            Servo1.write(angle_preh-i); // obligé de le soulever autant : à décider. Semble optimal ici
            }
        i++;
     }
  
    // étape 5 : recul final du bras jusqu'à sa position d'origine.
    Servo2.write(angle_serr-39/2);
    myStepper.step(-conversion_step+dist_recul);
    }
}
  

void catch_gold(float dist_a_palet, float dist_origine) // commande : 4
{ 
  // Attrape le goldenium placé à [dist_a_palet] du robot, sachant que le bras se trouve à la distance [dist_origine] de son point de départ.
  int i = 0;
  angle_ouv = 125;   //120
  angle_preh = 89; //89
  angle_serr = 35;
  float dist_recul = 0;
  float  angle_attente =86; //89
  float rapp_avancement = 0.1906;
//  float avancement_mm = dist_a_palet - dist_origine +5;
//
//
//  if ( (dist_a_palet + dist_origine) > 150)
//    {
//    Serial.println("Erreur : supérieur à la distance maximale d'avancement du bras. Commande annulée.\n ");
//    }

  // si la distance est bien prise avec un capteur ultrason en bas : 
   float avancement_mm = dist_a_palet - dist_origine +29 ;//24
   Serial.println("Avancement pour palet : ");
   Serial.print(avancement_mm);

  if ( (dist_a_palet + 24 ) > 150)
    {
    Serial.println("Erreur : supérieur à la distance maximale d'avancement du bras. Commande annulée.\n ");
    }
  
  float conversion_step = avancement_mm/rapp_avancement;
  float vit = 56.62; // 3.11s / 100mm environ pour 60 rpm (32.15) ; 1.766 / 100 mm env à 90 rpm (56.62)
  float tps_deplacement = avancement_mm / vit;
  
  // étape 1 : rapprochement de la cible
//  Servo1.write(angle_attente+5); // étape utile?
  Servo2.write(angle_ouv);       // étape utile?
  Servo1.write(angle_preh);
//  myStepper.step(conversion_step/4); 
  // ATTENTION : L'ARDUINO NE SEMBLE PLUS ETRE CAPABLE DE
  // REPONDRE PENDANT LE FONCTIONNEMENT DU STEPPER MOTOR!
  
  // étape 2 : mise en position pour préhension du palet
//  Servo1.write(angle_preh);
//  Servo2.write(angle_ouv);
  myStepper.step(conversion_step);
  
  // étape 3 : serrage progressif de la pince
  while (i<20)                      // 40
    {
      tps = millis();
      while ( (millis() - tps) < 25) // 100
        {
        Servo2.write(angle_serr-i); // i/2
        }
      i++;
    }
  
  // étape 4 : recul progressif du bras, relèvement de celui-ci pour assurer la capture. 
  i = 0;
  while (i<20)//40
   {
      if (i < 15)  //20
      {
      myStepper.step(-5); // réduction de la distance de recul : Etape vraiment utile
      dist_recul += 5;
      }
      tps = millis();
      while ( (millis() - tps) < 25) //possible de réduire?
          {
          Servo2.write(angle_serr-39/2);
          Servo1.write(angle_preh-i/2); // obligé de le soulever autant?
          }
      i++;
   }

  // étape 5 : recul final du bras jusqu'à sa position d'origine.
  myStepper.step(-conversion_step+dist_recul);
}

float catch_dist(int nbe_mes)
// Détermine la distance entre le télémètre et l'obstacle.
// Pour cela, prend un nombre nbe_mes de mesures, puis renvoie la valeur
// filtrée de ces mesures (via un filtre médian)
{
  float tab[nbe_mes];
  int i;
  int j;
  for (i=0; i< nbe_mes; i++)
  {
    float val_CAN = analogRead(sensor); // lecture du pin correspondant au capteur
    float dist = 56207.6149106033*pow(val_CAN,-1.1302177433799);
    // valeur dist obtenue via un calibrage; valeur analogique du capteur prise tous les
    // 5mm; dessin de la courbe obtenue sur excel, puis obtention de la courbe de tendance
    // indiquée ici.
    tab[i] = dist;
    // délai nécessaire d'après la documentation : valeur prise sans recherche d'optimisation
    delay(30);
  }
  // filtre médian : 1e étape : tri de la liste
 for (i=0;i<nbe_mes; i++)
 {
    for (j=0;j<i;j++)
      {
        if (tab[j]<tab[i])
         {
          tab[i],tab[j] = tab[j],tab[i];
         }
      }
  
 }
// for (i=0;i<nbe_mes; i++)
// {
//  Serial.print(tab[i]);
// }
 // prise de la valeur médiane dans liste triée
 float med = tab[int(nbe_mes/2)];
 return(med);

}
