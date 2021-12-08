import networkx as nx
import matplotlib.pyplot as plt
import pprint
import random

channel_size_high=200
channel_size_low=160

random.seed(100)

# according to tests we have done, 1 hop takes around 1.675 to 2 seconds


def createList(r1, r2):
    return [item for item in range(r1, r2+1)]

def generate_BA_network(m,n,seed):
    G = nx.barabasi_albert_graph(m, n,seed=seed)
    # nx.draw(G)

    all_edges=G.edges()
    for ii in all_edges:
        # print(ii)
        u,v=ii
        G.edges[u, v]['weight']=10000
    
    return G


class node:
    def __init__(self, name):
        self.name = name
        self.buffer = []
        self.channel = [-1]*channel_size_high
        self.item=-1
        self.prev_data=' ' 
        
    def MoveOn(self):
        self.channel.append(-1)
        self.item = self.channel.pop(0)

        
    def PutData(self,dd):
        loc=random.randint(channel_size_low,channel_size_high-1)
        while self.channel[loc] != -1:
            loc=random.randint(channel_size_low,channel_size_high-1)
        self.channel[loc]=dd
        
    def CheckData(self):
        if self.item != -1: # that means there is something to send
            return True,self.item
        else:
            return False,self.item
        

class CC:
    def __init__(self, number):
        self.name = 'CC_'+str(number)
        self.join_time = random.randint(100, sim_time)
        self.joined = False
        self.Active=False
        self.CCdatabase=set([])
        self.CCActivedatabase=set([])
        self.myinnocent=[]

import pickle
file = open('test10.pkl', 'rb') ########################################################################
CCs = pickle.load(file)
G = pickle.load(file)
file.close()


def GiveNeighborNodes(SrcCC,CCs):
    for ii,jj in enumerate(CCs):
        CCuo = CCs[jj]
        if CCuo.name==SrcCC:
            return CCuo.CCActivedatabase
    return -2


nodes={}

# G = generate_BA_network(150, 2, seed=1111)



for ii in G.nodes:
    # print(ii)
    nodes[ii]=node(ii)
    
    
    
# sp=nx.shortest_path(G, 'CC_1', 'CC_2')
# sp.append('messageSYNC')

# We can start with CC 11


# import ipdb;ipdb.set_trace()
KickStart='CC_150'

if len(CCs)==150:
    KickStart='CC_150'
if len(CCs)==100:
    KickStart='CC_36'
if len(CCs)==50:
    KickStart='CC_36'
if len(CCs)==25:
    KickStart='CC_15'
if len(CCs)==10:
    KickStart='CC_9'


sim_time=10*len(CCs)*channel_size_high # 150 is number of CC's

for tick in range(0,sim_time):

    if tick == 115: # we start sending the message here. The message is: messageSYNC and we start with CC_11
        Neighbors=GiveNeighborNodes(KickStart,CCs)
        if KickStart in Neighbors:
            Neighbors.remove(KickStart)
        
        for dest in Neighbors:
            sp=nx.shortest_path(G, KickStart, dest)
            sp.append('messageSYNC')
            NextHop = sp.pop(0)
            nodes[NextHop].PutData(sp)
            print(sp)
            print('Tick is ' + str(tick)+ ' DATA KONDU ' + 'NextHop ' +  str(NextHop))
        
    for nn in G.nodes(): # this is the idle time
        NNcur= nodes[nn]
        NNcur.MoveOn()
        
    for nn in G.nodes():
        ThereIsData,data= nodes[nn].CheckData()
        if ThereIsData:
            print('Tick is ' + str(tick) + ' Node is ' + str(nn) + ' Data is', data)
            if len(data) == 1:
                msg = data[0]
                # print(msg)
                
                if nodes[nn].prev_data != msg:
                    nodes[nn].prev_data=msg

                    src=nn;
                    
                    Neighbors=GiveNeighborNodes(src,CCs)
                    if src in Neighbors:
                        Neighbors.remove(src)
                    
                    for dest in Neighbors:
                        sp=nx.shortest_path(G, src, dest)
                        sp.append('messageSYNC')
                        NextHop = sp.pop(0)
                        nodes[NextHop].PutData(sp)
                        print(sp)
                        print('Tick is ' + str(tick)+ ' DATA KONDU ' + 'NextHop ' +  str(NextHop))

                    # import ipdb;ipdb.set_trace()
                
                
            if len(data) > 1:
                NextHop = data.pop(0)
                nodes[NextHop].PutData(data)
                # import ipdb;ipdb.set_trace()
                
        
        
        # import ipdb;ipdb.set_trace()
    
    
    
    
# print(sp)

