from bs4 import BeautifulSoup
import requests
import pandas
import glob
from collections import OrderedDict

pages_csv = 'characters_pages.csv'
characters_csv ='characters_data.csv'

def gel_all_links():
    page = requests.get('https://www.marvel.com/tv-shows')
    soup = BeautifulSoup(page.content, 'html.parser')
    pages =[]
    mvl_cards=soup.find('div', {'class':'masthead__cards'}).find_all('div', {'class':'mvl-card mvl-card--lob'})
    for i in range(len(mvl_cards)-1):
        link = mvl_cards[i]
        page = link.find('a')
        print(i,page['href'],page.text)
        pages.append(page['href'])

    df = pandas.DataFrame({'Link':pages})
    write_csv_file(df, pages_csv)

def write_csv_file(df,name):
    df.to_csv(name,index=False)
    print('Sucess\n')

def read_csv_file(name):
    df = pandas.read_csv(name)
    return df

def create_characters_df():
    base_url ='https://www.marvel.com'
    pages = pandas.read_csv(pages_csv)
    links = pages['Link']
    marvel_list=[]
    columns=[]

    for link in links:
        marvel_characters=OrderedDict()
        request = requests.get(base_url+str(link))
        content=request.content
        soup = BeautifulSoup(content,'html.parser')
        marvel_characters['Link'] = link
        label=soup.findAll('div',{'class':'featured__data__label'})
        stat=soup.findAll('div',{'class':'featured__data__copy'})

        for i in range(len(label)):
            column =label[i].text.title()
            if column not in columns:
                columns.append(column)
                try:
                    marvel_characters[column]=stat[i].text.replace("\n","").strip()
                except:
                    marvel_characters[column]=""
        marvel_list.append(marvel_characters)

    df = pandas.DataFrame(marvel_list)
    write_csv_file(df, characters_csv)

def main():
    files = glob.glob("*.csv")
    if characters_csv not in files:
        if pages_csv not  in files:
            print('Create characters pages')
            gel_all_links()
        print('Data set create')
        create_characters_df()

    df = read_csv_file(characters_csv)
    df = df.fillna('')
    print('Columns:', df.columns.values)
    print(df[['Link']])

if __name__ == '__main__':
    main()

df =pandas.read_csv('characters_data.csv')
