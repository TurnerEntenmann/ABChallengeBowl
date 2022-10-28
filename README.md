# ABChallengeBowl
Allows easy entry and summarization of answer sheets from the Asses Builder Challenge Bowls.
## Steps to Download and Use
1. Download python
    1. Go to the [python website](https://www.python.org/downloads/) and download the version for your operating system.
    2. Open the .exe and install python. Make sure to check the *add python to path* button.
    3. Open a command prompt / powershell window and execute `pip install matplotlib, pandas, pylatex`
2. Download MiKTeX
    1. Go to the [MiKTeX website](https://miktex.org/download) and download the version for your operating system.
    2. Open the .exe and install MiKTeX normally. Make sure to answer *Yes* when asked to install missing modules on the fly.
    3. Open the MiKTeX app, check for and install any updates.
3. Folder Set Up
    1. Create a folder on your computer for the program and all the files it creates. For example in your `Documents` folder, create a new folder and name it "ABChallengeBowl".
4. Download the .py
    1. On this page, look for the "Releases" section on the right and click on the latest release.
    2. Click on the .zip link to download the files.
    3. Once downloaded, in your file explorer right-click the *.zip* folder and choose *Extract All...*
    4. This will create a new folder named something like `ABChallengeBowl-1.X`, go into it and copy all the files into the folder you made in step (3).
    5. You may now delete the *.zip* and the `ABChallengeBowl-1.X` folders leaving only the `ABChallengeBowl` folder with the files on your computer.
5. Using the program
    1. Open a command prompt / powershell window
    2. Open your file explorer and copy the path of your folder i.e. of `ABChallengeBowl`. This is done differently on different operating systems.
        1. On **Windows 10**, click the down arrow button just below the close window X button in the upper right corner of the window, then single click the folder so that it is highlighted and finish by clicking the *Copy path* button on the top of the window to the immediate right of the `Paste` button.
        2. On **Windows 11**, single-click the folder so that it is highlighted then right-click it and select `Copy as path`
        3. On a **Mac**, select the folder and then right-click it, when the context menu pops up, press and hold the Options key on the keyboard, then select the `Copy ... as Pathname` options where `...` is the name of the folder
        4. If you're on **Linux**, you probably already know how to do this but if you don't, google how to on your specific distro.
    3. In the command prompt /  powershell window, type in `cd` then a space then paste the path and hit enter, the full command will look something like `cd "C:\Users\Owner\Documents\ABChallengeBowl"`
    4. To launch the program, type in (or copy and paste) `python ABChallengeBowl.py` and hit the enter button.
## How to Update:
1. Copy the `Answer_Sets` folder into your `Documents` folder.
2. Delete the `ABChallengeBowl` folder.
3. Repeat step (4) from the "Steps to Download and Use" section above.
4. Copy and paste the `Answer_Sets` folder back into the new `ABChallengeBowl` folder.
## Notes:
1. Steps 1-4 only need to be done once (and only if you dont have python or MiKTeX already downloaded).
2. When summarizing for the first time, the program will look like it has frozen, this is because MiKTeX is downloading and installing a lot of packages in the background, this is normal and should take ~5-10 minutes. All subsiquent summarizations will be much quicker.
