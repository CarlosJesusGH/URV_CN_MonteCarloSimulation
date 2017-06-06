char const* greet()
{
   return "hello, world";
}
 
#include &lt;boost/python.hpp&gt;
 
BOOST_PYTHON_MODULE(hello_ext)
{
    using namespace boost::python;
    def("greet", greet);
}
