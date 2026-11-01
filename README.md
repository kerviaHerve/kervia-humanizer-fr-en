# Kervia Humanizer FR/EN

Réviser un texte français ou anglais sans perdre les faits, les réserves et la voix de son auteur. Le skill sert aussi à rédiger depuis des notes fournies. Il ne cherche pas à tromper les détecteurs d’IA.

**Inspiré de [blader/humanizer](https://github.com/blader/humanizer), par Siqi Chen.** Nos règles d’exécution et notre contrôle local ont été rédigés pour ce projet. Le fichier amont est conservé séparément, inchangé, uniquement pour reproduire le benchmark. Voir les [attributions](THIRD_PARTY_NOTICES.md).

[English documentation](README.en.md)

## Ce qui change dans cette approche

Le français dispose de ses propres décisions : portée de « ne… que », modalités, référents, nominalisations et variantes régionales. Une formule surveillée n’est pas un mot interdit. Un vrai contraste, une liste utile ou un bon passage peuvent rester.

Le noyau et un seul module linguistique forment le chemin normal. Les exemples, recherches, benchmarks et références longues ne sont pas chargés pour une retouche ordinaire. La réponse contient le texte final, sans brouillon ni audit imposé.

Les informations matérielles sont protégées : acteurs, quantités, unités, dates, comparaisons, conditions, exceptions, négations, attributions et engagements. Une affirmation fournie ne devient pas vérifiée parce qu’elle a été mieux écrite.

## Utiliser le skill

Installer le dossier contenant `SKILL.md` selon la méthode de ton agent compatible Agent Skills. Avec le CLI Hermes :

```text
hermes skills install kerviaHerve/kervia-humanizer-fr-en
```

 Avec Hermes, charger `kervia-humanizer-fr-en` puis la demande. Ne pas installer la baseline de comparaison comme un second skill.

Exemples de demandes :

- « Révise légèrement ce courriel en français. Garde toutes ses conditions. »
- « Audit this British English text. Keep passages that already work. »
- « Rédige à partir de ces notes, sans inventer de chiffres ni d’expérience personnelle. »

La règle maison évite les tirets cadratins en prose nouvelle. Les citations exactes, commandes, liens et données restent protégés.

## Benchmark et exemples

Le [protocole](benchmarks/README.md) compare le SKILL.md intégral de Humanizer 3.1.0 à notre noyau accompagné du seul module utile. Même texte, même modèle, même consigne et contextes de messages séparés. Les tokens sont lus dans la réponse du moteur, pas estimés à partir de mots.

- [Mesures et limites](benchmarks/results/qwen36-16k-2026-11-01.md)
- [Données et sorties finales brutes](benchmarks/results/qwen36-16k-2026-11-01.json)
- [Exemple français : avant, Humanizer, Kervia](examples/fr-slop.md)
- [Exemple anglais : avant, Humanizer, Kervia](examples/en-slop.md)
- [Contrôle sur un texte français déjà clair](examples/fr-clean.md)

Il s’agit d’un petit essai de développement, sans jury humain indépendant. Il ne démontre ni une qualité universellement supérieure ni une meilleure détection. Les défauts éventuels et les échecs de préparation sont conservés. Le coût d’un appel d’édition n’est pas celui d’une session d’agent complète.

## Tokens observés sur ce pilote

| Chemin | Entrée | Sortie | Total |
|---|---:|---:|---:|
| Humanizer 3.1.0 complet | 23501 | 565 | 24066 |
| Kervia : noyau + langue utile | 5192 | 574 | 5766 |

Réduction observée : **77.91 % des tokens d’entrée** et **76.04 % du total**, sur les trois paires terminées. Les compteurs incluent le cache déclaré par le moteur : ce n’est pas une économie monétaire mesurée. Les réponses Kervia ne sont pas plus courtes en tokens au total ; la réduction vient du contexte d’instructions.

La [lecture des sorties](benchmarks/QUALITY.md) signale aussi les limites : les deux skills préservent le texte déjà clair et Humanizer produit des intertitres anglais plus précis sur cet exemple. Les alertes de fréquence des noms restent visibles dans les données.

## Contrôle local facultatif

Le [script de préservation](references/checker.md) utilise seulement Python standard et ne modifie pas les fichiers :

```text
python3 scripts/check_preservation.py original.md revision.md
```

Il ne fait aucun appel à un modèle. Lire son résultat peut néanmoins coûter des tokens à l’agent. Il repère des écarts littéraux, pas tous les changements de sens ; une sortie sans alerte n’est jamais une validation sémantique.

## Tests

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

Python 3.10 ou plus récent. Les tests sont hors ligne et ne lancent pas le modèle de benchmark. Un contrôle natif Hermes supplémentaire utilise uniquement des homes jetables, jamais les profils utilisateur.

Les [contrôles de validation et leur portée](VALIDATION.md) sont documentés séparément.

## Sources et licence

[Sources et portée des recommandations](references/sources.md).

Licence [MIT](LICENSE), autorisée par Hervé Barrilliet. Les mentions et la licence de Humanizer sont préservées avec sa baseline. Aucun modèle, secret, texte client ou configuration de compte n’est distribué.
