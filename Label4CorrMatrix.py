# -*- coding: utf-8 -*-
import xlrd
import os
import csv
import statistics as st
class Data_Preparation:

    def __init__(self, spec_loc, project_folder):
        self.spec_loc = spec_loc
        self.project_folder = project_folder
        self.ydata_loc = os.path.join(self.project_folder, 'labels.xlsx')
    def txt2list(self, file, type):
        l = []
        with open(file, 'r') as f:
            for index, line in enumerate(f):
                if index > 6:
                    l.append(float(line.strip()))

        if type == 'S':
            return l[275:1815]
        elif type == 'NIR':
            return l
        else:
            raise Exception('Type error')

    def read_spec_label(self):
        res = {}
        self.exlFile = xlrd.open_workbook(self.spec_loc)

        res_sheet = self.exlFile.sheet_by_name('Sheet1')
        res['flame-S']= res_sheet.col_values(0)[1:]
        res['flame-NIR']= res_sheet.col_values(1)[1:129]
        return res

    def read_xdata(self):

        samples_s_loc = os.path.join(self.project_folder,'Flame-S Spectra')
        samples_nir_loc = os.path.join(self.project_folder,'Flame-NIR Spectra')
        num_s = len(os.listdir(samples_s_loc))
        num_nir = len(os.listdir(samples_nir_loc))
        assert num_nir == num_s
        samples_num = num_s

        sample_s = []
        sample_nir = []

        for index in range(samples_num):
            file_name = str(index+1)+'.txt'
            tmp = self.txt2list(os.path.join(samples_s_loc, file_name), 'S')
            sample_s.append(tmp)
        for index in range(samples_num):
            file_name = str(index+1)+'.txt'
            tmp = self.txt2list(os.path.join(samples_nir_loc, file_name), 'NIR')
            sample_nir.append(tmp)

        return sample_s, sample_nir, samples_num



    def read_ydata(self):
        exlFile = xlrd.open_workbook(self.ydata_loc)
        res_sheet = exlFile.sheet_by_name('nematode_res')
        res = res_sheet.col_values(0)
        return res

    def lists2csv(self, name, dest_loc, lists):

        file_loc = os.path.join(dest_loc, name)

        with open(file_loc, 'w') as resultFile:
            wr = csv.writer(resultFile, dialect='excel')
            wr.writerows(lists)


project_30 = '/home/ysyncby/courses/RA/Data/data/Walnut_Project_30'
project_IV = '/home/ysyncby/courses/RA/Data/data/Walnut_Project_IV'
project_VI = '/home/ysyncby/courses/RA/Data/data/Walnut_Project_VI'
spec_loc = '/home/ysyncby/courses/RA/Data/data/kobin_spectra_wavelengths.xlsx'
dest_loc = '/home/ysyncby/courses/RA/Data/data/'

dp = Data_Preparation(spec_loc, project_30)
dp2 = Data_Preparation(spec_loc, project_IV)
dp3 = Data_Preparation(spec_loc, project_VI)
sample_s, sample_nir, _ = dp.read_xdata()
sample_s2, sample_nir2, _ = dp2.read_xdata()
sample_s3, sample_nir3, _ = dp3.read_xdata()

sample_s = sample_s + sample_s2 + sample_s3
sample_nir = sample_nir + sample_nir2 + sample_nir3

name = 'All_flame_S_data.csv'
dp.lists2csv(name, dest_loc, sample_s)

name = 'ALL_flame_NIR_data.csv'
dp.lists2csv(name, dest_loc, sample_nir)


label = dp.read_spec_label()

name = 'ALL_flame_S_label.csv'
dp.lists2csv(name, dest_loc, [label['flame-S'][275:1815]])

name = 'ALL_flame_NIR_label.csv'
dp.lists2csv(name, dest_loc, [label['flame-NIR']])


