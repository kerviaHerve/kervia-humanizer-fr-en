# Benchmark local : Humanizer et Kervia FR/EN

Essai exploratoire sur des textes fictifs, pas une preuve de supériorité générale.

Modèle demandé : `qwen3.6-35b-a3b`. Paramètres demandés : température 0, seed 42, thinking désactivé.
Même modèle, même texte et même contrat de sortie finale seule. Chaque appel reçoit un contexte de messages neuf. Les tokens viennent du champ usage du fournisseur, pas d’une estimation en mots.

| Cas | Skill | Tokens entrée | Tokens sortie | Total | Alertes mécaniques |
|---|---|---:|---:|---:|---:|
| fr-slop | humanizer | 7989 | 236 | 8225 | 1 |
| fr-slop | kervia | 1911 | 278 | 2189 | 1 |
| en-slop | kervia | 1654 | 203 | 1857 | 1 |
| en-slop | humanizer | 7900 | 196 | 8096 | 1 |
| fr-clean | humanizer | 7612 | 133 | 7745 | 0 |
| fr-clean | kervia | 1534 | 133 | 1667 | 0 |

## Total des appels comparés

- humanizer : 23501 tokens d’entrée, 565 de sortie, 24066 au total.
- kervia : 5099 tokens d’entrée, 614 de sortie, 5713 au total.

Réduction observée : **78.30 %** des tokens d’entrée et **76.26 %** des tokens totaux.

### Cache déclaré par le moteur

- humanizer : 14750 tokens d’entrée déclarés en cache ; 8751 non déclarés en cache.
- kervia : 1297 tokens d’entrée déclarés en cache ; 3802 non déclarés en cache.

Les totaux d’entrée incluent les tokens déclarés en cache. Ils mesurent le volume de contexte compté par le moteur, pas une facture ni le nombre exact d’opérations de calcul. Aucune économie monétaire n’est déduite de ces pourcentages.

## Limites

- Le chemin Kervia contient le noyau et un seul module linguistique. Le chemin Humanizer contient son SKILL.md intégral, inchangé et épinglé. Les autres références Kervia ne sont pas nécessaires à ces retouches.
- Les métriques d’entrée incluent aussi le même emballage, le texte source et le gabarit de conversation du modèle. Ce n’est pas le coût d’une conversation Hermes complète.
- Aucun audit intermédiaire n’est affiché dans les deux conditions. Humanizer ne subit pas un surcoût artificiel de brouillon et d’audit en sortie.
- Trois exercices synthétiques, une génération par condition et aucun jury humain indépendant. Les cas ont été écrits pour le développement, pas échantillonnés aléatoirement.
- Les alertes mécaniques exigent une lecture. Une absence d’alerte ne valide ni le sens ni la qualité. Le coût inférieur peut coexister avec une erreur.
- Le temps brut comprend potentiellement le chargement du modèle et les effets de cache. Il n’est pas utilisé pour conclure à une accélération.
- Aucun détecteur d’IA n’a été utilisé pour noter les textes. Aucun dollar économisé ni taux d’authenticité n’est calculé.

Données et sorties finales brutes : [fichier JSON](qwen36-text-runtime-2026-11-01.json).

Inspiré de [blader/humanizer](https://github.com/blader/humanizer). Licence amont conservée avec la baseline.
