# execute 'make' to compile the example.cpp file
# execute 'make clean' to remove the compiled file

# location of the Python header files
PYTHON2_INCLUDE = `python-config --cflags --ldflags`
PYTHON3_INCLUDE = `python3-config --cflags --ldflags`
 
# location of the Pybind and Igraph include files and library
PYBIND_INC = ./include
IGRAPH_INC = /usr/local/include/igraph
 
# compile mesh classes
# TARGET = monte_carlo_cpp
TARGET = example
 
default:
	c++ -O3 -shared -std=c++11 -I$(PYBIND_INC) $(PYTHON3_INCLUDE) -fPIC $(TARGET).cpp -o $(TARGET).so

#c++ -O3 -shared -std=c++11 -I ./include `python3-config --cflags --ldflags` example.cpp -o example.so -fPIC
#c++ -O3 -shared -std=c++11 -I$(PYBIND_INC) $(PYTHON3_INCLUDE) -fPIC $(TARGET).cpp -o $(TARGET).so -I$(IGRAPH_INC) -L/usr/local/lib -ligraph
#c++ igraph_monte-carlo.cpp -I/usr/local/include/igraph -L/usr/local/lib -ligraph -o igraph_monte-carlo 

clean:
	rm $(TARGET).so && ls
