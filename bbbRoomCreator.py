import argparse
import logging
import uuid

from bbbutils.roomutil import RoomUtil

logging.basicConfig(level=logging.INFO)
logging.info("bbbRoomUtil Example")

parser = argparse.ArgumentParser(description='bbbRoomUtil Example')
parser.add_argument('-u', dest='bbbUrl', metavar='BBBURL', required=True,
                    help='https://bbb.yourserver.com/bigbluebutton/')
parser.add_argument('-s', dest='bbbSec', metavar='BBBSEC', required=True, help='BigBlueButton API Secret')
parser.add_argument('-r', dest='bbbRoom', metavar='BBBROOM', required=False, help='BigBlueButton room name',
                    default=None)
parser.add_argument('-n', dest='bbbLinks', metavar='BBBLINKS', required=False, help='BigBlueButton number of links',
                    default=1, type=int)
parser.add_argument('-m', dest='bbbModerator', metavar='BBBMOD', required=False, help='BigBlueButton moderator',
                    default="True")
args = parser.parse_args()

bbb = RoomUtil(args.bbbUrl, args.bbbSec)

if (args.bbbRoom == None):
    roomId = "room-{}".format(str(uuid.uuid4()))
else:
    roomId = args.bbbRoom

if args.bbbModerator.lower() in ('yes', 'true', 't', 'y', '1'):
    bbbModerator = True
else:
    bbbModerator = False

links = []
for i in range(args.bbbLinks):
    userName = "user-{}".format(str(uuid.uuid4()))
    links.append(bbb.getRoomUrl(roomId, userName, moderator=bbbModerator))

for l in links:
    logging.info(f"BBB Link: {l}")
