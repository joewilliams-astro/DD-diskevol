import os
import pandas as pd

class simulation():
    '''
    Class object that grabs and stores all the relevant data from
    the DD18 simulations.
    '''
    def __init__(self, directory):
        files = os.listdir(directory)
        files = [file[:-4] for file in files if file.endswith('.dat')]
        files = list( filter(lambda x: 'infall2' not in x, files))   # Remove unwanted files like infall2

        for file in files:
            data = self.read_data(file, directory)
            setattr(self, file, data)
        self.rgrid = pd.read_csv(directory+'../grid.info').values[:,0]
    

    def read_data(self, file, directory):
        '''
        Function to read in the data. Reshapes the data if required,
        and adds an extra row of zeros at t=0 if required.
        '''
        df = pd.read_csv(directory+f'{file}.dat').values
        length = len(df)

        try:
            if length == 281400:
                df = df.reshape(201, 1400)
                return df[1:, :]    # Bin t=0
            elif length == 200:
                return df[:,0]
            elif length == 0:
                return None
            else:
                print(f"Couldn't reshape {file}!")
                return df
        except ValueError:
            print(f'Error with data "{file}" -> shape is {df.shape}')
    

    def print_shapes(self):
        '''
        Function that prints the shapes of all the non-method attributes
        of the class.
        '''
        attributes = [attr for attr in dir(self) if not attr.startswith('__') and not callable(getattr(self, attr))]
        for object in attributes:
            exec(f"print(f'{object}: {{self.{object}.shape}}') if self.{object} is not None else None")