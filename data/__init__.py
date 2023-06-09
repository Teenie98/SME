import pickle
import numpy as np
from torch.utils.data import Dataset as _Dataset
import random

col_num = [('MovieID', 4000),
           ('UserID', 6050),
           ('Age', 7),
           ('Gender', 2),
           ('Occupation', 21),
           ('Year', 83),
           ('Genres', 25),
           ('Title', 5000)]


def read_pkl(file):
    with open(file, 'rb') as f:
        t = pickle.load(f)
    return t


def get_data(data, fea_mask):
    one_hot_feat = [col for col, _ in col_num[:-2]]
    data_x = data[one_hot_feat].to_numpy()
    data_g = np.array(data.Genres.apply(lambda x: np.array((4 - len(x)) * [0] + x[:4])).to_list())
    data_t = np.array(data.Title.apply(lambda x: np.array((8 - len(x)) * [0] + x[:8])).to_list())
    if fea_mask:
        for title in data_t:
            idx = np.nonzero(title)[0]
            if idx.size > 1:
                # random_mask_idx = random.choice(idx)
                # title[random_mask_idx] = title[idx[0]]
                title[idx[0]] = 0

    data_y = data['y'].values.reshape(-1, 1)
    return np.hstack([data_x, data_g, data_t]), data_y


class Dataset(_Dataset):
    def __init__(self, name, fea_mask=False):
        super().__init__()
        data = read_pkl(name + '.pkl')
        self.x, self.y = get_data(data, fea_mask)

    def __getitem__(self, idx):
        return self.x[idx], self.y[idx]

    def __len__(self):
        return len(self.x)
