# 🎞️ Humble Software Tracker (Darkroom Edition)

> "Surveillance automatisée des bundles logiciels dans une chambre noire numérique."

![Status](https://img.shields.io/github/actions/workflow/status/Bloodeyesx/Bloodeyesx.github.io/main.yml?label=Développement&style=for-the-badge&color=ef4444)
![Last Scan](https://img.shields.io/badge/Dernier%20Scan-12h-black?style=for-the-badge&logo=clock&logoColor=white)
![System](https://img.shields.io/badge/Système-Actif-success?style=for-the-badge&color=171717)

## 🌑 À propos

Ce projet est une **application de surveillance automatisée** hébergée sur GitHub Pages. Elle scanne en permanence la section *Software* de Humble Bundle pour détecter les nouvelles offres.

Conçu avec une esthétique **"Film Noir / Darkroom"**, le site transforme les données brutes en une planche contact visuelle et interactive. Le système fonctionne en totale autonomie : un robot (Scraper) développe de nouveaux "clichés" des offres toutes les 12 heures.

**🔗 [ACCÉDER AU TRACKER EN DIRECT](https://bloodeyesx.github.io/)**

---

## 📸 Fonctionnalités

* **🕵️ Scraper Furtif :** Un script Python optimisé qui navigue dans le code source de Humble Bundle pour extraire les données cachées.
* **📡 Flux RSS Natif :** Génère et héberge un fichier `software_feed.xml` compatible avec tous les lecteurs RSS du marché.
* **🔴 Interface Darkroom :** * Design inspiré des laboratoires photo (Grain argentique, Noir profond).
  * Mode "Lumière inactinique" (Accents rouges).
  * Révélation des images au survol de la souris.
* **⚡ 100% Automatisé :** Zéro maintenance requise. GitHub Actions gère l'exécution, le commit et le déploiement.
* **📱 Responsive :** Les planches s'adaptent parfaitement aux mobiles, tablettes et écrans larges.

---

## 🛠️ Stack Technique

Le projet repose sur une architecture "Serverless" utilisant l'infrastructure gratuite de GitHub :

| Composant | Technologie | Rôle |
| :--- | :--- | :--- |
| **Moteur** | `Python 3.9` | Extraction des données JSON de Humble Bundle |
| **Chimie** | `BeautifulSoup4` | Traitement et nettoyage du HTML |
| **Diffusion** | `FeedGen` | Création du flux XML standardisé |
| **Automate** | `GitHub Actions` | Exécution programmée (CRON 12h) |
| **Rendu** | `TailwindCSS` | Interface utilisateur "Darkroom" |

---

## 🎞️ Comment ça marche ?

1.  **Déclenchement :** Toutes les 12 heures, le workflow GitHub se réveille.
2.  **Exposition :** Le script `scraper.py` capture l'état actuel des bundles.
3.  **Développement :** Un fichier `software_feed.xml` est généré à la racine.
4.  **Tirage :** GitHub pousse automatiquement le fichier et met à jour le site.
5.  **Révélation :** Le site web lit le XML et affiche les nouvelles cartes.

---

## 🔧 Installation (Pour Forker)

Si vous souhaitez créer votre propre instance de ce tracker :

1.  **Forkez** ce dépôt sur votre compte GitHub.
2.  Activez les **GitHub Actions** dans l'onglet "Actions" de votre nouveau dépôt.
3.  Allez dans **Settings > Pages** et activez le déploiement depuis la branche `main` / dossier `root`.
4.  Lancez le workflow **Update Software RSS** manuellement une première fois pour initialiser les données.

---

## 📝 Crédits & Licence

* **Concept Original :** Inspiré par les outils de tracking open-source.
* **Design & Code :** Refonte complète "Darkroom" (2026).
* **Données :** Les informations et images des bundles appartiennent à Humble Bundle Inc. Ce projet est un outil de veille non-officiel.

---

<div align="center">
  <p><i>Développé avec ❤️ et du café noir.</i></p>
</div>
---

## 📝 Crédits

* **Concept Original :** Inspiré par les travaux de la communauté open-source sur les RSS Humble Bundle.
* **Design & Code :** Refonte complète "Darkroom" et optimisation du scraper Python (2026).
* **Données :** Fournies par Humble Bundle Inc. (Ce projet n'est pas affilié à Humble Bundle).

---

<div align="center">
  <p><i>Développé avec ❤️ et du café noir.</i></p>
</div>
