import json



#these are the key components of the graph, the actor object holds relevant 
#information about a certain actor
#the movie object holds relevant information about a certain movie
#the edge object links actors that were in certain movies, and associates
#a weight to the edge, based on the position of the actor on the starring list
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



#this is the class that defines the graph that we will make over the course
#of a scrape
#the graph itself is a list of edge objects
#the edge object contains the actor object and the movie object, and a weight
#there are some graph analysis functions you can call on a graph object
class movieGraph:
    # constructing functions #
    def __init__(self):
        self.edgeList = []
        self.actorInfoHelper = {}


    #this is the function that adds an edge object to the edge list
    def addEdge(self, edgeObject):
        self.edgeList.append(edgeObject)


 
    #calculateActorInfoHelper is used for some of the data analysis
    #it sets up the actorinfohelper dict which calculates the money
    #each actor made
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

    #a graph analysis, scans the graph and returns the box office amount
    #for a certain movie
    def moneyMovieMade(self, movie):
        for edge in self.edgeList:
            if edge.movieObject.title == movie:
                return edge.movieObject.money
        return "Movie not found"

    #a graph analysis function, lists the cast list of a movie by scanning the graph
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

    #graph analysis function, lists the movies that a certain actor has been in
    def listMoviesofActor(self, actor):
        moviesOfActor = []
        actorFound = False
        for edge in self.edgeList:
            if edge.actorObject.name == actor:
                actorFound = True
                moviesOfActor.append(edge.movieObject.title)
        if actorFound == False:
            return "Actor not found"
        return moviesOfActor


    #graph analysis function, uses actorInfoHelper to return the top X highest
    #earning actors, based on my parameterization of money earned by actor
    #if there are not X actors in the list, it says so 
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


#this graph analysis function scans the graph and calculates the X oldest actors of the list
#and returns the list of actors, if there are not X actors in graph, it says so
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


#this function scans the graph to find movies that 
#came out in a certain year
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


#this function scans the graph to find the actors who acted in movies that 
#came out in a certain year
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


#this function calculates the most central actors, the actors that have
#acted in movies with other actors 
    def hubActors(self):
     	movieActorDict = {}
     	for edge in self.edgeList:
     		movieTitle = edge.movieObject.title
     		actorName = edge.actorObject.name
     		if movieTitle not in movieActorDict:
     			movieActorDict[movieTitle] = []
     		movieActorDict[movieTitle].append(actorName)

     	actorCount = {}
     	for movie in movieActorDict:
     		actorList = movieActorDict[movie]

     		for actor in actorList:
     			if actor not in actorCount:
     				actorCount[actor] = len(actorList)
     			else:
     				actorCount[actor] += len(actorList)

     	

     	print(actorCount)
     	return 

#this function calculates the amount of money that actors of a certain age
#made, the amount is found by multiplying the weight of the actor (1/spot on cast list)
#by the grossing amount of that movie
    def mostGrossingAge(self):
    	ageMoneyCount = {}
    	for edge in self.edgeList:
    		weight = edge.weight
    		moneyActorMade = weight * edge.movieObject.money
    		actorAge = edge.actorObject.age

    		if actorAge not in ageMoneyCount:
    			ageMoneyCount[actorAge]= moneyActorMade
    		else:
    			ageMoneyCount[actorAge] += moneyActorMade

    	print(ageMoneyCount)		
    	return 







#JSONtoGraph takes a json file and parses it into the graph structure
#that represents the data for analysis 
def JSONtoGraph(data):

	graph = movieGraph()
	movieActorDict = {}

	for i in range(len(data)):
		current = data[i]
		for thing in current:
			
			singleActorMovieDict = current[thing]
			
			nclass = singleActorMovieDict['json_class']

			#go through the movies and save their list of actors
			#save its movie information and make a movie object
			#we will make a dictionary that lists the actors for 
			#a movie object			
			if(nclass == "Movie"):

				title = singleActorMovieDict["name"]
				year = singleActorMovieDict["year"]
				money = singleActorMovieDict["box_office"]
				# print(title)
				# print(year)
				# print(money)
				if(year==0 and money==0):
					continue
				newmovie = movieObject(title, year, money)
				movieActorDict[newmovie] = []
				actors = singleActorMovieDict["actors"]
				
				rank = 2
				for actor in actors:
					actor = actor.replace("(actor)", "")
					actor = actor.replace("(singer)", "")
					actor = actor.replace("(entertainer)", "")
					actorTuple = (actor, rank)
					rank+=1
					movieActorDict[newmovie].append(actorTuple)

	#at this point the movieActorDict should be full, we will now 
	#go and process the actors in the list
	#if they match a movie that was already found, we insert the 
	#actor object and make an edge
	for i in range(len(data)):
		current = data[i]
		for thing in current:
			
			singleActorMovieDict = current[thing]
			
			nclass = singleActorMovieDict['json_class']
			if(nclass == "Actor"):
				#if the current object is an actor
				age = singleActorMovieDict['age']
				#some name cleaning 
				name = singleActorMovieDict["name"]
				name = name.replace("(actor)", "")
				name = name.replace("(singer)", "")
				name = name.replace("(entertainer)", "")

				#check if the entry is valid , if so make an actor object
				if age > 0:
					if name.find('%')== -1:
						newactor = actorObject(name, age)
				movies = singleActorMovieDict["movies"]
				for movie in movies: #the movies that an actor object held
					for testmovieObject in movieActorDict:
						if testmovieObject.title == movie:
							actorList = movieActorDict[testmovieObject]
							if actorList == []:
								continue
							for actor in actorList:
								#print actor
								if actor[0] == newactor.name:
									rank = actor[1]
									newEdge = edgeObject(rank, newactor, testmovieObject)
									graph.addEdge(newEdge)



	return graph








#This is the main portion of the program
#it opens the json file, and sends it to the graph parser
#it calls all of the data analysis functions

with open('jdata.json') as data_file:    
	data = json.load(data_file)

graph = JSONtoGraph(data)



for edge in graph.edgeList:
	print(edge.movieObject.title+", "+edge.actorObject.name+", "+str(edge.weight))
	# print edge.actorObject.name
	# print((edge.actorObject.age))
	# if edge.actorObject.age == 94:
	# 	print "here"
	# 	print edge.actorObject.name

# print(graph.moneyMovieMade("The Expendables"))
# print(graph.moneyMovieMade("Cop Out"))

# print(graph.listActorsofMovie("Pulp Fiction"))

# print(graph.listMoviesofActor("Jason Statham"))


# print(graph.listTopXOldestActors(2))
# print(graph.listTopXHighestMoneyActors(2))

# print(graph.listActorsOfAYear(1995))
# print(graph.listActorsOfAYear(2019))

# print(graph.listMoviesOfAYear(1995))
# print(graph.listMoviesOfAYear(2019))


graph.hubActors()
graph.mostGrossingAge()


