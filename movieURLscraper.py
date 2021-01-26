inputURL = "https://en.wikipedia.org/wiki/Boy_Eats_Girl"
i2 = "https://en.wikipedia.org/wiki/Avatar_(2009_film)"
i3 = "https://en.wikipedia.org/wiki/All_Souls_Day_(film)"
i4 = "https://en.wikipedia.org/wiki/Borat"
i5 = "https://en.wikipedia.org/wiki/Frankenstein_(1910_film)"
i6 = "https://en.wikipedia.org/wiki/Sin_City_(film)"
i7 = "https://en.wikipedia.org/wiki/Harry_Potter_and_the_Deathly_Hallows_%E2%80%93_Part_2"
i8 = "https://en.wikipedia.org/wiki/Fantastic_Four_(2015_film)"
i9 = "https://en.wikipedia.org/wiki/Poseidon_(film)"
i10 = "https://en.wikipedia.org/wiki/Rise_of_the_Guardians"
i11 = "https://en.wikipedia.org/wiki/Sinbad:_Legend_of_the_Seven_Seas"
i12 = "https://en.wikipedia.org/wiki/Solo:_A_Star_Wars_Story"


inputURLList = {inputURL, i2, i3, i4, i5, i6, i7, i8, i9, i10, i11, i12}

resultUrl = {inputURL:False}
# key is a url we want. value is True or False. True means already crawled

# from urllib import urlopen
import urllib2
import urlparse
import time
import pprint

import BeautifulSoup # get html links

def processOneUrl(url):
    try:    # in case of 404 error
        html_page = urllib2.urlopen(url)
        soup = BeautifulSoup.BeautifulSoup(html_page)
      #  print(soup.prettify())
       # print(soup.title.string)
    #     castlist = soup.find('span', {'class', 'toclevel-1 tocsection-2'})

        #check it is a movie#
        infotable = soup.findAll('p')
        if('film' not in str(infotable)):
            print("not a film")
       #     movieURLQueue[url] = True
            return


        #FIND THE MOVIE TITLE#
        infotable = soup.find('table', {'class':'infobox vevent'}, {"style":"width:22em;font-size:90%;"})
        movieTitle = infotable.find('th', {'class':'summary'}).text
        print(movieTitle)

        #FIND THE YEAR#
        infotable = soup.find('table', {'class':'infobox vevent'}, {"style":"width:22em;font-size:90%;"})
        yearData = infotable.find('span', {'class':'bday dtstart published updated'})
        year = yearData.text[:4]
        print(year)


        infotable = soup.find('table', {'class':'infobox vevent'}, {"style":"width:22em;font-size:90%;"})
        rows = infotable.findAll('tr')
        
        #FIND THE GROSSING INFORMATION#

        boxOfficeBool = False
        for row in rows: 
            if('Box office' in row.text):
                boxOfficeBool = True
                grossingRaw = row.find('td').text

                for i in range(100):
                    if '&#91;'+str(i)+'&#93;' in grossingRaw:
                        grossingRaw = grossingRaw.replace('&#91;'+str(i)+'&#93;', '')

                grossingAmount = grossingRaw.replace('$', '').replace(',', '')
                if grossingAmount[-7:] == "million":
                    grossingMultiplier = 1000000
                    grossingDigits = float(grossingAmount[:-7])
                    money = grossingMultiplier * grossingDigits
                elif grossingAmount[-7:] == "billion":
                    grossingMultiplier = 1000000000
                    grossingDigits = float(grossingAmount[:-7])
                    money = grossingMultiplier * grossingDigits
                else:
                    money = float(grossingAmount)
        if boxOfficeBool == False:
            money = "Not in Theatres"

        print(money)




        #find the list of actor urls who were in this movie#
        #add them to a list, we will process them one at a time
        #when we are done processing them, we will pick a random movie from lead
        #this will be the new url to process 

        #making actor object will happen here since we have to give it a rank
        actorURLList = []
        starringList = True
        for row in rows:
           # print(row)
         #   print(row.text)
            if('Starring' in row.text):
                starringListFound = True
                #sometimes the starring list is stored as a plainlist#
                plainlist = row.find('div', {'class':'plainlist'})
                if plainlist != None:
                    starList = plainlist.findAll('li') 
                    rank = 1
                    for star in starList:
                        link = star.a['href']
                        actorURLList.append("https://en.wikipedia.org/" + link)
                        rank += 1

                else: #on some movies, there is no list, just items under td
                    starList = row.findAll('a')
                    rank = 1
                    for star in starList:
                        link = star['href']
                        actorURLList.append("https://en.wikipedia.org/" + link)
                        rank+=1

                    
        if starringListFound == False:
            print("No Starring list found")
        print(actorURLList)




    except:
        resultUrl[url] = True   # set as crawled


processOneUrl(i12)
# for url in inputURLList:
#     processOneUrl(url)

