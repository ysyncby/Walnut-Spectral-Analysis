# -*- coding: utf-8 -*-
import xlrd
import os
import numpy as np
import statistics as st
# import matplotlib.pyplot as plt
import matplotlib.pyplot as plt


class Data_Preparation:

    def __init__(self, spec_loc, project_folder):
        self.spec_loc = spec_loc
        self.project_folder = project_folder
        self.ydata_loc = os.path.join(self.project_folder, 'labels.xlsx')
    def txt2list(self, file):
        l = []
        with open(file, 'r') as f:
            for index, line in enumerate(f):
                if index > 6:
                    l.append(float(line.strip()))
        return l

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
            tmp = self.txt2list(os.path.join(samples_s_loc, file_name))
            sample_s.append(tmp)
        for index in range(samples_num):
            file_name = str(index+1)+'.txt'
            tmp = self.txt2list(os.path.join(samples_nir_loc, file_name))
            sample_nir.append(tmp)

        return sample_s, sample_nir, samples_num

    def draw(self, x, Ys, project_name):

        plt.title(project_name)
        for y in Ys:
            plt.plot(x, y)

        plt.legend()

        plt.xlabel('wavelength')
        plt.ylabel('Spectral Intensity')
        plt.show()

    def get_raw(self, bound1 = 300, bound2 = 935):
        spec_label = self.read_spec_label()
        ind_flame_s = {}
        ind_flame_nir = {}
        for index, label in enumerate(spec_label['flame-S']):
            if bound1 <= label <= bound2:
                    if label not in ind_flame_s:
                        ind_flame_s[label] = index
        for index, label in enumerate(spec_label['flame-NIR']):
                if label not in ind_flame_nir:
                    ind_flame_nir[label] = index

        sample_s, sample_nir, samples_num = self.read_xdata()

        samples_spec = []
        for index in range(samples_num):
            wavelength_s = list(ind_flame_s.keys())
            sample_strength_s = []
            for wave in wavelength_s:
                sample_strength_s.append(sample_s[index][ind_flame_s[wave]])

            wavelength_nir = list(ind_flame_nir.keys())
            sample_strength_nir = []
            for wave in wavelength_nir:
                sample_strength_nir.append(sample_nir[index][ind_flame_nir[wave]])

            sample_spec = sample_strength_s+sample_strength_nir
            samples_spec.append(sample_spec)

        return samples_spec, wavelength_s+wavelength_nir

    def get_down_scaling(self, delta = 5, bound1 = 300, bound2 = 935):
        spec_label = self.read_spec_label()
        ind_flame_s = {}
        spec_flame_s = {}
        ind_flame_nir = {}
        spec_flame_nir = {}

        assert delta != 0

        for mid in range(bound1, 1660+delta, delta):
            for index, label in enumerate(spec_label['flame-S']):
                if bound1 <= label <= bound2:
                    if mid-(delta/2) < label <= mid+(delta/2):
                        if mid not in ind_flame_s:
                            ind_flame_s[mid] = [index]
                            spec_flame_s[mid] = [label]
                        else:
                            ind_flame_s[mid].append(index)
                            spec_flame_s[mid].append(label)
            for index, label in enumerate(spec_label['flame-NIR']):
                if mid-(delta/2) < label <= mid+(delta/2):
                    if mid not in ind_flame_nir:
                        ind_flame_nir[mid] = [index]
                        spec_flame_nir[mid] = [label]
                    else:
                        ind_flame_nir[mid].append(index)
                        spec_flame_nir[mid].append(label)

        sample_s, sample_nir, samples_num = self.read_xdata()

        samples_spec = []
        for index in range(samples_num):
            wavelength_s = list(ind_flame_s.keys())
            sample_strength_s = []
            for wave in wavelength_s:
                down_wave = []
                for ind in ind_flame_s[wave]:
                    down_wave.append(sample_s[index][ind])
                sample_strength_s.append(st.mean(down_wave))

            wavelength_nir = list(ind_flame_nir.keys())
            sample_strength_nir = []
            for wave in wavelength_nir:
                down_wave = []
                for ind in ind_flame_nir[wave]:
                    down_wave.append(sample_nir[index][ind])
                sample_strength_nir.append(st.mean(down_wave))

            sample_spec = sample_strength_s+sample_strength_nir
            samples_spec.append(sample_spec)

        return samples_spec, wavelength_s+wavelength_nir

    # def SNV_sample(self, samples_spec):
    #     samples_spec_snv = []
    #     for sample in samples_spec:
    #         aver = st.mean(sample)
    #         std = st.stdev(sample)
    #         datas = []
    #         for data in sample:
    #             datas.append((data-aver)/std)
    #         samples_spec_snv.append(datas)
    #     return samples_spec_snv

    def SNV_sample_group(self, samples_spec, aver, std):
        samples_spec_snv = []
        for sample in samples_spec:
            datas = []
            for data in sample:
                datas.append((data-aver)/std)
            samples_spec_snv.append(datas)
        return samples_spec_snv

    def read_ydata(self):
        exlFile = xlrd.open_workbook(self.ydata_loc)
        res_sheet = exlFile.sheet_by_name('nematode_res')
        res = res_sheet.col_values(0)
        return res

    def classify_groups(self, bound1 = 5, bound2 = 15, bound3 = 100):
        # low: 0-5
        # mid: 5-15
        # high: 15-100
        # very_high: >100
        nematode_res = self.read_ydata()
        res_dict = {'low':[], 'mid':[], 'high':[], 'very_high':[]}
        for ind, nema in enumerate(nematode_res):
            if nema <= bound1:
                res_dict['low'].append(ind)
            elif nema <= bound2:
                res_dict['mid'].append(ind)
            elif nema <= bound3:
                res_dict['high'].append(ind)
            else:
                res_dict['very_high'].append(ind)

        return res_dict

    def classify_sample(self, bound1 = 5, bound2 = 15, bound3 = 100):

        samples_spec, wavelength = self.get_down_scaling()

        exlFile = xlrd.open_workbook(self.ydata_loc)
        res_sheet = exlFile.sheet_by_name('Label')
        res = res_sheet.col_values(1)[1:]

        assert len(res) == len(samples_spec)
        classes = {'control':[], 'low':[], 'mid':[], 'high':[], 'very_high':[]}

        for ind, nema in enumerate(res):
            if nema == 0:
                classes['control'].append(samples_spec[ind])
            elif nema <= bound1:
                classes['low'].append(samples_spec[ind])
            elif nema <= bound2:
                classes['mid'].append(samples_spec[ind])
            elif nema <= bound3:
                classes['high'].append(samples_spec[ind])
            else:
                classes['very_high'].append(samples_spec[ind])

        sam_all = []
        for sam in samples_spec:
            sam_all += sam
        aver = st.mean(sam_all)
        std = st.stdev(sam_all)

        for clas in classes.keys():
            snv_spec = self.SNV_sample_group(classes[clas], aver, std)
            classes[clas] = snv_spec
        return classes, wavelength

    def draw_raw_classes(self, classes, wavelength, project_name):
        # low: black
        # mid: blue
        # high: yellow
        # very_high: red

         # = self.classify_sample()
        pattern = {'control': 'yellow', 'low': 'green', 'mid': 'black', 'high': 'blue', 'very_high': 'red'}

        plt.title(project_name)
        for key in pattern.keys():
            for i, sam in enumerate(classes[key]):
                if i == 0:
                    plt.plot(wavelength, sam, color=pattern[key], label=key + ':' + str(len(classes[key])))
                else:
                    plt.plot(wavelength, sam, color=pattern[key])

        plt.legend()

        plt.xlabel('wavelength')
        plt.ylabel('Spectral Intensity')
        plt.show()

    def draw_aver_classes(self, classes, wavelength, project_name):
        # low: black
        # mid: blue
        # high: yellow
        # very_high: red

        # classes, wavelength = self.classify_sample()
        print(len(classes['low']))
        print(len(classes['mid']))
        print(len(classes['high']))
        print(len(classes['very_high']))
        aver_classes = {'low':[0]*len(classes['mid'][0]),
                        'mid':[0]*len(classes['mid'][0]),
                        'high':[0]*len(classes['mid'][0]),
                        'very_high':[0]*len(classes['mid'][0])}

        for key in classes.keys():
            samples = classes[key]
            for sam in samples:
                tmp = aver_classes[key]
                aver_classes[key] = [x + y for x, y in zip(tmp, sam)]

            aver_classes[key] = [x / len(classes[key]) for x in aver_classes[key]]

        pattern = {'low': 'green', 'mid': 'black', 'high': 'blue', 'very_high': 'red'}

        plt.title(project_name)
        for key in pattern.keys():
            plt.plot(wavelength, aver_classes[key], color=pattern[key], label=key)

        plt.legend()

        plt.xlabel('wavelength')
        plt.ylabel('Spectral Intensity')
        plt.show()





