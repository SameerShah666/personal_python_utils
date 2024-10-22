from web3 import Web3, EthereumTesterProvider
from contracts import healthcaresystem
from solcx import set_solc_version, compile_source

set_solc_version('0.8.26')

class Connector:
    
    naccounts = []

    def __init__(self,url) -> None:
        self.access_point = Web3.HTTPProvider(url)

    def connect(self):
        self.w3 = Web3(self.access_point)
        self.naccounts = self.w3.eth.accounts
        return self.w3.is_connected()
    
    def connect_test(self):
        self.w3 = Web3(EthereumTesterProvider())
        self.naccounts = self.w3.eth.accounts
        return self.w3.is_connected()
    
    def create_account(self):
        account = self.w3.eth.account.create()
        self.naccounts.append(account.address)
        print(f"Account created: {account.address}\nPrivate key: {account._private_key.hex()}")
    
    def get_accounts(self):
        return self.naccounts
    
    def get_balance(self,account):
        return self.w3.eth.get_balance(account)
    
    def send_transaction(self,account,recipient,amount):
        transaction = {
            'from': account.address,
            'to': recipient,
            'value': amount,
            'gas': 2000000,
            'gasPrice': self.w3.toWei('50', 'gwei'),
            'nonce': self.w3.eth.getTransactionCount(account.address),
        }
        signed = account.sign_transaction(transaction)
        tx_hash = self.w3.eth.send_raw_transaction(signed.rawTransaction)
        return tx_hash.hex()
    
    def get_transaction(self,tx_hash):
        return self.w3.eth.get_transaction(tx_hash)
    
    def get_block(self,block_number):
        return self.w3.eth.get_block(block_number)
    
    def get_block_number(self):
        return self.w3.eth.block_number
    
    def get_block_transaction_count(self,block_number):
        return self.w3.eth.get_block_transaction_count(block_number)
    
    def get_transaction_receipt(self,tx_hash):
        return self.w3.eth.get_transaction_receipt(tx_hash)
    
    def get_transaction_count(self,account):
        return self.w3.eth.get_transaction_count(account.address)
    
    def get_gas_price(self):
        return self.w3.eth.gas_price
    
    def get_transaction_count(self,account):
        return self.w3.eth.get_transaction_count(account.address)
    
    def deploy_contract(self,cont):
        compiled_sol = compile_source(
            cont,
            output_values=['abi', 'bin']
        )

        self.contract_id, self.contract_interface = compiled_sol.popitem()
        self.bytecode, self.abi = self.contract_interface['bin'], self.contract_interface['abi']

        self._contract = self.w3.eth.contract(abi=self.abi, bytecode=self.bytecode)

        # Deploy the contract
        self.system = self.w3.eth.contract(abi=self.contract_interface['abi'], bytecode=self.contract_interface['bin'])
        self.tx_hash = self.system.constructor().transact()
        self.tx_receipt = self.w3.eth.wait_for_transaction_receipt(self.tx_hash)
        
        # Contract instance
        self.contract_address = self.tx_receipt.contractAddress
        self.Con = self.w3.eth.contract(address=self.contract_address, abi=self.contract_interface['abi'])



url = "http://127.0.0.1:7545"

connector = Connector(url)
connector.connect_test()
connector.create_account()

print(connector.get_accounts())
print(connector.get_balance('0x7E5F4552091A69125d5DfCb7b8C2659029395Bdf'))

connector.deploy_contract(healthcaresystem)

# Add a doctor
doctor_address = connector.w3.eth.accounts[1]
tx_hash = connector.Con.functions.addDoctor(doctor_address).transact()
connector.w3.eth.wait_for_transaction_receipt(tx_hash)

# Add a patient
patient_address = connector.w3.eth.accounts[2]
tx_hash = connector.Con.functions.addPatient(patient_address, "John Doe", 30).transact({'from': doctor_address})
connector.w3.eth.wait_for_transaction_receipt(tx_hash)

name, age = connector.Con.functions.getPatientBasicInfo(patient_address).call({'from': patient_address})
print(f"Patient: {name}, {age}")
