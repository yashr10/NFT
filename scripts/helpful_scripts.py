from brownie import (
    accounts,
    config,
    network,
    Contract,
    VRFCoordinatorMock,
    LinkToken,
)

OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
BREED_MAPPING = {0: "PUG", 1: "SHIBA-INU", 2: "ST-BERNARD"}


def get_breed(breed_number):
    return BREED_MAPPING[breed_number]


def get_Account(index=None, id=None):

    if index:
        return accounts[index]

    if id:
        return accounts.load(id)

    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]

    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )

    return contract


DECIMAL = 8
INITIAL_VALUE = 200000000000


def deploy_mocks(decimals=DECIMAL, initial_value=INITIAL_VALUE):
    account = get_Account()
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})

    print("Deployed!")


def fund_with_Link(
    contract_address, account=None, link_token=None, amount=100000000000000000
):  # 0.1 Link

    account = account if account else get_Account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})

    #  link_token_contract = interface.LinkTokenInterface(link_token.address)
    # tx = link_token.transfer(contract_address, {"from": account})

    tx.wait(1)
    print(f"Funded {contract_address}")
    return tx
