from enum import StrEnum
from typing import BinaryIO

from torch import mean
from torchaudio import load
from torchaudio.functional import resample
from torchaudio.transforms import MFCC
from onnxruntime import InferenceSession

from app.src.exception import (AudioDurationException,
                               ModelPredictionException)


class AudioResult(StrEnum):
    real = 'real'
    fake = 'fake'


async def determine_audio_auth(audio_file: BinaryIO) -> AudioResult:
    sample_rate: int = 1024 * 6
    two_secs: int = 2
    sample, sr = load(audio_file, normalize=True, channels_first=True)
    max_audio_duration: int = sr * two_secs

    if len(sample[0]) < max_audio_duration:
        raise AudioDurationException('Audio duration is less than two seconds')

    sample = sample[:, 0:sr * two_secs]
    sample = mean(sample, dim=0, keepdim=True)

    resampled = resample(sample, sr, sample_rate)

    transform = MFCC(sample_rate=sample_rate, n_mfcc=40)
    mfcc = transform(resampled.unsqueeze(0)).numpy()

    onnx_session = InferenceSession('./res/test.onnx')

    try:
        output = onnx_session.run(['sigmoid_1'], {'l_x_': mfcc})
    except Exception as e:
        raise ModelPredictionException('internal model prediction error')

    sigmoid_val: float = float(output[0])

    if sigmoid_val > 0.5:
        return AudioResult.fake

    return AudioResult.real
