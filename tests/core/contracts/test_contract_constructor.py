
import pytest

from eth_utils import (
    decode_hex,
)
from web3 import (
    Account,
    Web3,
)
# Ignore warning in pyethereum 1.6 - will go away with the upgrade
pytestmark = pytest.mark.filterwarnings("ignore:implicit cast from 'char *'")


def test_contract_deployment_no_constructor(web3, MathContract,
                                            MATH_RUNTIME):
    
    deploy_txn = MathContract.constructor().transact()

    txn_receipt = web3.eth.getTransactionReceipt(deploy_txn)
    assert txn_receipt is not None

    assert txn_receipt['contractAddress']
    contract_address = txn_receipt['contractAddress']

    blockchain_code = web3.eth.getCode(contract_address)
    assert blockchain_code == decode_hex(MATH_RUNTIME)


def test_contract_deployment_with_constructor_without_args(web3,
                                                           SimpleConstructorContract,
                                                           SIMPLE_CONSTRUCTOR_RUNTIME):

    deploy_txn = SimpleConstructorContract.constructor().transact()

    txn_receipt = web3.eth.getTransactionReceipt(deploy_txn)
    assert txn_receipt is not None

    assert txn_receipt['contractAddress']
    contract_address = txn_receipt['contractAddress']

    blockchain_code = web3.eth.getCode(contract_address)
    assert blockchain_code == decode_hex(SIMPLE_CONSTRUCTOR_RUNTIME)


def test_contract_deployment_with_constructor_with_arguments(web3,
                                                             WithConstructorArgumentsContract,
                                                             WITH_CONSTRUCTOR_ARGUMENTS_RUNTIME):


    deploy_txn = WithConstructorArgumentsContract.constructor(args=[1234, 'abcd']).transact()

    txn_receipt = web3.eth.getTransactionReceipt(deploy_txn)
    assert txn_receipt is not None

    assert txn_receipt['contractAddress']
    contract_address = txn_receipt['contractAddress']

    blockchain_code = web3.eth.getCode(contract_address)
    assert blockchain_code == decode_hex(WITH_CONSTRUCTOR_ARGUMENTS_RUNTIME)


def test_contract_deployment_with_constructor_with_address_argument(web3,
                                                                    WithConstructorAddressArgumentsContract,  # noqa: E501
                                                                    WITH_CONSTRUCTOR_ADDRESS_RUNTIME):  # noqa: E501
    deploy_txn = WithConstructorAddressArgumentsContract.constructor(
        args=["0x16D9983245De15E7A9A73bC586E01FF6E08dE737"],
    ).transact()

    txn_receipt = web3.eth.getTransactionReceipt(deploy_txn)
    assert txn_receipt is not None

    assert txn_receipt['contractAddress']
    contract_address = txn_receipt['contractAddress']

    blockchain_code = web3.eth.getCode(contract_address)
    assert blockchain_code == decode_hex(WITH_CONSTRUCTOR_ADDRESS_RUNTIME)

def test_contract_deployment_gas_estimate_no_constructor(web3, MathContract,
                                            MATH_RUNTIME):

    gas_estimate = MathContract.constructor().estimateGas()

    assert isinstance(gas_estimate, int)  # Assert Estimate is an int


def test_contract_deployment_gas_estimate_with_constructor_without_args(web3,
                                                           SimpleConstructorContract,
                                                           SIMPLE_CONSTRUCTOR_RUNTIME):

    gas_estimate = SimpleConstructorContract.constructor().estimateGas()

    assert isinstance(gas_estimate, int)  # Assert Estimate is an int


def test_contract_deployment_gas_estimate_with_constructor_with_arguments(web3,
                                                             WithConstructorArgumentsContract,
                                                             WITH_CONSTRUCTOR_ARGUMENTS_RUNTIME):


    gas_estimate = WithConstructorArgumentsContract.constructor(args=[1234, 'abcd']).estimateGas()

    assert isinstance(gas_estimate, int)  # Assert Estimate is an int


