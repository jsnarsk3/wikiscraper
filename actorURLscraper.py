inputURL = "https://en.wikipedia.org/wiki/Patricia_Vonne"
inputURL2 = "https://en.wikipedia.org/wiki/Alexis_Bledel"
inputURL3 = "https://en.wikipedia.org/wiki/Jessica_Alba"
inputURL4 = "https://en.wikipedia.org/wiki/Devon_Aoki"
inputURL5 = "https://en.wikipedia.org/wiki/Brittany_Murphy"
inputURL6 = "https://en.wikipedia.org/wiki/Devon_Aoki"
inputURL7 = "https://en.wikipedia.org/wiki/Leonardo_DiCaprio"
inputURL8 = "https://en.wikipedia.org/wiki/Devon_Aoki"
inputURL9 = "https://en.wikipedia.org/wiki/Devon_Aoki"
inputURL10 = "https://en.wikipedia.org/wiki/Devon_Aoki"
inputURL11 = "https://en.wikipedia.org/wiki/Devon_Aoki"
inputURL12 = "https://en.wikipedia.org/wiki/Devon_Aoki"
inputURL13 = "https://en.wikipedia.org/wiki/Devon_Aoki"
inputURL14 = "https://en.wikipedia.org/wiki/Devon_Aoki"


inputURLList = {inputURL, inputURL2, inputURL3, inputURL4, inputURL5, inputURL6, inputURL7, inputURL8, inputURL9, inputURL10, inputURL11, inputURL12, inputURL13, inputURL14}

resultUrl = {inputURL:False}
# key is a url we want. value is True or False. True means already crawled

# from urllib import urlopen
import urllib2
import urlparse
import time
import pprint
import random

import BeautifulSoup # get html links

def processOneUrl(url):
    try:    # in case of 404 error
        html_page = urllib2.urlopen(url)
        soup = BeautifulSoup.BeautifulSoup(html_page)
      #  print(soup.prettify())
       # print(soup.title.string)
    #     castlist = soup.find('span', {'class', 'toclevel-1 tocsection-2'})

        name = soup.title.string[:-11]
        print(name)


        infotable = soup.find('table', {'class':'infobox biography vcard'}, {"style":"width:22em"})
        if infotable == None:
            infotable = soup.find('table',{'class':'infobox vcard plainlist'})

        rows = infotable.findAll('tr')
        #print(rows)

        isDead = False
        for row in rows:
            if('Born' in row.text):
                bornIndex = row.findAll('span', {'style':'display:none'})[0]
                yearBorn = bornIndex.text[1:5]

            if('Died' in row.text):
                isDead = True
                deadIndex = row.findAll('span', {'style':'display:none'})[0]
                yearDied = deadIndex.text[1:5]
                currentYear = 2019
                age = int(yearDied) - int(yearBorn)

        if isDead == False:
            ageData = infotable.find('span', {'class':'noprint ForceAgeToShow'})
            age = ageData.text[10:-1]
       
        print(age)




    #    filmtable = soup.find('table', {'class':'wikitable sortable jquery-tablesorter'})
      #  print(filmtable)

                # index = row.text.find('aged')
                # age = row.text[index+10:]
      #  print (age)
      #  print(getNewMovieURLfromActor(url))

        getNewMovieURLfromActor(url)
      #  print(getNewMovieURLfromActor(url))

     
    except:
        resultUrl[url] = True   # set as crawled




def getNewMovieURLfromActor(url):
    try:    # in case of 404 error
        html_page = urllib2.urlopen(url)
        soup = BeautifulSoup.BeautifulSoup(html_page)
        
        if soup.find('span', {'id':'Filmography'}) == None:
            return -1

        filmtable = soup.find('table', {'class':'wikitable sortable'})
        if filmtable == None:
            #in the case that filmography is stored in simple wikitable
            filmtable = soup.find('table', {'class':'wikitable'})


        if filmtable == None:
            #if its not one of these formats (some actors have lists) give up because im not checking for it
            return -1


        # #in the case that filmography is stored in simple wikitable
        rows = filmtable.findAll('tr')
      #  print(rows)
        randomURLlist = []
        for row in rows:
            if(row.find('a')!= None):
                rawLink = row.find('a')
             #   print(rawLink)
                randomURLlist.append(rawLink['href'])
        numLinks = len(rows)
        randomIndex = random.randrange(numLinks)
        randomURL = rows[randomIndex]
        print(randomURL.a['href'])





     
    except:
        resultUrl[url] = True   # set as crawled

for url in inputURLList:
    processOneUrl(url)

# processOneUrl(inputURL5)



