import time
from timeit import timeit
import ft_fft
import numpy as np
import matplotlib.pyplot as plt


Dft_time=[]
fft_time=[]
Dft_result=[]
fft_result=[]
Size=[]
Error=[]
dft_real=[]
dft_imag=[]
fft_real=[]
fft_imag=[]


for i in range(10):
    input=list(range(0,2**(i+1)))
    Size.append(2**(i+1))

    time_ft=timeit(lambda:ft_fft.dft(input),number=1)
    time_fft=timeit(lambda:ft_fft.fft(input),number=1)
    Dft_time.append(time_ft)
    fft_time.append(time_fft)

    get_dft=ft_fft.dft(input)
    Dft_result.append(get_dft)

    get_real_dft=ft_fft.dft_real(input)
    dft_real.append(get_real_dft)

    get_imag_dft=ft_fft.dft_imag(input)
    dft_imag.append(get_imag_dft)

    get_fft=ft_fft.fft(input)
    fft_result.append(get_fft)

    get_real_fft=ft_fft.fft_real(input)
    fft_real.append(get_real_fft)

    get_imag_fft=ft_fft.fft_imag(input)
    fft_imag.append(get_imag_fft)
    
   #Calculate the mean square error
    difference_array = np.subtract(fft_result[i],Dft_result[i])
    squared_array = np.square(difference_array)
    mse =abs( squared_array.mean() )
    Error.append(mse)


# plt.figure(3)
# plt.plot(Size, Dft_time, color='blue')
# plt.title('DFT function')
# plt.xlabel("DFT size")
# plt.ylabel('DFT time')

# plt.figure(4)
# plt.plot(Size, fft_time, color='red')
# plt.title('FFT function')
# plt.xlabel("FFT size")
# plt.ylabel('FFT time')

#plotting the dft and fft

plt.figure(1)
plt.plot(Size, Dft_time, color='blue',label='$DFT$')
plt.plot(Size, fft_time, color='red',label='$FFT$')
plt.title('DFT and FFT functions')
plt.legend(loc='best')
plt.xlabel("size")
plt.ylabel('time')

#plotting the error 
plt.figure(2)
plt.plot(Size, Error, color='green',label='$Error$')
plt.title('Error Vs Size')
plt.legend(loc='best')
plt.xlabel("size")
plt.ylabel('Error')


'''
print("final_dft",Dft_result)
print("dft_real=",dft_real)
print("dft_imag=",dft_imag)

print("final_fft",fft_result)
print("fft_real=",fft_real)
print("fft_imag=",fft_imag)

print("dft_time=",Dft_time)
print("fft_time=",fft_time)

print("length=",Size)
print("error",Error)
'''

plt.show()




