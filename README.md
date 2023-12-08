# YA-FAH Stats Website
#### Video Demo:  TODO
#### Description:
[![wakatime](https://wakatime.com/badge/user/a74de5a2-6029-42fc-af5a-6c68022b44ae/project/018baf29-6c05-4cd2-b960-a2952007eeba.svg)](https://wakatime.com/badge/user/a74de5a2-6029-42fc-af5a-6c68022b44ae/project/018baf29-6c05-4cd2-b960-a2952007eeba)

The name stands for yet another foldingathome stats website. If you do not know what folding at home (abbreviated as FAH) is, you should checkout their [website](https://foldingathome.org/). TLDR is it is a project to simulate how proteins interact with each other, and cause problems. It works by many people contributing their idle usage to running these simulations to help find cures for diseases. As people contribute to these simulations, they get points to gameify the idea.

My website, using FAH's api, creates charts to visualize a specific user's points in ways that I find more useful over the othera (still grea)t FAH stats websites.

These stats are saved in a database, I used [planetscale](https://planetscale.com/) so the data could be accessed remotely from different I may run this on. The website itself is built using [flask](https://flask.palletsprojects.com/). I wanted to use a diffeent framework, but flask was much faster to do the things I wanted it to do because of using it during CS50. The CSS in this website is generated using [tailwindcss](https://tailwindcss.com/). This may seem like a odd choice, but I heard a lot of great things about it, and I really liked how easy it was to make things look how I want it to look, without having to look it up. It was very intuative.

Here's how to use the website as it is right now. The url is at [folding.aamira.me](folding.aamira.me), this may change. You will be redireced to /user. I hope to implement team statistics soon. (See the list of extra goals) There will be a form to enter your folding@home username, if you do not know your username, you probably need to create a [passkey](https://foldingathome.org/support/faq/points/passkey/) first. Enter you username (or id, if you know it) and two graphs will populate (they may take a second to pop up, be patient). But at first, they will be empty. That is because I just made this website, and I have not been logging every user's statiscics. If you want to add your user to the list to be saved, click the add user to auto save button once you submit the username form. Once you do this, every day, at 11:59 GMT (All times on this website are in GMT) your user stats will be saved. If you manually want to trigger this save, click the save data checkbox in the username form. Now you should see two graphs. The first one is your daily statistics. This is how many points you earned for a given day. You can look at the controls to interact with the graph, you can also zoom with scroll wheel. Hover over each point to find out the specific data. Next graph is your total points (since you added yourself to the auto save list). If there is any issue, feel free to make a issue.

List of (extra) features to implement:
- [X] Daily user stats
- [ ] Team stats
- [ ] Compare users
- [ ] Remember user based on session

My [CS50](https://pll.harvard.edu/course/cs50-introduction-computer-science) final project.
