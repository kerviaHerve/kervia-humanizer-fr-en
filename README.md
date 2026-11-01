<p>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/brand/kervia-logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/brand/kervia-logo-clair.svg">
    <img src="assets/brand/kervia-logo-clair.svg" alt="Kervia" width="232">
  </picture>
</p>

# Kervia Humanizer FR/EN

[Français](README.md) · [English](README.en.md)

**Version expérimentale : relecture humaine nécessaire avant publication.** Les exemples du benchmark montrent aussi des limites de style et de portée.

Un skill Kervia pour réviser les textes français et anglais : retirer les formulations creuses, préserver les informations et garder la voix de l’auteur. Il peut aussi rédiger depuis des notes fournies. Son objectif est la qualité de lecture, pas le contournement des détecteurs d’IA.

**Inspiré de [blader/humanizer](https://github.com/blader/humanizer), par Siqi Chen.** Nos règles d’exécution et notre contrôle local ont été rédigés pour ce projet. Le fichier amont est conservé séparément, inchangé, uniquement pour reproduire le benchmark. Voir les [attributions](THIRD_PARTY_NOTICES.md).

## Ce qui change dans cette approche

Le français dispose de ses propres décisions : portée de « ne… que », modalités, référents, nominalisations et variantes régionales. Une formule surveillée n’est pas un mot interdit. Un vrai contraste, une liste utile ou un bon passage peuvent rester.

Le noyau et un seul module linguistique forment le chemin normal. Les exemples, recherches, benchmarks et références longues ne sont pas chargés pour une retouche ordinaire. La réponse contient le texte final, sans brouillon ni audit imposé.

Les informations matérielles sont protégées : acteurs, quantités, unités, dates, comparaisons, conditions, exceptions, négations, attributions et engagements. Une affirmation fournie ne devient pas vérifiée parce qu’elle a été mieux écrite.

## Utiliser le skill

Installer uniquement le dossier `skills/kervia-humanizer-fr-en/`, qui contient le `SKILL.md` et ses références texte. Le banc d’essai et le code du dépôt ne sont pas des dépendances installées. Avec le CLI Hermes :

```text
hermes skills install kerviaHerve/kervia-humanizer-fr-en/skills/kervia-humanizer-fr-en
```

Avec Hermes, charger `kervia-humanizer-fr-en` puis la demande. Ne pas installer la baseline de comparaison comme un second skill.

Exemples de demandes :

- « Révise légèrement ce courriel en français. Garde toutes ses conditions. »
- « Audit this British English text. Keep passages that already work. »
- « Rédige à partir de ces notes, sans inventer de chiffres ni d’expérience personnelle. »

La règle maison évite les tirets cadratins en prose nouvelle. Les citations exactes, commandes, liens et données restent protégés.

## Benchmark et exemples

Le [protocole](benchmarks/README.md) compare le SKILL.md intégral de Humanizer 3.1.0 à notre noyau accompagné du seul module utile. Même texte, même modèle, même consigne et contextes de messages séparés. Les tokens sont lus dans la réponse du moteur, pas estimés à partir de mots.

- [Mesures et limites](benchmarks/results/qwen36-text-runtime-2026-11-01.md)
- [Données et sorties finales brutes](benchmarks/results/qwen36-text-runtime-2026-11-01.json)
- [Exemple français : avant, Humanizer, Kervia](examples/fr-slop.md)
- [Exemple anglais : avant, Humanizer, Kervia](examples/en-slop.md)
- [Contrôle sur un texte français déjà clair](examples/fr-clean.md)

Il s’agit d’un petit essai de développement, sans jury humain indépendant. Il ne démontre ni une qualité universellement supérieure ni une meilleure détection. Les défauts éventuels et les échecs de préparation sont conservés. Le coût d’un appel d’édition n’est pas celui d’une session d’agent complète.

## Tokens observés sur ce pilote

| Chemin | Entrée | Sortie | Total |
|---|---:|---:|---:|
| Humanizer 3.1.0 complet | 23501 | 565 | 24066 |
| Kervia : noyau + langue utile | 5099 | 614 | 5713 |

Réduction observée : **78,30 % des tokens d’entrée** et **76,26 % du total**, sur les trois paires terminées. Les compteurs incluent le cache déclaré par le moteur : ce n’est pas une économie monétaire mesurée. Les réponses Kervia ne sont pas plus courtes en tokens au total ; la réduction vient du contexte d’instructions.

La [lecture des sorties](benchmarks/QUALITY.md) signale aussi les limites : les deux skills préservent le texte déjà clair ; Humanizer produit des intertitres anglais plus précis et une formulation française de Kervia demande une vérification de portée. Les alertes de fréquence des noms restent visibles dans les données.

## Contrôle local facultatif

Cet outil reste dans le dépôt, hors du paquet installable. Son usage demande un choix explicite ; charger le skill ne le lance pas et ne le télécharge pas. Voir la [frontière d’installation](SECURITY.md).

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

## Kervia et l’identité du dépôt

Les logos clair et sombre viennent du kit de marque Kervia v02 fourni pour cette présentation. Ils restent hors du paquet installé ; ni le chargement du skill ni les mesures publiées ne changent. [Provenance des assets](assets/brand/README.md) · [Kervia](https://kervia.ch).

## Sources et licence

[Sources et portée des recommandations](references/sources.md).

Licence [MIT](LICENSE), autorisée par Hervé Barrilliet. Les mentions et la licence de Humanizer sont préservées avec sa baseline. Aucun modèle, secret, texte client ou configuration de compte n’est distribué.
