import Romavehiculos
from Romavehiculos import GSP


if __name__ == '__main__':
    threshold = 3 # minimum support
    folder_path = './DataRomalargo/'
    g = GSP(threshold, folder_path)
    g.get_support_items()
    