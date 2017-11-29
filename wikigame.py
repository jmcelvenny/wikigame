import requests
from collections import deque

#Change these
START_PAGE="Jumio" #Should be random
END_PAGE="Adolf_Hitler" #Whatever you want

#Don't change these
WIKI_BASE="https://en.wikipedia.org/wiki/"
LINK_START="<a href=\"/wiki/"
LINK_END="\""
MAPPINGS = {}

#Definitely don't change this
def __main__():
	MAPPINGS[START_PAGE] = ""
	q = deque([START_PAGE])
	while(len(q) != 0):
		cur = q.popleft()
		print("Made CURL request to %s" % WIKI_BASE+cur)
		links = getAllReferences(cur);
		for link in links:
			if (link not in MAPPINGS):
				MAPPINGS[link] = cur
				q.append(link)
			if (link == END_PAGE):
				exitRoutine()

	print("Searched through all of the pages and could not find a path to the destination!")

def exitRoutine():
	stack = []
	look = END_PAGE
	while(look != ""):
		stack.append(look)
		look = MAPPINGS[look]

	total = len(stack)
	print("Found the shortest path: %s clicks" % (total-1))
	while(len(stack) != 0):
		cur = stack.pop()
		count = total - len(stack)
		print("\t%s.\t%s" % (count, cur))

	exit()

def getAllReferences(item):
	res = []
	headers = {
	    'user-agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
	    'cache-control': "no-cache"
	}

	response = requests.request("GET", WIKI_BASE+item, headers=headers)
	text = response.text.encode('utf-8').strip()
	links = findAllLinks(text)

	for link in links:
		if (":" not in link and link is not "Main_Page"):
			res.append(link)

	return res

def findAllLinks(text):
	res = []
	index = 0
	while index < len(text):
		index = text.find(LINK_START, index)
		if (index == -1):
			break
		end_index = text.find(LINK_END, index+len(LINK_START))
		res.append(text[index+len(LINK_START):end_index])
		index += len(LINK_START)
	return res

__main__()