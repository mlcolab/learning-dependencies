# the format is needed for plotly dashboard
import json
import numpy as np

def np_encoder(object): # WHAT IS HAPPENING HERE?
    if isinstance(object, np.generic):
        return object.item()

def save_graph(to, concepts, dependencies):
    # nodes
    #elements_all = {target: {"data":{"id":target,"label":target,"external": False}} for target in concepts}
    elements_all = {target: {"data":{"id":target,"label":target}} for target in concepts}
    for deps in dependencies:
        for source in deps:
            if source not in elements_all.keys(): elements_all[source] = {"data":{"id":source,"label":source},"classes": "blue"}
    elements_all = list(elements_all.values())

    # edges
    for target, sources in zip(concepts, dependencies):
        for source in sources:
            elements_all.append({"data":{"source":source,"target":target}})
    #print(elements_all)
    with open(to, 'w') as f:
        json.dump(elements_all, f, default=np_encoder)

# HIGHLIGHTS EXTERNAL CONCEPTS

#def build_graph(concepts, dependencies, internal_concepts):
#    elements =[]
#    unique_nodes = set()
#    unique_nodes.update(concepts)
#    for target,sources in zip(concepts, dependencies):
#        elements.append({"data":{"id":target,"label":target},"classes": "blue"})
#        for source in sources:
#            elements.append({"data":{"source":source,"target":target}})
#            if source not in unique_nodes:
#                unique_nodes.add(source)
#                if source in internal_concepts:
#                    elements.append({"data":{"id":source,"label":source},"classes": "blue"})
#                else:
#                    elements.append({"data":{"id":source,"label":source}})
#    return elements

def build_graph(df,dep_column,concept, depth=2):
    for i in range(depth):
        if i == 0: 
            elements = [{"data":{"id":concept,"label":concept}}]
            unique_nodes = set()
            unique_nodes.add(concept)
            deps_last = df.loc[df.concept==concept,dep_column].to_list()[0]
            unique_nodes.update(deps_last)
            elements.extend([{"data":{"id":node,"label":node}} for node in deps_last])
            elements.extend([{"data":{"source":dep,"target":concept}} for dep in deps_last ])
        else:
            df_deps = df.loc[df.concept.isin(deps_last)]
            deps_current = df_deps[dep_column].to_list()
            deps_last = df_deps["concept"].to_list()
            elements.extend([{"data":{"source":dep,"target":deps_last[k]}} for k,dep_list in enumerate(deps_current) for dep in dep_list])
            deps_last = [dep for dep_list in deps_current for dep in dep_list]
            elements.extend([{"data":{"id":node,"label":node}} for node in deps_last if  node not in unique_nodes])
            unique_nodes.update(deps_last)
    
    df_deps = df.loc[df.concept.isin(deps_last)]
    deps_current = df_deps[dep_column].to_list()
    deps_last = df_deps["concept"].to_list()
    deps_current = df.loc[df.concept.isin(deps_last),dep_column].to_list()
    elements.extend([{"data":{"source":dep,"target":deps_last[k]}} for k,dep_list in enumerate(deps_current) for dep in dep_list  if dep in unique_nodes])
    deps_last = [dep for dep_list in deps_current for dep in dep_list  if dep in unique_nodes]
    return elements



