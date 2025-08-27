
# Update Logs(Development Build V.6.45)

# Hello! This is an old project being reworked, everything is under construction so no pull requests at this time. (previous Commits 39+)

# Recent update-logs

--(4.6) completely revamped how uploading and creating is handeled on the client side. I made it so it works all under one function, no more reloading to be able to hover/remove content.

--(4.6) fixed bugs, and removed code snippets that served no purpose. The user experience should be cleaner now, expect more revamps like these I want to completely overhaul the system to make it work in favor for the user!


--(4.7) Spent 3 hours fixing this but you can now dynamically upload, and remove at the same time without reloading the page. There was a problem with syncing backend data with the client because I just couldn't figure out HOW. But i found the answer and it was very simple! Expect the same for text as well on 4.8.


--(4.75) Finalized yesterday's changes and fixed some stuff that i missed regarding uploading. After today I think i'm fully ready to complete the main landing page then finish the log in system along with profile pictures : ) I really wanted to end off with something fun and something I'd think users would enjoy so profile pictures will be a thing along with obviously refactors and clean up to the back end to accomadate the new changes!

--(4.75) Started working on main landing page, added pricing description, and FAQ section. Also QOL on pricing Divs.

--(4.8) I'm back! landing page is now 10x better, compeleted FAQ section, Pricing Section, made some small adjustments on how things are displayed (more or less this is the best I got for now, I would outsource a landing page but releasing a fullstack application sounds cooler with my own landing page)

--(4.9) QOL on landing page, Nav bar now follows your scroll, you can now select pricing, faq etc. Opened a path towards my old sign in page just so you can visualize the old architecture of the website. This is nothing special, just to show what It used to look like and If an existing user has a log-in saved in the data base they can log in and start 
using their board. For now I'm working on a guest feature that allows users who aren't signed up to automatically go through and use all the features (upload content etc.) Although this may take some time as It's new content I've started working on it slowly and it's coming along well

--(4.95) Refactoring back-end, nothing besides hompage should work as of now. I decided to shutdown some processes so I can make sure to complete this new guest feature

--(5) Guest feature completed, now I just need to implement it on to the website when picking start free, I also will give a limited time notice to guest users as well, that their time is limited and they can only transfer so much etc. 

--(5.1) Huge improvements to the back-end data base, guest users now have an indicator, and also they now expire after 1 day instead of 7. To compensate for the day changes guest users are given 25 gb (the maximum that normal non-premium accounts are given). 

--(5.1) Fixed a small bug that wouldn't allow text uploads on your board to be hovered, this bug had made it so you had to reload the page to delete your text. But now thats fixed and everything should work real time...besides the small spacing bug which I'll fix in the next patch along with users being able to access guest accounts (hopefully, if not then i'll compensate by making sure the next new features are top tier in terms of QOL)

--(5.2) Huge Improvements to the board overall in terms of spacing. So i realized that i missed a crucial feature where if you remove an item it SHOULD respace all other items, i don't know how that even went over my head. Solo testing did wonders. Since I worked on this for today I'll make sure guest features are done in another patch as this patch is more focused on fixing inconsistent features and making sure there is consistency towards what the user is experiencing when using this application.


--(5.3) New front end features today, as promised guest users can now make accounts without signing up and now their time limit on their account is shown at the top. Front end is going to look more modern in the next few patches as I'm transitioning some css buttons. 

--(5.3) New page for choices, as stated above, you can now choose whether you want to be a guest or a new user. 

--(5.35) New button styling, new account deletion section to FAQ, buttons now work (most of them) although some don't work because I've yet to implement the feature that button takes you to

--(5.4) Update to back-end features/front-end. Your board now tracks how much data you have uploaded. This is just a framework of what i want so nothing really is working properly as it should but, this is how it should be before I put it all together.


--(5.5) Huge update to storage, you can now see your storage progress bar (bottom left). It gauges your usage based on the back end and displays. You can remove items and it will update real time. Today mostly was implementing yesterdays features, you should safely now be able to track your storage usage ETC. *Note: Premium User Storage is not implemented yet as I'm still testing and fixing bugs.

--(6) Fixed major bugs, cleaned up a lot of yesterdays work so now everything should work as intended and look much cleaner in terms of code. Mobile users now also can see the
progress bar. Added QOL feature to where if you upload more than 99MB it displays it as GB now. Now I just need to complete the  unlimited storage feature for premiums, and then we should be on our way to implementing that onto the website. Along with users finally being able to log-in/sign-up and content blocks for guest users. Just because I want people to sign up and have more of a personalized experienced, with this I'll lower guest storage limit to about 15. 


--(6.1) Revamped homepage a bit, added new payment page, premium features almost done. 

--(6.2) Finalized payment page, you can now test it out with fake information to gain premium for your account. Next update will be stripe integration and more secure measures to ensure the information that is entered in the payment page is secure and proper. Everything is coming along well and I'm almost certain that this will be complete and ready for a new release by the end of this month, as long as progress is smooth. 


--(6.3) Huge improvements to the project, This is my biggest update yet! I missed so much that I didn't realize I had to fix this before It became too late. The project is now in Development Build status, meaning there are heavy improvments and revamps going on through the back-end.

--(6.3) Removed extra junk files, stripe payment integrated, you can now test payments! changed how development was handled.

--(6.3) This took me a few hours but realized this project had been pointing to an old build, the settings.py was never updated and never had postgreSQL being used I believe. Thankfully after debugging I fixed most if not all things that were causing underlying hidden issues that I would have never found out.

--(6.4) Added auto-fill feature so now when the form at payment template is entered, the customers data will appear on checkout.

--(6.45) Quick update, once premium is paid for user should automatically gain the given benefits!


# Bugs that need fixing / Things being worked on:

- add guest feature (99%) -need to delete guests, -cooldown on how many someone can create to not allow overfill

- finish user auth, add some customization, privacy safety, deploy (15%)

- Real time countdown for guests (maybe) (0%)

- Storage system (pretty easy to implement but i'd like to add a progress bar showcasing how much remaining storage you have, (unlimited if you got premium)) (100%) 

- System for other file formats?? Not just MP4 and Images (50%)

- Make it so if user is not authenticated, the pricing for basic says "Sign-up"



