# cooldays

Nouvelle version du site des gîtes Cool Days (Sippenaeken), style « D · Charte d'origine ».

Site statique : HTML + CSS, un petit fichier JavaScript facultatif, aucune dépendance, aucun build.

## Voir le site en local

```sh
python -m http.server 8000
```

Puis ouvrir http://localhost:8000.

## Structure

| Fichier | Contenu |
|---|---|
| `index.html` | Accueil |
| `gite-1.html`, `gite-2.html` | Détail de chaque gîte + photos |
| `photos.html` | Toutes les photos |
| `tarifs.html` | Grilles de prix, frais, calendrier des saisons |
| `seminaire.html` | Salle de séminaire |
| `environs.html` | Activités autour + liens utiles |
| `contact.html` | Coordonnées + formulaire |
| `nl/`, `de/` | Les mêmes 8 pages en néerlandais et en allemand |
| `assets/css/style.css` | Toute la mise en forme (couleurs en haut du fichier) |
| `assets/js/main.js` | Menu mobile, visionneuse photos, formulaire |
| `assets/fonts/` | Baloo 2 et Nunito Sans (licence SIL OFL), servies localement |
| `assets/img/` | Photos reprises du site actuel cooldays.be |

L'en-tête et le pied de page sont répétés dans chaque page : une modification (téléphone, menu…) doit être faite dans les 24 fichiers (8 pages × 3 langues).

## À savoir

- Toutes les pages contiennent `<meta name="robots" content="noindex">` tant que c'est une version de test. À retirer à la mise en ligne définitive.
- Le formulaire de contact n'a pas de serveur : il ouvre la messagerie du visiteur avec le message prérempli, adressé à info@cooldays.be.
- Le français est à la racine, le néerlandais dans `nl/`, l'allemand dans `de/`. Le sélecteur FR · NL · DE renvoie vers la même page dans l'autre langue.

## Modifier les textes

Les pages sont générées par `tools/build.py` à partir des textes de `tools/i18n.py` (une section par langue).

```sh
pip install pillow      # une seule fois, sert à lire la taille des images
python tools/build.py   # régénère les 24 pages
```

Le script écrase les fichiers `.html` : faire les modifications dans `tools/`, pas directement dans les pages. Le dossier `tools/` n'est pas nécessaire pour faire tourner le site.
