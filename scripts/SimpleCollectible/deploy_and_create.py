from scripts.helpful_scripts import get_Account
from brownie import SimpleCollectible


def main():
    account = get_Account()
    simple_collectible = SimpleCollectible.deploy({"from": account})
