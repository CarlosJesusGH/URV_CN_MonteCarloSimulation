#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <random>
#include <iostream>
#include <Eigen/LU>

// ----------------
// regular C++ code
// ----------------

Eigen::MatrixXd inv(Eigen::MatrixXd xs) {
    return xs.inverse();
}

double det(Eigen::MatrixXd xs) {
    return xs.determinant();
}

Eigen::MatrixXd simulate(Eigen::MatrixXd adj_mat) {
    return adj_mat.inverse();
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
