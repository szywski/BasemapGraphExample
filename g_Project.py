import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
import xlrd


#przyjęcie początku i celu podróży

poczatek = input("miejsce początkowe podróży: ")
cel = input("miejsce docelowe podróży: ")

#ustawienie mapy
m = Basemap(
        projection='merc',
        llcrnrlon=13,
        llcrnrlat=49,
        urcrnrlon=26,
        urcrnrlat=55,
        lat_ts=0,
        resolution='i',
        suppress_ticks=True)

#plik z danymi
doc = ("miasta.xlsx")
wb = xlrd.open_workbook(doc)
sheet = wb.sheet_by_index(0)


i = 1
row_max = 0
#stąd pobieram informację o tym ile jest wierszy w pliku
for sheet in wb.sheets():
    for row in range(sheet.nrows):
       row_max = row
          

G = nx.Graph()

#inicjalizacja współrzędnych
lats =[sheet.cell_value(1,1)]

lons = [sheet.cell_value(1,2)]
#tworzę listę ze współrzednymi
while i != row_max+1:
        lats.append(sheet.cell_value(i,1))
        lons.append(sheet.cell_value(i,2))
        i+=1


#wrzucam listę w numpy
lats = np.array(lats)
lons = np.array(lons)
#żeby sobie przekonwertować dane na odpowiedni typ
lats = np.asfarray(lats,float)
lons = np.asfarray(lons,float)

#konwertuje współrzędne z geograficznych na basemapowe
mx,my = m(lats,lons)
pos={}

i=1

#dodaje sobie krawędzie i wierzchołki
while i != row_max+1:
        
        #czas połączeń z warszawy
        G.add_edge(sheet.cell_value(i,0),sheet.cell_value(1,0), weight=sheet.cell_value(i,3))
        #czas połączeń z krakowa
        if sheet.cell_value(i,4) != 0:
                G.add_edge(sheet.cell_value(5,0),sheet.cell_value(i,0), weight=sheet.cell_value(i,4))
        #czas połączeń z wrocławia
        if sheet.cell_value(i,5) != 0:        
                G.add_edge(sheet.cell_value(7,0),sheet.cell_value(i,0), weight=sheet.cell_value(i,5))
        #dodaje basemapowe współrzędne odpowiadające odpowiedniej miejscowości
        pos[sheet.cell_value(i,0)]=(mx[i],my[i])
        i+=1


#rysuje sobie graf który zawiera wszystkie dodane połączenia. Założyłem że jeśli istnieje połączenie z miejscowości x do y to istnieje y do x 
nx.draw_networkx(G,pos,node_size=100,node_color='blue',edge_color='grey')

#zaznaczenie najkrótszej ścieżki między miastami
path = nx.dijkstra_path(G,poczatek,cel)
path_edges = zip(path,path[1:])
path_edges = set(path_edges)
nx.draw_networkx_nodes(G,pos,nodelist=path,node_color='lightskyblue')
nx.draw_networkx_edges(G,pos,edgelist=path_edges,edge_color='skyblue',width=3)
#wyświetlenie info o połączeniu w konsoli
print(nx.single_source_dijkstra(G,poczatek,cel))

#rysowanie mapy
m.drawcountries()
m.drawcoastlines()
m.readshapefile('POL_adm\POL_adm1','POL_adm1', color='silver') #siatka administracyjna z pliku
plt.title('Loty i lotniska')
plt.axis('equal')
plt.show()