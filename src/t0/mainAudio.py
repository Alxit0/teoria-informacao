from scipy.io import wavfile
import sounddevice as sd
import matplotlib.pyplot as plt
import numpy as np

def apresentarInfo(nomeFicheiro, fs, nrBitsQuant):
	print('Informações do ficheiro')

	print(f'Nome: {nomeFicheiro}')
	print(f'Taxa de amostragem: {fs}')
	print(f'Quantização: {nrBitsQuant}')

def visualizacaoGrafica(data:np.ndarray, fs:int, tini=0, tfim=-1):

	if tfim == -1:
		tfim = len(data)/fs

	data_max = np.max(np.abs(data))

	eixo_x = [i/fs for i in range(len(data))]
	eixo_y_e = data[:,0]/data_max
	eixo_y_d = data[:,0]/data_max

	plt.figure(1)
	plt.subplot(211)
	plt.plot(eixo_x, eixo_y_e)
	plt.axis([tini, tfim, -1, 1])
	plt.xlabel('Tempo [s]')
	plt.ylabel('Amplitude [-1:1]')
	plt.title('Canal Esquerdo')
	plt.subplots_adjust(hspace=0.5)
	
	plt.subplot(212)
	plt.plot(eixo_x, eixo_y_d)
	plt.axis([tini, tfim, -1, 1])
	plt.xlabel('Tempo [s]')
	plt.ylabel('Amplitude [-1:1]')
	plt.title('Canal Direito')
	plt.subplots_adjust(hspace=0.5)

	plt.show()

def main():
	filename = './files/drumloop.wav'

	fs, data = wavfile.read(filename)

	visualizacaoGrafica(data, fs)

if __name__ == "__main__":
	main()
