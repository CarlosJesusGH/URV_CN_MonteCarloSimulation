#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <random>
#include <iostream>
#include <Eigen/LU>

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

Eigen::MatrixXd simulate(Eigen::MatrixXd xs, int n_rep, float p_0, int t_max, int t_trans, int n_samples_B, float u) {

    return xs;
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
