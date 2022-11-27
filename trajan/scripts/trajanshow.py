# Utility script to quickly plot a drifter collection file

import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import trajan as ta
import click
from pathlib import Path
import lzma

@click.command()
@click.argument('tf')
def main(tf):
    tf = Path(tf)
    if tf.suffix == '.xz':
        with lzma.open(tf) as fd:
            ds = xr.open_dataset(fd)
            ds.load()
    else:
        ds = xr.open_dataset(tf)

    if 'status' in ds:  # hack for OpenDrift files
        ds = ds.where(ds.status>=0)

    ds.traj.plot()

    start_time = np.nanmin(ds.time.data).astype('datetime64[s]')
    end_time = np.nanmax(ds.time.data).astype('datetime64[s]')
    name = tf

    plt.gca().set_title(f'{name} [ {start_time} to {end_time} ]')

    plt.show()

if __name__ == '__main__':
    main()
