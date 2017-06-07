#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <random>
#include <iostream>
//#include <Eigen/Dense>

namespace py = pybind11;
using Eigen::MatrixXd;

int simulate(Eigen::MatrixXd big_mat){
    //for (size_t j = 0; j < cols; ++j)
        //std::cout << array[i][j] << '\t';
    return 12345;
}

PYBIND11_MODULE(monte_carlo_cpp, m) {
    m.doc() = "pybind11 example plugin"; // optional module docstring
    //m.def("add", &add, "A function which adds two numbers");
    m.def("simulate", &simulate, "A function which performs the monte carlo simulation");
    //m.def("random_number", &random_number, "A function which prints a random number");  
}









//--------------------------------
//--------------------------------
//--------------------------------
// NOT USED
// --------

//#include <igraph.h>

int random_number(void){
    std::mt19937 rng;
    rng.seed(std::random_device()());

    for (unsigned int i = 0; i < 5; i += 1)
    {
    std::uniform_int_distribution<std::mt19937::result_type> dist6(1,6); // distribution in range [1, 6]
    std::cout << dist6(rng) << std::endl;  
    }
}

int add(int i, int j) {
    return i + j;    
}

int simulate_old(int n_rep){
    // NOTE: couldn't make this method work, so I will try with simple primitives using the adjency matrix.
    //igraph_integer_t diameter;
    //igraph_t graph;
    //igraph_rng_seed(igraph_rng_default(), 42);
    //igraph_erdos_renyi_game(&graph, IGRAPH_ERDOS_RENYI_GNP, 1000, 5.0/1000, 
    //IGRAPH_UNDIRECTED, IGRAPH_NO_LOOPS);
    //igraph_diameter(&graph, &diameter, 0, 0, 0, IGRAPH_UNDIRECTED, 1);
    //printf("Diameter of a random graph with average degree 5: %d\n", (int) diameter);
    //igraph_destroy(&graph);
    return 123;
}

