# Soccer results

Gather footbal scores, matches and standings from different world wide football leagues.
![Script in acction](./futbol_anim.gif)

## Requirements

requests, beautifulsoup

## Usage

``from futbol import Futbol

fut = Futbol()

fut.leagues.keys()   # To watch the leagues available

league = fut.get_league(fut.LEAGUE)

league.results
league.next_rounds      # return a dict with rounds with matches to come
league.results          # return a dict with rounds with matches already played
league.stands           # return a list with the standings, points, goals and other data
`` 
