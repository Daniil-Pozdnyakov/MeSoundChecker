# MESoundChecker
Program for auto check New Relic and Pingdom. Created for Monitoring team.

Installation:
1. Download project and unpack.
2. Move project folder (MESoundChecker into MeSoundChecker-main) to your home folder.

Example:
  
  MacOS:
    
Use Finder panel. Select "Go" > "Home" for install ![MacOS Finder panel](https://www.cnet.com/a/img/nv6yIA6MZtMm7NV9hs4ZkK2Pqto=/2017/01/27/e5d49edd-f9c8-4e3a-b211-5a91d07526c1/go-home.jpg)
    
3. Open project folder and **change code, where have comments # about login, password and url in "main.py"** (You can open that with TextEdit. Use right mouse button and select "Open With" > TextEdit)
5. Open terminal and install Selenium module ```pip install selenium```
6. Open terminal and use ```cd MESoundChecker``` 
7. Use ```python main.py```
8. Profit!

That script check service every minute. Duration after start: 1 - 1.5 minutes. That normal, just wait and after full run push up terminal window. You can see all information in terminal.

- Last update: last check time
- Ignore list: contains services where sound alert not need (You can add services in code search list "ignore_list" in "def main()". And you can add service after alert). You continue see services in "Down Pingdom" and in "Down New Relic".
- Warning list: Services and down time. After 5 minutes will launch alert. Ignoring services not can show in that list.
- Down on New Relic: down New Relic services
- Down on Pingdom: down Pingdom services

Alert will run "audio.mp3" in project folder. You can replace sound on another with "audio.mp3" name.

After alert you need send any key in terminal and sound will turn off. After terminal will offer to add the service to the ignore list. Reboot programm for clear ignore list. For add send 'y' key. Else send another key and wait after minute new information about last check.

Script created by Daniil Pozdnyakov. Search me in chats or message me for help on pozd20001@yandex.ru
