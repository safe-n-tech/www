## Installation

### Installer Hugo (au moins la version v0.133.1+extended)
https://gohugo.io/getting-started/installing/

### Installer les dependences
`yarn i`

### Démarrer le server
`yarn dev`  

## Hébergement
Le site est hébergé sur Netlify, sur le compte de Noesya

## Gestionnaire de contenu (CMS)
[DecapCMS](https://decapcms.org/) est le gestionnaire de contenu utilisé pour Safe-N-Tech.

### Gestion des utilisateurs
Il faut aller sur le compte Netlify qui héberge le site > Site configuration > Identity > Registration

> [!WARNING]
> Mettre l'inscription à "Open" permet à n'importe qui de modifier le contenu du site. Il faut donc ajouter des utilisateur via Github, ou via un lien d'invitation.
> **Vérifiez bien que "Registration preference" est à "Invite-Only**

#### Ajout via un compte (sans GitHub)
Vous pouvez inviter un utilisateur à se créer un compte dans Identity > Users

#### Ajout via Github
Si vous activez la connexion via GitHub, tous les utilisateurs de GitHub qui sont éditeurs sur ce projet pourront se connecter.

