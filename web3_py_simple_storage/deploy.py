from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()


install_solc("0.6.0")
#Compile our solidity
compiled_sol = compile_standard(
    {
        "language":"Solidity",
        "sources":{"SimpleStorage.sol" : {"content" : simple_storage_file}},
        "settings":{
            "outputSelection":{
                "*":{
                    "*":["abi","metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        }
    },
    solc_version="0.6.0",
)
with open("compiled_code.json","w") as file: 
    json.dump(compiled_sol,file)

#get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

#for connecting to rinkeby
w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/19ff456a41c5436dbc1d5caaa52d9ef2"))
chain_id = 4
my_address = "0xF7575c46eA44411e5181fc2ac913F04e5DFC487c"

private_key = os.getenv("PRIVATE_KEY")

#Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi,bytecode=bytecode)

#get the latest tx
nonce = w3.eth.getTransactionCount(my_address)

#1. build a Tx
transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId":chain_id,"from":my_address,"nonce":nonce,"gasPrice": w3.eth.gas_price}
)
#2. Sign a Tx
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print("Deploying contract...")
#3. Send a Tx
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
#Code stop until response
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed contract!")


#working with Contract
#contract addr
#contract abi
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
#call vs transact

print(simple_storage.functions.retrieve().call())
print("Updating contract...")
#Create tx
store_transaction = simple_storage.functions.store(15).buildTransaction(
        {
            "chainId":chain_id,"from":my_address,"nonce":nonce+1,"gasPrice":w3.eth.gas_price
            })
#sign transaction
signed_store_txn=w3.eth.account.sign_transaction(
        store_transaction,private_key=private_key)
#send transaction
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
#Wait for transacted 
tx_receipt=w3.eth.wait_for_transaction_receipt(send_store_tx)
print("Updated!")
#show tx result
print(simple_storage.functions.retrieve().call())


