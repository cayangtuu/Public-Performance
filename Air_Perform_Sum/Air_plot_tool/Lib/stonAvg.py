import pandas as pd

def stonAvg(data, stons):
    hr_ = {ston: 0 for ston in stons}
    data_ = {ston: 0 for ston in stons}
    sumhr_ = 0
    sumdata_ = 0
    for ston in stons:
        for i in range(0, len(data)):
            if (float(data[ston][i]) != -999):
                hr_[ston] += 1  # 各個測站總共模擬的小時
                sumhr_ += 1     # 所有測站總共模擬的小時

                data_[ston] += data[ston][i]
                sumdata_ += data[ston][i]                

        if hr_[ston] != 0:
            data_[ston] /= hr_[ston]
        else:
            data_[ston] = -999

    if sumhr_ != 0:
        sumdata_ /= sumhr_
    else:
        sumdata_ = -999
       

    return { 'each_stn' : data_ ,
             'sum_stn'  : sumdata_  }
