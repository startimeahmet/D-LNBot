

import networkx as nx
import matplotlib.pyplot as plt
import pprint
import random
import ipdb

random.seed(100)


def createList(r1, r2):
    return [item for item in range(r1, r2+1)]

'''
def generate_BA_network(m,n,seed):
    G = nx.barabasi_albert_graph(m, n,seed=seed)
    # nx.draw(G)

    all_edges=G.edges()
    for ii in all_edges:
        # print(ii)
        u,v=ii
        G.edges[u, v]['weight']=10000
    
    return G
'''


import pickle

with open('filename2021.pickle', 'rb') as handle:
    g = pickle.load(handle)


cnt=1
convrted_dict={}


for ii in g.nodes:
    convrted_dict[ii]=cnt
    cnt=cnt+1

G = nx.Graph()

for ii in g.edges():
    uu,vv=ii
    G.add_edge(convrted_dict[uu],convrted_dict[vv])



largest_component = max(nx.connected_components(G), key=len)

# Create a subgraph of G consisting only of this component:
G2 = G.subgraph(largest_component)

Y = nx.Graph()

for jj in G2.edges():
    uu,vv=jj
    Y.add_edge(uu,vv)

G=Y

for ii in G.edges():
    uu,vv=ii
    G.edges[uu, vv]['weight']=10000

all_edges=list(G.edges())

# ====================================================
# ====================================================
def get_most_connected(G,x):
    freq={}
    all_edges=G.edges()
    for ii in all_edges:
        u,v=ii
        try:
            freq[u]=freq[u]+1
        except:
            freq[u]=1
        try:
            freq[v]=freq[v]+1
        except:
            freq[v]=1

    freq_sorted={k: v for k, v in sorted(freq.items(), key=lambda item: item[1],reverse=True)}
    
    return list(freq_sorted)[:x],list(freq_sorted)[x:];

# ====================================================
# ====================================================

# pprint.pprint(G.edges[8,2]['weight'])


sim_time=10*len(G.edges)
max_allowable_active=2

num_of_CCs_in_total = 150

class CC:
    def __init__(self, number):
        self.name = 'CC_'+str(number)
        self.join_time = random.randint(100, sim_time)
        self.joined = False
        self.Active=False
        self.CCdatabase=set([])
        self.CCActivedatabase=set([])
        self.myinnocent=[]


# CONSTANTS
number_of_innocent      = 3


# G = generate_BA_network(200, 3,seed=1111)
most_connected,least_connected  = get_most_connected(G,number_of_innocent)


time_in_observation = set([]) # we do not need to run everything every time (to increase speed in simulation)


CCs={}
for ii in range(1,num_of_CCs_in_total+1):
    CCs[ii]= CC(ii)
    dum=createList(CCs[ii].join_time-5,CCs[ii].join_time+5)
    time_in_observation.update(set(dum))


ActiveCCs=[]

toggler=0

all_edges=list(G.edges())

for tick in range(0,sim_time+100):
    
    if tick in time_in_observation:
        
        # Assume that all of them can query the network QUERIED ONCE
        # most_connected,least_connected  = get_most_connected(G,number_of_innocent)
        # all_edges=G.edges()
        active_edges=0
        
        toggler+=1
        
        
        for ic,vc in enumerate(CCs):
            CCno = vc
            
            CCsim = CCs[CCno]
            
            if CCsim.joined == True:
                active_edges=0
                for jj in all_edges:
                    uu,v=jj

                    if G[uu][v]['weight']==777:
                        # import ipdb;ipdb.set_trace()
                        if uu in most_connected: # then it is not a CC
                            if v in most_connected: # there is a problem (our malware is becoming popular :)))
                                pass
                            else: # u is in most connected, v is not most connected, v is CC
                                CCsim.CCdatabase.add((v))
                                active_edges+=1
                                if CCsim.Active==True:
                                    CCsim.CCActivedatabase.add((v))
                                    if v not in ActiveCCs:
                                        ActiveCCs.append((v))
                        else:
                            if v in most_connected: # uu is not popular but v is, uu is CC
                                CCsim.CCdatabase.add((uu))
                                active_edges+=1
                                if CCsim.Active==True:
                                    CCsim.CCActivedatabase.add((uu))
                                    if uu not in ActiveCCs:
                                        ActiveCCs.append((uu))
                            else: # u is in most connected, v is not most connected
                                pass
                '''                                
                if active_edges > max_allowable_active:
                    try:
                        G.remove_edge(CCsim.name, CCsim.myinnocent)
                        print(CCsim.name +' ' + str(CCsim.myinnocent) + ' removed')
                        CCsim.Active = False
                    except:
                        pass
                    # PROBLEM HERE here all of them remove at the same time. So we need to pick one. This can be handled by random backoff.
                    most_connected,least_connected  = get_most_connected(G,number_of_innocent)
                    print('--- Tick is '+ str(tick) + ' ' + CCsim.name + ' has LEFT')
                    all_edges=G.edges()
                '''                        
                    
            
            if CCsim.joined== False:
                # This is for joining        
                if tick==CCsim.join_time:
                    toggler=0
                    print('Tick is '+ str(tick) + ' ' + CCsim.name + ' has joined')
                    
                    # When you join you pick a random innocent node and make a connection to it
                    # Pick an innocent random node
                    rand_innocent = random.choice(most_connected)
                    rand_other    = random.choice(least_connected)
                    
                    # create an edge
                    G.add_edge(CCsim.name,rand_innocent)
                    all_edges.append((CCsim.name,rand_innocent))
                    G.edges[CCsim.name, rand_innocent]['weight']=777
                    CCsim.myinnocent = rand_innocent

                    G.add_edge(CCsim.name,rand_other)
                    all_edges.append((CCsim.name,rand_other))
                    G.edges[CCsim.name, rand_other]['weight']=10000

                    # mark it as joined
                    CCsim.joined = True
                    CCsim.Active = True


        if active_edges > max_allowable_active and toggler == 2:
            CCtoRemove=ActiveCCs.pop(0)
            for jj,kk in enumerate(CCs):
                CCsim=CCs[kk]
                if CCsim.name==CCtoRemove:
                    break;
            

            try:
                G.remove_edge(CCsim.name, CCsim.myinnocent)
                print(CCsim.name +' ' + str(CCsim.myinnocent) + ' removed')
                CCsim.Active = False
            except:
                pass
            try:
                all_edges.remove((CCsim.name,CCsim.myinnocent))
            except:
                pass
            try:
                all_edges.remove((CCsim.myinnocent,CCsim.name))
            except:
                pass

            # PROBLEM HERE here all of them remove at the same time. So we need to pick one. This can be handled by random backoff.
            # most_connected,least_connected  = get_most_connected(G,number_of_innocent)
            print('--- Tick is '+ str(tick) + ' ' + CCsim.name + ' has LEFT')
            # all_edges=G.edges()


for ii in range(1,num_of_CCs_in_total+1):
    print (CCs[ii].name,CCs[ii].CCdatabase)

print ('\n'*2)

for ii in range(1,num_of_CCs_in_total+1):
    print (CCs[ii].name,CCs[ii].CCActivedatabase)


import pickle

file = open('test.pkl','wb')

pickle.dump(CCs, file)
pickle.dump(G, file)

file.close()



# import ipdb;ipdb.set_trace()

# pprint.pprint(CCs)

# print(most_connected)



