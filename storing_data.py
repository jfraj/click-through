"""This module is used to produce saved dataframe from train.csv file."""
import os
import pandas as pd


def save_df_by_chunk(fname, save_dir='pkld_data', chunksize=4000000):
    """Save dataframe in chunks in the given directory.

    Args:
        fname: path to the csv data file

        save_dir: where the pickled data will be saved

        chunksize: number of rows per saved chunk
    """
    save_name = os.path.join(save_dir, 'pkled_chunk')
    ichunk = 0
    for chunk in pd.read_csv(fname, chunksize=chunksize, dtype={'id': str}):
        print('pickling chunk {}'.format(ichunk))
        chunk.to_pickle('{}_{}.pkl'.format(save_name, ichunk))
        ichunk += 1


def get_df(data_dir, **kwargs):
    """Get and merge pickled dataframe from the given directory.

    Args:
        data_dir: directory where the pickled chunks are

    Kwargs:
        max_chunks: max number of chunk file to merge
                    for a subsample of the data

    """
    max_chunks = kwargs.get('max_chunks', None)
    basename = 'pkled_chunk'
    df_list = []
    for ifname in os.listdir(data_dir)[:max_chunks]:
        if ifname.find(basename) < 0:
            continue
        ifname = os.path.join(data_dir, ifname)
        print('adding chunk {}'.format(ifname))
        df_list.append(pd.read_pickle(ifname))
    return pd.concat(df_list)

if __name__ == '__main__':
    traincsvpath = 'data/train.csv'
    #######
    # Call example

    # to save
    #save_df_by_chunk(traincsvpath)

    # to load
    #df = get_df('pkld_data')
    #print(df.shape)
