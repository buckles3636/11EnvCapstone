from notify import Flag, TeleBot
from datetime import datetime

my_bot = TeleBot("ChamberStatusBot", "@chamber_status_bot", "8188655307:AAGeScy3L7QligWqJnyGN4JCnrkXvtBYUtg", "@incubatorstatus")

flag = Flag("Humidity", 90, 5.0, datetime.now(), "deviated", 10.0)

sum = 0
for i in range(10):
    now = datetime.now()
    report_string = flag.to_report()
    my_bot.send_message(report_string)
    delta = datetime.now() - now
    sum += delta.microseconds

print(sum/1000/10)