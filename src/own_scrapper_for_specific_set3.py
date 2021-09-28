import pandas as pd
import argparse
from urllib.request import urlopen
from bs4 import BeautifulSoup
from string import punctuation
import time
import csv 
import os
from datetime import datetime, timedelta
import json

def create_match_files(match):

    # for each url get a df
    
    finished_df, fixed_data = get_rows(match)
    print(finished_df.tail())
    finished_df.to_csv(f'new_1.csv', index = False, header = True, mode='w')
    time.sleep(0.5)


def get_matches(finished_url, date, current = False):
    if not current:
        soup = get_url(f'{finished_url}&dm={date}')
    else:
        soup = get_url(finished_url)
    match_anchors = soup.findAll("a",{"title":"H2H stats - match details"})
    match_urls = [i["href"] for i in match_anchors]
    return create_match_files(match_urls, current)

def get_col_names():
    return ['player1_name',
            'player2_name',
            'set_index',
            'player1_game_score',
            'player2_game_score',
            'server',
            'points',
            'break_point',
            'tournament',
            'round',
            'date',
            'surface',
            'result'
            ]


def get_rows(match):
    match_html = get_url(match)
    fixed_data = get_static_data(match_html)
    scores_data = get_dynamic_data(match_html,fixed_data)
    if not scores_data:
        return False, False
    rows = list()
    for k,v in scores_data.items():
        for score,points in v.items():
            rows.extend(merge_static_dynamic(k,score,points,fixed_data))
    
    return pd.DataFrame.from_records(rows,columns = get_col_names()), fixed_data

def merge_static_dynamic(set,score,points,fixed_data):
    result_list = list()
    row_list = {'player1': fixed_data['player1_name'],
                'player2': fixed_data['player2_name'],
                'set':set,
                'p1_score':score.split('-')[0],
                'p2_score': score.split('-')[1] if len(score.split('-'))>1 else '',
                'server':points[-1],
                'points': 0,
                'break_point': '',
                'tournament':fixed_data['tournament'],
                'round': fixed_data['round'],
                'date': fixed_data['date'],
                'surface': fixed_data['surface'],
                'result': fixed_data['result']
                }
    for i in range(len(points)-1):
        row_list['break_point'] = ''
        if 'BP' in points[i]:
            row_list['break_point'] = 'BP'
        row_list['points'] = points[i].replace('[BP]','')
        result_list.append(list(row_list.values()))
    return result_list

def get_static_data(match_html):
    tr = match_html.find("tr", {"class": "tour_head unpair"})
    static_data = dict()    
    match_details = tr.findAll("td")
    static_cols = ['date','round','player1_name','player2_name', 'result','tournament','surface']
    for index in range(len(static_cols)):
        static_data[static_cols[index]] = match_details[index].text
    static_data['result'] = get_clean_result(match_html)
    return static_data

def get_clean_result(match_html):
    span = match_html.find("span", attrs={"id": "score"})
    tags = span.findAll()
    for tag in tags:
        tag.extract()
    return "".join(span.findAll(text=True))

def get_dynamic_data(match_html,fixed_data):
    scores_div = match_html.find("div", {"id": "ff_p"})
    set_tables = scores_div.findAll('table', {'class': 'table_stats_match'})
    dynamic_data = dict()
    for set in range(len(set_tables)):
        dynamic_data[set+1] = get_scores(set_tables[set],set+1,fixed_data['tournament'])
        if not dynamic_data[set+1]:
            return False

    return dynamic_data

def get_scores(set_table,set_,tournament):
    rows = set_table.findChildren('tr')
    rows = rows[1:-1] if len(rows)%2==0 else rows[1:]
    score_dict = dict()
    print(set_,tournament)
    if set_ == 3 and tournament == ' Melbourne ':
        print('set 3')
        
        for row_index in range(0,len(rows)):
            
            if row_index != 1:
                score , serve = get_current_score(rows[row_index])
                if not score and not serve:
                    return False
                points = [score]
                points.append(serve)
                score_dict[score] = points
    else:
        
        for row_index in range(0,len(rows), 2):
            score , serve = get_current_score(rows[row_index])
            if not score and not serve:
                return False
            points = get_points(rows[row_index + 1])
            points.append(serve)
            score_dict[score] = points
    print(score_dict)
    return score_dict

# Correct the function reflect the score and the serve
def get_current_score(row):
    try:
        server = row.text
        score = ''
        
        cells = row.findAll("td")
        score = cells[1].text
        server = server.replace(score,'')
        return score, server
    except Exception as  e:
        return False, False 

# make the point to win in the last row i.e, if win=True
def get_points(row):
    return row.find("td").text.split(',')


def get_players_data(match_url):
    pass

def get_menu_links(url):
    soup = get_url(url)
    ul = soup.find("ul", {"id": "topmenu_full"})
    li_list = ul.findChildren("li" , recursive=False)
    url_list = []
    for i in [0,2]:
        url_list.append(li_list[i].findChildren("a")[0]["href"])
    return url_list[0], url_list[1]

def get_url(url):
    req = urlopen(url)
    html = str(req.read())
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def get_file_name(fixed_data):
    tour = process_string(fixed_data['tournament'])
    date = process_string(fixed_data['date'])
    rnd = process_string(fixed_data['round'])
    p1 = process_string(fixed_data['player1_name'])
    p2 = process_string(fixed_data['player2_name'])
    
    file_name = f'{tour}_{date}_{rnd}_{p1}_{p2}'
    return file_name


def process_string(str):
    punc = set(punctuation)
    output = []
    for i in str:
        if i not in punc:
            output.append(i)
    
    result = "".join(output)
    result = result.replace(" ", "")

    return result

def get_result(result):
    result = result.replace(" ","")
    results = result.split(',')

    count = 0
    for res in results:
        games = res.split('-')
        if games[0] > games[1]:
            count += 1
        elif games[0] < games[1]:
            count -=1
    
    if count > 0:
        return 1
    
    return 2

def main():
    #fin_url = r'https://www.tennislive.net/wta/match/victoria-azarenka-VS-yulia-putintseva/grampians-trophy-melbourne-2021/'
    #fin_url = r'https://www.tennislive.net/wta/match/elise-mertens-VS-elina-svitolina/melbourne-1-melbourne-2021/'
    #fin_url = r'https://www.tennislive.net/atp/match/felix-corwin-VS-luis-faria/m25-sintra-2021/'
    fin_url = r'https://www.tennislive.net/atp/match/feliciano-lopez-VS-lorenzo-sonego/australian-open-melbourne-2021/'
    create_match_files(fin_url)

if __name__ == '__main__':
    main()