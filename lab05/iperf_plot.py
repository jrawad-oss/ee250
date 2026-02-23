import matplotlib
matplotlib.use("Agg")  # saves plots without needing a display <-- issue with rpi as Pi is trying to open a plot window, but it has no GUI display
import pandas as pd
import matplotlib.pyplot as plt


distances_m = [2, 4, 5, 6, 8] #array for the distance (m) we collected
# x-axis labels for every plot
run_labels = ["Run1", "Run2", "Run3", "Run4", "Run5"]

#save named files based on distance from VM 
#for loop because it'll save 5 different files according to the distances 
for d in distances_m:
    tcp_path = f"iperf_tcp_{d}m.csv"
    udp_path = f"iperf_udp_{d}m.csv"

    # load csvs
    tcp_df = pd.read_csv(tcp_path)
    udp_df = pd.read_csv(udp_path) 
    tcp_row = tcp_df.iloc[-1] # use last row (most recent run) for both tcp and udp
    udp_row = udp_df.iloc[-1]

    # pull five run values and make one plot per distance
    tcp_vals = [tcp_row[r] for r in run_labels]
    udp_vals = [udp_row[r] for r in run_labels]
    plt.figure()
    plt.plot(run_labels, tcp_vals, marker="o", label="tcp throughput")
    plt.plot(run_labels, udp_vals, marker="s", label="udp throughput")

    # label axes 
    plt.xlabel("test runs")
    plt.ylabel("throughput (mbps)")
    plt.title(f"tcp & udp throughput at {d}m")
    plt.legend()

    # save the deliverable image
    plt.savefig(f"throughput_{d}m.png")
