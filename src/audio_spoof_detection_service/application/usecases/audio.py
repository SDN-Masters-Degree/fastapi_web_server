from datetime import datetime

from audio_spoof_detection_service.domain.entities.audio import AudioEntity, AudioMetaInfoEntity
from audio_spoof_detection_service.application.common.interactor import Interactor
from audio_spoof_detection_service.application.contracts.audio import (
    CheckAudioSpoofInputDTO, CheckAudioSpoofOutputDTO,
    GetAudioMetaInfosInputDTO, GetAudioMetaInfosOutputDTO
)
from audio_spoof_detection_service.application.protocols.neural_model_gateways.cnn import CnnNeuralModelGateway
from audio_spoof_detection_service.application.protocols.database_gateways.audio_gateway import AudioMetaInfoGateway
from audio_spoof_detection_service.application.business_rules.audio import IsValidAudioFileRule


class CheckAudioSpoofUseCase(Interactor[CheckAudioSpoofInputDTO, CheckAudioSpoofOutputDTO]):
    def __init__(self, cnn_model_gateway: CnnNeuralModelGateway, audio_meta_info_gateway: AudioMetaInfoGateway,
                 is_valid_audio_business_rule: IsValidAudioFileRule):
        self.cnn_model_gateway = cnn_model_gateway
        self.audio_meta_info_gateway = audio_meta_info_gateway
        self.is_valid_audio_business_rule = is_valid_audio_business_rule

    async def __call__(self, input_dto: CheckAudioSpoofInputDTO) -> CheckAudioSpoofOutputDTO:
        audio = AudioEntity(
            file=input_dto.audio_file,
            meta_info=AudioMetaInfoEntity(
                id=None,
                user_id=None,
                name=input_dto.audio_file_name,
                analyze_result=None,
                created_at=datetime.now()
            )
        )
        await self.is_valid_audio_business_rule(audio)
        result = await self.cnn_model_gateway.predict(audio)
        await self.audio_meta_info_gateway.add_audio_meta_info(audio.meta_info)

        return CheckAudioSpoofOutputDTO(result=result)


class GetAudioMetaInfosUseCase(Interactor[GetAudioMetaInfosInputDTO, GetAudioMetaInfosOutputDTO]):
    def __init__(self, audio_meta_info_gateway: AudioMetaInfoGateway):
        self.audio_meta_info_gateway = audio_meta_info_gateway

    async def __call__(self, input_dto: GetAudioMetaInfosInputDTO) -> GetAudioMetaInfosOutputDTO:
        audio_meta_infos = await self.audio_meta_info_gateway.get_all_audio_meta_infos_by_user_id(input_dto.user_id)
        return GetAudioMetaInfosOutputDTO(result=audio_meta_infos)
