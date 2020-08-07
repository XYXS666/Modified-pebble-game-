import pebblegame

if __name__ == '__main__':
    G = pebblegame.pebble() # initialize a pebble game

    #initialize agents' coordinates
    G.agentcoor = {'0':(0,0),'1':(0,1),'2':(1,0)}
    G.srange = 2
    G.calneighbor()

    print('---------adding bond-----------')
    for i in G.bond:
        if G.add_bond(i[0],i[1]):
            print('added bond %d --- %d, independent bond'%i)
        else:
            print('added bond %d --- %d, redundent bond'%i)
    print('-------------------------------\n\n')
    print('raw graph:')
    print(G.graph)
    print('raw directed graph with pebble number, format: {site number:[list of connected sites, pebble number]}')
    print(G.digraph)
    print('-------------------------------\n\n')