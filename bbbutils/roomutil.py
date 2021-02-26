import json
import logging
import uuid

from bigbluebutton_api_python import BigBlueButton

class RoomUtil:

    def __init__(self, bbbUrl, bbbSecret):
        logging.info("setup BBB connection")
        self.bbb = BigBlueButton(bbbUrl, bbbSecret)

    def __existRoom(self, roomId):
        try:
            self.bbb.get_meeting_info(roomId)
            return True
        except:
            return False

    def getRoomUrl(self, roomId, username="user-{}".format(str(uuid.uuid4())), moderator=False):
        # logging.info("getRoomUrl with roomId: {}".format(roomId))
        if not self.__existRoom(roomId):
            attendeePW = str(uuid.uuid4())
            moderatorPW = str(uuid.uuid4())
            dict = {'attendeePW': attendeePW, 'moderatorPW': moderatorPW}
            self.bbb.create_meeting(roomId, params=dict)
        else:
            meetingInfoR = self.bbb.get_meeting_info(roomId)
            meetingInfo = meetingInfoR.get_meetinginfo()
            attendeePW = meetingInfo.get_attendeepw()
            moderatorPW = meetingInfo.get_moderatorpw()

        if (moderator):
            userPw = moderatorPW
        else:
            userPw = attendeePW

        meetingInfoJson = self.bbb.get_meeting_info(meeting_id=roomId)
        logging.debug(json.dumps(meetingInfoJson, indent=1))

        return self.bbb.get_join_meeting_url(username, roomId, userPw)