def test_contract_deployment_gas_estimate_with_constructor_with_address_argument(web3,
                                                                    WithConstructorAddressArgumentsContract,  # noqa: E501
                                                                    WITH_CONSTRUCTOR_ADDRESS_RUNTIME):  # noqa: E501

    gas_estimate = WithConstructorAddressArgumentsContract.constructor(
        args=["0x16D9983245De15E7A9A73bC586E01FF6E08dE737"],
    ).estimateGas()

    assert isinstance(gas_estimate, int)  # Assert Estimate is an int

@pytest.fixture(params=['instance', 'class'])
def acct(request, web3):
    if request.param == 'instance':
        return web3.eth.account
    elif request.param == 'class':
        return Account
    raise Exception('Unreachable!')

@pytest.mark.parametrize(
    'txn, private_key, expected_raw_tx, tx_hash, r, s, v',
    (
        (
            {
                'to': '0xF0109fC8DF283027b6285cc889F5aA624EaC1F55',
                'value': 1000000000,
                'gas': 2000000,
                'gasPrice': 234567897654321,
                'nonce': 0,
                'chainId': 1
            },
            '0x4c0883a69102937d6231471b5dbb6204fe5129617082792ae468d01a3f362318',
            '0xf902ac8086d55698372431831e848094f0109fc8df283027b6285cc889f5aa624eac1f55843b9aca00b90240606060405261022e806100126000396000f360606040523615610074576000357c01000000000000000000000000000000000000000000000000000000009004806316216f391461007657806361bc221a146100995780637cf5dab0146100bc578063a5f3c23b146100e8578063d09de08a1461011d578063dcf537b11461014057610074565b005b610083600480505061016c565b6040518082815260200191505060405180910390f35b6100a6600480505061017f565b6040518082815260200191505060405180910390f35b6100d26004808035906020019091905050610188565b6040518082815260200191505060405180910390f35b61010760048080359060200190919080359060200190919050506101ea565b6040518082815260200191505060405180910390f35b61012a6004805050610201565b6040518082815260200191505060405180910390f35b6101566004808035906020019091905050610217565b6040518082815260200191505060405180910390f35b6000600d9050805080905061017c565b90565b60006000505481565b6000816000600082828250540192505081905550600060005054905080507f3496c3ede4ec3ab3686712aa1c238593ea6a42df83f98a5ec7df9834cfa577c5816040518082815260200191505060405180910390a18090506101e5565b919050565b6000818301905080508090506101fb565b92915050565b600061020d6001610188565b9050610214565b90565b60006007820290508050809050610229565b9190505625a0bd41479adfd78ca00529aeca20a4e65184f68c80a875929ecace609d128817aea02ce577b132c54c2ae993de571c4552419a07df553676d629f9b414f46c90a04a',  # noqa: E501
            '0x2484ced54d4df3d46d2dfa26b5583159a7f18bdea611c4b57177fb711bd5de79',
            85602467640843664143041950298420621146490699692467068327557735343058057697198,
            20307199400570577342187658236524042671596982801027962119589359657057027924042,
            37,
        ),
        (
            {
                'to': '0xF0109fC8DF283027b6285cc889F5aA624EaC1F55',
                'value': 0,
                'gas': 31853,
                'gasPrice': 0,
                'nonce': 0,
                'chainId': 1
            },
            '0x4c0883a69102937d6231471b5dbb6204fe5129617082792ae468d01a3f362318',
            '0xf902a18080827c6d94f0109fc8df283027b6285cc889f5aa624eac1f5580b90240606060405261022e806100126000396000f360606040523615610074576000357c01000000000000000000000000000000000000000000000000000000009004806316216f391461007657806361bc221a146100995780637cf5dab0146100bc578063a5f3c23b146100e8578063d09de08a1461011d578063dcf537b11461014057610074565b005b610083600480505061016c565b6040518082815260200191505060405180910390f35b6100a6600480505061017f565b6040518082815260200191505060405180910390f35b6100d26004808035906020019091905050610188565b6040518082815260200191505060405180910390f35b61010760048080359060200190919080359060200190919050506101ea565b6040518082815260200191505060405180910390f35b61012a6004805050610201565b6040518082815260200191505060405180910390f35b6101566004808035906020019091905050610217565b6040518082815260200191505060405180910390f35b6000600d9050805080905061017c565b90565b60006000505481565b6000816000600082828250540192505081905550600060005054905080507f3496c3ede4ec3ab3686712aa1c238593ea6a42df83f98a5ec7df9834cfa577c5816040518082815260200191505060405180910390a18090506101e5565b919050565b6000818301905080508090506101fb565b92915050565b600061020d6001610188565b9050610214565b90565b60006007820290508050809050610229565b9190505626a0febaa6f7e6a2cde7610cccd93be3659059c732ee4a4209907c4a3e83f9f9f5a6a065ae079e8d82f754ad54e24e0c8438e6a138048a21aa7649d6d4a3af9e46be5b',  # noqa: E501
            '0x8440180d01b87ca03b3e97a55a313123eaf7f7c7e24abca4b859c9e953b1f390',
            115217249467487637044952468322258519831413572401151656560143794693893900596646,
            45991081682980254511403891738286950033298278453362760844115458783923365396059,
            38,
        ),
    ),
    ids=['web3js_example', '31byte_r_and_s'],
)

