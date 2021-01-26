import urllib2
import urlparse
import time
import pprint

import logging

import BeautifulSoup


logging.basicConfig(filename='scrapelog.log',level=logging.DEBUG)




movieURLQueue = {}
actorURL = {}


# processMovieURL does the scraping of a single movie url 
# it gathers the actors in the movies and adds them to an actor url 
# queue, and then calls on processActorURL for each
# in the full graph generating version, it makes the movie object nodes, 
# the actor object nodes and the edges 
#
def processMovieURL(graph, url):
    try:    # in case of 404 error          

        html_page = urllib2.urlopen(url)
        soup = BeautifulSoup.BeautifulSoup(html_page)
        movieURLQueue[url] = True

        #check it is a movie#
        infotable = soup.findAll('p')
        if('film' not in str(infotable)):
            print("not a film")
            logging.warning("not a film")
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
            #    print grossingRaw

                for i in range(100):
                    if '&#91;'+str(i)+'&#93;' in grossingRaw:
                        grossingRaw = grossingRaw.replace('&#91;'+str(i)+'&#93;', '')
                        grossingRaw = grossingRaw.replace("&#160;", "")

                grossingAmount = grossingRaw.replace('$', '').replace(',', '')
              #  print grossingAmount
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

        if money == "Not in Theatres":
            logging.warning("invalid movie")
            movieURLQueue[url] = True
            return
        movie = movieObject(movieTitle, year, money)




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
                        newstring = ("https://en.wikipedia.org/" + link)
                        rank += 1
                        tuple = (newstring, rank)
                        actorURLList.append(tuple)

                else: #on some movies, there is no list, just items under td
                    starList = row.findAll('a')
                    rank = 1
                    for star in starList:
                        link = star['href']
                        newstring = ("https://en.wikipedia.org/" + link)
                        rank += 1
                        tuple = (newstring, rank)
                        actorURLList.append(tuple)

                    
        if starringListFound == False:
            movieURLQueue[url] = True
            return

        for tuple in actorURLList:
            url = tuple[0]
            rank = tuple[1]
            if url not in actorURL:
                actorURL[url] = False
                actor = processActorURL(url)
                if actor == None:
                    logging.warning("invalid actor")
                    continue
                edge = edgeObject(rank, actor, movie)
                graph.addEdge(edge)
                getNewMovieURLfromActor(url)


        movieURLQueue[url] = True
        logging.info(movieTitle+ " movie url processed")
    except:
        movieURLQueue[url] = True   # set as crawled



# this is the function that processes a single actor URL, creates the actor 
# object and returns it to its calling function which was processMovieURL
# processMovieURL calls on getNewmovieURlFromActor
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

        actor = actorObject(name, age)
        return actor
        logging.info(name + " processed")
    except:
        actorURL[url]=True 




# getNewMovieURLfromActor takes a actor url page and gets their
# filmography, and adds those movie URLs to the movie queue 
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
         
        return 
    except:
        logging.debug("page not found")
        print "404"








class edgeObject:
    def __init__(self, rank, actorObject, movieObject):
        self.actorObject = actorObject
        self.weight = 1.0/rank
        self.movieObject = movieObject


class movieObject:
    def __init__(self, title, year, money):
        self.title = title
        self.year = year
        self.money = money


class actorObject:
    def __init__(self, name, age):
        self.name = name
        self.age = age


