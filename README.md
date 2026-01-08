# 🎞️ Humble Software Tracker (Darkroom Edition)

> "Surveillance automatisée des bundles logiciels dans une chambre noire numérique."

![Status](https://img.shields.io/github/actions/workflow/status/Bloodeyesx/Bloodeyesx.github.io/main.yml?label=Développement&style=for-the-badge&color=ef4444)
![Last Scan](https://img.shields.io/badge/Dernier%20Scan-12h-black?style=for-the-badge&logo=clock)

## 🌑 À propos

Ce projet est une **application automatisée** hébergée sur GitHub Pages qui surveille en permanence la section *Software* de Humble Bundle.

Conçu avec une esthétique **"Film Noir / Darkroom"**, il transforme les données brutes en une planche contact visuelle élégante. Le système fonctionne de manière autonome grâce à un robot (Scraper) qui développe de nouvelles "clichés" des offres toutes les 12 heures.

**🔗 [Voir le Tracker en Direct](https://bloodeyesx.github.io/)**

---

## 📸 Fonctionnalités

* **🕵️ Scraper Furtif :** Un script Python blindé qui détecte les bundles cachés dans le code source de Humble Bundle.
* **📡 Flux RSS Natif :** Génère automatiquement un fichier `software_feed.xml` compatible avec n'importe quel lecteur RSS.
* **🔴 Darkroom UI :** Une interface utilisateur personnalisée inspirée des laboratoires photo (Grain argentique, Noir profond, Lumière inactinique).
* **⚡ 100% Automatisé :** Zéro maintenance. GitHub Actions gère l'exécution, le commit et le déploiement.
* **📱 Responsive :** Les cartes se développent parfaitement sur mobile, tablette et bureau.

---

## 🛠️ Stack Technique

Le projet repose sur une architecture "Serverless" utilisant l'infrastructure gratuite de GitHub :

| Composant | Technologie | Rôle |
| :--- | :--- | :--- |
| **Moteur** | `Python 3.9` | Scrape les données JSON de Humble Bundle |
| **Chimie** | `BeautifulSoup4` & `FeedGen` | Traitement du HTML et création du RSS |
| **Automate** | `GitHub Actions` | Lance le script via CRON (toutes les 12h) |
| **Interface** | `HTML5` & `TailwindCSS` | Affichage "Darkroom" avec effet de grain |
| **Hébergement** | `GitHub Pages` | Diffusion statique du site et du flux XML |

---

## 🎞️ Comment ça marche ?

1.  **Déclenchement :** Toutes les 12 heures, GitHub réveille l'automate.
2.  **Exposition :** Le script `scraper.py` capture les données depuis Humble Bundle.
3.  **Développement :** Un fichier `software_feed.xml` est généré/mis à jour.
4.  **Tirage :** GitHub pousse le nouveau fichier et met à jour le site web instantanément.
5.  **Révélation :** L'interface `index.html` lit le XML et affiche les nouvelles cartes avec un effet de révélation au survol.

---

## 🔧 Installation (Pour Forker)

Si vous souhaitez créer votre propre instance de ce tracker :

1.  **Forkez** ce dépôt.
2.  Activez les **GitHub Actions** dans l'onglet "Actions" de votre nouveau dépôt.
3.  Allez dans **Settings > Pages** et activez le déploiement depuis la branche `main` / dossier `root`.
4.  Lancez le workflow **Update Software RSS** manuellement une première fois pour initialiser les données.

---

## 📝 Crédits

* **Concept Original :** Inspiré par les travaux de la communauté open-source sur les RSS Humble Bundle.
* **Design & Code :** Refonte complète "Darkroom" et optimisation du scraper Python (2026).
* **Données :** Fournies par Humble Bundle Inc. (Ce projet n'est pas affilié à Humble Bundle).

---

<div align="center">
  <p><i>Développé avec ❤️ et du café noir.</i></p>
</div>
