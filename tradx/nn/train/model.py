"""
imho we need way more d (too little imput columns)
some will be what the industry is.
some will be the news coverage 

"""

'''
WE NEED POSITIOANAL ENCODER
https://pytorch.org/tutorials/beginner/introyt/trainingyt.html

'''



import torch

model = torch.nn.Transformer(d_model=5)

NUM_EPOCHS = 4

# create data loaders torch.utils.data.DataLoader, shuffle=True


# some adam optimizer
optimizer=torch.optim.Adam(params=model.parameters(),lr=1e-3)