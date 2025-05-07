from torch import mean
from torchaudio import load
from torchaudio.functional import resample
from torchaudio.transforms import MFCC
from onnxruntime import InferenceSession

from audio_spoof_detection_service.application.protocols.neural_model_gateways.cnn import CnnNeuralModelGateway
from audio_spoof_detection_service.domain.entities.audio import AudioEntity
from audio_spoof_detection_service.domain.error import NeuralModelError
from audio_spoof_detection_service.infrastructure.settings import Settings


class OnnxCnnNeuralModelGateway(CnnNeuralModelGateway):
    def __init__(self, session: InferenceSession, settings: Settings):
        self.session = session
        self.settings = settings

    async def predict(self, audio: AudioEntity) -> float:
        sample_rate: int = self.settings.target_sample_rate
        audio_dur_sec = int(self.settings.audio_min_duration_milli / 1000)
        sample, sr = load(audio.file, normalize=True, channels_first=True)
        audio.file.seek(0)
        min_audio_duration: int = sr * audio_dur_sec

        if len(sample[0]) < min_audio_duration:
            raise NeuralModelError(
                f'Audio duration is less than '
                f'{min_audio_duration / sr} seconds'
            )

        sample = sample[:, 0:sr * audio_dur_sec]
        sample = mean(sample, dim=0, keepdim=True)
        resampled = resample(sample, sr, sample_rate)

        transform = MFCC(sample_rate=sample_rate, n_mfcc=40)
        mfcc = transform(resampled.unsqueeze(0)).numpy()

        try:
            output = self.session.run(['sigmoid_1'], {'l_x_': mfcc})
        except Exception as e:
            raise NeuralModelError(str(e))

        sigmoid_val: float = float(output[0])

        return sigmoid_val
