import igraph as igraph
import itertools
import random
import numpy as np
import utils_files, settings, utils_plots

class MonteCarloSim:
    """A class to simulate an epidemic spreading using a Monte Carlo simulation"""
    net_name = ""
    infected_set = []
    p_t = []

    def __init__(self, graph, net_name):
        self.g = graph
        self.net_name = net_name
        self.n_vertices = len(self.g.vs)
        self.n_edges = len(self.g.es)
        self.p_t = []

    def initialize_infected(self, p_0):
        self.infected_set = []
        n_infected = int(self.n_vertices * p_0)
        while len(self.infected_set) < n_infected:
            new_infected = random.randint(0, self.n_vertices - 1)
            if new_infected not in self.infected_set:
                self.infected_set.append(new_infected)

    def run_simulation(self, n_rep, p_0, t_max, t_trans, n_samples_B, u):
        Bs = np.linspace(0, 1, num= n_samples_B, retstep=True)[0]
        for B in Bs:
            pt_before_avg = []
            for rep in range(n_rep):
                self.initialize_infected(p_0)
                result_sim_fixed = self.run_simulation_fixed_b(t_max, B, u)
                # average of ρ(t) over many time steps, when the systems has reached the stationary state.
                stat_size = t_max - t_trans
                avg_stationary = sum(result_sim_fixed[-stat_size:]) / stat_size
                pt_before_avg.append(avg_stationary)
            pt_after_avg = sum(pt_before_avg)/len(pt_before_avg)
            self.p_t.append(pt_after_avg)
            # print("Done with B=%f." % B)
        utils_plots.plot_data(Bs, self.p_t, title=self.net_name + "\nSIS(" + r"$N_{rep}$= " + str(n_rep) +
                                                  r", $T_{max}$= " + str(t_max) +
                                                  r", $T_{trans}$= " + str(t_trans) +
                                                  r", $N_{\beta}$= " + str(n_samples_B) +
                                                  r", $\mu$= " + str(u) +
                                                  r", $\rho_0$= " + str(p_0) + ")"
                              , xlabel=r'$\beta$', ylabel=r'$\rho$')

        # TODO: delete
        print(self.p_t)
        utils_files.add_row_to_csv(settings.csv_pt, settings.csv_header_pt, self.p_t)

    def run_simulation_fixed_b(self, t_max, B, u):
        num_infected_by_step = [len(self.infected_set)/self.n_vertices]
        for step in range(t_max):
            infected_to_add = []
            for i in self.infected_set:
                neighbors = igraph.Graph.neighbors(self.g, i)
                for n in neighbors:
                    if (random.random() < B) and (n not in self.infected_set) and (n not in infected_to_add):
                        infected_to_add.append(n)
            # Add the new infected nodes to the infected set
            self.infected_set.extend(infected_to_add)
            # Recover some of the infected nodes using probability u
            for i in self.infected_set:
                if random.random() < u:
                    self.infected_set.remove(i)
            # Update infected percentage history
            num_infected_by_step.append(len(self.infected_set) / self.n_vertices)
        return num_infected_by_step

    def run_simulation_cpp(self, n_rep, p_0, t_max, t_trans, n_samples_B, u, figure=None):
        # Import c++ directory and monte_carlo_cpp module (integrated using PyBind11)
        import sys
        sys.path.append("../c++/")
        import monte_carlo_cpp

        # Load network and create adjacency matrix
        adj_mat = np.array(igraph.Graph.get_adjacency(self.g).data)
        # Simulate the monte-carlo
        p_t = monte_carlo_cpp.simulate(adj_mat, n_rep, p_0, t_max, t_trans, n_samples_B, u)
        print("monte carlo cpp = %s" % p_t)
        # Plot
        Bs = np.linspace(0, 1, num=n_samples_B, retstep=True)[0]
        if figure is None:
            figure = utils_plots.plot_data(Bs, p_t, title=self.net_name + "\nSIS(" + r"$N_{rep}$= " + str(n_rep) +
                                                  r", $T_{max}$= " + str(t_max) +
                                                  r", $T_{trans}$= " + str(t_trans) +
                                                  r", $N_{\beta}$= " + str(n_samples_B)
                                                  # + r", $\mu$= " + str(u)
                                                  # + r", $\rho_0$= " + str(p_0)
                                                  + ")"
                                            , xlabel=r'$\beta$', ylabel=r'$\rho$'
                                            ,legend=r"$\mu$= " + str(u) + r", $\rho_0$= " + str(p_0))
        else:
            figure = utils_plots.add_plot_to_figure(Bs, p_t, figure=figure, title=self.net_name + "\nSIS(" + r"$N_{rep}$= " + str(n_rep) +
                                                          r", $T_{max}$= " + str(t_max) +
                                                          r", $T_{trans}$= " + str(t_trans) +
                                                          r", $N_{\beta}$= " + str(n_samples_B)
                                                          # + r", $\mu$= " + str(u)
                                                          # + r", $\rho_0$= " + str(p_0)
                                                          + ")"
                                                    , legend=r"$\mu$= " + str(u) + r", $\rho_0$= " + str(p_0))

        return figure
