import torch, torch.nn as nn
import math, copy

def clone(module, N):
    return nn.ModuleList([copy.deepcopy(module) for _ in range(N)])

class Embedding(nn.Module):

    def __init__(self, vocab_dim, embed_dim):
        super(Embedding, self).__init__()
        self.weights = nn.Parameter(torch.empty(vocab_dim, embed_dim))
        nn.init.uniform_(self.weights, -0.01, 0.01)

    def forward(self, inputs):
        return nn.functional.normalize(self.weights[inputs], dim=-1)

class PositionalEncoding(nn.Module):

    def __init__(self, embed_dim, dropout, max_len=5000):
        super(PositionalEncoding, self).__init__()
        self.dropout = nn.Dropout(dropout)

        enc = torch.zeros(max_len, embed_dim)
        position = torch.arange(0, max_len).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, embed_dim, 2) * -(math.log(10000) / embed_dim))
        enc[:, 0::2] = torch.sin(position * div_term)
        enc[:, 1::2] = torch.cos(position * div_term)
        self.register_buffer('enc', enc.unsqueeze(0))

    def forward(self, inputs):
        return self.dropout(inputs + self.enc[:, : inputs.size(1)])

class Linear(nn.Module):

    def __init__(self, input_dim, output_dim):
        super(Linear, self).__init__()
        self.weights = nn.Parameter(torch.empty(input_dim, output_dim))
        self.bias = nn.Parameter(torch.zeros(output_dim))
        nn.init.xavier_uniform_(self.weights)

    def forward(self, inputs, bias=True):
        if not bias:
            return inputs @ self.weights
        return inputs @ self.weights + self.bias

class LogSoftmax(nn.Module):

    def __init__(self, embed_dim, vocab_size):
        super(LogSoftmax, self).__init__()
        self.weights = nn.Parameter(torch.empty(vocab_size, embed_dim))
        nn.init.uniform_(self.weights, -0.01, 0.01)

    def forward(self, inputs, softmax=True):
        weights = nn.functional.normalize(self.weights, dim=-1)
        if not softmax:
            return inputs @ weights.transpose(0, 1)
        return torch.log_softmax(inputs @ weights.transpose(0, 1), dim=-1)

class FeedForward(nn.Module):

    def __init__(self, embed_dim, ff_dim, dropout):
        super(FeedForward, self).__init__()
        self.ff_1 = Linear(embed_dim, ff_dim)
        self.ff_2 = Linear(ff_dim, embed_dim)
        self.dropout = nn.Dropout(dropout)

    def forward(self, inputs):
        return self.ff_2(self.dropout(self.ff_1(inputs).relu()))

class ScaleNorm(nn.Module):

    def __init__(self, scale):
        super(ScaleNorm, self).__init__()
        self.scale = nn.Parameter(scale)

    def forward(self, inputs):
        return self.scale * nn.functional.normalize(inputs, dim=-1)

class MultiHeadAttention(nn.Module):

    def __init__(self, embed_dim, num_heads, dropout):
        super(MultiHeadAttention, self).__init__()
        assert embed_dim % num_heads == 0
        self.linears = clone(Linear(embed_dim, embed_dim), 4)
        self.dropout = nn.Dropout(dropout)
        self.key_dim = embed_dim // num_heads
        self.num_heads = num_heads

    def attention(self, query, key, value, mask=None):
        scores = query @ key.transpose(-2, -1) / math.sqrt(self.key_dim)
        if mask is not None:
            scores.masked_fill_(mask.unsqueeze(1) == 0, -torch.inf)
        return self.dropout(scores.softmax(dim=-1)) @ value

    def _reshape_from(self, inputs):
        return inputs.reshape(*inputs.size()[:2], self.num_heads, self.key_dim)

    def _reshape_to(self, inputs):
        return inputs.reshape(*inputs.size()[:2], -1)

    def forward(self, query, key, value, mask=None):
        query, key, value = [self._reshape_from(linear(inputs)).transpose(1, 2)
            for linear, inputs in zip(self.linears, (query, key, value))]
        outputs = self.attention(query, key, value, mask)
        return self.linears[-1](self._reshape_to(outputs.transpose(1, 2)))
