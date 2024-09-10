import re
from bs4 import BeautifulSoup as bs


def parse(html_str: str):
    soup = bs(html_str, features="html.parser")

    game_url = soup.head.find(attrs={'property': 'og:url'})["content"]
    game_id = game_url.split("/")[-1]

    info_box = soup.body.find(attrs={'class': re.compile('^results_gameInfo')})  
    map_url = info_box.a['href']
    map_name = info_box.a.text

    results_table = soup.body.find(attrs={'class': re.compile('^results_table')})
    results = results_table.findAll(attrs={'class': re.compile('^results_row_')})
    
    parsed_results = []
    
    for result in results[1:]:
        columns = result.findAll(attrs={'class': re.compile('^results_column')})
        
        name = columns[0].find('div', re.compile('^user-nick_nick')).text.strip()
        
        total_column_list = list(columns[-1].children)
        points = int(total_column_list[0].text.replace(",", "").split(" ")[0]) 
        # meta = total_column_list[1].text
        
        single_result = (name, points)
        parsed_results.append(single_result)
        
    return (game_id, map_name, parsed_results)
        
        