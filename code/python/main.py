import os, time
import utils_networks
from monte_carlo import *
from multiprocessing import Pool

# Mark start time
startTime = time.clock()

# Clear output files and directories
utils_files.remove_file_dir(settings.csv_pt)
utils_files.clear_dir(settings.output_directory + "plots/")
utils_files.clear_dir(settings.output_directory + "temp/")

# Erdös-Rényi (ER)
if False:
    utils_files.clear_dir(settings.output_directory + "nets/")
    ns = [500, 1000]       # n: The number of nodes.
    ps = [0.05, 0.1]    # p: Probability for edge creation.
    # Iterate over n's and p's
    for n in ns:
        for p in ps:
            g = igraph.Graph.Erdos_Renyi(n=n, p=p)
            iter_desc = "erdos_renyi_[n=" + str(n) + ",p=" + str(p) + "]"
            utils_networks.save_graph_in_pajek_format(g, iter_desc, is_igraph=True)

# Watts-Strogatz (WS)
if False:
    utils_files.clear_dir(settings.output_directory + "nets/")
    ns = [500]                              # n: The number of nodes
    k = 4                                   # k: Each node is joined with its ``k`` nearest neighbors in a ring topology
    ps = [0.5, 0.9]                         # p: The probability of rewiring each edge
    # Iterate over n's and p's
    for n in ns:
        for p in ps:
            g = igraph.Graph.Watts_Strogatz(dim=1, size=n, nei=k, p=p)
            # G = cnc.watts_strogatz_network(n=n, k=k, p=p)
            iter_desc = "watts_strogatz_[n=" + str(n) + ",k=" + str(k) + ",p=" + str(p) + "]"
            utils_networks.save_graph_in_pajek_format(g, iter_desc, is_igraph=True)
            utils_networks.plot_graph_with_communities(g, [0] * len(g.vs), settings.output_directory + "plots/" + iter_desc + "_ini.png")

# Barabási & Albert (BA)
if False:
    utils_files.clear_dir(settings.output_directory + "nets/")
    ns = [500, 1000]                              # n : Number of nodes
    ms = [1, 2, 4]                      # m : Number of edges to attach from a new node to existing nodes
    # Iterate over n's and m's
    for n in ns:
        for m in ms:
            g = igraph.Graph.Barabasi(n=n, m=m)
            iter_desc = "barabasi_albert_[n=" + str(n) + ",m=" + str(m) + "]"
            utils_networks.save_graph_in_pajek_format(g, iter_desc, is_igraph=True)
            utils_networks.plot_graph_with_communities(g, [0] * len(g.vs), settings.output_directory + "plots/" + iter_desc + "_ini.png")


# Define nets directory and loop over it recursively
nets_dir = settings.output_directory + "nets"

for subdir, dirs, files in os.walk(nets_dir):
    for file in files:
        if file.endswith(".net"):
            # Create file path
            net_name = file.replace('.net', '')
            png_name = file.replace('.net', '_ini.png')
            net_path = subdir + os.sep + file
            png_path = settings.output_directory + "plots/" + png_name
            print('\n==========================='); print(net_path)

            # Read pajek network into igraph
            g = igraph.Graph.Read(net_path, format="pajek")
            # Simplify the graph by removing self-loops and/or multiple edges
            g.simplify()

            # For every graph we perform the monte-carlo simulation
            utils_networks.plot_graph_with_communities(g, [0]*len(g.vs), png_path)

            print("n_vertices = %d, n_edges = %d" % (len(g.vs), len(g.es)))

            # Iterate over several values for p_0, u and B using a single network.
            run_all_simulation_for_one_network(g, net_name)
            # Try this using parallel execution by using multiprocessing-Pool
                #result1 = Pool().apply_async(run_all_simulation_for_one_network, [g, net_name])   # evaluate 'run_all_simulation_for_one_network(g, net_name)' asynchronously
                #answer1 = result1.get()


# Delete temporal files
utils_files.remove_file_dir(settings.output_directory + "temp/", is_dir=True)
# Show execution statistics after finishing
measuredTime = time.clock() - startTime
print('Execution time = {}'.format(measuredTime))