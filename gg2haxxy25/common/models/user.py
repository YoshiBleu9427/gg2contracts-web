from uuid import UUID
from gg2haxxy25.common.basemodel import AppBaseModel
from gg2haxxy25.common.models.contract import Contract
from gg2haxxy25.common.enums import GameClass


class User(AppBaseModel):
    identifier: UUID
    username: str
    contracts: list[Contract]
    main_class: GameClass
