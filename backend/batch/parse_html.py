from bs4 import BeautifulSoup as bs


def parse(html_str: str):
    soup = bs(html_str)

    game_url = soup.head.find(attrs={'property': 'og:url'})["content"]
    game_id = game_url.split("/")[-1]

    info_box = soup.body.find(attrs={'class': 'results_gameInfo__qH8f9'})  
    map_url = info_box.a['href']
    map_name = info_box.a.text

    results_table = soup.body.find(attrs={'class': 'results_table__FHKQm'})
    results = results_table.findAll(attrs={'class': 'results_row__2iTV4'})
    
    for result in results[1:]:
        columns = result.findAll(attrs={'class': 'results_column__BTeok'})
        
        name = columns[0].find('div', 'user-nick_nick__5rr7K').text.strip()
        
        total_column_list = list(columns[-1].children)
        points = int(total_column_list[0].text.replace(",", "").split(" ")[0]) 
        meta = total_column_list[1].text
        
        print(name, points, meta)
        
        