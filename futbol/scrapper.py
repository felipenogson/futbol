# coding: utf-8
# Comentarios en spanglish
# comentarios: felipe@nogson.com
# 2020-09-27 22:00:27

from bs4 import BeautifulSoup
import requests
import string

scorespro = 'https://scorespro.com'


class Futbol:
    def __init__(self):
        self.leagues = self.get_leagues()
        for key in list(self.leagues):
            setattr(self, key, key)

    def get_league(self, league):
        results = self.results(league)
        next_rounds = self.next_rounds(league)
        return League(self.leagues[league], results, next_rounds)

    def get_leagues(self):
        ''' Return a dictionary { league_code: url } '''

        # Scrap off the soccer leagues from the footer of the page
        website = requests.get(scorespro)
        soup = BeautifulSoup(website.text, 'html.parser')
        football = soup.select("div#collapseFootball")[0]
        leagues_raw = football.select("li")
        leagues = [] 
        for league in leagues_raw:
            liga = league.select('h4')[0]
            url = liga.a

            # !!!!! Este hack es por que en el sitio de scrap la url esta mal direccionada para la liga española
            if url.attrs['href'] == "/soccer/spain/primera-division/":
                url.attrs['href'] = "/soccer/spain/laliga/"

            # simplifying the leagues names
            league = (liga.text.replace('-', '_').replace('–','_').replace(' ', ''), url.attrs['href'])

            leagues.append(league)
        # Just selecting club leagues (No world cup, no uefa)
        leagues = leagues[4:-3]
        return {league:url for league,url in leagues}


    def next_rounds(self, liga: str) -> dict:
        # Descarga los datos de la liga seleccionada
        # Revisa los nombres que hacepta con la función get_leagues()
        liga = requests.get(scorespro+self.leagues[liga]+"/fixtures") 
        soup = BeautifulSoup(liga.text, 'html.parser')
        national = soup.select('div#national')[0]

        # Hace un diccionario de las jornadas {rounds}
        rounds = {'league':[]} # Here goes the title of the table that we are not going to use
        round = 'league' # the same prupose than above
        for child in national.children:
            if hasattr(child,'attrs'): 
                    if 'ncet' in child.attrs.get('class', ''):
                        round = (child.text)
                        if round not in rounds:
                            rounds[round] = []
                    if child.name == 'table':
                        # Limpia el string de caracteres que no se imprimen
                        item = ''.join(ch for ch in child.text if ch in string.printable).strip().strip(' \n-')
                        rounds[round].append(item)
        return rounds

    def results(self, liga: str) -> dict:
        # Descarga los datos de la liga seleccionada
        # Revisa los nombres que hacepta con la función get_leagues()
        liga = requests.get(scorespro+self.leagues[liga]+"/results") 
        soup = BeautifulSoup(liga.text, 'html.parser')
        national = soup.select('div#national')[0]

        # Hace un diccionario de las jornadas {rounds}
        results = {'league':[]} # Here goes the title of the table that we are not going to use
        result = 'league' # the same prupose than above
        for child in national.children:
            if hasattr(child,'attrs'): 
                    if 'ncet' in child.attrs.get('class', ''):
                        result = (child.text)
                        if result not in results:
                            results[result] = []
                    if child.name == 'table':
                        # Limpia el string de caracteres que no se imprimen
                        item = ''.join(ch for ch in child.text if ch in string.printable).strip().strip(' \n-')
                        item = item[:item.find('\n')].strip()
                        results[result].append(item)
        return results

class League:
    def __init__(self, league, results, next_rounds):
        self.league = league
        self.results = results
        self.next_rounds = next_rounds
        self.stands = self.standings()
    
    def standings(self):
        stands = requests.get(scorespro+self.league+"standings")
        soup = BeautifulSoup(stands.text, "html.parser")
        standings_1a = soup.select('div#standings_1a')[0]
        teams = standings_1a.select('table.gteam')
        # La primera lista seran los Headers
        stands = []
        header = standings_1a.select('table.st-tbl-header')[0]
        ths = header.select('th')
        t = []
        for th in ths:
           t.append(th.text.strip())
        stands.append(t)
        for team in teams:
            tds = team.select('td')
            t = []
            for td in tds:
                t.append(td.text.strip())
            stands.append(t)
        return stands