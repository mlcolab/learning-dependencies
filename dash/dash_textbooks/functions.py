import numpy as np

def generate_graph_data(nbook_thr,confidence_thr, filter_type = "DE1"):
    concepts_array = np.load("data/wiki_concepts.npy")
    adj = np.load("data/adj.npy")

    if filter_type =="DE1":
        filter1 = (adj>=nbook_thr)
        filter2 = ((filter1+filter1.T)!=2)
        idx = np.where(filter1 & filter2)

    elif filter_type=="DE1+DE3":
        pass
    elif filter_type=="DE1+DE4":
        pass
   

    elements = []
    sources = concepts_array[idx[0]]
    targets = concepts_array[idx[1]]
    nodes = set(list(sources) + list(targets))

    for node in nodes:
        elements.append({"data":{"id":node,"label":node}})
    for  source, target in zip(sources, targets):
        elements.append({"data":{"source":source,"target":target}})
    
    return elements
