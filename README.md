# Task3_ImageMixer
# AGMD TEAM 3ALA KAWKAB ELARD 

# El Steps de 5asa l most5dme Linux :"

 ```
 1- python3 -m pip install python-dev-tools --user --upgrade
 ```
 ```
 2- wget http://www.cmake.org/files/v2.8/cmake-2.8.3.tar.gz
 ```
 ```
 3- tar xzf cmake-2.8.3.tar.gz
 ```
 ```
 4- cd cmake-2.8.3
 ```
 ```
 5- ./configure --help
 ```
 ```
 6- ./configure --prefix=/opt/cmake
 ```
 ```
 7- make
 ```
 ```
 8- pip install pybind11
 ``` 
 ```
 9- c++ -O3 -Wall -shared -std=c++11 -fPIC $(python3 -m pybind11 --includes) ft_fft.cpp -o ft_fft$(python3-config --extension-suffix)
 ```
 ```
 10- python3 ft.py
 ```

