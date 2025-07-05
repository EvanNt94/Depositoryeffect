from tradx.nn.llm.mistralSmall3224BLlamaCppWrapper import LlamaCppWrapper
import matplotlib.pyplot as plt

def test_memory_module():
    llm  = LlamaCppWrapper("/home/a2/.cache/models/llm/llama.cpp/models/mistral/mistral-small-3.2-24b-instruct-2506-q5-k-xl.gguf", "cuda")
    x = "Apple released a new chip."

    # Test surprise score calculation
    surprise = llm.surprise(x)
    print("Surprise Score:", surprise)
    llm.update_memory(x)
    surprise2 = llm.surprise(x)
    print(surprise2)
    assert surprise >= surprise2, "should be lower"

    # Test with 100 memory updates and plot surprise scores
    scores = []
    for _ in range(100):
        s = llm.surprise(x)
        scores.append(s)
        llm.update_memory(x)

    plt.plot(scores)
    plt.title("Surprise Score over Memory Updates")
    plt.xlabel("Update Step")
    plt.ylabel("Surprise Score")
    plt.grid(True)
    plt.savefig("surprise_scores.png")
    print("Saved plot to surprise_scores.png")


if __name__ == "__main__":
    test_memory_module()