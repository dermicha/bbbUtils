import argparse
import requests
import threading
import time
import uuid
from urllib.error import HTTPError

import logging

from bbbutils.roomutil import RoomUtil

logging.basicConfig(level=logging.INFO)
logging.info("bbbRoomUtil Loadtester")

parser = argparse.ArgumentParser(description='bbbRoomUtil Example')
parser.add_argument('-ho', dest='bbbHost', metavar='BBBHOST', required=True,
                    help='https://bbb.yourserver.com')
parser.add_argument('-p', dest='bbbPath', metavar='BBBPATH', required=True,
                    help='/bigbluebutton/')

parser.add_argument('-s', dest='bbbSec', metavar='BBBSEC', required=True, help='BigBlueButton API Secret')

parser.add_argument('-r', dest='bbbRooms', metavar='BBBROOMS', required=False, help='BigBlueButton number of rooms',
                    default=1000, type=int)
parser.add_argument('-u', dest='bbbUsers', metavar='BBBUSERS', required=False, help='BigBlueButton number of users',
                    default=30, type=int)

parser.add_argument('-t', dest='threads', metavar='THREADS', required=False, help='parallel threads',
                    default=100, type=int)
parser.add_argument('-td', dest='threadDelay', metavar='THREADDELAY', required=False,
                    help='delay between each thread (in ms)',
                    default=50, type=int)
parser.add_argument('-ud', dest='userDelay', metavar='USERDELAY', required=False,
                    help='delay between each user open his/her room URL (in ms)',
                    default=50, type=int)

args = parser.parse_args()

bbbHost = args.bbbHost
bbbPath = args.bbbPath
bbbUrl = "%s%s" % (bbbHost, bbbPath)

bbbRooms = args.bbbRooms
bbbUsers = args.bbbUsers
bbbThreads = args.threads
bbbThreadDelay = args.threadDelay
bbbUserDelay = args.userDelay

timings = []
threads = []
errors = 0

bbb = RoomUtil(bbbUrl, args.bbbSec)

def doTest(t, br, bu, ud, ts):
    global errors
    for ri in range(1, br + 1):
        roomName = "room_{}_{}".format(ri, str(uuid.uuid4()))
        for ui in range(1, bu + 1):
            userName = "user-{}".format(str(uuid.uuid4()))
            try:
                if ui == 1:
                    mod = True
                else:
                    mod = False
                userRoomUrl = bbb.getRoomUrl(roomName, userName, moderator=mod)
                # logging.info("({}) roomUrl: {}".format(str(t), userRoomUrl))

                time.sleep(ud / 1000)

                currentTime = time.time_ns()
                result = requests.get(userRoomUrl)
                ts.append(time.time_ns() - currentTime)

                if result.status_code >= 400:
                    errors += 1
                    logging.error("({}) get room failed".format(str(t)))

            except HTTPError as e:
                e_rrr = e.read()
                logging.error("({}) httpError: {}".format(str(t), e_rrr))
            except Exception as ex:
                logging.error("({}) error: {}".format(str(t), ex))


for t in range(1, bbbThreads + 1):
    x = threading.Thread(target=doTest, args=(t, bbbRooms, bbbUsers, bbbUserDelay, timings,))
    x.start()
    threads.append(x)
    time.sleep(bbbThreadDelay / 1000)

for th in threads:
    th.join()

logging.info("runs: {}".format(str(len(timings))))
logging.info("avg: {}".format(str(sum(timings) / len(timings) / 1000000)))
logging.info("min: {}".format(str(min(timings) / 1000000)))
logging.info("max: {}".format(str(max(timings) / 1000000)))

logging.info("errors: {}".format(errors))

