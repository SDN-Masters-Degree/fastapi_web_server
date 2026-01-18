from torch import Tensor
from torch import nn


class TorchCnnModel(nn.Module):
    def __init__(self, input_tensor: Tensor):
        super().__init__()

        in_channels: int = input_tensor.shape[0]
        out_channels: int = in_channels * 32

        self.conv1 = nn.Conv2d(in_channels, out_channels, (3, 3))
        self.max_pool1 = nn.MaxPool2d((2, 2))

        x = self.conv1(input_tensor)
        x = self.max_pool1(x)

        self.conv2 = nn.Conv2d(out_channels, out_channels * 2, (3, 3))
        self.max_pool2 = nn.MaxPool2d((2, 2))
        self.flatten = nn.Flatten()

        x = self.conv2(x)
        x = self.max_pool2(x)
        x = self.flatten(x)
        lin_input_shape = x.shape
        in_features: int = lin_input_shape[0] * lin_input_shape[1]

        self.linear1 = nn.Linear(in_features, 256)
        self.dropout1 = nn.Dropout(0.5)
        self.linear2 = nn.Linear(256, 128)
        self.dropout2 = nn.Dropout(0.5)
        self.linear3 = nn.Linear(128, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.conv1(x)
        x = nn.functional.relu(x)
        x = self.max_pool1(x)

        x = self.conv2(x)
        x = nn.functional.relu(x)
        x = self.max_pool2(x)

        x = self.flatten(x)
        x = self.linear1(x)
        x = nn.functional.relu(x)

        x = self.dropout1(x)
        x = self.linear2(x)
        x = nn.functional.relu(x)

        x = self.dropout2(x)
        x = self.linear3(x)

        y = self.sigmoid(x)

        return y
