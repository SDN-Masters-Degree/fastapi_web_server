import torch
from torchaudio import load
from torchaudio.functional import resample
from torchaudio.transforms import MFCC

from audio_spoof_detection_service.application.protocols.neural_model_gateways.cnn import CnnNeuralModelGateway
from audio_spoof_detection_service.domain.entities.audio import AudioEntity
from audio_spoof_detection_service.domain.types_and_consts import AudioResult
from audio_spoof_detection_service.domain.error import NeuralModelError
from audio_spoof_detection_service.infrastructure.settings import Settings
from audio_spoof_detection_service.infrastructure.neural_model_gateways.torch.cnn.model import TorchCnnModel


class TorchCnnNeuralModelGateway(CnnNeuralModelGateway):
    def __init__(self, settings: Settings):
        self.settings = settings
        device = torch.device('cpu')
        input_shape = torch.zeros((1, 40, 31))
        self.model = TorchCnnModel(input_shape)
        self.model.load_state_dict(torch.load(settings.cnn_model_path, map_location=device, weights_only=False))
        self.model.eval()
        self.transform = MFCC(sample_rate=self.settings.target_sample_rate, n_mfcc=40)

    async def predict(self, audio: AudioEntity) -> AudioResult:
        sample_rate: int = self.settings.target_sample_rate
        audio_dur_sec = int(self.settings.audio_min_duration_milli / 1000)
        sample, sr = load(audio.file, normalize=True, channels_first=True)
        audio.file.seek(0)
        min_audio_duration: int = sr * audio_dur_sec

        if len(sample[0]) < min_audio_duration:
            raise NeuralModelError(f'Audio duration is less than {min_audio_duration / sr} seconds')

        sample = resample(sample, sr, sample_rate)
        mono_sample = torch.mean(sample, dim=0)
        chunk_size: int = sample_rate * audio_dur_sec
        chunks = torch.split(mono_sample, chunk_size)

        if chunks[-1].shape[0] < chunk_size: # удаляем недо-чанк
            chunks = chunks[:-1]

        datas = torch.stack([self.transform(chunk).unsqueeze(0) for chunk in chunks])

        try:
            output = self.model(datas)
        except Exception as e:
            raise NeuralModelError(str(e))

        sigmoid_val: float = output.mean().float()

        return AudioResult.fake if sigmoid_val > 0.5 else AudioResult.real
