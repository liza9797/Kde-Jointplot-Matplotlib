import numpy as np
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

CMAP_FROM_COLORS = {
    "orange": ["orange","orange" ,"darkorange" ,
               "saddlebrown", "black"]
}
CMAP_FROM_ALPHAS = {
    "orange": lambda N: np.linspace(0.01, 1, N),
}

def get_cmap(name, alphas=None):
    
    cmap = LinearSegmentedColormap.from_list(name, CMAP_FROM_COLORS[name])
    
    alphas = alphas if alphas else CMAP_FROM_ALPHAS[name](cmap.N)
    cmap = cmap(np.arange(cmap.N))
    cmap[:,-1] = alphas
    cmap = ListedColormap(cmap)
        
    return cmap

