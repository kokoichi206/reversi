import torch
import model

def main():
    m = torch.load('model')

    for param in m.parameters():
        # 型を調べるとCPUかGPUかわかる。
        # CPU: torch.FloatTensor
        # GPU: torch.cuda.FloatTensor
        print(type(param.data))

if __name__ == '__main__':
    main()