#Pre-requisites:
    1. C++:
        * igraph
        * pybind
        * eigen
    2. Python:
        *igraph
        *networkx
        *numpy
        *matplot

    
#C++ - igraph (not used at the end)
  download and install:
    wget http://igraph.org/nightly/get/c/igraph-0.7.1.tar.gz
    tar -xvzf igraph-0.7.1.tar.gz
    cd igraph-0.7.1
    ./configure
    make
    make check
    make install
    sudo ldconfig
        
  Compile C++ code:
    gcc igraph_monte-carlo.cpp -I/usr/local/include/igraph -L/usr/local/lib -ligraph -o igraph_monte-carlo -std=c++11

  Run program:
    ./igraph_monte-carlo
    
#C++ - pybind
  download and install:
    wget https://github.com/pybind/pybind11/archive/master.zip
    unzip pybind11-master.zip
    cp ./pybind11-master/include c++_code_dir
    cd c++_code_dir
    // Create cpp file as example.cpp in the beginner's tutorial.
    
  Compile C++ code:
    c++ -O3 -shared -std=c++11 -I ./include `python3-config --cflags --ldflags` example.cpp -o example.so -fPIC
    
  Test program:
    python              // Should be using python 3.6
    import example
    example.add(2,2)    // Should print "4"
    
#C++ - eigen
    wget http://bitbucket.org/eigen/eigen/get/3.3.3.tar.gz
    tar -xvzf 3.3.3.tar.gz
    cp ./eigen-eigen-67e894c6cd8f/Eigen/ c++_code_dir
    cd c++_code_dir
