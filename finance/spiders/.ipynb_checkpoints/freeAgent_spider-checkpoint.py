from pathlib import Path

import scrapy
import pandas as pd
import re

# the global list
items = []
class FreeAgentSpider(scrapy.Spider):
    name = "freeAgent"

    def start_requests(self):
        urls = [
            "https://www.cbssports.com/nba/news/2020-nba-free-agency-tracker-anthony-davis-re-signs-with-lakers-bogdan-bogdanovic-joins-hawks/",
            "https://www.cbssports.com/nba/news/nba-free-agency-tracker-2021-lakers-reload-with-carmelo-anthony-dwight-howard-other-vets-bulls-make-moves/",
            "https://www.cbssports.com/nba/news/2022-nba-free-agency-tracker-james-harden-76ers-agree-to-two-year-deal-raptors-sign-juancho-hernangomez/",
            "https://www.cbssports.com/nba/news/2023-nba-free-agency-tracker-latest-deals-signings-with-notable-names-still-available/"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # year
        year_info = response.css("div.ArticleContentHeader-title::text").get()
        if year_info is None:
            year_info = response.css("div.Article-bodyContent h2::text").get()
        year = re.findall("\d+",year_info)[0]
        for fa_row in response.css("table.TableBase-table.free-agent-tracker tbody tr.TableBase-bodyTr"):
            
            # Get Player Name and Age
            player_info = fa_row.css("td div span.player-name a::text").get()
            if player_info is None:
                player_info = fa_row.css("td div span::text").get()
                player_name = " ".join(player_info.replace('\n', '').split())
            else:
                player_name = player_info.replace('\n', '').strip()
                
            # Get position info
            pos = fa_row.css('td:nth-child(3)::text').get()
            
            # Get Contract info
            contract = fa_row.css('td:nth-child(6)::text').get()
            
            item={
                "FreeAgent": player_name,
                "Position": pos,
                "Contract": contract,
                "FA_Year": year
            }
            items.append(item)
            
    def closed(self, reason):
        '''Method to be called after the spider finishes'''

        # create datafrane from the global list 'items'
        df = pd.DataFrame(items, columns=['FreeAgent', 'Position', 'Contract', 'FA_Year'])
        
        # print(df['contracts'][0])
        # do whatefer operations you want
        df_new = df[df['Contract'] == df['Contract']]
        
        # print(df_new.shape)
        def get_contract(x):
            contract = re.findall('(?<=\$)\d+\.?\d*', x['Contract'])
            if not contract:
                return 0
            return float(contract[0]) * 1000000
        
        def get_years(x):
            # print(x['Contract'])
            year = re.findall('\d+(?=[-\s]year)', x['Contract'])
            print(year)
            if not year:
                return 1
            return float(year[0])
        
        # print(df_new.apply(lambda x: get_contract(x), axis = 1).shape)
        df_new.loc[:, 'Years'] = df_new.apply(lambda x: get_years(x), axis = 1)
        df_new.loc[:,'Contract'] = df_new.apply(lambda x: get_contract(x), axis = 1)
        
        df_new = df_new[df_new['Contract'] > 0]
        df_new['AVG_SALARY'] = df_new['Contract'] / df_new['Years']
        df_new.to_csv('nba_contracts.csv', index=False)