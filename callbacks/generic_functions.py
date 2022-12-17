import pandas as pd
import numpy as np
import h5py
import io
def read_hdf5_file(decoded):
     # Open the HDF5 file using h5py
        h5_file = h5py.File(io.BytesIO(decoded), 'r')
        datasets = h5_file.values()
        # Find the dataset that you want to read
        for dataset in datasets:
            # Check if the object is a dataset
            if isinstance(dataset, h5py.Dataset):
                # Check if the dataset has the desired shape
                if dataset.shape[0] > 2000:
                    # Read the first 2000 rows of the dataset
                    data = dataset[:2000]
                    break
            # If the object is a group, recursively search for the dataset
            elif isinstance(dataset, h5py.Group):
                for key, dataset in dataset.items():
                    for key, dataset in dataset.items():
                        for key, dataset in dataset.items():
                            if isinstance(dataset, h5py.Dataset):
                                print("dataset 2")
                                # Check if the dataset has the desired shape
                                if dataset.shape[0] > 2000:
                                    # Read the first 2000 rows of the dataset
                                    data = dataset[:2000]
                                    break
        # def print_keys(name, obj):
        #     if isinstance(obj, h5py.Dataset):
        #         print(name)
        # h5_file.visititems(print_keys)
        # Read the first 2000 rows of the dataset into a NumPy array
        # shape = (2000,) + h5_file.shape[1:]
        # data = np.empty(shape, dtype=h5_file.dtype)
        # h5_file.read_direct(data, np.s_[:2000])
        # Close the file
        h5_file.close()
        # Create a Pandas dataframe from the data
        return pd.DataFrame(data)