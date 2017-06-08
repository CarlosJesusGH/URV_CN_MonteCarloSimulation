#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <random>
#include <iostream>
#include <Eigen/LU>
#include <vector>

// Some useful terminal commands:
// source activate venv_conda && make && python ../python/main.py
// source activate venv_conda
// make
// python ../python/main.py
// make clean && make && python ../python/main.py

// ----------------
// regular C++ code
// ----------------

void count_ones(Eigen::MatrixXd);

Eigen::MatrixXd inv(Eigen::MatrixXd xs) {        
    return xs.inverse();
}

double det(Eigen::MatrixXd xs) {
    return xs.determinant();
}

std::vector<int> initialize_infected(int n_nodes, float p_0, std::vector<int> infected_set){
    std::random_device rd;  //Will be used to obtain a seed for the random number engine
    std::mt19937 gen(rd()); //Standard mersenne_twister_engine seeded with rd()
    std::uniform_int_distribution<> dis(0, n_nodes);

    int max_infected = n_nodes * p_0;

    // printf("max_inf= %d \n", max_infected);
    int count = 0;
    while(infected_set.size() < max_infected && count < n_nodes*n_nodes){
        int new_rand = dis(gen);
        // printf("inf size= %d, new_rand=%d \n", infected_set.size(), new_rand);
        if (!(std::find(infected_set.begin(), infected_set.end(), new_rand) != infected_set.end())){
            // printf("now let's push \n");
            infected_set.push_back(new_rand);
        }
        count++;
    }
    return infected_set;
}

void print_vector_int(std::vector<int> vector){
    for (auto i = vector.begin(); i != vector.end(); ++i)
        std::cout << *i << ' ';
    std::cout << std::endl;
}

void print_vector_float(std::vector<float> vector){
    for (auto i = vector.begin(); i != vector.end(); ++i)
        std::cout << *i << ' ';
    std::cout << std::endl;
}

std::vector<float> run_simulation_fixed_b(Eigen::MatrixXd adj_mat, std::vector<int> infected_set,
int t_max, float B, float u){
    std::random_device rd;  //Will be used to obtain a seed for the random number engine
    std::mt19937 gen(rd()); //Standard mersenne_twister_engine seeded with rd()
    std::uniform_real_distribution<> dist(0, 1);

    std::vector<float> num_infected_by_step;
    int n_vertices = adj_mat.rows();
    num_infected_by_step.push_back((float) infected_set.size() / n_vertices);

    // Now start looping with fixed B
    for (int step = 0; step < t_max; step++){
        std::vector<int> infected_to_add;
        for (int inf = 0; inf < infected_set.size(); inf++){
            for (int neighbor = 0; neighbor < n_vertices; neighbor++){
                if (adj_mat(infected_set[inf],neighbor) == 1){
                    float new_rand = dist(gen);
                    //printf("new_rand1=%f \n", new_rand);
                    if (new_rand < B
                    && !(std::find(infected_set.begin(), infected_set.end(), neighbor) != infected_set.end())
                    && !(std::find(infected_to_add.begin(), infected_to_add.end(), neighbor) != infected_to_add.end()))
                        infected_to_add.push_back(neighbor);
                }
            }
        }
        // Add the new infected nodes to the infected set
        infected_set.insert(infected_set.end(), infected_to_add.begin(), infected_to_add.end());
        // Recover some of the infected nodes using probability u
        for (int inf = 0; inf < infected_set.size(); inf++){
            float new_rand = dist(gen);
            //printf("new_rand2=%f \n", new_rand);
            if (new_rand < u){
                infected_set.erase(infected_set.begin() + inf);
            }
        }
        // Update infected percentage history
        num_infected_by_step.push_back((float) infected_set.size() / n_vertices);
    }
    return num_infected_by_step;
}

Eigen::VectorXd simulate(Eigen::MatrixXd adj_mat, int n_rep, float p_0, int t_max, int t_trans, int n_samples_B, float u) {
    //RowVectorXd joined(7); joined << vec1, vec2;
    //v.tail(2) // to get last 2 values from vector
    std::vector<float> p_t;
    for (int x=0; x<n_samples_B; x++){
		float B = (float) x / (n_samples_B - 1);
        //RowVectorXd pt_before_avg(t_max);
        //float pt_before_avg[n_rep];
        std::vector<float> pt_before_avg;
        for (int rep=0; rep<n_rep; rep++){
            //printf("B=%f, rep=%d \n",B,rep);
            // initialize infected set
            std::vector<int> infected_set;
            infected_set = initialize_infected(adj_mat.rows(), p_0, infected_set);
            // Run simulation for fixed B
            std::vector<float> result_sim_fixed;
            result_sim_fixed = run_simulation_fixed_b(adj_mat, infected_set, t_max, B, u);
            // average of ρ(t) over many time steps, when the systems has reached the stationary state.
            int stat_size = t_max - t_trans;
            //std::vector<float> v(result_sim_fixed(stat_size),v.end());
            float avg_stationary = accumulate(result_sim_fixed.begin() + stat_size, result_sim_fixed.end(), 0.0)/result_sim_fixed.size();
            pt_before_avg.push_back(avg_stationary);
            //pt_before_avg[rep] = avg_stationary
            //print_vector(infected_set);
            //result_sim_fixed = self.run_simulation_fixed_b(t_max, B, u)
        }
        float pt_after_avg = accumulate(pt_before_avg.begin(), pt_before_avg.end(), 0.0)/pt_before_avg.size();
        p_t.push_back(pt_after_avg);
        printf("Done with B=%f. \n", B);
    }
    Eigen::VectorXd v(p_t.size());
    for(int i=0; i < p_t.size(); i++){
        v(i) = p_t[i];
    }

    return v;
}

void count_ones(Eigen::MatrixXd xs){
    int count_ones = 0;
    int count_zeros = 0;
    for (size_t i = 0, nRows = xs.rows(), nCols = xs.cols(); i < nRows; ++i){
        for (size_t j = 0; j < nCols; ++j){
            if (xs(i,j) == 1)
                count_ones++;
            else
                count_zeros++;
        }
    }
    printf("count_ones=%d, count_zeros=%d \n", count_ones, count_zeros);
}

// ----------------
// Python interface
// ----------------

namespace py = pybind11;

PYBIND11_PLUGIN(monte_carlo_cpp) {
    pybind11::module m("monte_carlo_cpp", "monte_carlo module");
    m.def("inv", &inv);
    m.def("det", &det);
    m.def("simulate", &simulate);
    return m.ptr();
}
