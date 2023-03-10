
import torch as th
import torch.nn as nn
from gym import spaces
from torchvision.models import alexnet
from stable_baselines3.common.torch_layers import BaseFeaturesExtractor

class MyAlexNet(BaseFeaturesExtractor):
    """
    Neural network model consisting of layers propsed by AlexNet paper.
    """
    def __init__(self, 
    observation_space: spaces.Box, 
    features_dim: int = 256):
        """
        Define and allocate layers for this neural net.
        Args:
            num_classes (int): number of classes to predict with this model
        """

        super().__init__(observation_space, features_dim)
        # input size should be : (b x 3 x 227 x 227)
        # The image in the original paper states that width and height are 224 pixels, but
        # the dimensions after first convolution layer do not lead to 55 x 55.
        
        n_input_channels = 1
        self.net = alexnet(pretrained= True)
        self.net.features[0] = nn.Conv2d(in_channels=n_input_channels, out_channels=64, kernel_size=11, stride=4)  # (b x 96 x 55 x 55)

        self.net.classifier[6] = nn.Linear(in_features=4096, out_features=features_dim)
        self.net.classifier[5] = nn.Tanh()
        self.net.classifier[2] = nn.Tanh()
        self.float()
        

    def forward(self, observations: th.Tensor) -> th.Tensor:
        return self.net(observations).float()

policy_kwargs = dict(
    features_extractor_class=MyAlexNet,
    features_extractor_kwargs=dict(features_dim=128),
)
