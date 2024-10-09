from enum import StrEnum
from typing import BinaryIO

# import librosa
# from librosa.feature import mfcc
from torch import Tensor
from torchaudio import load
from torchaudio.functional import resample
from torchaudio.transforms import MFCC
from onnxruntime import InferenceSession


class AudioResult(StrEnum):
    real = 'real'
    fake = 'fake'


async def determine_audio_auth(audio_file: BinaryIO) -> AudioResult:
    sample_rate: int = 1024 * 6
    sample, sr = load(audio_file, normalize=True)
    resampled = resample(sample, sr, sample_rate)

    transform = MFCC(sample_rate=sample_rate, n_mfcc=40)
    mfcc_1 = transform(resampled[0].unsqueeze(0)).numpy()
    mfcc_2 = transform(resampled[1].unsqueeze(0)).numpy()
    onnx_session = InferenceSession('./res/model.onnx')

    try:
        output_1 = onnx_session.run(['sigmoid_1'], {'l_x_': [mfcc_1]})
        output_2 = onnx_session.run(['sigmoid_1'], {'l_x_': [mfcc_2]})
    except Exception as e:
        print(e)
        return AudioResult.fake

    sigmoid_val_avg: float = (output_1[0] + output_2[0]) / 2.0

    if sigmoid_val_avg > 0.5:
        return AudioResult.fake

    return AudioResult.real
