# Validation de l’édition 0.1.1

Date : 2026-11-01.

## Contrôles exécutés

- 62 tests unitaires réussis : contrôleur local, erreurs de commande, limites de comptage, calculs, chemins de cas, version épinglée de la baseline et concordance entre mesures et prompts.
- Chargement natif Hermes de la version 0.1.1 dans un home jetable : noyau, français, anglais, référence approfondie et licence disponibles ; aucun script ou asset exécutable dans ce paquet.
- Précontrôle avec le scanner natif Hermes, source communautaire : verdict safe, aucune alerte et aucune option de forçage. Voir [le relevé et l’empreinte du paquet](validation/runtime-scan.json).
- Six appels du benchmark courant terminés, avec les compteurs réellement retournés par le moteur. L’essai précédent reste dans l’historique, sans retouche des sorties.

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

## Frontière d’installation

Le paquet installé est `skills/kervia-humanizer-fr-en/`, texte seul. Le code du contrôleur, le client de benchmark, les tests et la baseline sont des outils de développement séparés. La [frontière et le premier blocage](SECURITY.md) sont documentés ; aucune règle du scanner n’est changée et aucune installation n’est forcée.

## Portée

Un test logiciel ou un chargement réussi ne valide pas une qualité littéraire. La [lecture des sorties](benchmarks/QUALITY.md) signale les intertitres anglais génériques et une vérification de portée nécessaire sur une formulation française. Les alertes mécaniques restent présentes dans les données.

Les contrôles de distribution inspectent les fichiers publiés et l’archive, pas les caches locaux ignorés par Git. Les profils utilisateur ne sont pas modifiés. Les serveurs temporaires d’inférence sont arrêtés après les essais ; aucune configuration de service permanente n’est modifiée.

## CI

Aucun workflow GitHub Actions n’est ajouté dans cette livraison. Les tests décrits ici sont des exécutions locales, pas un statut CI GitHub. Aucun secret de CI n’est demandé et aucun benchmark payant n’est lancé automatiquement.