project_30 = '/home/ysyncby/courses/RA/Data/data/Walnut_Project_30'
project_IV = '/home/ysyncby/courses/RA/Data/data/Walnut_Project_IV'
project_VI = '/home/ysyncby/courses/RA/Data/data/Walnut_Project_VI'
spec_loc = '/home/ysyncby/courses/RA/Data/data/kobin_spectra_wavelengths.xlsx'


# # step 1: get raw
# dp = Data_Preparation(spec_loc, project_VI)
# samples_spec, wavelength = dp.get_raw()
# dp.draw(wavelength, samples_spec, 'Walnut_Project_VI')

# step 2: get down scaling
# dp = Data_Preparation(spec_loc, project_VI)
# samples_spec, wavelength = dp.get_down_scaling()
# dp.draw(wavelength, samples_spec, 'Walnut_Project_VI')

# step 3: SNV
# dp = Data_Preparation(spec_loc, project_VI)
# samples_spec, wavelength = dp.get_down_scaling()
# snv_spec = dp.SNV_sample(samples_spec)
# dp.draw(wavelength, snv_spec, 'Walnut_Project_VI')

# step 4: grouped SNV
dp = Data_Preparation(spec_loc, project_VI)
samples_spec, wavelength = dp.classify_sample()
dp.draw_raw_classes(samples_spec, wavelength, 'Walnut_Project_VI')






