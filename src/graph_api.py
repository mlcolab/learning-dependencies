# the format is needed for plotly dashboard
import json
import numpy as np

def np_encoder(object):
    if isinstance(object, np.generic):
        return object.item()

def save_graph(to, concepts, dependencies):
    # nodes
    elements_all = {target: {"data":{"id":target,"label":target,"external": False}} for target in concepts}
    for deps in dependencies:
        for source in deps:
            if source not in elements_all.keys(): elements_all[source] = {"data":{"id":source,"label":source,"external": True}}
    elements_all = list(elements_all.values())

    # edges
    for target, sources in zip(concepts, dependencies):
        for source in sources:
            elements_all.append({"data":{"source":source,"target":target}})
    #print(elements_all)
    with open(to, 'w') as f:
        json.dump(elements_all, f, default=np_encoder)