import Sanfranciscovelocidad
from Sanfranciscovelocidad import GSPP


if __name__ == '__main__':
    threshold = 2 # minimum support
    folder_path = './Data_SanFrancisco/'
    g = GSPP(threshold, folder_path)
    g.get_support_items()
    