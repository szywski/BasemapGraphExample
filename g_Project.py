import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
import xlrd

#comments are first in polish and then english


#przyjęcie początku i celu podróży
#setting start and destination. Be sure u use cities from file bc i didnt average person validation

poczatek = input("miejsce początkowe podróży: ") #start
cel = input("miejsce docelowe podróży: ")       #destinatnio

#ustawienie mapy
#setting the map
m = Basemap(
        projection='merc',
        llcrnrlon=13, #these are coordinates of Poland 
        llcrnrlat=49,
        urcrnrlon=26,
        urcrnrlat=55,
        lat_ts=0,
        resolution='i',
        suppress_ticks=True)

#plik z danymi
#file with data
doc = ("miasta.xlsx")
wb = xlrd.open_workbook(doc)
sheet = wb.sheet_by_index(0)

#im not very into python so that i use simple while loops ant this is why i declare i here
i = 1
row_max = 0
#stąd pobieram informację o tym ile jest wierszy w pliku
#here I look for how many rows in file is so i wouldnt go out of range
for sheet in wb.sheets():
    for row in range(sheet.nrows):
       row_max = row
          
# starting graph nothing emotional here
G = nx.Graph()

#inicjalizacja współrzędnych
#initialization of coordinates. You have to be familiar with my file to undersrtand it. 
lats =[sheet.cell_value(1,1)]# value(row collumn) this is essential
lons = [sheet.cell_value(1,2)]
#tworzę listę ze współrzednymi
#here i put coords into array and this is where my 'i' is useful
while i != row_max+1:
        lats.append(sheet.cell_value(i,1))
        lons.append(sheet.cell_value(i,2))
        i+=1


#wrzucam listę w numpy
#add array to numpy so  can
lats = np.array(lats)
lons = np.array(lons)
#żeby sobie przekonwertować dane na odpowiedni typ
#convert it into floats
lats = np.asfarray(lats,float)
lons = np.asfarray(lons,float)

#konwertuje współrzędne z geograficznych na basemapowe
#and then convert them from geo tags to basemap map projection to suit projection
mx,my = m(lats,lons)
#declare position array
pos={}
#my deer i is back to 1 so i can now set rest of data
i=1

#dodaje sobie krawędzie i wierzchołki
#here i add edges and nodes
while i != row_max+1:
        
        #czas połączeń z warszawy
        #from warsaw
        G.add_edge(sheet.cell_value(i,0),sheet.cell_value(1,0), weight=sheet.cell_value(i,3))
        #czas połączeń z krakowa
        #from cracow. The point where 0 in datasheet is means taht there is no connection so program ignores it
        if sheet.cell_value(i,4) != 0:
                G.add_edge(sheet.cell_value(5,0),sheet.cell_value(i,0), weight=sheet.cell_value(i,4))
        #czas połączeń z wrocławia
        #from wroclaw
        if sheet.cell_value(i,5) != 0:        
                G.add_edge(sheet.cell_value(7,0),sheet.cell_value(i,0), weight=sheet.cell_value(i,5))
        #dodaje basemapowe współrzędne odpowiadające odpowiedniej miejscowości
        #add coordinates which i convert into basemap projection earlier to position i relation with city namie
        #pos[city_name]=(x,y)
        pos[sheet.cell_value(i,0)]=(mx[i],my[i])
        i+=1


#rysuje sobie graf który zawiera wszystkie dodane połączenia. Założyłem że jeśli istnieje połączenie z miejscowości x do y to istnieje y do x 
#now I draw a graph that shows all possible connections
nx.draw_networkx(G,pos,node_size=100,node_color='blue',edge_color='grey')

#zaznaczenie najkrótszej ścieżki między miastami
#now I draw shortest possible path where weight of edge is travel time
path = nx.dijkstra_path(G,poczatek,cel)#początek, cel = start,destination
path_edges = zip(path,path[1:])#setting iterator to path array
path_edges = set(path_edges)
nx.draw_networkx_nodes(G,pos,nodelist=path,node_color='lightskyblue')#and ondraw nodes and edges
nx.draw_networkx_edges(G,pos,edgelist=path_edges,edge_color='skyblue',width=3)
#wyświetlenie info o połączeniu w konsoli
#info about path in console
print(nx.single_source_dijkstra(G,poczatek,cel))

#rysowanie mapy
#map drawing
m.drawcountries()
m.drawcoastlines()
m.readshapefile('POL_adm\POL_adm1','POL_adm1', color='silver') #siatka administracyjna z pliku/ this is where the vivodeships are stored
plt.title('Loty i lotniska')# title xd
plt.axis('equal')
plt.show()
