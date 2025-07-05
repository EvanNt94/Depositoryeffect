import matplotlib.pyplot as plt

class PathPlotter:
    @staticmethod
    def plot_price_paths(S, title="Simulierte Preis-Pfade"):
        for path in S:
            plt.plot(path, alpha=0.5)
        plt.title(title)
        plt.xlabel("Zeitschritte")
        plt.ylabel("Preis")
        plt.show()

    @staticmethod
    def plot_vol_paths(v, title="Simulierte Volatilitätspfade", is_variance=True):
        for path in v:
            plt.plot(path, alpha=0.5)
        plt.title(title)
        plt.xlabel("Zeitschritte")
        ylabel = "Varianz" if is_variance else "Volatilität"
        plt.ylabel(ylabel)
        plt.show()

    @staticmethod
    def plot_multiple_processes(data_dict, title="Vergleich mehrerer Prozesse"):
        for label, series in data_dict.items():
            for path in series:
                plt.plot(path, alpha=0.3, label=label)
        plt.title(title)
        plt.xlabel("Zeitschritte")
        plt.ylabel("Wert")
        plt.legend()
        plt.show()

    @staticmethod
    def plot_heatmap(v, title="Heatmap Volatilität"):
        import numpy as np
        plt.imshow(np.array(v).T, aspect='auto', cmap='viridis')
        plt.colorbar(label='Volatilität')
        plt.title(title)
        plt.xlabel("Pfad")
        plt.ylabel("Zeitschritt")
        plt.show()

if __name__ == "__main__":
    PathPlotter.plot_heatmap([[0,1],[1,0]], "test")