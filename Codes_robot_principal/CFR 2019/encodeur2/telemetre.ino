
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