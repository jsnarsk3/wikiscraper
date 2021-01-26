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

    def movieInGraph(self, title):
        for edge in self.edgeList:
            if edge.movieObject.title == title:
                return movieObject
            else:
                return -1

    def actorInGraph(self, name):
        for edge in self.edgeList:
            if edge.actorObject.name == name:
                return actorObject
            else:
                return -1



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
            if edge.actorObject.name == actor:
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







#testing
# m1 = movieObject('Hello', 1995, 7110000)
# m2 = movieObject("Movie", 2019, 1000000)
# a1 = actorObject("Juliana Snarski", 23)
# a2 = actorObject("Dany Kofman", 23)
# a3 = actorObject("mike snarski", 60)
# e4 = edgeObject(3, a3, m1)
# e1 = edgeObject(1, a1, m1)
# e2 = edgeObject(2, a2, m1)
# e3 = edgeObject(1, a3, m2)

# graph = movieGraph()
# graph.addEdge(e1)
# graph.addEdge(e2)
# graph.addEdge(e3)
# graph.addEdge(e4)



# print(graph.moneyMovieMade("Hello"))
# print(graph.moneyMovieMade("Movie"))

# print(graph.listActorsofMovie("Hello"))

# print(graph.listMoviesofActor("Juliana Snarski"))


# print(graph.listTopXOldestActors(2))
# print(graph.listTopXHighestMoneyActors(2))

# print(graph.listActorsOfAYear(1995))
# print(graph.listActorsOfAYear(2019))

# print(graph.listMoviesOfAYear(1995))
# print(graph.listMoviesOfAYear(2019))








