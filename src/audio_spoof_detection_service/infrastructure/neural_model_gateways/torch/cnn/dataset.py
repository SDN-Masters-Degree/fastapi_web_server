import multiprocessing
from pathlib import Path

import torch
from torchaudio import load
from torchaudio.transforms import MFCC
from torchaudio.functional import resample
from torch.utils.data import Dataset


def _resample_audios(audiofile) -> torch.Tensor:
    sample, sr = load(audiofile, normalize=True, channels_first=True)
    sample = torch.mean(sample, dim=0).unsqueeze(0) # stereo to mono
    resampled = resample(sample, sr, AudioDataset.sample_rate)
    return resampled


class AudioDataset(Dataset):
    sample_rate: int = 1024 * 6

    def __init__(self, real_path: Path, fake_path: Path, device: torch.device):
        self.device = device
        self.transform = MFCC(sample_rate=AudioDataset.sample_rate, n_mfcc=40)

        real_x = AudioDataset.__get_audios(real_path)
        real_y = torch.zeros(len(real_x))

        fake_x = AudioDataset.__get_audios(fake_path)
        fake_y = torch.ones(len(fake_x))

        preprocessed_x = torch.stack([self.transform(x) for x in real_x + fake_x])
        y = torch.cat((real_y, fake_y)).unsqueeze(1)

        self.data = preprocessed_x
        self.labels = y

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index: int) -> tuple[torch.Tensor, torch.Tensor]:
        x = self.data[index]
        y = self.labels[index]
        return x, y

    @staticmethod
    def __get_audios(audio_folder_path: Path) -> list[torch.Tensor]:
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            audios: list[torch.Tensor] = pool.map(_resample_audios, list(audio_folder_path.rglob('*.wav')))
        return audios
