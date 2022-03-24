from brownie import accounts,config,SimpleStorage,network

def deploy_simple_storage():
    #method1 : account from ganache
    account = getAccount()
    #method2: account added to brownie (from Metamask) . Recommended
    # print(accounts.load("myTestAcc"))
    #method3 : from env and config.yaml
    # account_from_env=accounts.add(config["wallets"]["from_key"])
    # print(account_from_env)
    simple_storage = SimpleStorage.deploy({"from":account})
    initValue = simple_storage.retrieve()
    print(initValue)
    transaction=simple_storage.store(15,{"from":account})
    transaction.wait(1)
    updated_storage_value= simple_storage.retrieve()
    print(updated_storage_value)

def getAccount():
    if(network.show_active()=="development"):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])




def main():
    deploy_simple_storage()
