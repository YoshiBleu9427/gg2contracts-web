from gg2haxxy25.common.enums import ContractType
from gg2haxxy25.common.models import Contract, User

# TODO test assert all enum options are here

VALUE_BY_TYPE = {ContractType.DEBUG: 0}

POINTS_BY_TYPE = {ContractType.DEBUG: 0}


def generate_contract(for_user: User) -> Contract:
    # contract_type: ContractType = random.choice(list(ContractType))
    contract_type: ContractType = ContractType.DEBUG
    return Contract(
        contract_type=contract_type,
        value=0,
        target_value=VALUE_BY_TYPE[contract_type],
        game_class=for_user.main_class,  # TODO
        points=POINTS_BY_TYPE[contract_type],
        user=for_user,
    )
