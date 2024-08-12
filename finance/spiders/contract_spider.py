from pathlib import Path

import scrapy
import pandas as pd

# the global list
items = []
class ContractSpider(scrapy.Spider):
    name = "contract"

    def start_requests(self):
        urls = [
            "https://hoopshype.com/salaries/players/"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        header_raw = response.css("table.hh-salaries-ranking-table thead tr td::text").getall()
        
        header = [name.replace('\n', '').replace('\t','') for name in header_raw]
        for player_row in response.css("table.hh-salaries-ranking-table tbody tr"):
            item={
                "Player":player_row.css('td.name a::text').get().replace('\n','').replace('\t', ''),
                "contracts": [contract.strip('\n').strip('\t').replace(',', '').strip('$')
                              for contract in player_row.css('td[style]::text').getall()],
                "type": [color.replace('color:', '') for color in player_row.css('td[style]::attr(style)').getall()]
            }
            items.append(item)
            
    def closed(self, reason):
        '''Method to be called after the spider finishes'''

        # create datafrane from the global list 'items'
        df = pd.DataFrame(items, columns=['Player', 'contracts', 'type'])
        
        # print(df['contracts'][0])
        # do whatefer operations you want
        df[["Y2023-24", "Y2024-25", "Y2025-26", "Y2026-27", "Y2027-28", "Y2028-29"]] = pd.DataFrame(df['contracts'].to_list(), index= df.index)
        df[["Type2023-24", "Type2024-25", "Type2025-26", "Type2026-27", "Type2027-28", "Type2028-29"]] = pd.DataFrame(df['type'].to_list(), index= df.index)
        df = df.replace(["black", "rgb(4, 134, 176)", "rgb(255, 0, 0)", "rgb(0, 153, 0)", "rgb(168, 0, 212)"],
                  ["Guaranteed", "Player Option", "Team Option", "Qualifying Offer", "Two-Way"])
        df = df.drop(columns = ['contracts', 'type'])
        df_new = pd.wide_to_long(df.reset_index(), stubnames=['Y', 'Type'], i = 'index', j='Season', suffix='[0-9\-]+').reset_index()
        df_new = df_new.rename(columns={"Y":"Salary"}).sort_values(by=['index', 'Season']).reset_index(drop=True)
        df_new = df_new.drop(columns = ['index'])
        df_new.to_csv('Finance.csv', index=False)