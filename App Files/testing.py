import requests
from bs4 import BeautifulSoup


def wiki_scrape(url):

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    movie_name = None
    year = None
    budget = None
    box_office = None
    rt_url = None

    if soup.find(id="firstHeading") != None:
        movie_name = soup.find(id="firstHeading")
    
    infobox = soup.find('table', {'class': 'infobox'})


    box_len = len(infobox.find_all('th', class_="infobox-label"))
    for i in range(box_len):
        tag = soup.find_all("th", class_="infobox-label")[i]

        #Find Budget
        if tag.text == "Budget" or tag.text == "Box office":
            temp = soup.find_all("td", class_="infobox-data")[i]
            temp = temp.text

            #convert string to int
            temp = temp.split()
            num = ""
            for c in temp[0]:
                if (ord(c) >= 48 and ord(c) <= 57) or c == '.':
                    num = num + c
                elif c == '[' or c == ']':
                    break
            num = float(num)

            if temp[-1][0] == "m":
                num = num *1000000
            elif temp[-1][0] == "b":
                num = num *1000000000
            elif temp[-1][0] == "t":
                num = num *1000

            if tag.text == "Budget":
                budget = int(num)
            else:
                box_office = int(num)

        if tag.text == "Release dates":
            temp = soup.find_all("td", class_="infobox-data")[i]
            temp = temp.text
            temp = temp.split()
            for x in temp:
                if len(x) == 4:
                    if x[0] == '2' or x[0] == '1':
                        temp = x
                        break
            year = int(temp)



    return movie_name.string, budget, box_office, year

    

def rt_scrape(url, num, movie_id):

    url =  url+"/reviews?type=top_critics"

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    review_table = soup.find(class_="review_table")
    num_revs = 20

    if num_revs > num:
        num_revs = num

    ret = []
    
    for i in range(num_revs):
        row = soup.find_all(class_="row review_table_row")[i]
        review_text = row.find(class_="the_review").text.strip()
        critic_name = row.find(class_="unstyled bold articleLink").text
        ret.append([critic_name, review_text])
    
    return ret

            

    



def main():

    # print(wiki_scrape("https://en.wikipedia.org/wiki/Spider-Man:_No_Way_Home"))
    # print(wiki_scrape("https://en.wikipedia.org/wiki/The_Meyerowitz_Stories"))

    print(rt_scrape("https://www.rottentomatoes.com/m/spider_man_no_way_home",45,1))

main()