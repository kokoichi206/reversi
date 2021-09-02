import torch
import model

def main():
    # モデルの作成
    m = model.DummyModel()

    # GPUに転送
    m = m.cuda()

    # 保存
    torch.save(m, 'model')


if __name__ == '__main__':
    main()