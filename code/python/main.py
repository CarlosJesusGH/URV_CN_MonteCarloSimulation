import igraph as igraph
import os, time
import utils_files
import utils_networks
import settings as settings
from monte_carlo import *

# Mark start time
startTime = time.clock()

# Clear output files and directories
utils_files.remove_file_dir(settings.csv_pt)
utils_files.clear_dir(settings.output_directory + "plots/")
utils_files.clear_dir(settings.output_directory + "temp/")

# Erdös-Rényi (ER)
if False:
    utils_files.clear_dir(settings.output_directory + "nets/")
    ns = [30, 50]                          # n: The number of nodes.
    ps = [0.07, 0.1]    # p: Probability for edge creation.
    # Iterate over n's and p's
    for n in ns:
        for p in ps:
            # G = nx.erdos_renyi_graph(n=n, p=p)
            g = igraph.Graph.Erdos_Renyi(n=n, p=p)
            iter_desc = "erdos_renyi_[n=" + str(n) + ",p=" + str(p) + "]"
            utils_networks.save_graph_in_pajek_format(g, iter_desc, is_igraph=True)
            # utils_networks.plot_graph_with_communities(g, [0] * len(g.vs), settings.output_directory_plots + iter_desc + "_ini.png")


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
            utils_networks.plot_graph_with_communities(g, [0]*len(g.vs), png_path, )

            print("n_vertices = %d, n_edges = %d" % (len(g.vs), len(g.es)))
            mc_sim = MonteCarloSim(g, net_name)
            # mc_sim.run_simulation(n_rep=100, p_0=0.2, t_max=1000, t_trans=900, n_samples_B=100, u=1)  # sample sim
            # mc_sim.run_simulation(n_rep=10, p_0=0.2, t_max=1000, t_trans=900, n_samples_B=51, u=1)
            # mc_sim.run_simulation_cpp(n_rep=100, p_0=0.2, t_max=1000, t_trans=900, n_samples_B=101, u=1)
            mc_sim.run_simulation_cpp(n_rep=10, p_0=0.2, t_max=100, t_trans=90, n_samples_B=11, u=0.5)




            # TODO: plot mc_sim.num_infected_by_step
            # TODO: run simulation using different initial values, and iterate using B from 0 to 1 (steps 0.01)
            # cont... maybe we can change the name from run_simulation to run_simulation_fixed_b and then
            # cont... create a new method run_simulation where it goes over all values for B.
            # TODO: plot results after iterate for all values of B

            # break


            # --------------------------------------------------------------------------------
            # Plot resulting community detection separately in a temporal file
            # utils_networks.plot_graph_with_communities(g, membership_ref, file_name="../output/temp/temp_1.png")
            # utils_networks.plot_graph_with_communities(g, membership_m1, file_name="../output/temp/temp_2.png")
            # utils_networks.plot_graph_with_communities(g, membership_m2, file_name="../output/temp/temp_3.png")
            # utils_networks.plot_graph_with_communities(g, membership_m3, file_name="../output/temp/temp_4.png")

            # Read all temporal created images and create a sub-ploted figure
            # utils_networks.plot_all_temp_images(file, subdir[subdir.rfind('/')+1:])

            # Add new values to compare communities table
            # modularity_values = [file, mod_ref, mod_m1, mod_m2, mod_m3]
            # utils_files.add_row_to_csv(path=settings.output_csv_modularity, headers=settings.csv_header_modularity, values=modularity_values)


# Delete temporal files
utils_files.remove_file_dir(settings.output_directory + "temp/", is_dir=True)
# Show execution statistics after finishing
measuredTime = time.clock() - startTime
print('Execution time = {}'.format(measuredTime))