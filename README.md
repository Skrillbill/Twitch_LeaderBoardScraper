# Twitch Leaderboard Scraper
Version 3.0.0

## Uses
For archival purposes. This tool opens the configured Twitch channel’s chat in a browser window, expands the
leaderboards for both Bits and Gifted Subs, and takes a screenshot of each. 

This does not use the Twitch API in any way — it uses Chromedriver directly:  
https://chromedriver.chromium.org/

## Features
- Automatic Chromedriver updates
- User-configurable settings via config.ini
- Written in Python, distributed as a standalone .exe for easy use

## How to Use It
1. [Download the Latest Release](https://github.com/YourUsername/YourRepoName/releases/latest)
2. Unzip to a desired location. It’s recommended you override the existing `config.ini` with the new one included.
3. Uncomment any options / make any changes to config.ini(see below for full config.ini reference).


## Config.ini Options 


### [DEFAULT]
These values should not be changed directly. Uncomment the options you want to change under TWITCH_SETTINGS or
SCRAPPER_SETTINGS. 
```
Version                   = Internal version reference
chromedriver_latest       = Endpoint for latest stable release tag
chromedriver_mirror       = Download base URL for Chromedriver zip
chromedriver_version      = JSON endpoint for all release channels
Streamer                  = Twitch chat popout URL
output_dir                = Default screenshot output directory
delay_init                = Delay before first interaction (seconds)
delay_screenshots         = Delay between screenshots (seconds)
```

### [TWITCH_SETTINGS]
```
Streamer                  = Full Twitch chat popout URL for the desired streamer. If not specified, the default value is used. 
```

### [SCRAPER_SETTINGS]
```
output_dir                        = Directory where screenshots are saved
delay_screenshots                 = Delay between each screenshot (in seconds)
delay_init                        = Delay after loading stream before taking action (in seconds)
show_popup                        = If True, display a popup window on script completion
enable_topclips                   = If True, capture screenshot of the “Top Clips” leaderboard
title_cheers                      = Title to match for the cheerers leaderboard
title_gifters                     = Title to match for the gifters leaderboard
title_clips                       = Title to match for the top clips leaderboard

leaderboard_title_xpath           = XPath to the leaderboard title element
expand_leaderboard_button_xpath  = XPath to the default expand button
rotate_leaderboard_button_xpath  = XPath to rotate leaderboard views
twitch_message_popup_xpath       = XPath to detect annoying Twitch overlay popup
alt_expand_leaderboard_button_xpath = Fallback XPath to expand leaderboard if popup is present
```

### [UPDATER_SETTINGS]
```
chromedriver_latest        = (Optional override)
chromedriver_mirror        = (Optional override)
```

## Troubleshooting

If screenshots are not being saved or the tool seems to do nothing, check the `error.log` file.  
The most common issue is the tool not being able to find `config.ini`. Make sure the `.exe` and `config.ini` are in the same folder.

## Error Messages

**Message: session not created: This version of ChromeDriver only supports Chrome version 123**  
Your version of Chrome is out of date or incompatible with the current Chromedriver.  
Update Chrome and re-run the tool.
