# BulletinBoard

Description: This is a bulletin board system that allows users to connect to it using a terminal program and perform various functions. 

Technology used: We used python because, for our group members, it was the easiest way for us to visualize the client-server side interactions using socket programming. 

Challenges faced:The main problem that we faced was getting part 1, which is the public message board portion of the code and part2, which is the private message board portion, to work seamlessly. The other main problem that we faced was getting the client and server side code to work properly and seeing the relationship between the two and how they were supposed to interact. Both of these issues caused us the most issues and are what took the most amount of time to get working properly. We still have some things that could be improved. Extra: we also faced issues when trying to implement the GUI, so much so that we decided to completely scrap the idea of doing it as it was too difficult for us.

Instructions:
(Assuming person is using Visual Studios(VS))
I. run the server in the VS code terminal then run the client in one(or more depending on the # of users) new terminal
II. *When using the commands, the % is necessary before every command*
III. enter "%connect 127.0.0.1 12340" (do not include quotation marks)
IV. enter the name you want to use
V. Enter whichever command you would like to use, key to start with either %join(public) and/or %groupjoin <Group#>(private)
VI. From here you can choose from a list of commands, including: %join, %post, %users, %leave, %message, %exit, %groups, %groupjoin, %grouppost, %groupusers, %groupleave, %groupmessage
VII. Every one of these commands has a unique formatting for them to work properly.

