import os
import codecs
from queue import Full
import pandas as pd
import itertools
import operator
import csv

class GSPP:
    def __init__(self, min_sup, folder_path):
        
        self.min_sup = min_sup
        self.folder_path = folder_path
        self.data = self.parse_data()
        self.items = {}
        self.num_users = len(self.data)
        self.num_files = len([file for file in os.listdir(folder_path) if file.endswith(".csv")])
        
    def parse_data(self):
        files = os.listdir(self.folder_path)
        files = [file for file in files if file.endswith(".csv")]
        seqs = []
        for filename in files:
            full_path = self.folder_path+filename
            df = pd.read_csv(full_path,  sep=';')
          #  print (full_path)
            ans = {}
            seq = {'file': full_path}
            s1 = []
            s2 = []
            for index, row in df.iterrows():
                # Asignando valores a las variables
                grupo_long = row['grupo_long']
                grupo_lat = row['grupo_lat']
                vel_prom = row['vel_prom']
                #grupo = row['grupo']
                #lat_minima = row['lat_minima']
                # Creando el diccionario x
                x = {'grupo_long': grupo_long, 'grupo_lat': grupo_lat, 'vel_prom': vel_prom}
                if x:
                    ans[index] = x
                    s1.append(x)
                    s2.append(tuple(x.items()))
            seq['data'] = ans
            seq['seq_individual'] = s1
            seq['seq_combined'] = s2
            seqs.append(seq)
        return seqs


    def write_to_csv(self, output_file):
        with open(output_file, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',')
            csvwriter.writerow(['grupo_long', 'grupo_lat', 'vel_prom', 'support'])
            for pattern, support in self.items.items():
                values = {}
                values["grupo_long"] = pattern[0][1]
                values["grupo_lat"] = pattern[1][1]
                values["vel_prom"] = pattern[2][1]
                csvwriter.writerow([values['grupo_long'], values['grupo_lat'], values['vel_prom'], support])
                


    def get_support_items(self):
        for i in range(len(self.data)):
            for seq in self.data[i]['seq_combined']:
                sup = self.find_support(seq)
                if sup >= self.min_sup:
                    self.items[seq] = sup
        sorted_patterns = sorted(self.items.items(), key=operator.itemgetter(1), reverse=True)
        print("Number of files: ", self.num_files)
        print(" grupo_long", " grupo_lat"," vel_prom"," support")
        for t in sorted_patterns:
            pattern = t[0]
            support = t[1]
            values = {}
            values["grupo_long"] = pattern[0][1]
            values["grupo_lat"] = pattern[1][1]
            values["vel_prom"] = pattern[2][1]
            print(values['grupo_long'], values['grupo_lat'], values['vel_prom'], support)
        
        with open("SANFRANCISCOVELOCIDAD2.csv", 'w',) as f:
            writer = csv.writer(f)
            writer.writerow(['grupo_long', 'grupo_lat', 'vel_prom', 'support'])
            for t in sorted_patterns:
                pattern = t[0]
                support = t[1]
                values = {}
                values["grupo_long"] = pattern[0][1]
                values["grupo_lat"] = pattern[1][1]
                values["vel_prom"] = pattern[2][1]
                writer.writerow([values['grupo_long'], values['grupo_lat'], values['vel_prom'], support])    
            

    def find_support(self, seq):
        count = 0
        for i in range(len(self.data)):
            if seq in self.data[i]['seq_combined']:
                count += 1
        return count
