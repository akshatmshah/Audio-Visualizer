from visualizer import Visualizer
from device import inputAudio

def main():
	#obtain device and the object used 
	device, po = inputAudio()
	#send this device and the object
	vis = Visualizer(device, po)
	#go
	vis.animate()


if __name__ == '__main__':
	main()