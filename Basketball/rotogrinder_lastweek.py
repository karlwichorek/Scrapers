#scraper for Rotogrinders Misc

from bs4 import BeautifulSoup
import urllib2
import csv
import demjson

url = "https://rotogrinders.com/game-stats/nba-player?site=fanduel&range=1week"

page = urllib2.urlopen(url).read()
soup = BeautifulSoup(page, "html.parser")

rotogrinder_lastweek = open('rotogrinder_lastweek.csv', 'w')
rotogrinder_lastweek.write("Player, Team, Pos, Salary, GP, MIN, REB, AST, STL, BLK, TO, PTS, USG, FPTS" + "\n")

script = soup.find_all('script')[6:7]
js_obj = script[0].text
js_obj = js_obj.lstrip()
js_obj = js_obj.rstrip()
js_obj = js_obj[31:]
js_obj = js_obj.lstrip()
js_obj = js_obj[11:]
js_obj = js_obj[:-55]
js_obj = js_obj.rstrip()
js_obj = js_obj[:-30]
js_obj = js_obj.rstrip()
js_obj = js_obj[:-1]

py_obj = demjson.decode(js_obj)

for line in py_obj:
    player = (line['player'])
    team = line['team']
    pos = line['pos']
    salary = line['salary']
    gp = line['gp']
    mins = float(line['min']) / float(gp)
    reb = float(line['reb']) / float(gp)
    ast = float(line['ast']) / float(gp)
    stl = float(line['stl']) / float(gp)
    blk = float(line['blk']) / float(gp)
    to = float(line['to']) / float(gp)
    pts = float(line['pts']) / float(gp)
    usg = line['usg']
    fpts = line['fpts']
    fpts = float(fpts) / float(gp)
    fpts = round(fpts, 2)

    data = (player, team, pos, salary, gp, mins, reb, ast, stl, blk, to, pts, usg, fpts)
    rotogrinder_lastweek.write('%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s \n' % data)

rotogrinder_lastweek.close()

reader = csv.reader(open("rotogrinder_lastweek.csv"))

row = 0

html = '<table>'

for row in reader:
    html += '<tr>'
    for column in row:
            html += '<th>' 
            html += column 
            html += '</th>'
    html += '</tr>'

html += '</table>'
