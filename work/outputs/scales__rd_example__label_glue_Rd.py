import pandas as pd
import numpy as np
from plotnine import *
import matplotlib.pyplot as plt

# r2py:entity:demo_discrete
def demo_discrete(data, labels_expr=None, labels_val=None):
    """
    Mimics scales::demo_discrete by printing the call and rendering a plot.
    """
    # In R, demo_discrete prints the scale call it is using.
    # We use labels_expr to mimic the R code string that produced the labels.
    if labels_expr:
        print(f"      scale_x_discrete(labels = {labels_expr})")
    
    # Construct a simple plot to satisfy the graphics requirement
    df = pd.DataFrame({'x': data, 'y': [1] * len(data)})
    
    # Handle the labeling logic
    plot_labels = labels_val if labels_val is not None else data

    p = (ggplot(df, aes(x='x', y='y')) 
         + geom_point() 
         + scale_x_discrete(labels=plot_labels))
    
    # Render the plot to ensure graphics are captured
    p.draw()
    plt.gcf().clf() 
    return p

# r2py:entity:animal
animal = "penguin"
# r2py:entity:species
species = ["Adelie", "Chinstrap", "Emperor", "Gentoo"]

# R: demo_discrete(species, labels = label_glue("The {x}\n{animal}"))
# r2py:entity:demo_discrete
expr1 = 'label_glue("The {x}\\n{animal}")'
labels1 = [f"The {x}\n{animal}" for x in species]
demo_discrete(species, labels_expr=expr1, labels_val=labels1)

# R: demo_discrete(species[-3], labels = label_glue("The {x}\n{animal}"))
# r2py:entity:demo_discrete_1
species_subset = [s for i, s in enumerate(species) if i != 2]
expr2 = 'label_glue("The {x}\\n{animal}")'
labels2 = [f"The {x}\n{animal}" for x in species_subset]
demo_discrete(species_subset, labels_expr=expr2, labels_val=labels2)

# R: demo_discrete(species[-3], labels = glue::glue("The {species}\n{animal}"))
# In R, glue::glue("The {species}") uses the whole vector species[-3]
# r2py:entity:demo_discrete_2
expr3 = 'glue::glue("The {species}\\n{animal}")'
# glue::glue of a vector results in a single string containing the vector's elements
species_str = ", ".join(species_subset) 
# The exact format of glue on a vector is usually: "The Adelie, Chinstrap, Gentoo\npenguin"
# but R labels are usually a vector of labels. glue::glue on a vector produces one string.
labels3 = [f"The {species_str}\n{animal}"] * len(species_subset)
demo_discrete(species_subset, labels_expr=expr3, labels_val=labels3)