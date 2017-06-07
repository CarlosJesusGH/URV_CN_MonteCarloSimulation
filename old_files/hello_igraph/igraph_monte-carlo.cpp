#include <igraph.h>
#include <random>
#include <iostream>

int diameter(void){
  igraph_integer_t diameter;
  igraph_t graph;
  igraph_rng_seed(igraph_rng_default(), 42);
  igraph_erdos_renyi_game(&graph, IGRAPH_ERDOS_RENYI_GNP, 1000, 5.0/1000,
                         IGRAPH_UNDIRECTED, IGRAPH_NO_LOOPS);
  igraph_diameter(&graph, &diameter, 0, 0, 0, IGRAPH_UNDIRECTED, 1);
  printf("Diameter of a random graph with average degree 5: %d\n",
         (int) diameter);
  igraph_destroy(&graph);
}

int random_number(void){
  std::mt19937 rng;
  rng.seed(std::random_device()());
  std::uniform_int_distribution<std::mt19937::result_type> dist6(1,6); // distribution in range [1, 6]

  std::cout << dist6(rng) << std::endl;
}

int main(void){
   diameter();
   random_number();
   return 0;
}
