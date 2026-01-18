import torch
from torch.nn import BCELoss
from torch.optim import Adam
from torch.utils.data import DataLoader, random_split
from tqdm import tqdm

from audio_spoof_detection_service.infrastructure.neural_model_gateways.torch.cnn.model import TorchCnnModel
from audio_spoof_detection_service.infrastructure.neural_model_gateways.torch.cnn.dataset import AudioDataset


def model_train(model: TorchCnnModel, audio_dataset: AudioDataset,
                device: torch.device, n_epochs: int = 15,
                batch_size: int = 128, train_size: float = 0.7) -> None:
    train_loss = 0
    loss_fn = BCELoss()
    optimizer = Adam(model.parameters(), lr=0.0001)

    train_size = int(train_size * len(audio_dataset))
    test_size = len(audio_dataset) - train_size

    train_dataset, test_dataset = random_split(audio_dataset, (train_size, test_size))
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=4, pin_memory=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=True, num_workers=4, pin_memory=True)
    first: bool = True

    for epoch in range(1, n_epochs + 1):
        model.train()

        with tqdm(train_loader, mininterval=0) as bar:
            bar.set_description(f'Epoch {epoch}')

            for data, target in bar:
                if first:
                    print(data.shape)
                    first = False
                data, target = data.to(device), target.to(device)
                output = model(data)
                loss = loss_fn(output, target)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                train_loss += loss.item()

                loss, acc = __test(model, test_loader, loss_fn, device)
                bar.set_postfix(loss=float(loss), acc=float(acc))


def __test(model: TorchCnnModel, test_loader: DataLoader, loss_fn: BCELoss, device: torch.device) -> tuple[float, float]:
    model.eval()
    test_loss = 0
    correct = 0

    with torch.no_grad():
        batch_count = 0
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            batch_count += 1
            output = model(data)
            test_loss += loss_fn(output, target).item()
            predicted = torch.round(output).int()
            target = target.int()
            correct += torch.sum(target == predicted).item()

    avg_loss = test_loss / batch_count
    avg_acc = correct / len(test_loader.dataset)

    return avg_loss, avg_acc
