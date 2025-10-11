
# Update Logs(Development Build V.7.75)

# Hello! This is an old project being reworked, everything is under construction so no pull requests at this time. (previous Commits 39+)

# Recent update-logs



- I am back for my hiatus, with that being said todays update brought in more finalizations to subscription payment features. You can now cancel your subscription, implemented
a date time feature to indicate the expiration of your current subscription. More QOL to make the website sophisticated. I also cleaned up the read me because we had a lot of version changes on one page, Im gonna keep it short and simple and only announce major changes as I am finally nearing the end of development.



- 7.7 Log (2 part/2 day update)

--(7.7) Stripe WebHook now implemented (day 1)

--(7.7) Cleaned up choice page, also removed unecessary back end code that involved hard coded checks for premium users (day 1)

--(7.7) Back-end function names renamed to accomadate clean architecture. No more confusion! (day 2)

--(7.75) Stripe WebHook now fully works and now each user will have unique id's towards their subscription to prevent confusion, no more email checks. This took around 3-4 hours
of debugging because I just could not find out why my webhook was exiting early. Now it works and not i'll be on my haitus for a few days lol (day 2)



- (complete patch 2 of 4 next)


# Next Update 7.8

- ???



# URGENT

- N̶e̶x̶t̶ ̶I̶'̶l̶l̶ ̶f̶o̶c̶u̶s̶ ̶o̶n̶ ̶t̶h̶e̶ ̶f̶r̶o̶n̶t̶-̶e̶n̶d̶ ̶i̶n̶ ̶t̶e̶r̶m̶s̶ ̶o̶f̶ ̶d̶i̶s̶p̶l̶a̶y̶ ̶i̶s̶s̶u̶e̶s̶,̶ ̶s̶o̶ ̶i̶'̶l̶l̶ ̶f̶i̶x̶ ̶b̶e̶i̶n̶g̶ ̶a̶b̶l̶e̶ ̶t̶o̶ ̶c̶r̶e̶a̶t̶e̶ ̶g̶u̶e̶s̶t̶ ̶w̶h̶i̶l̶e̶ ̶y̶o̶u̶'̶r̶e̶ ̶l̶o̶g̶g̶e̶d̶ ̶i̶n̶,̶ ̶a̶n̶d̶ ̶a̶l̶s̶o̶ ̶m̶a̶k̶e̶ ̶i̶t̶ ̶s̶o̶ ̶y̶o̶u̶ ̶c̶a̶n̶ ̶O̶N̶L̶Y̶ ̶p̶a̶y̶ ̶f̶o̶r̶ ̶p̶r̶e̶m̶i̶u̶m̶ ̶i̶f̶ ̶y̶o̶u̶ ̶d̶o̶ ̶h̶a̶v̶e̶ ̶a̶n̶ ̶a̶c̶c̶o̶u̶n̶t̶ ̶a̶n̶d̶ ̶a̶r̶e̶n̶'̶t̶ ̶a̶ ̶g̶u̶e̶s̶t̶. 

-  ̶a̶l̶s̶o̶ ̶m̶a̶k̶e̶ ̶i̶t̶ ̶s̶o̶ ̶i̶f̶ ̶g̶u̶e̶s̶t̶ ̶i̶s̶ ̶e̶x̶p̶i̶r̶e̶d̶ ̶R̶E̶M̶O̶V̶E̶ ̶t̶h̶e̶ ̶a̶c̶c̶o̶u̶n̶t̶ ̶a̶n̶d̶ ̶d̶e̶a̶u̶t̶h̶ ̶t̶h̶e̶ ̶u̶s̶e̶r̶

- c̶r̶e̶a̶t̶e̶ ̶t̶r̶a̶n̶s̶f̶e̶r̶ ̶f̶e̶a̶t̶u̶r̶e̶ ̶s̶o̶ ̶g̶u̶e̶s̶t̶s̶ ̶c̶a̶n̶ ̶t̶r̶a̶n̶s̶f̶e̶r̶ ̶o̶v̶e̶r̶ ̶a̶n̶d̶ ̶c̶r̶e̶a̶t̶e̶ ̶a̶ ̶n̶e̶w̶ ̶a̶c̶c̶o̶u̶n̶t̶ ̶

- finish payment subscriptions, if user does not pay by due date take away their benefits and have them repay to continue their subscription (98%, finish subscription editing/cancellation)

- when guest page expires force reload

- fix log out button on home page. Still makes u delete account even if you're not guest

- finish updating cache, so user timer doesn't reset.

- instead of having a manage account button, I'll create a profile dropdown menu for all users so they can edit avatars, manage subscriptions, customize etc. (45%)

- Link subscription time to back-end (stripes time)

- rewrite front home page, some things are placeholders but I am nearing the end of development so gotta make everything look sophisticated.

- Fix storage issues (shows negative on unlimited plan, visual bug)



- add guest feature (100%) 

- finish user auth, add some customization, privacy safety, deploy (15%)

- Storage system (pretty easy to implement but i'd like to add a progress bar showcasing how much remaining storage you have, (unlimited if you got premium)) (100%) 

- System for other file formats?? Not just MP4 and Images (50%)



# Board Updates (Coming Soon)

- Implement GB Limits

- Visual Improvements

- More File Types EX. PDF, TXT, Any 


# QOL (Soon)

- Make it so if user is not authenticated, the pricing for basic says "Sign-up"

- Resize Alerts make them more seamless

- Real time countdown for guests (Least priority, can be finished after deployment)



^ my entire checklist that needs to get done after that we complete and bring back log in pages and log out pages and tie them into my current system. After that expand upon em and add profile pictures and such, along with some well needed updates on the board with the users name "Hello, username", as well as their profile picture showing up! (guests won't have these features)
