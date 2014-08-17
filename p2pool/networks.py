from p2pool.bitcoin import networks
from p2pool.util import math

# CHAIN_LENGTH = number of shares back client keeps
# REAL_CHAIN_LENGTH = maximum number of shares back client uses to compute payout
# REAL_CHAIN_LENGTH must always be <= CHAIN_LENGTH
# REAL_CHAIN_LENGTH must be changed in sync with all other clients
# changes can be done by changing one, then the other

nets = dict(
    digibyteSkein=math.Object(
        PARENT=networks.nets['digibyteSkein'],
        SHARE_PERIOD=15, # seconds target spacing
        CHAIN_LENGTH=12*60*60//10, # shares
        REAL_CHAIN_LENGTH=12*60*60//10, # shares
        TARGET_LOOKBEHIND=20, # shares diff regulation
        SPREAD=50, # blocks
        IDENTIFIER='48a4ebc31b798115'.decode('hex'),
        PREFIX='5685a276c2dd81db'.decode('hex'),
        P2P_PORT=15030,
        MIN_TARGET=0,
        MAX_TARGET=2**256//2**20 - 1,
        PERSIST=False,
        WORKER_PORT=15031,
        BOOTSTRAP_ADDRS=''.split(' '),
        ANNOUNCE_CHANNEL='#p2pool-alt',
        VERSION_CHECK=lambda v: True,
    ),
    digibyteSkeintestnet=math.Object(
        PARENT=networks.nets['digibyteSkein_testnet'],
        SHARE_PERIOD=15, # seconds target spacing
        CHAIN_LENGTH=12*60*60//10, # shares
        REAL_CHAIN_LENGTH=12*60*60//10, # shares
        TARGET_LOOKBEHIND=20, # shares diff regulation
        SPREAD=50, # blocks
        IDENTIFIER='58a4ebc31b798115'.decode('hex'),
        PREFIX='6685a276c2dd81db'.decode('hex'),
        P2P_PORT=25030,
        MIN_TARGET=0,
        MAX_TARGET=2**256//2**20 - 1,
        PERSIST=False,
        WORKER_PORT=25031,
        BOOTSTRAP_ADDRS=''.split(' '),
        ANNOUNCE_CHANNEL='#p2pool-alt',
        VERSION_CHECK=lambda v: True,
    ),

)
for net_name, net in nets.iteritems():
    net.NAME = net_name
