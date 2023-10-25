# License : AGPLv3

from rtlsdr import RtlSdr
import numpy as np
import asyncio

from .utils import *

class RtlSdr_NFS32002:

    def __init__(self):
        self.sdr = RtlSdr()
        self.sdr.sample_rate = 1e6
        self.sdr.center_freq = 868.3e6

    def __detectNFS32002Frame(self, samples_array, error_rate):
        nfs32002_timings = [625, 312.5, 312.5, 207.5, 207.5, 500, 500, 250, 250, 250, 250, 500, 500, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 500, 250, 250, 500, 250, 250, 500, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250]
        
        data = np.abs(samples_array)**2
        mean_data = np.mean(data)
        normalized = np.where(data > mean_data, 1, 0)
        bin_data = normalized[np.where(normalized != 0)[0][0]:]
        bin_data = np.append([0], bin_data)

        values, timings = find_runs(bin_data)
        error_rate_min, error_rate_max = 1-error_rate, 1+error_rate

        detected_frame = False

        i = 0
        while i < len(values):
            # Check the presence of a syncword
            data = True
            if values[i] == 1:
                j = i
                for timing in nfs32002_timings:
                    if (timings[j] >= (timing*error_rate_min) and \
                        timings[j] <= (timing*error_rate_max) and \
                        j < len(values)):
                        j += 1
                    else:
                        data = False
                        break
                if data:
                    detected_frame = True
                    break
            i += 1

        return(detected_frame)
    
    def __detectNFS32002FrameSimple(self, samples_array, error_rate):
        sequence = "001101010011010101010100101101001010101010101010"
        
        data = np.abs(samples_array)**2
        mean_data = np.mean(data)
        normalized = np.where(data > mean_data, 1, 0)
        # bin_data = normalized[np.where(normalized != 0)[0][0]:]
        # bin_data = np.append([0], bin_data)
        bin_data = normalized
        bin_data = bin_data[0::250]
        binlist = "".join(list(map(str, bin_data.tolist())))
        
        return (sequence in binlist)

    async def __detectionLoop(self, callback, error_rate, simple_detect):
        samples_array = np.array([])
        stream = self.sdr.stream()
        
        if simple_detect:
            detect = self.__detectNFS32002FrameSimple
        else:
            detect = self.__detectNFS32002Frame
            
        async for samples in stream:
            samples_array = np.append(samples_array, samples)
       
            if len(samples_array) > 250*200:
                
                try:
                    detected = detect(samples_array, error_rate)
                except:
                    detected = False
                # Flush samples array
                samples_array = np.array([])

                if detected:
                    callback()
                    while not stream.queue.empty():
                        stream.queue.get_nowait()
                        stream.queue.task_done()


    def startDetection(self, callback, error_rate = 0.2, simple_detect = False):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.__detectionLoop(callback, error_rate, simple_detect))
