# Validation de la première édition publique

Date : 2026-11-01. Édition : 0.1.0.

## Contrôles exécutés

- 61 tests unitaires réussis avec Python standard : invariants du contrôleur, erreurs de commande, usage réellement fourni par le moteur, calculs, isolement des cas, empreinte de la baseline et concordance des observations avec leurs prompts.
- Chargement natif Hermes du noyau, des deux langues et des fichiers de support dans deux homes jetables : mode local et mode `external_dirs`. Les profils utilisateur n’ont pas été modifiés.
- Six appels de révision terminés : trois cas, deux méthodes, même modèle et même consigne de sortie finale seule. Les compteurs et les sorties proviennent des réponses du moteur.
- Les contrôles de contenu et de distribution portent sur les fichiers destinés à Git et à l’archive ; les caches locaux de développement sont exclus, pas considérés comme des fichiers de publication.

Commande de test :

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

## Portée

Les tests unitaires vérifient le logiciel et des propriétés de paquet, pas une qualité littéraire. Les sondes de chargement ne lancent pas d’agent ni de modèle. Le benchmark est un pilote synthétique, sans jury indépendant et sans détecteur d’IA.

La [lecture des sorties](benchmarks/QUALITY.md) documente une faiblesse réelle : certains intertitres anglais de Kervia restent génériques. Les noms moins répétés déclenchent aussi des alertes conservées dans le relevé, même quand leur identité est préservée.

Le modèle temporaire utilisé pour le benchmark a été arrêté après l’essai. La configuration permanente des services locaux n’a pas été changée.

## CI

Aucun workflow GitHub Actions n’est ajouté dans cette première livraison. Les tests ci-dessus sont des exécutions locales réelles, pas un statut CI GitHub. Le dépôt ne demande aucun secret de CI et le benchmark n’est jamais lancé automatiquement sur un service payant.
