from bigbluebutton_api_python import BigBlueButton

b = BigBlueButton('https://bbbackend02.bastelgenosse.de', 'J34qRjDPwzLTOhtdfUe3ISJ6Ms6f6diSh6pgmOsw6q')

#params
dict = { 'moderatorPW':'pw' }
#use create meeting
print(b.create_meeting ('room',params=dict))
#get info
print(b.get_meeting_info('room'))
#get url
print(b.get_join_meeting_url('user','fake2', 'pw'))
