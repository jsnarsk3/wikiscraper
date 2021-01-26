import fullScraperGraphGenerator as gg
import json

startURL = "https://en.wikipedia.org/wiki/Ratatouille_(film)"
# movieURLQueue = {}
# movieURLQueue[startURL] = False
# actorURL = {}
graph = gg.makeGraph(startURL, 10)
# for edge in graph.edgeList:
# 	print(edge.movieObject.title)
#print(graph)





#graph to JSON takes in a graph object (the one I made), and converts it
#to a json file that can be read by my json parser 
def graphToJson(graph):
	actorDict = {}
	movieDict = {}
	jsonList = [actorDict, movieDict] #jsonList[0] is actors, jsonList[1] is movies

	for edge in graph.edgeList:
		actorName = edge.actorObject.name 
		actorAge = edge.actorObject.age
		movieTitle = edge.movieObject.title
		movieGrossing = edge.movieObject.money
		movieYear = edge.movieObject.year

		if actorName not in actorDict:
			currentActorDict = {}
			currentActorDict["json_class"] = "Actor"
			currentActorDict["name"] = actorName
			currentActorDict["age"] = actorAge
			currentActorDict["movies"] = []

		currentActorDict["movies"].append(movieTitle)
		actorDict[actorName] = currentActorDict
		
		if movieTitle not in movieDict:
			currentmovieDict = {}
			currentmovieDict["json_class"] = "Movie"
			currentmovieDict["name"] = movieTitle
			currentmovieDict["box_office"] = movieGrossing
			currentmovieDict["year"] = movieYear
			currentmovieDict["actors"] = []
		currentmovieDict["actors"].append(actorName)
		movieDict[movieTitle] = currentmovieDict
		

	return jsonList


data = graphToJson(graph)

with open('mydata.json', 'w') as outfile:
    json.dump(data, outfile)
