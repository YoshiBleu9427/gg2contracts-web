from uuid import UUID
from gg2haxxy25.common.enums import ContractType, GameClass
from gg2haxxy25.common.basemodel import AppBaseModel


class Contract(AppBaseModel):
    identifier: UUID
    contract_type: ContractType
    value: int
    target_value: int
    game_class: GameClass
