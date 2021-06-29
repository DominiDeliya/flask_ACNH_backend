import requests
from bs4 import BeautifulSoup

from db_client import add_villagers

URL = 'https://animalcrossing.fandom.com/wiki/Villager_list_(New_Horizons)'


def scrape_data(tbl_name):
    # load data from website
    page = requests.get(URL)

    # parse web page with soup
    soup = BeautifulSoup(page.content, 'html.parser')

    # get main table
    main_table = soup.select_one('#mw-content-text > div > table:nth-child(3) > tbody > tr:nth-child(2) > td > table')
    if main_table is None:
        return 1, 'Unable to find the main table'

    table_body = main_table.find('tbody')
    rows = table_body.find_all('tr')
    records = []
    for row in rows:
        cols = row.find_all('td')
        cols = [col for col in cols]

        record = []
        if cols:
            # Name contains space were parsed as items in the list
            name_as_list = cols[0].text.strip().split(' ')
            name = ' '.join(name_as_list)
            record.append(name)

            # image url is inside <a> tag
            full_image_url = cols[1].select_one('a')['href']
            image_url = full_image_url.split('/revision/')[0]
            record.append(image_url)

            # item 0 contains the gender, item 1 is personality
            personality = cols[2].text.strip().split(' ')[1]
            record.append(personality)

            # list always contains one item
            species = cols[3].text.strip().split(' ')[0]
            record.append(species)

            # b-day is present in a format March-13th
            b_day_full = cols[4].text.strip().split(' ')
            b_month = b_day_full[0]
            b_day = b_day_full[1][:-2]
            record.append(b_month)
            record.append(b_day)

            # catch phrase contains space were parsed as items in the list
            catch_phrase = cols[5].text.strip().split(' ')
            catch_phrase = ' '.join(catch_phrase)
            record.append(catch_phrase)

            # list always contains one item
            hobbies = cols[6].text.strip().split(' ')[0]
            record.append(hobbies)

        if record:
            records.append(record)

    # add data to db
    success = add_villagers(tbl_name, records)
    if success:
        return 0, '{} records were added to the Database'.format(len(records))

    return 1, 'Unable to update Database'
