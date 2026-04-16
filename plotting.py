from pathlib import Path
import matplotlib.pyplot as plt

from basic import run_basic
# TODO: after we implement run_efficient(), uncomment the efficient_graph plotting lines below
# from efficient import run_efficient


# Iterate through the Datapoints folder and run both algorithms on the different inputs
def collect_results(input_dir="Datapoints"):
    input_files = sorted(Path(input_dir).iterdir())

    basic_results = []
    efficient_results = []

    for i_file in input_files:
        basic_results.append(run_basic(str(i_file), "temp_basic.txt"))
        # efficient_results.append(run_efficient(str(i_file), "temp_efficient.txt"))

    return basic_results, efficient_results


# Plot 2 graphs with problem_size x memory and problem_size x time
def plot_results(basic_results, efficient_results):

    basic_results = sorted(basic_results, key=lambda r: r["problem_size"])
    efficient_results = sorted(efficient_results, key=lambda r: r["problem_size"])

    # Problem size is the same for efficient/basic so the x values are consistent
    x = [r["problem_size"] for r in basic_results]

    # --- Time Plot ---
    plt.figure()
    plt.plot(x, [r["time_ms"] for r in basic_results], marker="o", label="Basic")
    # plt.plot(
    #     x,
    #     [r["time_ms"] for r in efficient_results],
    #     marker="o",
    #     label="Memory-efficient",
    # )
    plt.xlabel("Problem size (m + n)")
    plt.ylabel("Time (ms)")
    plt.title("Time vs Problem Size")
    plt.legend()
    plt.grid(True)
    plt.savefig("time_plot.png")
    plt.close()

    # --- Memory Plot ---
    plt.figure()
    plt.plot(x, [r["memory_kb"] for r in basic_results], marker="o", label="Basic")
    # plt.plot(
    #     x,
    #     [r["memory_kb"] for r in efficient_results],
    #     marker="o",
    #     label="Memory-efficient",
    # )
    plt.xlabel("Problem size (m + n)")
    plt.ylabel("Memory (KB)")
    plt.title("Memory vs Problem Size")
    plt.legend()
    plt.grid(True)
    plt.savefig("memory_plot.png")
    plt.close()


if __name__ == "__main__":
    basic_results, efficient_results = collect_results("Datapoints")
    plot_results(basic_results, efficient_results)
