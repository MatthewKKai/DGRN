import torch
from torch import nn
from Config import get_opt
from models.DGRN import DGRN_Encoder, DGRN_Decoder, Gated_Unit
import tqdm

def train(opt):
    pass



if __name__ == "__main__":
    opt = get_opt()
    train(opt)