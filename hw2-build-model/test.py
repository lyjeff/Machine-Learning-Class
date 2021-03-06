import torch
from pathlib import Path
import pandas as pd
from dataset import MLDataset
from models import MyModel
from sklearn.preprocessing import MinMaxScaler

def test():
    # load model and use weights we saved before.
    model = MyModel()
    model.load_state_dict(torch.load('mymodel.pth', map_location='cpu'))
    model.eval()
    # load testing data
    data = pd.read_csv('test.csv', encoding='utf-8')
    label_col = [
        'Input_A6_024' ,'Input_A3_016', 'Input_C_013', 'Input_A2_016', 'Input_A3_017',
        'Input_C_050', 'Input_A6_001', 'Input_C_096', 'Input_A3_018', 'Input_A6_019',
        'Input_A1_020', 'Input_A6_011', 'Input_A3_015', 'Input_C_046', 'Input_C_049',
        'Input_A2_024', 'Input_C_058', 'Input_C_057', 'Input_A3_013', 'Input_A2_017'
    ]

    # ================================================================ #
    # if do some operations with training data,
    # do the same operations to the testing data in this block

    # fill NAN with the median values
    data = data.fillna(value=data.median(axis=0, skipna=True))

    # normalize with MinMaxScaler in range [0, 1]
    scaler = MinMaxScaler(feature_range=(0, 1), copy=True).fit(data)
    data = pd.DataFrame(data=scaler.transform(data), columns=data.columns)

    # ================================================================ #
    # convert dataframe to tensor, no need to rewrite
    inputs = data.values
    inputs = torch.tensor(inputs)
    # predict and save the result
    result = pd.DataFrame(columns=label_col)
    outputs = model(inputs.float())
    for i in range(len(outputs)):
        tmp = outputs[i].detach().numpy()
        tmp = pd.DataFrame([tmp], columns=label_col)
        result= pd.concat([result, tmp], ignore_index=True)
    result.to_csv('result.csv', index=False)

if __name__ == '__main__':
    test()
