import requests, argparse, subprocess, sys, re, string
from bs4 import *

def main():
    # The preliminary setup requires getting the game directory from the user, and checking if it has the game executable in it.

    # TODO


    # First, the script needs to determine what the latest version of BepinEx is. This will be accomplished by scraping the latest release.
    print("Sending GET request to https://github.com/BepInEx/BepInEx/")
    result = requests.get('https://github.com/BepInEx/BepInEx')
    
    print("Response obtained, parsing to find latest release.")
    soup = BeautifulSoup(result.content, 'html.parser')
    latestRelease = soup.find_all('span', class_='css-truncate css-truncate-target text-bold mr-2')
    if latestRelease:
        for item in latestRelease:
            print(f"Latest release: {item.get_text()}")

            # Now, use that to find the latest release of BepinEx and download it.
            versionData_A = re.search(r"((?:[0-9]+\.)+[0-9]+)", item.get_text())
            if versionData_A:

                downloadURL = f"https://github.com/BepinEx/BepinEx/releases/download/{"v" + str(versionData_A.group(1))}/BepinEx_win_x64_{str(versionData_A.group(1))}.zip"
                print(f"Download URL: {downloadURL}")

                print("Downloading latest release. This might take a moment.")
                download = requests.get(downloadURL, stream=True)

                with open("bepinex_latest.zip", "wb") as bpxZip:
                    for chunk in download.iter_content(chunk_size=8192):
                        if chunk:
                            bpxZip.write(chunk)
                
                print("Download complete. File saved as bepinex_latest.zip.")

                # TODO: move file and extract it

            else:
                print("Error! Regex Fail.")
                sys.exit()
    else:
        print("Error! Could not find github repo for BepinEx. Something is going horribly wrong.")
        sys.exit()
    
    

    # Move it to the game folder and extract it.

    # Clean up.


main()