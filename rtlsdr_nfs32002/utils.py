# License : AGPLv3

import numpy as np

# Find runs of consecutive items in an array.
# From https://gist.github.com/alimanfoo/c5977e87111abe8127453b21204c1065
def find_runs(x):
    # ensure array
    x = np.asanyarray(x)
    if x.ndim != 1:
        raise ValueError('only 1D array supported')
    n = x.shape[0]

    # handle empty array
    if n == 0:
        return np.array([]), np.array([]), np.array([])

    else:
        # find run starts
        loc_run_start = np.empty(n, dtype=bool)
        loc_run_start[0] = True
        np.not_equal(x[:-1], x[1:], out=loc_run_start[1:])
        run_starts = np.nonzero(loc_run_start)[0]

        # find run values
        run_values = x[loc_run_start]

        # find run lengths
        run_lengths = np.diff(np.append(run_starts, n))

        return run_values, run_lengths

# Convert data to digital frame
def dataToBinary(samples):
    samples = np.abs(samples)**2
    vmax = np.amax(samples)
    threshold = vmax/10 # 0.004
    binaryFrame = []
    for data in samples:
        if data > threshold:
            binaryFrame.append('1')
        else:
            binaryFrame.append('0')
    return binaryFrame