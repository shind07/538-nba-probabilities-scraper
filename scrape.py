import lxml.html
import requests
import string, datetime, os, csv, time, random, sys

SLEEP_TIME = 86000 # 1 day
SLEEP_TIME_BUFFER = 800 # 15 mins

csv_name = 'playoff_probabilities.csv'
schema = ['date', 'carmelo_full', 'carmelo_cur', 'team', 'record', 'conferece', 'proj_record', 'proj_diff','playoff_%', 'playoff_adj', 'finals_%', 'champion_%']

def main(*args):
    while True:
        url = 'https://projects.fivethirtyeight.com/2019-nba-predictions/'
        response = requests.get(url)
        tree = lxml.html.fromstring(response.text)
        #tree = lxml.html.parse('sample.html').getroot()
        rows = tree.xpath("//table[@id ='standings-table']/tbody//tr")
        table = []
        for row in rows:
            td_list = row.xpath('./td')
            r = []
            for td in td_list:
                a = td.xpath('./a')
                if len(a) > 0:
                    span = td.xpath('./span')
                    team = a[0].text_content()
                    record = span[0].text_content()
                    r = r + [team, record]
                elif len(td.text_content()) > 0:
                    r.append(td.text_content())
            table.append(r)

        # Check if we need to adjust time zone
        d = datetime.datetime.now()
        if len(args) > 1:
            d = d - datetime.timedelta(hours=8)
        date, current_time = str(d).split(' ')

        # Write data to csv
        file_exists = os.path.exists(csv_name)
        mode = 'a' if file_exists else 'w'
        print(schema)
        with open(csv_name, mode) as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(schema)
            for row in table:
                print([date]+row)
                writer.writerow([date]+row)

        # Sleep til tomorrow
        delay = SLEEP_TIME + (random.random() * SLEEP_TIME_BUFFER)
        print('Sleeping for {}'.format(str(datetime.timedelta(seconds=delay))))
        time.sleep(delay)
        
if __name__ == '__main__':
    main(*sys.argv)
