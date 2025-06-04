# Twitch Leaderboard Scraper
### Version 2.0.1

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

## Config.ini options explained

# 🛠️ `config.ini` Reference

This file controls behavior of the Twitch Leaderboard Scraper. Below is a detailed explanation of each section and its options.

---

## `[DEFAULT]`
These values are used internally for updating and startup logic. Do **not** modify unless you understand the update mechanisms.

| Key | Description |
|-----|-------------|
| `Version` | Current script version string. Used for internal reference. |
| `chromedriver_latest` | URL pointing to Google's latest stable ChromeDriver version tag. |
| `chromedriver_mirror` | Base path to the mirror for ChromeDriver ZIPs (used during updates). |
| `chromedriver_version` | JSON endpoint for querying latest known-good versions of ChromeDriver. |
| `Streamer` | Default Twitch chat popout URL (used if not overridden in `[TWITCH_SETTINGS]`). |
| `output_dir` | Path to save screenshots. Defaults to a public pictures folder. |
| `delay_init` | Delay (in seconds) after browser launch before performing first action. |
| `delay_screenshots` | Delay (in seconds) between screenshots and rotate actions. |

---

## `[TWITCH_SETTINGS]`
Used to override the stream chat popout URL.

| Key | Description |
|-----|-------------|
| `Streamer` | (Optional) Full URL to the Twitch chat popout for a specific streamer. If unset, the default is used. Example: `https://www.twitch.tv/popout/streamername/chat` |

---

## `[SCRAPER_SETTINGS]`
Controls scraping behavior, XPath definitions, and screenshot preferences.

| Key | Description |
|-----|-------------|
| `output_dir` | (Optional) Override the screenshot save path here. |
| `delay_screenshots` | Time (in seconds) to wait between screenshots and navigation steps. |
| `delay_init` | Time to wait after loading the page before taking any actions. Allows Twitch to finish rendering. |
| `show_popup` | Whether to show a desktop popup window on script success/failure. Set to `True` or `False`. |
| `enable_topclips` | Set to `True` to capture the “Monthly Top Clips” leaderboard. |
| `title_cheers` | Expected title string for the Cheerers leaderboard. Used for matching during rotation. |
| `title_gifters` | Expected title string for the Gifters leaderboard. |
| `title_clips` | Expected title string for the Top Clips leaderboard. |

### XPath Fields
Used by Selenium to locate elements on the Twitch chat popout page. These may change if Twitch updates its layout.

| Key | Description |
|-----|-------------|
| `leaderboard_title_xpath` | XPath to the currently displayed leaderboard title (used for comparison). |
| `expand_leaderboard_button_xpath` | XPath for the standard “expand leaderboard” button. |
| `rotate_leaderboard_button_xpath` | XPath to the button that rotates between leaderboards (e.g., Gifters → Cheerers → Clips). |
| `twitch_message_popup_xpath` | XPath to Twitch’s in-window popup (e.g., mod messages). If present, the alternate expand method is used. |
| `alt_expand_leaderboard_button_xpath` | Fallback XPath to be used for expanding leaderboard when the popup blocks the default button. |

---

## `[UPDATER_SETTINGS]`
Advanced configuration for the built-in ChromeDriver updater. Normally these mirror the `[DEFAULT]` values.

| Key | Description |
|-----|-------------|
| `chromedriver_latest` | (Optional) Override the default latest version tag URL. |
| `chromedriver_mirror` | (Optional) Override the ChromeDriver download base URL. |