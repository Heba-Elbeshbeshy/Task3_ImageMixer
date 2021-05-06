#include <complex>
#include <cstddef>
#include <vector>
#include<iostream>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h> 
#include <pybind11/complex.h>
#include <pybind11/functional.h>
#include <pybind11/chrono.h>
using std::size_t;
using std::complex;
using std::vector;
using std::exp;
using std::polar;


const double PI = 3.141592653589793238460;
namespace py = pybind11;

vector<complex<double> > dft(const vector<complex<double> > &input)
 {
	vector<complex<double> > output;
	size_t N = input.size();
	for (size_t k = 0; k < N; k++) {  // For each output element
		complex<double> sum(0, 0);
		for (size_t n = 0; n < N; n++) {  // For each input element
			double angle = 2 * M_PI * n * k / N;
			sum += input[n] * exp(complex<double>(0, -angle));
		}
		output.push_back(sum);
	}
	return output;
}


vector<double>dft_real(const vector<complex<double> > &input) 
{
	size_t N = input.size();
	vector<complex<double> > complex_Dft=dft(input);
	vector<double>  real_DFT(N);
	for (size_t i=0; i< N; i++) 
	{  
		real_DFT[i]=complex_Dft[i].real();
	}
	return real_DFT;
}


vector<double>  dft_imag(const vector<complex<double> >  &input) 
{
	size_t N = input.size();
	vector<complex<double> > complex_Dft=dft(input);
	vector<double>  imag_DFT(N);
	for (size_t i=0; i< N; i++) 
	{  
		imag_DFT[i]=complex_Dft[i].imag();
	}
	return imag_DFT;
}


vector<complex<double> > fft( vector<complex<double> > &input)
{
    int N=input.size();
    if(N==1) {return input;}
    int M=N/2 ;
    vector<complex<double> >Xeven(M,0);
    vector<complex<double> >Xodd(M,0);
    for(int i=0; i!=M;i++)
    {
        Xeven[i]=input[2*i];
        Xodd[i]=input[2*i+1];
    }
    vector<complex<double> >Feven(M,0);
    Feven=fft(Xeven);
    vector<complex<double> >Fodd(M,0);
    Fodd=fft(Xodd);
    vector<complex<double> >freqbins(N,0);
    for(int k=0;k!=N/2;k++)
    {
        complex<double> complex_exp=polar(1.0,-2*PI*k/N)*Fodd[k];
        freqbins[k]=Feven[k]+complex_exp;
        freqbins[k+N/2]=Feven[k]-complex_exp;

    }
    return freqbins;
}

vector<double>  fft_real(vector<complex<double> >  &input) 
{
	int N = input.size();
	vector<complex<double> > complex_fft=fft(input);
	vector<double>  real_fft(N);
	for (int i=0; i< N; i++) 
	{  
		real_fft[i]=complex_fft[i].real();
	}
	return real_fft;
}


vector<double>  fft_imag(vector<complex<double> >  &input) 
{
	int N = input.size();
	vector<complex<double> > complex_fft=fft(input);
	vector<double>  imag_fft(N);
	for (int i=0; i< N; i++) 
	{  
		imag_fft[i]=complex_fft[i].imag();
	}
	return imag_fft;
}





PYBIND11_MODULE(ft_fft, m) 
{
    m.doc() = "pybind11 ft_fft plugin"; // optional module docstring

    m.def("dft", &dft);
	m.def("dft_real", &dft_real);
	m.def("dft_imag", &dft_imag);
	m.def("fft", &fft);
	m.def("fft_real",&fft_real);
	m.def("fft_imag",&fft_imag);

}
/*
int main()
{
    int N=8;
    vector<complex<double> > sig;
    sig={1.5,70.0,81.0,90.5,0.0,2.0,15.7,0.0};
    vector<complex<double> > complex_dft= dft(sig);
	vector<double>  real_dft=dft_real(sig);
	vector<double>  imag_dft=dft_imag(sig);
	vector<complex<double> >  complex_fft=fft(sig);
	vector<double>  real_fft=fft_real(sig);
	vector<double>  imag_fft=fft_imag(sig);
    for (size_t i = 0; i < 8; i++)
    {
		std::cout<<"dft" << std::endl;
		std::cout<<complex_dft[i]<<std::endl;
		std::cout<<"dft_real"<<std::endl;
		std::cout<<real_dft[i]<<std::endl ;
		std::cout<<"dft_imag"<<std::endl;
		std::cout<<imag_dft[i]<<std::endl;
		std::cout<<"fft"<<std::endl;
		std::cout<<complex_fft[i]<<std::endl;
		std::cout<<"fft_real"<<std::endl;
		std::cout<<real_fft[i]<<std::endl ;
		std::cout<<"fft_imag"<<std::endl;
		std::cout<<imag_fft[i]<<std::endl;
    }
    
}*/