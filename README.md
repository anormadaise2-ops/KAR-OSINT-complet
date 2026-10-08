# KAR OSINT

Projet Flask prêt à lancer pour recherche OSINT orientée sources publiques.

## Lancer sous Windows
```powershell
cd KAR-OSINT
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
py app.py
```
Puis http://127.0.0.1:5000

### Inclus
- UI moderne responsive
- recherche pseudo/domaine
- moteurs publics Google/Bing/DuckDuckGo/Brave
- liens de profils candidats
- recherche GitHub API optionnelle via GITHUB_TOKEN
- déduplication
- rate limiting
- page confidentialité
- aucune base applicative d'historique

Le projet ne contourne pas les protections de plateformes et ne récupère pas de données privées.