# step 10: count groups
# print(dp.classify_groups())

# dp1 = Data_Preparation(spec_loc, project_30)
# classes1, _ = dp1.classify_sample()
# dp2 = Data_Preparation(spec_loc, project_VI)
# classes2, _ = dp2.classify_sample()
# dp3 = Data_Preparation(spec_loc, project_IV)
# classes3, wavelength = dp3.classify_sample()
#
# classes_all = {'low':[], 'mid':[], 'high':[], 'very_high':[]}
# classes_all['low'] = classes1['low'] + classes2['low'] + classes3['low']
# classes_all['mid'] = classes1['mid'] + classes2['mid'] + classes3['mid']
# classes_all['high'] = classes1['high'] + classes2['high'] + classes3['high']
# classes_all['very_high'] = classes1['very_high'] + classes2['very_high'] + classes3['very_high']
#
# dp1.draw_raw_classes(classes_all, wavelength, 'Walnut_Project_all')
# dp1.draw_aver_classes(classes_all, wavelength, 'Walnut_Project_all')

# class_res1 = dp1.classify_groups()
# print('low:',len(class_res1['low']), class_res1['low'])
# print('mid:',len(class_res1['mid']))
# print('high:',len(class_res1['high']))
# print('very_high:',len(class_res1['very_high']), class_res1['very_high'])