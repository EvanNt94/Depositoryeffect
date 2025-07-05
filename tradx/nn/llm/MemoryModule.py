import torch
import torch.nn as nn
import torch.nn.functional as F

class MemoryModule(nn.Module):
    def __init__(self, dim=4096, hidden=8192, device="cpu"):
        super().__init__()
        self.k_proj = nn.Linear(dim, dim).to(device)
        self.v_proj = nn.Linear(dim, dim).to(device)
        self.query_proj = nn.Linear(dim, dim).to(device)
        self.memory_mlp = nn.Sequential(
            nn.Linear(dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, dim)
        ).to(device)
        self.device = device
        

    def forward(self, x):
        q = self.query_proj(x)
        return self.memory_mlp(q)

    def surprise(self, x)-> torch.Tensor:
        k = self.k_proj(x)
        v = self.v_proj(x)
        pred = self.memory_mlp(k)
        score = F.mse_loss(pred, v, reduction='none').mean(dim=-1)
        return score

    def update(self, x, eta=0.9, theta=1e-3, surprise_threshold=0.1):
        surprise_score = self.surprise(x)
        if surprise_score.item() < surprise_threshold:
            return False

        k = self.k_proj(x).detach()
        v = self.v_proj(x).detach()

        pred = self.memory_mlp(k)
        loss = F.mse_loss(pred, v)
        loss.backward()

        with torch.no_grad():
            for param in self.memory_mlp.parameters():
                if param.grad is not None:
                    param -= theta * param.grad
            self.memory_mlp.zero_grad()

        return True

    def quantize(self):
        # Fake 8-bit quant (char) for demonstration
        for p in self.memory_mlp.parameters():
            p.data = (p.data * 127).round().clamp(-128, 127).char().float() / 127

    def dequantize(self):
        pass  # no-op for now