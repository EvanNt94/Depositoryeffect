from llama_cpp import Llama
import torch

from tradx.nn.llm.MemoryModule import MemoryModule


class LlamaCppWrapper:
    
    @staticmethod
    def load_memory(mem_path: str, dim: int, device: str):
        mem = MemoryModule(dim=dim, device=device)
        mem.load_state_dict(torch.load(mem_path, map_location=device))
        return mem
    
    def __init__(self, model_path: str, device: str = "cpu", mem_path: str = ""):
        self.llm = Llama(model_path=model_path, embedding=True, n_gpu_layers=999)
        vec = self.llm.embed("test")
        self.dim = len(vec[0]) if isinstance(vec[0], list) else len(vec)
        self.memory = MemoryModule(dim=self.dim, device=device) if mem_path == "" else self.load_memory(mem_path, self.dim, device)

    def save_memory():
        pass
    
    def embed(self, text):
        vec = self.llm.embed(text)
        return torch.tensor(vec).mean(dim=0).unsqueeze(0).to(self.memory.device)

    def surprise(self, text):
        x = self.embed(text)
        return self.memory.surprise(x).item()

    def update_memory(self, text):
        x = self.embed(text)
        return self.memory.update(x)