import Sanfrancisovehiculos
from Sanfrancisovehiculos import GSP


if __name__ == '__main__':
    threshold = 3 # minimum support
    folder_path = './Data_SanFrancisco/'
    g = GSP(threshold, folder_path)
    g.get_support_items()
    

