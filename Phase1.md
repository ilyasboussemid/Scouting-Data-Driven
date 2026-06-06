## PHASE 1 : DÉFINITION DU PROBLÈME & KPIs


### 1. Domaine Métier & Question Décisionnelle Centrale

*   **Domaine Métier :** Football Analytics / Sport Business & Gestion d'effectif.
*   **Contexte :** Notre club de football professionnel vient de vendre son attaquant vedette pour un montant de 35 Millions €. La direction sportive nous confie la mission de trouver son successeur avant la fin du mercato, avec une enveloppe budgétaire restreinte.
*   **Question Décisionnelle Centrale :**
    « Comment identifier, évaluer et recruter de jeunes attaquants (moins de 23 ans) sous-évalués sur le marché européen, capables de remplacer numériquement et statistiquement notre buteur vedette transféré, tout en respectant une contrainte budgétaire stricte ? »*


### 2. Définition des KPIs (Primaires & Secondaires)

Pour garantir la pertinence de notre système d'aide à la décision, nous divisons nos indicateurs de performance en deux catégories distinctes :

#### A. KPIs Primaires (Décisions Stratégiques & Impact Financier)
*   **npxG/90 (Non-Penalty Expected Goals per 90 mins) :** Probabilité qu'un tir (hors penalty) se transforme en but selon les conditions de l'action. Mesure la dangerosité réelle et la régularité offensive d'un joueur.
*   **Valeur Marchande Estimée (Market Value) :** Estimation financière du coût de transfert du joueur basée sur ses performances, son âge et sa situation contractuelle.
*   **Ratio d'Efficacité Budgétaire :** Rapport entre le coût d'achat du joueur et son apport statistique théorique.

#### B. KPIs Secondaires (Indicateurs Opérationnels & Performance Modèle)
*   **Taux de Conversion des Tirs (%) :** Pourcentage de tirs cadrés se transformant en buts réels (mesure de la précision à la finition).
*   **Touches dans la surface / 90 min :** Volume de ballons joués dans les 16,5 mètres adverses (mesure de la présence offensive).
*   **xA/90 (Expected Assists per 90 mins) :** Probabilité qu'une passe se transforme en passe décisive (mesure de la contribution collective).
*   **Rappel du Modèle (Recall) :** Capacité de notre algorithme à détecter un maximum de "pépites cachées" dans notre base de données sans en omettre.


### 3. Le KPI Tree Hiérarchique

Le diagramme ci-dessous illustre comment les métriques de performance collectées sur le terrain (données opérationnelles) influencent directement la réussite sportive et la rentabilité financière du club (objectifs stratégiques).

[ Droits TV & Billetterie ]   [ Plus-value sur Revente (Mercato) ]   [ Recruter des Talents Sous-évalués ]
|                                      |
+------------------+-------------------+
|
KPI Principal : Performance npxG / 90 min
|
+-----------------------+-----------------------+
|                                               |
[ KPI Sec : Volume de Tirs ]                  [ KPI Sec : Qualité du Placement ]
|                                               |
+------------+------------+                                  |
|                         |                                  |
[ Tirs tentés ]          [ Tirs Cadrés (%) ]         [ Touches dans la surface adverse ]

---

### 4. Business Case & Estimation du ROI de la Démarche Data

Afin de justifier l'implémentation de ce pipeline de données auprès de la direction générale, nous modélisons les gains financiers attendus sur une base de données de **50 000 lignes** de performances de joueurs.

#### A. Paramètres Initiaux (Avant la Data)
*   **Budget de remplacement alloué :** $12\text{ M€}$
*   **Risque du Scouting Traditionnel (Instinct) :** Taux d'erreur historique estimé à 40% sur le recrutement de jeunes joueurs à fort montant (risque de "flop" financier et sportif).

#### B. Impact de la Solution Data (Modélisation & Clustering)
Notre algorithme de clustering isole un jeune joueur à très haut potentiel évoluant dans un championnat secondaire, dont les métriques de $npxG/90$ et de $xA/90$ sont statistiquement similaires à notre ancien attaquant vedette.

*   **Coût d'achat de la pépite data-driven :** $5\text{ M€}$

#### C. Calcul du Retour sur Investissement (ROI)

1. **Économie immédiate sur enveloppe de transfert :**
   $$\text{Économie} = 12\text{ M€} - 5\text{ M€} = 7\text{ M€}$$

2. **Gain Sportif Direct (Garantie de performance) :**
   Le joueur remplit les objectifs fixés par le modèle, permettant au club de se qualifier pour une compétition européenne (valorisation des droits TV et billetterie) :
   $$\text{Gain Sportif} = +4\text{ M€}$$

3. **Plus-value financière (Valorisation de l'actif à la revente après 2 saisons) :**
   Le modèle ayant correctement anticipé la courbe de progression, la valeur marchande du joueur atteint $25\text{ M€}$.
   $$\text{Bénéfice Revente} = 25\text{ M€} - 5\text{ M€} = 20\text{ M€}$$

4. **Synthèse financière & ROI Global de la cellule Data :**
   $$\text{Gains Totaux} = 7\text{ M€} + 4\text{ M€} + 20\text{ M€} = 31\text{ M€}$$
   $$\text{ROI} = \frac{\text{Gains Totaux} - \text{Investissement Initial}}{\text{Investissement Initial}} = \frac{31\text{ M€}}{5\text{ M€}} = 620\%$$
