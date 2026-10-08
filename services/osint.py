import os,re
from urllib.parse import quote_plus,urlparse
import requests
TIMEOUT=8

def add(results,title,url,source,description='',kind='public-search'):
    if url.startswith(('http://','https://')): results.append({'title':title,'url':url,'source':source,'description':description,'kind':kind})

def dedupe(results):
    seen=set(); out=[]
    for x in results:
        k=x['url'].rstrip('/').lower()
        if k not in seen: seen.add(k); out.append(x)
    return out

def search_username(username):
    username=re.sub(r'\s+',' ',username.strip())[:80]; q=quote_plus(f'"{username}"'); u=quote_plus(username); r=[]
    profiles=[('GitHub',f'https://github.com/{u}'),('GitLab',f'https://gitlab.com/{u}'),('Reddit',f'https://www.reddit.com/user/{u}/'),('Twitch',f'https://www.twitch.tv/{u}'),('YouTube',f'https://www.youtube.com/@{u}'),('TikTok',f'https://www.tiktok.com/@{u}'),('Instagram',f'https://www.instagram.com/{u}/'),('X',f'https://x.com/{u}'),('Steam',f'https://steamcommunity.com/id/{u}')]
    for source,url in profiles: add(r,f'{source} — profil potentiel',url,source,'Page candidate à vérifier.','profile-candidate')
    for source,url in [('Google',f'https://www.google.com/search?q={q}'),('Bing',f'https://www.bing.com/search?q={q}'),('DuckDuckGo',f'https://duckduckgo.com/?q={q}'),('Brave Search',f'https://search.brave.com/search?q={q}')]: add(r,f'{source} — recherche Web',url,source,'Recherche publique du pseudo.','web-search')
    for source,domain in [('GitHub','github.com'),('Reddit','reddit.com'),('YouTube','youtube.com'),('Twitch','twitch.tv'),('GitLab','gitlab.com'),('Discord public web','discord.com')]:
        add(r,f'{source} — occurrence Web',f'https://www.google.com/search?q={quote_plus(f"site:{domain} \'{username}\'")}',source,'Recherche de pages publiques indexées.','web-search')
    token=os.getenv('GITHUB_TOKEN','').strip()
    if token:
        try:
            x=requests.get('https://api.github.com/search/users',params={'q':username,'per_page':10},headers={'Accept':'application/vnd.github+json','Authorization':f'Bearer {token}','User-Agent':'KAR-OSINT/1.0'},timeout=TIMEOUT)
            if x.ok:
                for user in x.json().get('items',[]):
                    if user.get('login') and user.get('html_url'): add(r,f"GitHub — {user['login']}",user['html_url'],'GitHub API','Compte public renvoyé par l’API GitHub.','api-public')
        except requests.RequestException: pass
    return dedupe(r)

def search_domain(domain):
    domain=domain.strip().lower(); domain=urlparse(domain).netloc if '://' in domain else domain.split('/')[0]; q=quote_plus(domain); r=[]
    add(r,'Google — domaine',f'https://www.google.com/search?q={q}','Google','Recherche publique du domaine.','web-search')
    add(r,'Bing — domaine',f'https://www.bing.com/search?q={q}','Bing','Recherche publique du domaine.','web-search')
    add(r,'crt.sh — certificats publics',f'https://crt.sh/?q={q}','crt.sh','Certificats TLS publiquement consultables.','public-dataset')
    add(r,'Internet Archive — Wayback',f'https://web.archive.org/web/*/{q}','Internet Archive','Archives publiques potentiellement disponibles.','public-archive')
    return dedupe(r)
