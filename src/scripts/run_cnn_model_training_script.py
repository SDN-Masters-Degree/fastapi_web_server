from argparse import ArgumentParser
from pathlib import Path

import torch

from audio_spoof_detection_service.infrastructure.neural_model_gateways.torch.cnn.model import TorchCnnModel
from audio_spoof_detection_service.infrastructure.neural_model_gateways.torch.cnn.train import model_train
from audio_spoof_detection_service.infrastructure.neural_model_gateways.torch.cnn.dataset import AudioDataset


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument('--real-path', type=str)
    parser.add_argument('--fake-path', type=str)
    parser.add_argument('--output', type=str)

    args = parser.parse_args()

    real_audio_path: Path = Path(args.real_path)
    fake_audio_path: Path = Path(args.fake_path)
    output_path: Path = Path(args.output)

    extension_name: str = output_path.suffix

    if extension_name not in ('.pt', '.pth', '.onnx'):
        print(f'{extension_name} is not supported model extension')
        return

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    print(f'Using {device} for model training')
    print('Loading and extracting features from dataset...')

    dataset = AudioDataset(real_audio_path, fake_audio_path, device)
    input_tensor = dataset[0][0]
    print("dataset length:", len(dataset))
    print("model input shape:", input_tensor.shape)

    model = TorchCnnModel(input_tensor).to(device)

    print('Model training...')

    model_train(model, dataset, device, n_epochs=2)
    model.eval()

    if extension_name in ('.pt', '.pth'):
        print(model.state_dict())
        torch.save(model.state_dict(), output_path)
    else:
        input_plug = torch.rand((1, *dataset[0][0].size()), dtype=torch.float32).to(device)
        onnx_program = torch.onnx.dynamo_export(model, input_plug)
        onnx_program.save(str(output_path))

    print(f'Model saved in {output_path}')


if __name__ == '__main__':
    main()