def test_contract_deployment_data_no_constructor(MathContract, acct, txn, private_key, expected_raw_tx, tx_hash, r, s, v):

    txn = MathContract.constructor().buildTransaction()

    txn['nonce'] = 0
    txn['to'] = ''

    signed = acct.signTransaction(txn, private_key)

    #assert signed.r == r
    #assert signed.s == s
    #assert signed.v == v
    #raw_tx = Web3.toHex(signed.rawTransaction)
    #assert raw_tx == expected_raw_tx
    #assert Web3.toHex(signed.hash) == tx_hash

    #account = acct.privateKeyToAccount(private_key)
    #assert account.signTransaction(txn) == signed

'''
@pytest.mark.parametrize(
    'txn, private_key, expected_raw_tx, tx_hash, r, s, v',
    (
        (
            {
                'to': '0xF0109fC8DF283027b6285cc889F5aA624EaC1F55',
                'value': 1000000000,
                'gas': 2000000,
                'gasPrice': 234567897654321,
                'nonce': 0,
                'chainId': 1
            },
            '0x4c0883a69102937d6231471b5dbb6204fe5129617082792ae468d01a3f362318',
            '0xf8ac8086d55698372431831e848094f0109fc8df283027b6285cc889f5aa624eac1f55843b9aca00b84160606040526003600055602c8060156000396000f3606060405260e060020a600035046373d4a13a8114601a575b005b602260005481565b6060908152602090f326a0984511dd3e9da8429ac93ef7968f949544a3f82f753f09dbc7cc1350ddcc3484a064d04a42b522aaffa7a250a796604a12aa274fa103c52a15ef8ca1d3081467c4',  # noqa: E501
            '0xcc4a0a6ded88c762e3a6a1e921afab6ed182da7c6d733abe0afa4e0297fecd5f',
            68873588726556526952363198393762541904039605980887431217156134944386004563076,
            45599301575462471676533160893789686525332879866187322507903874658043344218052,
            38,
        ),
        (
            {
                'to': '0xF0109fC8DF283027b6285cc889F5aA624EaC1F55',
                'value': 0,
                'gas': 31853,
                'gasPrice': 0,
                'nonce': 0,
                'chainId': 1
            },
            '0x4c0883a69102937d6231471b5dbb6204fe5129617082792ae468d01a3f362318',
            '0xf8a18080827c6d94f0109fc8df283027b6285cc889f5aa624eac1f5580b84160606040526003600055602c8060156000396000f3606060405260e060020a600035046373d4a13a8114601a575b005b602260005481565b6060908152602090f326a0886f747f74e47ac451f365b7dcb503d4def22e63f7bdf0f75ae6c724a89031d9a00c4c8c9f9e052a5a32daf8d8579f437d479b54255020d278a5b003679ee28fdf',  # noqa: E501
            '0xfc0c69bc23d670970e4d7d0eea80016a17ddb55930959df238d05846a5c62bb6',
            61711471470314300784969137351093467319738708305914557018954217683388040491481,
            5563005107683891647322860606868955945559777731600276139365376420219547979743,
            38,
        ),
    ),
    ids=['web3js_example', '31byte_r_and_s'],
)


def test_contract_deployment_with_constructor_without_args(SimpleConstructorContract, acct, txn, private_key, expected_raw_tx, tx_hash, r, s, v):

    deploy_data = SimpleConstructorContract.constructor().buildTransaction()

    txn['data'] = deploy_data

    signed = acct.signTransaction(txn, private_key)

    assert signed.r == r
    assert signed.s == s
    assert signed.v == v

    raw_tx = Web3.toHex(signed.rawTransaction)
    assert raw_tx == expected_raw_tx
    _tx_hash = Web3.toHex(signed.hash)
    assert _tx_hash == tx_hash

    account = acct.privateKeyToAccount(private_key)
    assert account.signTransaction(txn) == signed


@pytest.mark.parametrize(
    'txn, private_key, expected_raw_tx, tx_hash, r, s, v',
    (
        (
            {
                'to': '0xF0109fC8DF283027b6285cc889F5aA624EaC1F55',
                'value': 1000000000,
                'gas': 2000000,
                'gasPrice': 234567897654321,
                'nonce': 0,
                'chainId': 1
            },
            '0x4c0883a69102937d6231471b5dbb6204fe5129617082792ae468d01a3f362318',
            '0xf901118086d55698372431831e848094f0109fc8df283027b6285cc889f5aa624eac1f55843b9aca00b8a660606040818152806066833960a09052516080516000918255600155603e908190602890396000f3606060405260e060020a600035046388ec134681146024578063d4c46c7614602c575b005b603460005481565b603460015481565b6060908152602090f300000000000000000000000000000000000000000000000000000000000004d2abcd00000000000000000000000000000000000000000000000000000000000026a031cf98c2f0f22f689d2c4f37af4824b5f4bb52a3714fb74618abaed81224911da07a0c25492bd272f70f50add714422cf23a8f53ff5da3ae1f1139a65701b9b338',  # noqa: E501
            '0x3bcf6292f2c28818e2d637527e986293d68e859507a45de7c380be561e63ed2d',
            22530121244038123388368627906258278852203537716864315681247185755184814133533,
            55203627029241780219121410169331087721925987526626082016480451892565348299576,
            38,
        ),
        (
            {
                'to': '0xF0109fC8DF283027b6285cc889F5aA624EaC1F55',
                'value': 0,
                'gas': 31853,
                'gasPrice': 0,
                'nonce': 0,
                'chainId': 1
            },
            '0x4c0883a69102937d6231471b5dbb6204fe5129617082792ae468d01a3f362318',
            '0xf901068080827c6d94f0109fc8df283027b6285cc889f5aa624eac1f5580b8a660606040818152806066833960a09052516080516000918255600155603e908190602890396000f3606060405260e060020a600035046388ec134681146024578063d4c46c7614602c575b005b603460005481565b603460015481565b6060908152602090f300000000000000000000000000000000000000000000000000000000000004d2abcd00000000000000000000000000000000000000000000000000000000000026a081ba76a9445046ac16cc504aa179a1a00f83e140d3507c966997d44691ac61f0a078a2094caf04d34b54a5de4867f3e5c40d53f9550420c39153f0305fb46d8263',  # noqa: E501
            '0xa51361b96f8169375b310c1ad2236afd9b93bcc414f2627a2dd3bf6d0813b955',
            58677809990784311110938269820876873533474979477406807277121451199701208293872,
            54563835237590768768054463437637293096105667696261505012227606369069364511331,
            38,
        ),
    ),
    ids=['web3js_example', '31byte_r_and_s'],
)

def test_contract_deployment_with_constructor_with_arguments(WithConstructorArgumentsContract, acct, txn, private_key, expected_raw_tx, tx_hash, r, s, v):

    deploy_data = WithConstructorArgumentsContract.constructor(args=[1234, 'abcd']).buildTransaction()

    txn['data'] = deploy_data

    signed = acct.signTransaction(txn, private_key)

    assert signed.r == r
    assert signed.s == s
    assert signed.v == v

    raw_tx = Web3.toHex(signed.rawTransaction)
    assert raw_tx == expected_raw_tx
    _tx_hash = Web3.toHex(signed.hash)
    assert _tx_hash == tx_hash

    account = acct.privateKeyToAccount(private_key)
    assert account.signTransaction(txn) == signed

@pytest.mark.parametrize(
    'txn, private_key, expected_raw_tx, tx_hash, r, s, v',
    (
        (
            {
                'to': '0xF0109fC8DF283027b6285cc889F5aA624EaC1F55',
                'value': 1000000000,
                'gas': 2000000,
                'gasPrice': 234567897654321,
                'nonce': 0,
                'chainId': 1
            },
            '0x4c0883a69102937d6231471b5dbb6204fe5129617082792ae468d01a3f362318',
            '0xf901018086d55698372431831e848094f0109fc8df283027b6285cc889f5aa624eac1f55843b9aca00b8966060604052604051602080607683395060806040525160008054600160a060020a031916821790555060428060346000396000f3606060405260e060020a600035046334664e3a8114601a575b005b603860005473ffffffffffffffffffffffffffffffffffffffff1681565b6060908152602090f300000000000000000000000016d9983245de15e7a9a73bc586e01ff6e08de73726a01c67a9775b8ad0de0904da71be7f2d62401ea121f552e6f653ebbcea28ea471ba01334298097dec178cc60b0bfcb2a10a0302aad64de14327c62c590475cceb427',  # noqa: E501
            '0x7f9f9e125976cb96c9f3436bc5c354d0e573589b1c72ace5cf8fe28f7a5c9407',
            12847914621010417542523589102293120000714638503710429163002302755560900675355,
            8686106608917721614818207962626470233486399023673498181162492721732762121255,
            38,
        ),
        (
            {
                'to': '0xF0109fC8DF283027b6285cc889F5aA624EaC1F55',
                'value': 0,
                'gas': 31853,
                'gasPrice': 0,
                'nonce': 0,
                'chainId': 1
            },
            '0x4c0883a69102937d6231471b5dbb6204fe5129617082792ae468d01a3f362318',
            '0xf8f68080827c6d94f0109fc8df283027b6285cc889f5aa624eac1f5580b8966060604052604051602080607683395060806040525160008054600160a060020a031916821790555060428060346000396000f3606060405260e060020a600035046334664e3a8114601a575b005b603860005473ffffffffffffffffffffffffffffffffffffffff1681565b6060908152602090f300000000000000000000000016d9983245de15e7a9a73bc586e01ff6e08de73725a0724bfb50b52f80211b4292489822437baf018d5e5ea4d9773ae097095eae50f2a03eb784037880d16d062102567f8b9f25b05e450de5ca5e42e19915505030b247',  # noqa: E501
            '0xc037d56a1a8910453aa4d28bd193a9e91cfc3bb9640fd6df0562921a81ad158b',
            51697912782560590269279343002095891073040138366570439304470614233188068643058,
            28367640749105044447798463648099632309297781255732120427438668075853556003399,
            37,
        ),
    ),
    ids=['web3js_example', '31byte_r_and_s'],
)

def test_contract_deployment_with_constructor_with_address_argument(WithConstructorAddressArgumentsContract, acct, txn, private_key, expected_raw_tx, tx_hash, r, s, v):  # noqa: E501

    deploy_data = WithConstructorAddressArgumentsContract.constructor(
        args=["0x16D9983245De15E7A9A73bC586E01FF6E08dE737"],
    ).buildTransaction()

    txn['data'] = deploy_data

    signed = acct.signTransaction(txn, private_key)


    assert signed.r == r
    assert signed.s == s
    assert signed.v == v

    raw_tx = Web3.toHex(signed.rawTransaction)
    assert raw_tx == expected_raw_tx
    _tx_hash = Web3.toHex(signed.hash)
    assert _tx_hash == tx_hash

    account = acct.privateKeyToAccount(private_key)
    assert account.signTransaction(txn) == signed'''