class movieGraph:
    # constructing functions #
    def __init__(self):
        self.edgeList = []
        self.actorInfoHelper = {}

    def addEdge(self, edgeObject):
        self.edgeList.append(edgeObject)


    def calculateActorInfoHelper(self):
    #enumerate through the edge list, for each new actor, add the weight*grossing of the movie and pass to dictionary
        for edge in self.edgeList:
            actor = edge.actorObject
            weight = edge.weight
            grossing = edge.movieObject.money
            actorGrossing = weight*grossing
            if actor in self.actorInfoHelper:
                self.actorInfoHelper[actor]+=actorGrossing
            self.actorInfoHelper[actor] = actorGrossing
        return 1




    #functionality functions #
    def moneyMovieMade(self, movie):
        for edge in self.edgeList:
            if edge.movieObject.title == movie:
                return edge.movieObject.money
        return "Movie not found"


    def listActorsofMovie(self, movie):
        actorsOfMovie = []
        movieFound = False 
        for edge in self.edgeList:
            if edge.movieObject.title == movie:
                movieFound = True
                actorsOfMovie.append(edge.actorObject.name)
        if movieFound == False:
            return "Movie not found"
        return actorsOfMovie


    def listMoviesofActor(self, actor):
        moviesOfActor = []
        actorFound = False
        for edge in self.edgeList:
            if edge.actorObject.name.strip() == actor.strip():
                actorFound = True
                moviesOfActor.append(edge.movieObject.title)
        if actorFound == False:
            return "Actor not found"
        return moviesOfActor


    def listTopXHighestMoneyActors(self, X):
            #enumerate through actors and take the highest grossing one of that pass
        highestGrossingActors = []
        self.calculateActorInfoHelper()

        for y in range(X):
            maxGrossingonPass = 0
            currentactor = actorObject("none", 0)
            for key in self.actorInfoHelper:
                if self.actorInfoHelper[key] >= maxGrossingonPass:
                    if key.name not in highestGrossingActors:
                        maxGrossingonPass = self.actorInfoHelper[key]
                        currentactor = key
            if currentactor.name != "none":
                highestGrossingActors.append(currentactor.name)

        #a fail condition: werent enough actors to fill X spots
        if(len(highestGrossingActors) < X):
            return "Not enough actors in list"
        return highestGrossingActors


    def listTopXOldestActors(self, X):
        oldestActors = []

        for y in range(X):
            maxAge = 0;
            currentactor = actorObject("none", 0)
            for edge in self.edgeList:
                if edge.actorObject.age >= maxAge:
                    if edge.actorObject.name not in oldestActors:
                        maxAge = edge.actorObject.age
                        currentactor = edge.actorObject
            if currentactor.name != "none":
                oldestActors.append(currentactor.name)
        if len(oldestActors)<X:
            return "Not enough actors in list"
        return oldestActors



    def listMoviesOfAYear(self, year):
        moviesOfYear = []
        yearFound = False
        for edge in self.edgeList:
            if edge.movieObject.year == year:
                yearFound = True
                if edge.movieObject.title not in moviesOfYear:
                    moviesOfYear.append(edge.movieObject.title)
        if yearFound == False:
            return "No movies found from that year"
        return moviesOfYear



    def listActorsOfAYear(self, year):
        actorsOfYear = []
        yearFound = False
        for edge in self.edgeList:
            if edge.movieObject.year == year: 
                yearFound = True
                if edge.actorObject.name not in actorsOfYear:
                    actorsOfYear.append(edge.actorObject.name)
        if yearFound == False:
            return "No actors found from that year"
        return actorsOfYear





def populateGraph(graph, startURL, loopTimes):
    count = 0
    toCrawl = moreToCrawl()
    while(toCrawl):
        toCrawl = moreToCrawl()
        if not toCrawl:
            break
        if count > loopTimes:
            break
        processMovieURL(graph, toCrawl)
        count+=1
        #time.sleep(3)

#this function controls the loop 
def moreToCrawl():

    for url in movieURLQueue:
        if movieURLQueue[url] == False:
            return url
    return False



def makeGraph(startURL, loopTimes):
    # movieURLQueue = {}
    movieURLQueue[startURL] = False
    # actorURL = {}

    graph = movieGraph()
    populateGraph(graph, startURL, loopTimes)
  #  for edge in graph.edgeList:
      #  print(edge.movieObject.title+", "+edge.actorObject.name+", "+str(edge.weight))


    return graph



# startURL = "https://en.wikipedia.org/wiki/Clueless_(film)"
# #startURL = "https://en.wikipedia.org/wiki/The_Room_(film)"
# startURL = "https://en.wikipedia.org/wiki/Ratatouille_(film)"
# makeGraph(startURL, 15)

# for edge in graph.edgeList:
#     print(edge.movieObject.title+", "+edge.actorObject.name+", "+str(edge.weight))

# print(graph.moneyMovieMade("Clueless"))
# print(graph.moneyMovieMade("The Road to El Dorado"))


# #print(graph.moneyMovieMade("Clueless"))
# print(graph.listActorsofMovie("The Road to El Dorado"))


# print(graph.listMoviesofActor("Alicia Silverstone"))
# print(graph.listMoviesofActor("Meg Ryan"))

# print(graph.moneyMovieMade("The Road to El Dorado"))

# #print(graph.listMoviesofActor("Jeff Bridges"))

# # print(graph.listMoviesofActor("David Duchovny"))

# print(graph.listTopXOldestActors(1))
# print(graph.listTopXOldestActors(15))

# print(graph.listTopXHighestMoneyActors(40))
# print(graph.listTopXHighestMoneyActors(10))

# print(graph.listActorsOfAYear("2004"))
# # print(graph.listActorsOfAYear(2019))

# print(graph.listMoviesOfAYear("2000"))
# # print(graph.listMoviesOfAYear(2019))



