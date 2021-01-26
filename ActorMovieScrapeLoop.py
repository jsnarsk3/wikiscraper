import urllib2
import urlparse
import time
import pprint

import BeautifulSoup


#start on a movie website

#for each of its cast members, scrape the cast member
#add their movies to the queue

startURL = "https://en.wikipedia.org/wiki/Clueless_(film)"

movieURLQueue = {}
movieURLQueue[startURL] = False

actorURL = {}


#scrape a movie wikipedia
def processMovieURL(url):
    try:    # in case of 404 error    		

        html_page = urllib2.urlopen(url)
        soup = BeautifulSoup.BeautifulSoup(html_page)
    	movieURLQueue[url] = True

        #check it is a movie#
        infotable = soup.findAll('p')
        if('film' not in str(infotable)):
            print("not a film")
            movieURLQueue[url] = True
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
                        actorURLList.append("https://en.wikipedia.org" + link)
                        rank+=1

                    
        if starringListFound == False:
            print("No Starring list found")

        for url in actorURLList:
        	if url not in actorURL:
        		actorURL[url] = False
        		processActorURL(url)
        		getNewMovieURLfromActor(url)


    	movieURLQueue[url] = True
    except:
        movieURLQueue[url] = True   # set as crawled





def processActorURL(url):
    try:    # in case of 404 error
        html_page = urllib2.urlopen(url)
        soup = BeautifulSoup.BeautifulSoup(html_page)

        actorURL[url] = True


        name = soup.title.string[:-11]
        print(name)


        infotable = soup.find('table', {'class':'infobox biography vcard'}, {"style":"width:22em"})
        if infotable == None:
            infotable = soup.find('table',{'class':'infobox vcard plainlist'})

        rows = infotable.findAll('tr')
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
       

     	actorURL[url] = True
    except:
    	actorURL[url]=True 





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

        newURLlist = []
        for row in rows:
            if(row.find('a')!= None):
                rawLink = row.find('a')
                newURLlist.append(rawLink['href'])
       # print(newURLlist)

        newURLS =[]
        for link in newURLlist:
        	newURLstring = "https://en.wikipedia.org"+link 
        	newURLS.append(newURLstring)

        for newurl in newURLS:
        	if newurl not in movieURLQueue:
        		movieURLQueue[newurl] = False
         
     
    except:
    	print "404"




def moreToCrawl():

    for url in movieURLQueue:
    	if movieURLQueue[url] == False:
    		return url
    return False


toCrawl = moreToCrawl()
while(toCrawl):
    toCrawl = moreToCrawl()
    if not toCrawl:
        break
    processMovieURL(toCrawl)
    #time.sleep(3)


