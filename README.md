# Twitch Leaderboard Scraper
### Version 2.0.0

## Uses:
For archival uses. Tool will open the configured twitch channels' chat in a browser window, expands the <br>
leaderboards for both Bits and Gifts/gifted subs and takes a screenshot of each. Does not use the Twitch API <br> 
in any way. Instead we use the Chromedriver library (https://chromedriver.chromium.org/). 

## Features: 
1. Automatic updates
2. User configurable options
3. Writen in python with standalone exe for ease of use


## How to use it
1. Download the ***TwitchBitScraper_v2.0.1.zip*** from Releases. <br>
2. Unzip to desired location(it is recommended to override existing version of conifg.ini in this release due to additional options being added). 
3. Add your desired twitch stream to the *TWITCH_SETTINGS* section of the conifg.ini file. <br> (example: https://www.twitch.tv/popout/yourchannelhere/chat)
4. Change *output_dir* under *SCRAPER_SETTINGS* (make sure to put a \ at the end of your path!)
5. (Optional) Change show_popup to True in config.ini if you wish to see a popup each time tool is run. 



## Troubleshooting
Each time tool is run, it will log all actions to the error.log in the same directory as the tool. If your screenshots <br> 
are not being saved or it seems as if it is not doing anything, check the error.log for details. 

The most common error is not having the config.ini in the same directory as the tool exe. The tool will not <br> 
function without the ini file present. 

## Error Messages
"Message: session not created: This version of ChromeDriver only supports Chrome version 123" - This means your chrome browser is out of update. Please update your browser and try again (this tool does not invoke chrome browser updates). 

