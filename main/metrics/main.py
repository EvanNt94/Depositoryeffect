import json
import os
import re
from collections import defaultdict

# Pfad zum Nachbarordner "results"
nachbarordner = os.path.join(os.path.dirname(__file__), "..", "results")
nachbarordner = os.path.abspath(nachbarordner)

# Output Basisordner
output_base = os.path.join(os.path.dirname(__file__), "..", "output")
os.makedirs(output_base, exist_ok=True)

# Regex-Muster für AA, DG, Frequenz, Strategy
aa_pattern = re.compile(r"AA-([^-]+)-")
dg_pattern = re.compile(r"DG-([^-]+)-")
freq_pattern = re.compile(r"frqeuenc-(\d+)")
strategy_pattern = re.compile(r"strategy-([^-]+)")

# Alle .json-Dateien im Ordner auflisten
json_dateien = [
    f
    for f in os.listdir(nachbarordner)
    if f.endswith(".json") and os.path.isfile(os.path.join(nachbarordner, f))
]

gruppen = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))


def calculate_metric(dict, strategy):
    calculated_metric = {}
    diff_year = dict["end_year"] - dict["start_year"]
    durchschnittliche_rendite = (
        (strategy["end_amount"] - strategy["start_amount"]) / strategy["start_amount"]
    ) / diff_year
    calculated_metric["durchschnittliche_rendite"] = durchschnittliche_rendite

    effektive_rendite = (strategy["end_amount"] / strategy["start_amount"]) ** (
        1 / diff_year
    ) - 1
    calculated_metric["effektive_rendite"] = effektive_rendite
    calculated_metric["sharpe_ratio"] = strategy["sharpe_ratio"]
    calculated_metric["max_drawdown"] = strategy["max_drawdown"]
    calculated_metric["sigma_daily"] = strategy["sigma_daily"]

    return calculated_metric


def read_data(dict):
    result_dict = {}
    match = re.search(
        r"Start-Date:\s*(\d{4})-\d{2}-\d{2}.*?end date:\s*(\d{4})-\d{2}-\d{2}",
        dict["config"],
        re.IGNORECASE,
    )
    if match:
        start_jahr = int(match.group(1))
        end_jahr = int(match.group(2))
        result_dict["start_year"] = start_jahr
        result_dict["end_year"] = end_jahr

        # NormalMEtric:
        result_dict["normal_metrics"] = {}
        for key in [
            "start_amount",
            "end_amount",
            "sigma_daily",
            "sharpe_ratio",
            "max_drawdown",
        ]:
            result_dict["normal_metrics"][key] = dict["normal_metrics"][key]

        # DispoMetric:
        result_dict["dispo_metrics"] = {}
        for key in [
            "start_amount",
            "end_amount",
            "sigma_daily",
            "sharpe_ratio",
            "max_drawdown",
        ]:
            result_dict["dispo_metrics"][key] = dict["dispo_metrics"][key]

        # DispoMetric:
        result_dict["buy_and_hold_weighted"] = {}

        for key in [
            "start_amount",
            "end_amount",
            "sigma_daily",
            "sharpe_ratio",
            "max_drawdown",
        ]:
            result_dict["buy_and_hold_weighted"][key] = dict["buy_and_hold_metrics"][
                key
            ]

        # Calculate Metric
        result_dict["dispo_metrics"]["result"] = calculate_metric(
            result_dict, result_dict["dispo_metrics"]
        )
        result_dict["normal_metrics"]["result"] = calculate_metric(
            result_dict, result_dict["normal_metrics"]
        )

        result_dict["buy_and_hold_weighted"]["result"] = calculate_metric(
            result_dict, result_dict["buy_and_hold_weighted"]
        )

        result_dict["performance_gap"] = (
            result_dict["dispo_metrics"]["result"]["effektive_rendite"]
            - result_dict["normal_metrics"]["result"]["effektive_rendite"]
        )

        if result_dict["performance_gap"] > 0:
            result_dict["winner"] = "dispo"
        elif result_dict["performance_gap"] == 0:
            result_dict["winner"] = "unentschieden"
        else:
            result_dict["winner"] = "normal"

        return result_dict

    else:
        raise IOError("Kein gültiger Zeitraum gefunden.")


