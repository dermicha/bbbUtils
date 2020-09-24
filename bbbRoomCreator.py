import argparse
import logging
import uuid

from bbbutils.roomutil import RoomUtil

logging.basicConfig(level=logging.INFO)
logging.info("bbbRoomUtil Example")

parser = argparse.ArgumentParser(description='bbbRoomUtil Example')
parser.add_argument('-u', dest='bbbUrl', metavar='BBBURL', required=True, help='https://bbb.yourserver.com/bigbluebutton/')
parser.add_argument('-s', dest='bbbSec', metavar='BBBSEC', required=True, help='BigBlueButton API Secret')
parser.add_argument('-r', dest='bbbRoom', metavar='BBBROOM', required=False, help='BigBlueButton Room Name', default=None)
args = parser.parse_args()

bbb = RoomUtil(args.bbbUrl, args.bbbSec)

if (args.bbbRoom == None):
    roomId = "room-{}".format(str(uuid.uuid4()))
else:
    roomId = args.bbbRoom

userName = "user-{}".format(str(uuid.uuid4()))
logging.info(bbb.getRoomUrl(roomId))
logging.info(bbb.getRoomUrl(roomId, userName, moderator=True))
