---
title: Pas le temps de lire
description: Pas le temps de tout lire ? Voici les réflexes qui font vraiment la différence.
recommendations:
  - title: 01. Des mots de passe longs
    icon: passphrase
    text: >-
      Visez au moins 16 caractères. Une carte graphique récente casse un mot de
      passe de 12 caractères en quelques heures.


      Le plus simple est d'enchaîner 4 ou 5 mots pris au hasard, par exemple ChienPluieMontagneBougie. C'est plus solide qu'un mélange illisible, et vous vous en souviendrez.


      À éviter : prénoms, dates de naissance, nom du chat, suites clavier (azerty, 123456). Et pas de mot de passe noté sur un post-it, dans un fichier texte ou dans les notes du téléphone.


      Pour voir si un mot de passe circule déjà dans des fuites, il y a haveibeenpwned.com/passwords. Faites-le en navigation privée, et pas avec un mot de passe que vous utilisez réellement.
  - title: 02. Un mot de passe par compte
    icon: unique-keys
    text: >-
      Quand un site se fait pirater, les identifiants volés sont testés
      automatiquement sur des centaines d'autres sites. C'est le credential
      stuffing. Si vous utilisez partout le même mot de passe, une seule fuite
      suffit à ouvrir tous vos comptes.


      Commencez par votre boîte mail principale : c'est elle qui sert à réinitialiser tous les autres mots de passe. Ensuite la banque et PayPal, puis les réseaux sociaux, le site des impôts et Ameli. Ces comptes-là doivent avoir un mot de passe unique, même si vous n'utilisez pas de gestionnaire. Activez aussi la double authentification quand elle est proposée.
  - title: 03. Un gestionnaire de mots de passe
    icon: vault
    text: >+
      Trois options sérieuses :
       
      - KeePassXC : hors ligne, open source, recommandé par l'ANSSI.

      - Bitwarden : open source, audité de façon indépendante.

      - Proton Pass : hébergé en Suisse, chiffré de bout en bout.

      Pour les comptes sensibles, évitez le gestionnaire intégré au navigateur.
       
      Le mot de passe maître doit être une phrase de passe longue, utilisée nulle part ailleurs et jamais stockée en ligne. Exportez votre coffre de temps en temps sur un support chiffré, hors ligne. Si vous y gardez des accès professionnels, ne le synchronisez pas sur un cloud que vous ne maîtrisez pas.

  - title: 04. La double authentification
    icon: mfa
    text: >
      04. La double authentification
       
      Toutes les méthodes ne se valent pas :
       
      - SMS : à éviter. Un attaquant peut détourner votre numéro (SIM swapping) ou intercepter le message.

      - E-mail : ne vaut que ce que vaut la sécurité de votre boîte.

      - Application d'authentification (Aegis, Ente Auth, 2FAS) : c'est le bon choix pour la plupart des gens.

      - Clé physique FIDO2, type YubiKey : le niveau le plus élevé, et elle résiste au phishing.

      À l'activation, le service vous donne des codes de récupération. Gardez-les hors ligne. Et ne donnez jamais un code par téléphone, même à quelqu'un qui dit appeler du support technique.
  - title: 05. Un antivirus
    icon: antivirus
    text: >+
      Bitdefender, ESET et Malwarebytes Premium obtiennent régulièrement de bons
      résultats chez AV-Test (av-test.org) et AV-Comparatives
      (av-comparatives.org). Windows Defender, intégré à Windows 10 et 11,
      suffit pour un usage perso de base, mais pas seul en contexte
      professionnel.
       
      Ne coupez jamais l'antivirus pour installer un logiciel, même « juste cinq minutes ». C'est une méthode d'infection classique.
       
      Sur Android, un antivirus a aussi sa place, même si on y pense rarement. iOS est plus fermé et donc moins exposé.

  - title: 06. Alias et adresses jetables
    icon: email-alias
    text: >
      Un alias est une adresse qui redirige vers votre vraie boîte. Vous pouvez
      répondre depuis l'alias sans révéler votre adresse réelle.
       
      - SimpleLogin (simplelogin.io), open source, racheté par Proton.

      - addy.io, open source, avec une offre gratuite confortable.

      - Proton Mail (proton.me), alias inclus dans l'abonnement.

      - Apple Masquer mon adresse e-mail, avec iCloud+.

      L'idée est de créer un alias par service. Si vous recevez du spam sur amazon-xyz@alias.io, vous savez qui a fuité ou revendu votre adresse.
       
      Les adresses jetables (guerrillamail.com, temp-mail.org, 10minutemail.com) servent pour une inscription unique. Ne les utilisez pas pour un compte que vous voudrez récupérer un jour : l'adresse disparaît, et l'accès avec.
       
      Enfin, n'utilisez pas votre adresse professionnelle pour vous inscrire sur des services tiers.
  - title: 07. Plusieurs adresses e-mail
    icon: email-segmentation
    text: >+
      Quatre adresses, chacune avec son rôle :
       
      - Pro : uniquement pour le travail.

      - Perso : famille, amis, banque, administrations.

      - Achats : sites marchands, abonnements, cartes de fidélité.

      - Poubelle : forums, concours, téléchargements.

      Pour les usages sensibles, préférez Proton Mail (proton.me, Suisse) ou Tuta (tuta.com/fr, Allemagne) à Gmail ou Yahoo. Évitez aussi le format prenom.nom : il facilite le doxing et le phishing ciblé.

  - title: 08. Ce qu'on ne donne pas à une IA grand public
    icon: ai-data
    text: >-
      Ne collez jamais dans ChatGPT, Gemini ou Copilot :
       
      - des noms ou des données personnelles,

      - des données RH ou médicales,

      - des secrets industriels.

      Selon les conditions d'utilisation, ce que vous saisissez peut servir à entraîner le modèle, être lu par les équipes de l'éditeur ou se retrouver dans une fuite. Au minimum, désactivez l'historique ou l'amélioration des modèles dans les paramètres.
       
      Pour un usage pro, il y a deux pistes : une IA installée en local (Ollama avec Llama ou Mistral, rien ne sort de la machine), ou une offre cloud souveraine (Mistral AI entreprise, Azure avec données hébergées en France).
  - title: 09. Les mises à jour
    icon: updates
    text: >
      Une faille critique est souvent exploitée dans les 72 heures après sa
      publication. Activez les mises à jour automatiques.
       
      On oublie souvent le navigateur et ses extensions, la box internet, et tous les appareils connectés : smartphone, caméra IP, NAS, télé.
       
      Windows 10 n'est plus supporté depuis octobre 2025. Un système hors support ne reçoit plus de correctifs de sécurité. Désinstallez aussi les logiciels que vous n'utilisez plus : moins de logiciels, moins de failles possibles.
       
      En entreprise, WSUS ou SCCM permettent de centraliser les mises à jour pour que tous les postes soient au même niveau.
  - title: 10. Le phishing, sous toutes ses formes
    icon: phishing
    text: >-
      Le nom affiché d'un expéditeur se falsifie très facilement. Regardez
      l'adresse réelle, celle entre chevrons : <email@domaine.com>.
       
      Lisez les liens lettre par lettre : paypa1.com n'est pas paypal.com, et « rn » ressemble beaucoup à « m ». Pour vérifier un lien sans cliquer dessus : VirusTotal (virustotal.com) ou urlscan.io.
       
      Les attaques les plus efficaces sont aussi les plus discrètes :
       
      - Le spear phishing utilise des infos réelles sur vous (prénom, employeur, actualité récente) pour paraître crédible.

      - Le quishing passe par un QR code. Ne scannez pas un QR code reçu par mail ou collé dans un lieu public sans vérifier.

      - Le vishing se fait par téléphone, et les deepfakes audio peuvent imiter la voix d'un proche. Convenez d'un mot de code avec votre entourage, ou raccrochez et rappelez.

      En cas de doute, contactez l'organisme vous-même, avec un numéro ou une adresse trouvés ailleurs que dans le message.
---
