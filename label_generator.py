# -*- coding: utf-8 -*-
import xlrd
import xlwt
import argparse

def parse_args():
    """Parse in command line arguments"""
    parser = argparse.ArgumentParser(description='Label Generator')

    parser.add_argument(
        '-data_loc', '--data_loc',
        help='the root directory saving the labels data excel file', type=str, required=True)
    parser.add_argument(
        '-out_dir', '--out_dir',
        help='the path of folder', type=str, required=True)
    parser.add_argument(
        '-out_file_name', '--out_file_name',
        help='the label file name', default='label_test.xls')

    args = parser.parse_args()

    return args

class CreateLables:
    def __init__(self, data_location):
        self.data_loc = data_location
        self.exlFile = xlrd.open_workbook(self.data_loc)

    def getSheetName(self):
        return self.exlFile.sheet_names()
        # a list: ['Label', 'Nematode Results', 'Plot Map', 'Spectral Sample Numbers']

    def getRlngRoot(self):
        res_sheet = self.exlFile.sheet_by_name('Nematode Results')
        block = res_sheet.col_values(0)[11:]
        main_plot = res_sheet.col_values(1)[11:]
        cultivar = res_sheet.col_values(2)[11:]
        rlng_root = res_sheet.col_values(17)[11:]

        assert len(block)==len(main_plot)==len(cultivar)==len(rlng_root)
        res_dict = {}

        for index in range(len(block)):
            key = block[index] + '/' + \
                  main_plot[index] + '/' + \
                  str(int(cultivar[index]))
            res_dict[key] = rlng_root[index]

        return res_dict

    def getMap(self):
        map_sheet = self.exlFile.sheet_by_name('Plot Map')

        res_dict = {}

        sample_line_N_interval = [[9,7],[4,8]]
        for line, inter in sample_line_N_interval:
            samples = map_sheet.row_values(line)

            block = map_sheet.row_values(line+inter)
            main_plot = map_sheet.row_values(line+inter+1)
            cultivar = map_sheet.row_values(line+inter+2)

            for index, sample in enumerate(samples):
                res_dict[str(int(sample))] = block[index] + '/' + \
                                             main_plot[index] + '/' + \
                                             str(int(cultivar[index]))
                res_dict[str(int(sample+1))] = block[index] + '/' + \
                                               main_plot[index] + '/' + \
                                               str(int(cultivar[index]))

        return res_dict

    def getCorresponds(self):
        map_dict = self.getMap()
        rln_dict = self.getRlngRoot()

        results_list = []

        # assert len(map_dict)==len(rln_dict)

        sample_num = len(map_dict)
        for index in range(sample_num):
            sam = index+1
            result_loc = map_dict[str(sam)]
            result = rln_dict[result_loc]
            for loop in range(8):
                results_list.append(result)

        return results_list

    def writeLables(self, out_folder, out_name):
        correspondLabels = self.getCorresponds()
        filename = xlwt.Workbook()

        sheet = filename.add_sheet("test")
        for index, content in enumerate(correspondLabels):
            sheet.write(index, 0, index+1)
            sheet.write(index, 1, content)

        filename.save(out_folder+'/'+out_name)

if __name__ == "__main__":
    args = parse_args()
    data_loc = args.data_loc
    out_dir = args.out_dir
    out_file_name = args.out_file_name


    cl = CreateLables(data_loc)
    cl.writeLables()
