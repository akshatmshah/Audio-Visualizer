import pyaudio as pyaudio

def inputAudio():
    p = pyaudio.PyAudio();
    
    # Choose the first device we see (microphone)
    info = p.info = p.get_host_api_info_by_index(0);

    #see what devices our computer has
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):  
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device ID: ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

    #currently for microphones only since loopback branch won't work
    chosen_device = 0;

    return chosen_device, p;