# -*- coding: utf-8 -*-
import xlrd
import numpy as np
import matplotlib.pyplot as plt

class Data_Preparation:

    def read_pro30(self, loc):
        self.exlFile = xlrd.open_workbook(loc)
        # print(self.exlFile.sheet_names(),'p30')
        res_sheet = self.exlFile.sheet_by_name('Nematode Results')
        res = res_sheet.col_values(17)[11:]
        return res, len(res)

    def read_pro6(self, loc):
        self.exlFile = xlrd.open_workbook(loc)
        # print(self.exlFile.sheet_names(), 'p6')
        res_sheet = self.exlFile.sheet_by_name('Nematode Results')
        res = res_sheet.col_values(9)[7:]
        return res, len(res)

    def read_pro4(self, loc):
        self.exlFile = xlrd.open_workbook(loc)
        # print(self.exlFile.sheet_names(), 'p4')
        res_sheet = self.exlFile.sheet_by_name('Nemethod Results PRJ IV')
        res = res_sheet.col_values(10)[7:]
        return res, len(res)

class Hist:
    def hist_maker(self, interval, nem_res, project_name):
        data = nem_res
        freq = []
        upper_boundary = int(interval*(max(data)//interval+2))
        print(upper_boundary)
        used = []
        x_axis = list(range(0,upper_boundary,interval))
        for index, x in enumerate(x_axis):
            freq.append(0)
            for ind, nres in enumerate(data):
                if nres <= x and ind not in used:
                    freq[index] += 1
                    used.append(ind)

        print(x_axis)

        if len(x_axis) > 20:
            for index in range(len(x_axis)):
                if x_axis[index] % (5*interval) != 0:
                    x_axis[index] = ''
        print(x_axis)
        plt.figure()
        plt.xlabel("rln/g root")
        plt.ylabel("Freqency")
        plt.grid()
        plt.title("Histogram of Nematode Distribution of " + project_name)
        x = np.arange(len(freq))
        plt.bar(x, freq)
        plt.xticks(x, x_axis)
        plt.show()


loc_p30 = '/home/ysyncby/PycharmProjects/RA_Spectral_Data_Analysis/data/Labels - Proj 30- Walnut _08 20 2018.xlsx'
loc_p6 = '/home/ysyncby/PycharmProjects/RA_Spectral_Data_Analysis/data/Labels Project VI- August 2018.xlsx'
loc_p4 = '/home/ysyncby/PycharmProjects/RA_Spectral_Data_Analysis/data/Labels Project IV- August 2018.xlsx'

dp = Data_Preparation()
nem_res_p30, len_p30 = dp.read_pro30(loc_p30) # max: 2516.0
nem_res_p6, len_p6 = dp.read_pro6(loc_p6)     # max: 260.8
nem_res_p4, len_p4 = dp.read_pro4(loc_p4)     # max: 998.25

# to generate figure in a proper width,
# 2516 has been replaced by 877 !!!!!
# this list can only be used to draw histogram!!!
nem_res_p30[20] = 877

# print('max:', max(nem_res_p30), nem_res_p30)
# print('max:', max(nem_res_p6), nem_res_p6)
# print('max:', max(nem_res_p4), nem_res_p4)
# print(max(max(nem_res_p30),max(nem_res_p6),max(nem_res_p4)))

hist = Hist()
# hist.hist_maker(10,nem_res_p30,'Project 30')
# hist.hist_maker(10,nem_res_p6,'Project VI')
# hist.hist_maker(10,nem_res_p4,'Project IV')

nem_res_total = nem_res_p30 + nem_res_p6 + nem_res_p4
hist.hist_maker(10,nem_res_total,' All Project')