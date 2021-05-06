import ft_fft

sig=[1.5,70.0,81.0,90.5,0.0,2.0,15.7,0.0]
dft=ft_fft.dft(sig)
real_ft=ft_fft.dft_real(sig)
imag_ft=ft_fft.dft_imag(sig)
fft=ft_fft.fft(sig)
real_fft=ft_fft.fft_real(sig)
imag_fft=ft_fft.fft_imag(sig)
print("dft="," ", dft)
print("real_ft=","",real_ft)
print("imag_ft=","",imag_ft)
print("fft=","",fft)
print("real_fft=","",real_fft)
print("imag_fft=","",imag_fft)