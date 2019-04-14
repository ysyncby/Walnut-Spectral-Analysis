# -*- coding: utf-8 -*-
import xlrd
import numpy as np
import matplotlib.pyplot as plt

from statistics import mean
from sklearn import linear_model
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import cross_val_score

class Data_Preparation:

    def __init__(self, spec_loc, xdata_folder, ydata_loc):
        self.spec_loc = spec_loc
        self.xdata_folder = xdata_folder
        self.ydata_loc = ydata_loc


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

    def read_xdata(self, samples_num):
        res = []
        for index in range(samples_num):
            file_name = str(index+1)+'.txt'
            tmp = self.txt2list(self.xdata_folder+file_name)
            res.append(tmp)

        return res

    def read_ydata(self):
        self.exlFile = xlrd.open_workbook(self.ydata_loc)
        res_sheet = self.exlFile.sheet_by_name('Label')
        res = res_sheet.col_values(2)[1:]
        return res


    def read_data_full(self):
        ydata = self.read_ydata()
        samples_num = len(ydata)
        xdata = self.read_xdata(samples_num)

        return np.asarray(xdata), np.asarray(ydata)

    def read_data_selection(self):
        xdata, ydata = self.read_data_full()
        xdata = xdata.T

        return xdata, ydata

class Selection:

    def __init__(self, xdata, ydata):
        self.xdata = xdata
        self.ydata = ydata

    def linear_calculation(self, model):
        res = []
        for index in range(len(self.xdata)):
            x = self.xdata[index].reshape(-1,1)
            y = self.ydata

            scaler = MinMaxScaler()
            scaler.fit(x)
            x = scaler.transform(x)
            score = cross_val_score(model, x, y, cv=10)
            res.append(mean(score))

        return res
    def selection(self, label = 0):

        linear = linear_model.LinearRegression()
        lasso = linear_model.Lasso()
        ridge = linear_model.Ridge()
        models = [linear, lasso, ridge]
        model_names = ['linear_regression', 'lasso_regression', 'ridge_regression']
        plt.figure()
        for index in range(len(models)):
            y = self.linear_calculation(models[index])
            plt.subplot(131 + index)
            plt.xlabel("Wavelength (nm)")
            plt.ylabel("Cross Validation Score")
            plt.grid()
            plt.title(model_names[index])
            if label:
                plt.plot(label, y)
            else:
                plt.plot(range(len(y)), y)
        plt.show()

    def lassoCV(self, x_label=0):

        x = self.xdata
        scaler = MinMaxScaler()
        scaler.fit(x)
        x = scaler.transform(x)
        y = self.ydata
        als = [0.3, 0.6, 0.9]
        plt.figure()
        for index in range(len(als)):
            lasso = linear_model.Lasso(alpha=als[index])
            lasso.fit(x, y)

            plt.subplot(131 + index)
            plt.xlabel("Wavelength (nm)")
            plt.ylabel("lasso Score")

            plt.grid()
            plt.title("lasso selection alpha = " + str(als[index]))

            if x_label:
                plt.plot((x_label), lasso.coef_)
            else:
                plt.plot(range(len(lasso.coef_)), lasso.coef_)
        plt.show()


spec_loc = '/home/ysyncby/PycharmProjects/RA_Spectral_Data_Analysis/data/kobin_spectra_wavelengths.xlsx'
flame_NIR = '/home/ysyncby/PycharmProjects/RA_Spectral_Data_Analysis/data/Flame-NIR Spectra/'
flame_S = '/home/ysyncby/PycharmProjects/RA_Spectral_Data_Analysis/data/Flame-S Spectra/'
warm_res = '/home/ysyncby/PycharmProjects/RA_Spectral_Data_Analysis/data/Labels - Proj 30- Walnut _08 20 2018.xlsx'

# # step 0: label preparation
# dp = Data_Preparation(spec_loc, 0, 0)
# spec_label = dp.read_spec_label()
#
# # step 1: Flame-NIR with Linear
# dp1 = Data_Preparation(0, flame_NIR, warm_res)
# x_data1, y_data1 = dp1.read_data_selection()
# sel = Selection(x_data1, y_data1)
# sel.selection(spec_label['flame-NIR'])
#
# # step 2: Flame-S with Linear
# dp2 = Data_Preparation(0, flame_S, warm_res)
# x_data2, y_data2 = dp2.read_data_selection()
# sel = Selection(x_data2, y_data2)
# sel.selection(spec_label['flame-S'])
#
# # step 3: Flame-NIR with Lasso
# dp3 = Data_Preparation(0, flame_NIR, warm_res)
# x_data3, y_data3 = dp3.read_data_full()
# sel = Selection(x_data3, y_data3)
# sel.selection(spec_label['flame-NIR'])
#
# # step 4: Flame-S with Lasso
# dp4 = Data_Preparation(0, flame_S, warm_res)
# x_data4, y_data4 = dp4.read_data_full()
# sel = Selection(x_data4, y_data4)
# sel.selection(spec_label['flame-S'])











#
#
# dp = Data_Preparation(spec_loc, x, y)
# res = dp.read_spec_label()
#
# # xdata, ydata = dp.read_data_full()
# xdata, ydata = dp.read_data_selection()
# print('xxxxxx',len(xdata))
# sel = Selection(xdata,ydata)
# # sel.selection()
# sel.selection(res['flam-S'])
# # sel.lassoCV(res['flam-S'])
