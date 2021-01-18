from Account import instagram
from Account import reddit
from Account import github
from Helpers import hunter
import pprint

x = int(input("1.Search by Name\n2.Search by Domain\n"))

if x==1:
    y = int(input("1.Github\n2.Reddit\n3.Instagram\n"))
    if y==1:
        pprint.pprint(github.github(input("Enter Username\n")))
    elif y==2:
        pprint.pprint(reddit.reddit(input("Enter Username\n")))
    elif y==3:
        pprint.pprint(instagram.instagram(input("Enter Username\n")))
else:
    pprint.pprint(hunter.hunter(input("Enter Domain\n")))