'''
This code is used to call the GIF fitting code for a list of cells
'''
import csv
import os

'''
Whenever you run a new set of fits, update the version appropriately.
''' 
version = 'testing'

save_path = ('./GIFFittingToolbox/Saved_fits/' + version + '/')
os.makedirs(save_path, exist_ok=True)

from Main_Test_GIF import main_code

results = {}

cells = ['160824-08','160826-06','160826-07','161010-03','161012-00',
         '161107-04','161108-01','161130-02','161202-03','161207-03',
         '161209-02','161210-04','161020-01','161021-02','161024-01',
         '161104-01','230707-12','230711-01','230914-02','230919-00',
         '230919-02','230926-03','230926-04','230926-06','230929-00',
         '230929-02','231005-00','231005-03','231016-03','231017-01',
         '231024-00','231114-00','231114-02','231116-00','231116-03',
         '231205-03','231205-05','231213-02','231213-05']

cells = ['example']

for cell in cells:
    print(f'{cell=}')
    Md, percent_variance, var_explained_dV, var_explained_V = main_code(cell, version, save = False, plots = True)
    results[cell] = (Md, percent_variance, var_explained_dV, var_explained_V)

save = False
if save:

    output_file = save_path + version + '_overall_results.csv'
    with open(output_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['cell', 'md', 'percent_variance', 'var_explained_dV', 'var_explained_V'])
        for cell, (Md, percent_variance, var_explained_dV, var_explained_V) in results.items():
            writer.writerow([cell, Md, percent_variance, var_explained_dV, var_explained_V])
