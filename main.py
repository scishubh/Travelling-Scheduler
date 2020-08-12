from itertools import permutations
class Node:
    def __init__(self,data=None,lat=None,long=None):
        self.data=data
        self.next=None
        self.latitude=lat
        self.longitude=long

    def __repr__(self):
        return str(self.data)

class LinkedList:
    def __init__(self):
        self.head=Node()

    def __repr__(self):
        return str(self.data)

    def inserthead(self,x,lat,long):
        temp=Node(x,lat,long)
        temp.next=self.head.next
        self.head.next=temp

class hashtable:
    def __init__(self,size):
        self.elements=[None]*size
        self.size=size

    def __repr__(self):
        return str(self.data)

    def hashkey(self,x):
        #horners rule
        sum=0
        y=len(x)
        for ch in str(x):
            sum=sum+ord(ch)*(33**y)
            y=y-1
        return sum % self.size

    def insert(self,x,lat,long):
        s=self.elements[self.hashkey(x)]
        if s is None:
            s=LinkedList()
            s.inserthead(x,lat,long)
            self.elements[self.hashkey(x)]=s
            return 
        s.inserthead(x,lat,long)

    def search(self,x):
        for i in range(self.size):
            if self.elements[i] is not None:
                ptr=self.elements[i].head
                while ptr is not None:
                    if ptr.data==x:
                        return ptr
                    ptr=ptr.next
        return

    def printt(self):
        for i in range(self.size):
            if self.elements[i] is None:
                print(self.elements[i])
            else:
                ptr=self.elements[i].head.next
                while ptr is not None:
                    print(ptr.data,"  ",ptr.latitude,"  ",ptr.longitude)
                    ptr=ptr.next
        return

def distance(point1, point2):
    return (((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2) ** 0.5)*100  #aerial distance


def total_distance(points):

    return sum([distance(point, points[index + 1]) for index, point in enumerate(points[:-1])])


def travelling_salesman(points, start=None):

    if start is None:
        start = points[0]
    return min([perm for perm in permutations(points) if perm[0] == start], key=total_distance)

c=hashtable(33)
places=[]
f=open(".\latlong.txt","r")
while True:
    data =f.readline().split()
    if not data: break
    else:
        c.insert(data[0],data[1],data[2])

list_start=[]
list_lat_long=[]
print("Note:i) Working hour should always be greater than 2 times of speech hour\n")
working_hour=int(input("Enter working hour per day during trip: "))
speech_hour=int(input("Enter speech duration of each place: "))
if speech_hour >= working_hour//2 or speech_hour<=0 or working_hour<=0:
    exit(0)
print("Enter starting point")
while True:
    str_place=input().split()
    if float(str_place[1])<0.5:
        places.append(str_place[0])
        list_start.append(float(c.search(str_place[0]).latitude))
        list_start.append(float(c.search(str_place[0]).longitude))
        list_lat_long.append(list_start)
        break
    else:
        print("enter another place for starting threat is high here")

print("Enter number of places to visit")
n=int(input())

print("Enter places to visit")

for i in range(n):
    place=input().split()
    if float(place[1])<0.5:
        places.append(place[0])
        list_lat_long.append([float(c.search(place[0]).latitude),float(c.search(place[0]).longitude)])
    else:
        continue

list1=travelling_salesman(list_lat_long)
m=len(list1)-1
s=distance(list1[0],list1[m])
aerial_distance=total_distance(travelling_salesman(list_lat_long))+s
avg_speed=800                         #avg speed of aeroplane
print("Shortest Path :")
for k in range(m+1):
    l=list_lat_long.index(list1[k])
    print(places[l]," -->>",end=" ")
print(places[0])
print("Shortest Path Trip Distance :",aerial_distance," km")

travelling_time = aerial_distance/avg_speed
list_dist=[]
list_time=[]
for i in range(len(list1)-1):
    list_dist.append(distance(list1[i],list1[i+1]))
    list_time.append(round((list_dist[i]/avg_speed),2))
list_dist.append(distance(list1[0],list1[m]))
list_time.append(round((list_dist[m]/avg_speed),2))
sum=0
for i in range(0,m+1):
    sum=sum+list_time[i]
activity=[]
wasted=[]
activity.append(list_time[0])
curr_workhours=list_time[0]
next_workhours=speech_hour
i=1
count=0
days=1
while i<m+1:
    if next_workhours+curr_workhours<working_hour:
        activity.append(next_workhours)
        curr_workhours+=next_workhours
    else:
        curr_workhours=0
        days+=1
    if count==0:
        next_workhours=list_time[i]
        count=1
        i+=1
    elif count==1:
        next_workhours=speech_hour
        count=0

print("No. of days in whole trip: ",days)
    
