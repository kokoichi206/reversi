import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable

class DummyModel(nn.Module):
    def __init__(self):
        super(DummyModel, self).__init__()

        self.l1 = nn.Linear(100, 10)
        self.l2 = nn.Linear(10, 10)

    def forward(self, x):
        h1 = F.tanh(self.l1(x))
        return self.l2(h1)
      