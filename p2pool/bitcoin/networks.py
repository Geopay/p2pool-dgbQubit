import os
import platform

from twisted.internet import defer

from . import data
from p2pool.util import math, pack, jsonrpc

@defer.inlineCallbacks
def check_genesis_block(bitcoind, genesis_block_hash):
    try:
        yield bitcoind.rpc_getblock(genesis_block_hash)
    except jsonrpc.Error_for_code(-5):
        defer.returnValue(False)
    else:
        defer.returnValue(True)

nets = dict(
    digibyteSha=math.Object(
        P2P_PREFIX = 'fac3b6da'.decode('hex') #pchmessagestart
	P2P_PORT = 12024
	ADDRESS_VERSION = 30 #pubkey_address
	RPC_PORT = 14022
	RPC_CHECK = defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
	    'digibyteaddress' in (yield bitcoind.rpc_help()) and
	     not (yield bitcoind.rpc_getinfo())['testnet']
        )),
	SUBSIDY_FUNC = lambda height: __import__('digibyte_subsidy').GetBlockBaseValue(height)
	POW_FUNC = lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data))
	BLOCK_PERIOD = 60 # s
	SYMBOL = 'DGB'
	CONF_FILE_FUNC = lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'digibyte') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/digibyte/') if platform.system() == 'Darwin' else os.path.expanduser('~/.digibyte'), 'digibyte.conf')
	BLOCK_EXPLORER_URL_PREFIX = 'http://altexplorer.net/block/'
	ADDRESS_EXPLORER_URL_PREFIX = 'http://altexplorer.net/address/'
	TX_EXPLORER_URL_PREFIX = 'http://altexplorer.net/tx/'
	SANE_TARGET_RANGE = (2**256//1000000000 - 1, 2**256//1000 - 1)
	DUMB_SCRYPT_DIFF = 2**16
	DUST_THRESHOLD = 0.0001e8
    ),
    digibyteSha_testnet=math.Object(
        P2P_PREFIX='0b110907'.decode('hex'),
        P2P_PORT=18333,
        ADDRESS_VERSION=111,
        RPC_PORT=18332,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'bitcoinaddress' in (yield bitcoind.rpc_help()) and
            (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 50*100000000 >> (height + 1)//210000,
        POW_FUNC=data.hash256,
        BLOCK_PERIOD=600, # s
        SYMBOL='tBTC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'Bitcoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Bitcoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.bitcoin'), 'bitcoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://blockexplorer.com/testnet/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://blockexplorer.com/testnet/address/',
        TX_EXPLORER_URL_PREFIX='http://blockexplorer.com/testnet/tx/',
        SANE_TARGET_RANGE=(2**256//2**32//1000 - 1, 2**256//2**32 - 1),
        DUMB_SCRYPT_DIFF=1,
        DUST_THRESHOLD=1e8,
    ),

)
for net_name, net in nets.iteritems():
    net.NAME = net_name
