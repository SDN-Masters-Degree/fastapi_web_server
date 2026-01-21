from torchaudio import load

from audio_spoof_detection_service.infrastructure.settings import Settings
from audio_spoof_detection_service.domain.entities.audio import AudioEntity
from audio_spoof_detection_service.domain.error import AudioError
from audio_spoof_detection_service.application.common.business_rule import BusinessRule


class IsValidAudioFileRule(BusinessRule):
    def __init__(self, settings: Settings):
        self.settings = settings

    async def __call__(self, audio: AudioEntity):
        await self.__validate_extension(audio)
        await self.__validate_duration_and_sample_rate(audio)

    @staticmethod
    async def __validate_extension(audio: AudioEntity):
        allowed_audio_extensions = ('.mp3', '.wav', '.ogg')
        file_name: str = audio.name

        if not file_name.endswith(allowed_audio_extensions):
            raise AudioError(
                f'{file_name} is not allowed extension, '
                f'use {allowed_audio_extensions}'
            )

    async def __validate_duration_and_sample_rate(self, audio: AudioEntity):
        audio_dur_sec = int(self.settings.audio_min_duration_milli / 1000)
        sample, sr = load(audio.file, normalize=True, channels_first=True)
        audio.file.seek(0)
        # функция load не сбрасывает позицию чтения после работы с аудиофайлом, поэтому делаем это сами

        if sr < self.settings.target_sample_rate:
            raise AudioError(
                f'Audio sample rate should be equal or bigger than '
                f'target sample rate - {self.settings.target_sample_rate}'
            )

        min_audio_duration: int = sr * audio_dur_sec

        if len(sample[0]) < min_audio_duration:
            raise AudioError(
                f'Audio duration should be equal or longer than '
                f'{audio_dur_sec} seconds'
            )
