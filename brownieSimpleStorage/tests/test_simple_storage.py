from brownie import SimpleStorage,accounts

def test_deploy():
    #Arrange
    account = accounts[0]
    #Act - actual functionality
    simple_storage=SimpleStorage.deploy({"from":account})
    stored_value = simple_storage.retrieve()
    expected=0
    #assertion
    assert stored_value ==expected

def test_update_storage():
    #Arrange
    account = accounts[0]
    #Act - actual functionality
    expected=15
    simple_storage=SimpleStorage.deploy({"from":account})
    simple_storage.store(expected,{"from":account})
    #assertion
    assert simple_storage.retrieve() ==expected
