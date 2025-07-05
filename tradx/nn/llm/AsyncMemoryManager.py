import asyncio
import torch
from collections import OrderedDict
from pathlib import Path
from tradx.nn.llm.MemoryModule import MemoryModule

class AsyncMemoryManager:
    def __init__(self, max_active=12):
        self.active = OrderedDict()  # ISIN → MemoryModule
        self.max_active = max_active
        self.lock = asyncio.Lock()

    async def get_memory(self, isin):
        async with self.lock:
            if isin in self.active:
                self.active.move_to_end(isin)  # Mark as recently used
                return self.active[isin]

            # If over capacity → remove oldest
            if len(self.active) >= self.max_active:
                old_isin, old_mem = self.active.popitem(last=False)
                torch.save(old_mem.state_dict(), f"./memory/{old_isin}.pt")
                del old_mem
                torch.cuda.empty_cache()

            # Load or init
            mem = MemoryModule()
            path = Path(f"./memory/{isin}.pt")
            if path.exists():
                mem.load_state_dict(torch.load(path))
            self.active[isin] = mem.to("cuda")
            return mem