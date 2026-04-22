# Safe N Tech

**Safe N Tech** estun site web de sensibilisation à la cyber-sécurité et à l'hygiène numérique (Hugo + Tailwind CSS), hébergé chez Deuxfleurs (stockage S3-compatible). URL : https://www.safe-n-tech.org/

**Site en production** : [www.safe-n-tech.org](https://www.safe-n-tech.org/)
 
---
 
## Stack technique
 
- **Générateur de site statique** : [Hugo](https://gohugo.io/) (v0.145.0, extended)
- **CSS** : [Tailwind CSS](https://tailwindcss.com/) v3
- **Typographie** : Police Marianne
- **Gestionnaire de paquets** : Yarn
- **Node.js** : v20 (voir `.nvmrc`)
- **Hébergement** : [Deuxfleurs](https://deuxfleurs.fr/) (stockage objet Garage, compatible S3)
- **CI/CD** : GitHub Actions (build + déploiement automatique sur `main`)
---
 
## Prérequis
 
- **Hugo** v0.145.0+ (version *extended* requise pour le support SCSS/PostCSS)
- **Node.js** v20+
- **Yarn**
---
 
## Installation
 
```bash
# Cloner le dépôt avec les sous-modules
git clone --recurse-submodules <url-du-repo>
cd safe-n-tech
 
# Installer les dépendances JS
yarn install
```
 
---
 
## Développement
 
```bash
yarn dev
```
 
Cette commande lance en parallèle :
- Le serveur Hugo avec rechargement automatique
- Le watcher Tailwind CSS qui recompile les styles à chaque modification
Le site est alors accessible sur `http://localhost:1313`.
 
---
 
## Build de production
 
```bash
yarn build
```
 
Cela exécute successivement :
1. La compilation et minification de Tailwind CSS
2. Le build Hugo avec garbage collection et minification
Les fichiers générés se trouvent dans le dossier `public/`.
 
---
 
## Structure du projet
 
```
└── 📁www                                   Site Hugo "Safe N Tech" (safe-n-tech.org)
    │
    ├── 📁.github/workflows/
    │   └── deuxfleurs.yml                  CI/CD de déploiement
    │
    ├── 📁archetypes/                       Modèles de frontmatter pour créer du contenu
    │
    ├── 📁assets/
    │   ├── 📁css/                          Sources Tailwind + styles compilés
    │   └── 📁js/                           main.js (UI générale), quiz.js (logique du quiz)
    │
    ├── 📁content/                          Tout le contenu Markdown du site
    │   ├── 📁definitions/                  Glossaire cybersécurité (~40 termes)
    │   ├── 📁good-practices/               Fiches bonnes pratiques (~130 fiches)
    │   ├── 📁vulnerabilities/              Fiches de vulnérabilités associées (~110)
    │   ├── 📁thematiques/                  Thèmes regroupant bonnes pratiques (mots de passe, wifi…)
    │   ├── 📁questions/                    Questions du quiz (~50)
    │   ├── 📁quizz/                        Page d'accueil du quiz
    │   ├── 📁boite-a-outils/               Outils recommandés
    │   ├── 📁mes-donnees-ont-elles-fuite/  Vérificateur de fuite de données
    │   ├── 📁mille-bugs/                   Jeu de cartes "Mille Bugs"
    │   ├── 📁a-propos/                     Page à propos
    │   └── 📁legal/                        Mentions légales
    │
    ├── 📁layouts/                          Templates HTML Hugo
    │   ├── 📁_default/                     Layouts de base (baseof.html, sitemap…)
    │   ├── 📁partials/                     Composants réutilisables (header, footer, seo…)
    │   │   └── 📁quizz/                    Partials spécifiques au quiz (ingame, results)
    │   └── 📁[section]/                    Un dossier par section avec list.html / single.html
    │
    ├── 📁static/                           Fichiers servis tels quels (non traités par Hugo)
    │   ├── 📁admin/                        Interface DecapCMS (CMS headless)
    │   ├── 📁fonts/                        Police Marianne
    │   ├── 📁icons/                        Icônes par thématique
    │   ├── 📁images/                       Illustrations et logos
    │   ├── 📁svgs/                         Icônes UI (burger, flèches, logo…)
    │   ├── 📁sprites/                      Favicons et images optimisées
    │   └── 📁pdf/                          PDFs téléchargeables (Mille Bugs, fiches pratiques)
    │
    ├── config.yml                          Config Hugo (URL, menus, taxonomies, permalinks)
    ├── tailwind.config.js                  Config Tailwind CSS
    ├── package.json                        Dépendances JS
    └── netlify.toml                        Config de déploiement Netlify

```
 
---
 
## Contenu
 
Le contenu est organisé autour de plusieurs types interconnectés :
 
| Type | Description |
|---|---|
| **Thématiques** | Catégories principales (Mots de passe, Wi-Fi, Réseaux sociaux, etc.) |
| **Vulnérabilités** | Comportements à risque, avec les risques encourus et ce qu'il ne faut pas faire |
| **Bonnes pratiques** | Conseils concrets liés aux vulnérabilités, classés par niveau (basique, essentiel, avancé) |
| **Questions** | Questions du quiz avec choix multiples, corrections et liens vers les bonnes pratiques |
| **Définitions** | Termes du glossaire (phishing, VPN, keylogger, etc.) |
 
---


## Architecture du contenu

Le site repose sur des **types de contenu liés par UUID** dans leur frontmatter. Tous les fichiers de contenu ont `visibleInCms: true` et un champ `uuid` unique.

### Chaîne de relations

```
thematique  →  vulnerability  →  good-practice
```

- Une **vulnerability** référence sa thématique via `.Params.thematique` (UUID de la thématique).
- Une **vulnerability** contient un tableau `.Params.goodPractices` (liste d'UUIDs de `good-practice`).
- Une **good-practice** référence sa thématique via `.Params.thematique`.
- Une **question** (quiz) référence une thématique et une liste de `goodPractices` (UUIDs).

### Frontmatter par type

**thematiques** (`content/thematiques/`)
```yaml
uuid: thematique-xxx
title: ...
icon: fichier.svg          # icône dans /icons/thematiques/illustrations/
videoUrl: https://...      # optionnel
subtitle: ...
description: ...
```

**vulnerabilities** (`content/vulnerabilities/`)
```yaml
uuid: vulnerability-xxx
title: ...
thematique: thematique-xxx
risks: texte markdown
goodPractices:
  - good-practice-xxx
dontDo: texte markdown     # optionnel
```

**good-practices** (`content/good-practices/`)
```yaml
uuid: good-practice-xxx
title: ...
slug: mon-slug-personnalise
thematique: thematique-xxx
niveau: basique | essentiel | avance
tool:                      # optionnel
  name: Nom de l'outil
  url: https://...
  description: ...
```

**questions** (`content/questions/`)
```yaml
uuid: question-xxx
text: ...
correction: texte markdown
goodPractices:
  - good-practice-xxx
thematique: thematique-xxx
choices:
  - isCorrect: true
    text: ...
  - isCorrect: false
    text: ...
```

**definitions** (`content/definitions/`)
```yaml
uuid: definition-xxx
title: ...
contenu: texte
```

### Slugs

Les slugs sont dérivés du champ `uuid` (voir `config.yml` → `frontmatter.slug`). Toujours définir un `uuid` unique dans le frontmatter.

## Layout et templates

Les templates Hugo sont dans `layouts/`. Structure principale :
- `layouts/_default/baseof.html` — base HTML commune ; injecte `data-page-id="{{ .Params.uuid }}"` sur `<body>` (utilisé par le JS de progression).
- `layouts/thematiques/single.html` — page d'une thématique : liste les vulnerabilities liées, puis leurs good-practices. Gère la barre de progression (localStorage) et les dropdowns.
- `layouts/boite-a-outils/list.html` — page auto-générée listant toutes les `good-practices` qui ont un champ `tool.url`, groupées par thématique.
- `layouts/partials/` — head, header, footer, breadcrumb, seo, plausible.

## Styles

Tailwind CSS v3. Le fichier source est `assets/css/styles.css`, compilé vers `assets/css/output/styles.css` (ne pas éditer ce fichier généré).

Couleurs personnalisées définies dans `tailwind.config.js` : `primary`, `secondary`, `tertiary`, `green`, `orange`, `red`, `light_gray`, `dark_gray`.

Les niveaux de `good-practice` ont des couleurs associées : `basique` → `bg-green`, `essentiel` → `bg-blue-500`, `avance` → `bg-red`.

## JavaScript

- `assets/js/main.js` — comportements généraux du site.
- `assets/js/quiz.js` — logique du quiz interactif.
- La progression des checklists est persistée dans `localStorage` avec la clé `checklistState-{uuid}`.

## CMS

Le contenu est géré via **Decap CMS** (interface admin à `/admin/`), configuré dans `static/admin/config.yml`. L'authentification passe par **DecapBridge** (PKCE) connecté au dépôt GitHub `safe-n-tech/www`.

Les UUIDs sont générés automatiquement par le widget `uuid` de Decap avec le préfixe du type (`thematique-`, `vulnerability-`, `good-practice-`, etc.). Les noms de fichiers sont dérivés de l'UUID ou du slug personnalisé selon la collection.
 
## Fonctionnalités
 
- **Checklist interactive** : progression sauvegardée en `localStorage` par thématique, avec barres de progression
- **Quiz** : 10 questions aléatoires parmi le pool, score, correction détaillée, sauvegarde locale
- **Glossaire** : navigation alphabétique avec recherche en temps réel
- **Vérification de fuites** : liens vers Have I Been Pwned et Hack-Naq
- **Mille Bugs** : jeu de plateau téléchargeable en PDF pour la sensibilisation des seniors
---
