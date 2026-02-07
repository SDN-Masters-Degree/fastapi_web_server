from datetime import datetime, timezone

from audio_spoof_detection_service.domain.entities.audio import AudioEntity, AudioMetaInfoEntity
from audio_spoof_detection_service.application.common.interactor import Interactor
from audio_spoof_detection_service.application.contracts.audio import (
    CheckAudioSpoofInputDTO, CheckAudioSpoofOutputDTO,
    GetAudioMetaInfosInputDTO, GetAudioMetaInfosOutputDTO,
    GetAudioMetaInfoInputDTO, GetAudioMetaInfoOutputDTO,
    DeleteAudioMetaInfoInputDTO, DeleteAudioMetaInfoOutputDTO
)
from audio_spoof_detection_service.application.protocols.neural_model_gateways.cnn import CnnNeuralModelGateway
from audio_spoof_detection_service.application.protocols.database_gateways.audio_gateway import AudioMetaInfoGateway
from audio_spoof_detection_service.application.business_rules.audio import IsValidAudioFileRule
from audio_spoof_detection_service.domain.error import AudioError


class CheckAudioSpoofUseCase(Interactor[CheckAudioSpoofInputDTO, CheckAudioSpoofOutputDTO]):
    def __init__(self, cnn_model_gateway: CnnNeuralModelGateway, audio_meta_info_gateway: AudioMetaInfoGateway,
                 is_valid_audio_business_rule: IsValidAudioFileRule):
        self.cnn_model_gateway = cnn_model_gateway
        self.audio_meta_info_gateway = audio_meta_info_gateway
        self.is_valid_audio_business_rule = is_valid_audio_business_rule

    async def __call__(self, input_dto: CheckAudioSpoofInputDTO) -> CheckAudioSpoofOutputDTO:
        audio = AudioEntity(
            file=input_dto.audiofile,
            meta_info=AudioMetaInfoEntity(
                id=None,
                user_id=input_dto.user_id,
                name=input_dto.audiofile_name,
                analyze_result=None,
                created_at=datetime.now(tz=timezone.utc)
            )
        )
        await self.is_valid_audio_business_rule(audio)
        result = await self.cnn_model_gateway.predict(audio)
        audio.meta_info.analyze_result = result
        await self.audio_meta_info_gateway.add_audio_meta_info(audio.meta_info)

        return CheckAudioSpoofOutputDTO(result=result)


class GetAudioMetaInfosUseCase(Interactor[GetAudioMetaInfosInputDTO, GetAudioMetaInfosOutputDTO]):
    def __init__(self, audio_meta_info_gateway: AudioMetaInfoGateway):
        self.audio_meta_info_gateway = audio_meta_info_gateway

    async def __call__(self, input_dto: GetAudioMetaInfosInputDTO) -> GetAudioMetaInfosOutputDTO:
        audio_meta_infos = await self.audio_meta_info_gateway.get_all_audio_meta_infos_by_user_id(input_dto.user_id)
        return GetAudioMetaInfosOutputDTO(result=audio_meta_infos)


class GetAudioMetaInfoUseCase(Interactor[GetAudioMetaInfoInputDTO, GetAudioMetaInfoOutputDTO]):
    def __init__(self, audio_meta_info_gateway: AudioMetaInfoGateway):
        self.audio_meta_info_gateway = audio_meta_info_gateway

    async def __call__(self, input_dto: GetAudioMetaInfoInputDTO) -> GetAudioMetaInfoOutputDTO:
        try:
            audio_meta_info = await self.audio_meta_info_gateway.get_audio_meta_info_by_user_id(
                user_id=input_dto.user_id, audio_name=input_dto.audiofile_name
            )

            if audio_meta_info is None:
                raise AudioError('Отсутствует запись об аудио в БД.')

            return GetAudioMetaInfoOutputDTO(audio_info=audio_meta_info)
        except Exception as e:
            raise AudioError(f'Не удалось получить информацию об аудио: {e}')


class DeleteAudioMetaInfoUseCase(Interactor[DeleteAudioMetaInfoInputDTO, DeleteAudioMetaInfoOutputDTO]):
    def __init__(self, audio_meta_info_gate: AudioMetaInfoGateway):
        self.audio_meta_info_gate = audio_meta_info_gate

    async def __call__(self, input_dto: DeleteAudioMetaInfoInputDTO) -> DeleteAudioMetaInfoOutputDTO:
        try:
            audio_meta_info = await self.audio_meta_info_gate.get_audio_meta_info_by_user_id(
                user_id=input_dto.user_id, audio_name=input_dto.audiofile_name
            )

            if audio_meta_info is None:
                raise AudioError('Отсутствует запись об аудио в БД.')

            await self.audio_meta_info_gate.delete_audio_meta_info(
                user_id=input_dto.user_id, audio_name=input_dto.audiofile_name
            )
            return DeleteAudioMetaInfoOutputDTO(status=True)
        except Exception as e:
            raise AudioError(f'Не удалось удалить информацию об аудио: {e}')