for datei in json_dateien:
    aa_match = aa_pattern.search(datei)
    dg_match = dg_pattern.search(datei)
    freq_match = freq_pattern.search(datei)
    strategy_match = strategy_pattern.search(datei)

    if aa_match and dg_match and freq_match and strategy_match:
        aa = aa_match.group(1)
        dg = dg_match.group(1)
        freq = freq_match.group(1)
        strategy = strategy_match.group(1)
        key = f"AA-{aa}-DG-{dg}"
        pfad = os.path.join(nachbarordner, datei)
        gruppen[key][freq][strategy].append(pfad)


def avg_metrics(data_list):
    dispo_sum = defaultdict(float)
    normal_sum = defaultdict(float)
    buy_and_hold_weighted_sum = defaultdict(float)
    dispo_count = 0
    normal_count = 0
    buy_and_hold_count = 0

    winner_dispo_count = 0
    winner_normal_count = 0

    for item in data_list:
        # Dispo
        dispo_result = item["dispo_metrics"]["result"]
        for key in dispo_result:
            dispo_sum[key] += dispo_result[key]
        dispo_count += 1

        # Normal
        normal_result = item["normal_metrics"]["result"]
        for key in normal_result:
            normal_sum[key] += normal_result[key]
        normal_count += 1

        # Buy_and_hold
        buy_and_hold_weighted_result = item["buy_and_hold_weighted"]["result"]
        for key in buy_and_hold_weighted_result:
            buy_and_hold_weighted_sum[key] += buy_and_hold_weighted_result[key]
        buy_and_hold_count += 1

        winner = item["winner"]
        if winner == "dispo":
            winner_dispo_count += 1
        elif winner == "normal":
            winner_normal_count += 1

    dispo_avg = {key: dispo_sum[key] / dispo_count for key in dispo_sum}
    normal_avg = {key: normal_sum[key] / normal_count for key in normal_sum}
    buy_and_hold_weighted_avg = {
        key: buy_and_hold_weighted_sum[key] / buy_and_hold_count
        for key in buy_and_hold_weighted_sum
    }

    dispo_avg["performance_gap"] = (
        dispo_avg["effektive_rendite"] - normal_avg["effektive_rendite"]
    )
    normal_avg["performance_gap"] = (
        normal_avg["effektive_rendite"] - dispo_avg["effektive_rendite"]
    )

    dispo_avg["winner_quote"] = winner_dispo_count / (
        winner_dispo_count + winner_normal_count
    )
    normal_avg["winner_quote"] = winner_normal_count / (
        winner_dispo_count + winner_normal_count
    )
    return {
        "avg_dispo_metrics": dispo_avg,
        "avg_normal_metrics": normal_avg,
        "avg buy_and_hold_weighted_metrics": buy_and_hold_weighted_avg,
    }


# Ausgabe im gewünschten Format + JSON laden, Metriken berechnen und speichern
for key, freq_dict in gruppen.items():
    print(f"{key}:")
    for freq, strat_dict in sorted(freq_dict.items(), key=lambda x: int(x[0])):
        print(f"[ frequenz:{freq}: [")
        for strategy, pfade in strat_dict.items():
            print(f"  Strategy: {strategy} [")

            result_list_per_strategy = []
            for pfad in pfade:
                print(f"    {pfad}")
                # try:
                with open(pfad, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    result = read_data(data)
                    result_list_per_strategy.append(result)
                    # print(f"    {result}")

                    # Output-Pfad bauen:
                    aa_val = key.split("-")[1]  # z.B. 20
                    dg_val = key.split("-")[3]  # z.B. 5
                    result["name"] = (
                        f"AA-{aa_val} DG-{dg_val} freq_{freq} str {strategy}"
                    )

                # except Exception as e:
                #    print(f"    Fehler beim Laden: {e}")
            print("  ]")
            # Ergebnis abspeichern als JSON

            print(f"Ergebnis abspeichern für {strategy}")

            calculated_metric = avg_metrics(result_list_per_strategy)
            calculated_metric["data"] = result_list_per_strategy
            print(calculated_metric)
            output_dir = os.path.join(output_base, f"AA-{aa_val}-DG-{dg_val}")
            os.makedirs(output_dir, exist_ok=True)
            output_datei = os.path.join(
                output_dir, f"freq-{freq}-strategy_{strategy}.json"
            )
            with open(output_datei, "w", encoding="utf-8") as outfile:
                json.dump(calculated_metric, outfile, indent=4, ensure_ascii=False)
        print("] ]")
    print("---")
