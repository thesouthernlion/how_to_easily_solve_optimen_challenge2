import sys


def convert_last_num(value):
  return value.replace(",", "")

trips = []
def trip_id_creator(value):
  tripsNum = []
  tripsDate = []
  value = value.strip('"')
  trips = value.split(",")
  for item in trips:
    tripsNum.append(item[:4])
    tripsDate.append(item[4:])
  return tripsNum, tripsDate

def trip_num_list_creator(NumList, baseList):
  tripsNumList= []
  for num in NumList:
    newList = baseList.copy()
    newList[7] = '"' + num + '"'
    tripsNumList.append(newList)
  #print(tripsNumList)  
  return tripsNumList

def trip_index_list_creator(lenList, startIndex):
  indexList = []
  for item in lenList:
    startIndex += 1
    indexList.append(startIndex - 1)
  return indexList  

def bidgroup_list_creator(List):
  bidgroupList = []
  counter_line = 0
  for item in List:    
    if (item[2] == '"BIDGROUP"'):
      bidgroupList.append(counter_line - 1)
      counter_line = 0
    counter_line += 1
  
  bidgroupList.append(counter_line - 1 )
  return bidgroupList

def trip_index_list_creator_2(List):
  indexList = []
  counter_line = 0
  for item in List:    
    if (item[2] != '"BIDGROUP"'):
      counter_line += 1
      indexList.append(counter_line)
    elif (item[2] == '"BIDGROUP"'):
      counter_line = 0
    
  return indexList

lines = []

for line in sys.stdin:
  lines.append(line.strip())


outputsList = []
lineList = []
outputsInOneList = []
bidgroupCounter = 0
baseTripIdCounter = 0
advancedTripCounter = 0
bidgroupCounter2 = 0

""" Printing For """
for line in lines:
  # bidgroup counter  

  lineList = line.split(", ")     # Spliting the lines

  lastVal = convert_last_num(lineList[-1])      # solved the last item 
  lineList[-1] = lastVal
  
  if lineList[2] == '"BIDGROUP"':
    bidgroupCounter2 += 1

  if lineList[2] == '"ADVANCED_TRIP"' or lineList[2] == '"TRIP_ID"':
    advancedTripCounter += 1
    if (advancedTripCounter <= 1):
        baseTripIdCounter = lineList[4]
    #if lineList[2] == '"ADVANCED_TRIP"':
      #advancedTripCounter += 1  
      
      #if (advancedTripCounter <= 1):
        #baseTripIdCounter = lineList[4]
    #else:
      #baseTripIdCounter = lineList[4]
    
  
  if lineList[2] == '"ADVANCED_TRIP"':
    
    lineList[2] = '"TRIP_ID"'
    tripsNum, tripsDate = trip_id_creator(lineList[7])    # Getting the two list with the numbers and dates


    #print("\n")
    #print("The two list of data for the TRIP_ID new list are: ")
    #print(tripsNum)
    #print(tripsDate)
    #print("\n")
    #print("And the template trip List is:  ")
    #print(lineList)
    #print("\n")

    """ Getting the trip list with numbers """    
    tripsList = trip_num_list_creator(tripsNum, lineList)


    """ Getting the trip list with the date """
    counter = 0
    for trip in tripsList:
        trip[10] = tripsDate[counter]
        counter += 1
    
    """ Getting the index list """
    indexTripList = trip_index_list_creator(tripsNum, int(lineList[4]))

    #print(indexTripList)

    """ Getting teh index trip list """
    counter = 0
    for trip in tripsList:
      trip[4] = indexTripList[counter]
      counter += 1

    #print("The trip list with numbers is: ")    
    for item in tripsList:
      #print(item)
      bidgroupCounter += 1
      outputsList.append(item)


  else:
    #print("\n")
    #print(lineList)
    bidgroupCounter += 1
    outputsList.append(lineList)



""" Counting the trip id """
if (advancedTripCounter > 1):
  counter = 0 
  for item in outputsList:
    if item[2] == '"TRIP_ID"':    
      item[4] = int(baseTripIdCounter) + counter
      counter += 1

#print(baseTripIdCounter)
counter = 0 
for item in outputsList:
  if item[2] == '"TRIP_ID"':    
    item[4] = int(baseTripIdCounter) + counter
    counter += 1

    
indexLineList = trip_index_list_creator_2(outputsList)
#print(indexLineList)
counter = 0 
for item in outputsList: 
  if (item[2] != '"BIDGROUP"'):
    item[4] = indexLineList[counter]
    counter += 1
    
""" Changing the BIDGROUP """
for item in outputsList:
  if item[2] == '"BIDGROUP"':
    item[6] = bidgroupCounter  - 1

groupTotal = len(outputsList) - bidgroupCounter2
#print(groupTotal)
counter = 0
if (bidgroupCounter2 > 1):
  for item in outputsList:
    if (item[2] == '"BIDGROUP"'):
      counter += 1
      if(counter == bidgroupCounter2):
        item[6] = groupTotal
      else:
        item[6] = 0

bidGroupList = bidgroup_list_creator(outputsList)
bidGroupList.remove(bidGroupList[0])

counter = 0 
for item in outputsList: 
  if (item[2] == '"BIDGROUP"'):
    item[6] = bidGroupList[counter]
    counter += 1
  
#print(bidGroupList)


""" Format Output"""
#print("\n")
#print("The full list is")
#print(outputsList)
counter = 0
for item in outputsList:
  counter += 1  
  outputsInOneList.extend(item)
  if(counter < len(outputsList)):
    outputsInOneList.append("\n")
  
for item in outputsInOneList:
  if item != "\n":
    sys.stdout.write(str(item) + ", ")
  else:
    sys.stdout.write(str(item))
