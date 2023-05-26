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
        bin = normalized[np.where(normalized != 0)[0][0]:]
        bin = np.append([0], bin)

        values, timings = find_runs(bin)
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

    async def __detectionLoop(self, callback, error_rate):
        samples_array = np.array([])
        stream = self.sdr.stream()
        async for samples in stream:
            samples_array = np.append(samples_array, samples)
       
            if len(samples_array) > 250*200:
                
                try:
                    detected = self.__detectNFS32002Frame(samples_array, error_rate)
                except:
                    detected = False
                # Flush samples array
                samples_array = np.array([])

                if detected:
                    callback()
                    await stream.queue.get()


    def startDetection(self, callback, error_rate = 0.2):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.__detectionLoop(callback, error_rate))
