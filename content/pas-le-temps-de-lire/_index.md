---
title: Pas le temps de lire
description: Pas le temps de tout lire ? Voici les réflexes qui font vraiment la différence.
recommendations:
  - title: " 01 — Mots de passe longs et complexes"
    icon: 🔑
    text: >2
        Longueur et structure
      •	Minimum 16 à 20 caractères — les GPU modernes cassent un mot de passe de 12 caractères en quelques heures par force brute.

      •	Privilégier une phrase de passe (passphrase) : 4 à 5 mots aléatoires assemblés — ex. ChienPluieMontagneBougie — plus solide et mémorisable qu'une suite de caractères illisible.

      À ne jamais utiliser

      •	Prénoms, dates de naissance, noms d'animaux

      •	Suites clavier : azerty, 123456, qwerty

      •	Tout stockage en clair : fichier texte, post-it, notes de smartphone — un mot de passe doit rester secret.

      Vérification de robustesse

      •	A titre éducatif, vous pouvez vérifier si un mot de passe a déjà fuité sur haveibeenpwned.com/passwords — en navigation privée pour éviter toute identification et à ne pas tester sur un véritable mot de passe.
  - title: 02 — Un mot de passe différent par service
    icon: 🔑
    text: >
      Comprendre le risque : credential stuffing

      •	Les attaquants testent en masse des couples login/mot de passe issus de fuites sur des centaines de sites. Un seul mot de passe réutilisé = compromission en cascade.

      Comptes à sécuriser en priorité absolue

      •	Messagerie principale — c'est la clé maîtresse : tous les autres mots de passe se réinitialisent via cette boîte email.

      •	Banque et services financiers comme Paypal

      •	Réseaux sociaux, espace impôts, Ameli

      Ces comptes doivent avoir des mots de passe uniques même en l'absence de gestionnaire de mots de passe. Dans la mesure du possible, ayez recours à la double authentification
  - title: 03 — Gestionnaire de mots de passe
    icon: 🧰
    text: >2
       Solutions recommandées
      •	KeePassXC — hors ligne, open source, préconisé par l'ANSSI

      •	Bitwarden — open source, audité indépendamment

      •	Proton Pass — hébergement suisse, chiffrement E2E

      •	Proscrire les gestionnaires intégrés aux navigateurs pour les usages sensibles.

      Mot de passe maître

      •	Doit être une passphrase longue et unique (alphanumérique et caractères spéciaux), jamais réutilisée nulle part, jamais stockée en ligne.

      Sauvegarde et pièges

      •	Exporter régulièrement le coffre et stocker la sauvegarde sur support chiffré hors ligne.

      •	Ne pas synchroniser son coffre sur un cloud non maîtrisé si l'on gère des données professionnelles sensibles.
  - title: 04 — Double authentification (2FA / MFA)
    icon: 🤳
    text: >2
       Hiérarchie des méthodes (de la moins à la plus sécurisée)
      •	❌ SMS — vulnérable au SIM swapping et à l'interception SS7 — à éviter

      •	⚠️ E-mail — dépend entièrement de la sécurité de la boîte mail 

      •	✅ Application TOTP : Aegis (Android, open source), Ente Auth, 2FAS — recommandé

      •	✅✅ Clé physique FIDO2 (YubiKey) — résistante au phishing, niveau maximal

      Bonnes pratiques

      •	Sauvegarder ses codes de récupération lors de l'activation — les stocker hors ligne.

      •	Ne jamais communiquer un code 2FA par téléphone, même à quelqu'un se présentant comme le support technique (vishing et spoofing).
  - title: 05 — Protection antivirus et EDR
    icon: 🦠
    text: >2
       Solutions recommandées
      •	Bitdefender, ESET, Malwarebytes Premium — régulièrement bien notés par https://www.av-test.org et https://av-comparatives.org 

      •	Windows Defender (intégré à Windows 10/11) constitue une base acceptable, mais insuffisant seul pour un usage professionnel.

      Points de vigilance

      •	Ne jamais désactiver l'antivirus, même temporairement pour installer un logiciel — vecteur d'infection classique.

      •	Antivirus sur smartphone Android ( https://www.av-test.org) souvent négligé mais pertinent (iOS est plus fermé par architecture).
  - title: 06 — Alias e-mail et adresses jetables
    icon: ✉️
    text: >2
       Services d'alias (permanents)
      •	https://simplelogin.io  (par Proton, open source) — « alias » permanents redirigés vers votre vraie boîte, réponse possible sans révéler l'adresse réelle.

      •	https://addy.io  — open source, version gratuite généreuse.

      •	https://proton.me Proton Mail (abonnement) — gestion d'alias native.

      •	Apple Hide My Email https://support.apple.com/en-gb/105078  — intégré à l'écosystème Apple (iCloud+).

      Adresses jetables (usage unique)

      •	https://www.guerrillamail.com/fr/, https://temp-mail.org , https://10minutemail.com   — pour inscriptions ponctuelles sans suivi nécessaire.

      •	⚠️ Ne pas utiliser pour des comptes à récupérer : l'adresse expire et l'accès est définitivement perdu.

      Pratiques opérationnelles

      •	Créer un alias par service : si du spam arrive sur amazon-XYZ@alias.io, on sait quelle base de données a fuité ou été revendue.

      •	Ne jamais utiliser son adresse professionnelle institutionnelle pour des inscriptions à des services tiers.

      •	Compartimenter : un alias achats, un alias newsletters, un alias forums.
  - title: 07 — Segmentation des adresses e-mail
    icon: 📥
    text: >2
       Architecture recommandée
      •	Adresse pro institutionnelle — communications professionnelles officielles uniquement.

      •	Adresse perso principale (chiffrée si possible) — famille, amis, banque, administrations.

      •	Adresse achats/commerce — e-commerce, abonnements, cartes de fidélité.

      •	Adresse poubelle — forums, concours, téléchargements.

      Fournisseurs recommandés pour la confidentialité

      •	Proton Mail https://proton.me (Suisse, chiffrement E2E), Tuta https://tuta.com/fr   (Allemagne) — à préférer à Gmail/Yahoo pour les usages sensibles.

      •	Éviter prenom.nom comme identifiant dans le corps de son adresse émail: facilite le doxing et le spear phishing.
  - title: 08 — Données sensibles et IA grand public
    icon: 🧠
    text: >2
       Ce qui ne doit jamais être saisi dans une IA grand public
      •	Noms de personnes, données personnelles, informations sensibles nominatives

      •	Données RH, informations médicales, secrets industriels

      Pourquoi c'est risqué

      •	Les données saisies peuvent servir à l'entraînement des modèles (selon les CGU), être accessibles aux équipes de l'éditeur, ou exposées en cas de fuite.

      Mesures minimales sur ChatGPT / Gemini / Copilot

      •	Activer le mode "sans historique" ou désactiver l'amélioration des modèles dans les paramètres.

      Alternatives pour usage professionnel

      •	IA déployée en local : Ollama + LLaMA / Mistral — risque contrôlé, aucune donnée transmise.

      •	Offres cloud souveraines : Mistral AI entreprise, Azure avec résidence des données en France.

      Distinguer impérativement : IA grand public (risque élevé) vs IA sur infrastructure maîtrisée (risque contrôlé).
  - title: 09 — Mises à jour régulières
    icon: 💻
    text: >2
       Urgence des correctifs
      •	Une vulnérabilité critique est souvent exploitée dans les 72 heures suivant sa publication. Les mises à jour automatiques sont une nécessité, pas une option.

      Périmètre souvent oublié

      •	Navigateur web et ses extensions / plugins

      •	Routeur / box internet (firmware)

      •	Smartphones, caméras IP, NAS, téléviseurs connectés

      Fin de support et logiciels orphelins

      •	Windows 10 en fin de support (octobre 2025) — tout système hors support ne reçoit plus de correctifs de sécurité.

      •	Désinstaller les logiciels non utilisés réduit la surface d'attaque.

      Contexte professionnel

      •	WSUS / SCCM pour les structures professionnelles : centraliser la gestion des mises à jour pour garantir un déploiement homogène.
  - title: 10 — Vigilance phishing — toutes formes
    icon: 👺
    text: >2
       Vérifications techniques de base
      •	Display name spoofing : l'affichage du nom peut être falsifié. Toujours vérifier l'adresse réelle entre chevrons <email@domaine.com>.

      •	Homoglyphes : paypa1.com vs paypal.com, "rn" qui ressemble à "m" — lire l'URL caractère par caractère.

      •	Analyser un lien sans le visiter : https://www.virustotal.com/gui/home/upload, https://urlscan.io .

      Formes avancées d'attaque

      •	Spear phishing : attaques ciblées utilisant des informations personnelles (prénom, employeur, événement récent) pour paraître légitimes 

      •	Quishing : phishing via QR code — ne jamais scanner un QR reçu par e-mail ou affiché en lieu public sans vérification préalable.

      •	Vishing : phishing vocal — les deepfakes audio permettent d'imiter une voix connue. Instaurer un mot de code avec ses proches (ou raccrocher en cas de doute).

      Réflexe en cas de doute

      •	Contacter directement l'organisme supposé expéditeur via un numéro ou une adresse trouvée indépendamment — jamais via les coordonnées contenues dans le message suspect.
---
