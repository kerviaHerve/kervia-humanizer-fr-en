# Protocole de comparaison

## Question

Sur les mêmes textes, combien de tokens le chemin d’édition normal utilise-t-il avec Humanizer 3.1.0 et avec Kervia FR/EN ? Quels changements observe-t-on dans les textes finaux ? Ce protocole ne mesure pas l’origine humaine d’un document.

## Conditions fixées avant les sorties

- Une entrée française volontairement chargée, une anglaise chargée et un texte français déjà clair.
- Textes fictifs rédigés pour le développement ; aucune donnée client et aucun résultat attendu injecté dans le prompt.
- Référence : SKILL.md intégral de Humanizer 3.1.0, commit et empreinte dans [source.json](baselines/source.json). Aucun raccourcissement de cette baseline.
- Kervia : `SKILL.md` et le seul module `fr.md` ou `en.md` requis. Les références approfondies sont inutiles pour ces cas et ne sont pas chargées.
- Même moteur et même consigne finale seule. Ce contrat commun évite de pénaliser Humanizer en lui faisant afficher son brouillon et son audit.
- Un nouveau tableau de messages pour chaque requête, sans réponse précédente ni exemple de correction attendu.
- Température 0 et seed 42 demandés, thinking désactivé. Les réglages demandés ne garantissent pas un déterminisme bit à bit.
- Ordre alterné entre conditions. Une génération par cas et par condition ; aucun choix de la meilleure parmi plusieurs sorties.

## Reproduire

Depuis un endpoint local compatible OpenAI déjà disponible :

```text
python3 benchmarks/run_compare.py --base-url http://127.0.0.1:8080/v1 --model MODEL --out benchmarks/results/nouveau-test.json
```

Remplacer `MODEL` par un identifiant réellement disponible. Le script ne télécharge ni n’installe de modèle. Un endpoint distant exige `--allow-remote` ; il peut coûter de l’argent et transmettre les cas au fournisseur. Une clé éventuelle passe par `--api-key-env NOM_DE_VARIABLE`, jamais par sa valeur en argument.

Les fichiers existants ne sont pas écrasés. Une erreur est conservée et interrompt l’essai, sans remplacement par une estimation plausible. Un nouvel essai utilise un nouveau fichier.

Les observations publiées ont utilisé un modèle Qwen3.6-35B-A3B quantifié Q4_K_M sur un serveur llama.cpp temporaire, texte seul, contexte demandé de 16 384 tokens, reasoning budget 0. Un projecteur vision n’était pas utile pour ce travail. Les détails exposés sont enregistrés séparément ; les paramètres privés de la machine ne sont pas distribués.

## Mesures

- `prompt_tokens`, `completion_tokens` et `total_tokens` proviennent du champ `usage` réellement retourné.
- Les totaux sont vérifiés. Une absence de comptage ou une génération tronquée n’est pas un succès.
- Les tokens d’entrée comprennent instructions actives, consigne commune, texte et gabarit de conversation. Ce n’est pas le coût d’une session Hermes avec historique et outils.
- La durée est enregistrée, mais le chargement et le cache ne sont pas neutralisés : aucun classement de vitesse n’en est tiré.
- Le contrôle mécanique et les chaînes requises donnent des alertes à examiner. Ils ne certifient pas le sens, l’exhaustivité ou la préférence humaine.

## Limites et historique

Les exemples et métriques viennent d’un seul petit corpus synthétique, sans jury indépendant. Lire les sorties avant de conclure qu’un coût inférieur est utile. Une information perdue n’est pas une économie acceptable.

Le [premier essai via la passerelle](failed-attempts/local-qwen36-2026-11-01.json) a échoué au démarrage du projecteur vision par manque de mémoire GPU, avant de produire un texte ou un comptage exploitable. Ses zéros indiquent l’absence d’appels terminés, pas une consommation mesurée nulle. Une sonde de serveur isolé a aussi révélé une dépendance CUDA non chargée ; elle n’a produit aucune réécriture. Les tentatives réussies et échouées ne sont pas mélangées pour calculer une réduction.

Aucune sortie valide n’est retouchée ou écartée pour favoriser un skill. Les fichiers d’exemples sont générés à partir des réponses enregistrées. La qualité éditoriale, le coût en tokens et un score de détecteur sont trois observations distinctes.
