Pre-requisites:
    igraph, install it by:
        wget http://igraph.org/nightly/get/c/igraph-0.7.1.tar.gz
        tar -xvzf igraph-0.7.1.tar.gz
        cd igraph-0.7.1
        ./configure
        make
        make check
        make install
        sudo ldconfig
        

Compile C++ code:
    gcc igraph_monte-carlo.cpp -I/usr/local/include/igraph -L/usr/local/lib -ligraph -o igraph_monte-carlo

Run program:
    ./igraph_monte-carlo
