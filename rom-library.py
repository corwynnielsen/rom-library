import os
import requests
from bs4 import BeautifulSoup
from pathlib import Path

roms_dir = "/run/media/SN01T/Emulation/roms/"
systems_xml_path = "~/ES-DE/custom_systems/es_systems.xml"

# Based on the actual ROM download url, change the url below to correct urls.
snes_url   = "XXXXXXX"
nes_url    = "XXXXXXX"
n64_url    = "XXXXXXX"
gb_url     = "XXXXXXX"
gbc_url    = "XXXXXXX"
gba_url    = "XXXXXXX"
gc_url     = "XXXXXXX"
nds_url    = "XXXXXXX"
n3ds_url   = "XXXXXXX"
wii_url    = "XXXXXXX"
wiiu_url   = "XXXXXXX"
psx_url    = "XXXXXXX"
ps2_url    = "XXXXXXX"
psp_url    = "XXXXXXX"
psvita_url = "XXXXXXX"
dc_url     = "XXXXXXX"
rom_urls = [
    snes_url, nes_url, n64_url, gb_url, gbc_url, gba_url ,gc_url, nds_url,
    n3ds_url, wii_url, wiiu_url, psx_url, ps2_url, psp_url, psvita_url, dc_url
]

def read_files(url):
    # Send a GET request to the URL
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        # Find al the <a> tags with href attributes
        links = soup.find_all("a", href=True)
        print(f"Response received from url {url} with {len(links)} unfiltered links")

        usaTag = "(USA"
        filteredWords = ["(Beta)", "(Beta 1)", "(Beta 2)", "(Beta 3)", "(Rev 1)", "(Arcade)", "(Proto)", "(Proto 1)", "(Proto 2)", "(Sample)", "(Rev 2)", "(Rev 3)", "(Competition Cart", "(Pirate)", "(Demo)"]
        accepted_file_extensions = [".zip", ".7z", ".wua"]

        # Filter only USA full version files + allowed extensions - excluded words
        zip_links = []
        for link in links:
            if not any(w in link.text for w in filteredWords) and any(extension in link["href"] for extension in accepted_file_extensions) and usaTag in link.text:
                zip_links.append(link)

        libraryPath = f"{roms_dir}romlibrary"
        print(f"Library path: {libraryPath}")
        if not os.path.exists(libraryPath):
            os.makedirs(libraryPath)
        else:
            print(f"Library path already exists, skipping mkdir.")

        if snes_url == url:         
            consolePath = libraryPath + "/snes"
        elif nes_url == url:
            consolePath = libraryPath + "/nes"
        elif n64_url == url:
            consolePath = libraryPath + "/n64"
        elif gb_url == url:
            consolePath = libraryPath + "/gb"
        elif gbc_url == url:
            consolePath = libraryPath + "/gbc"
        elif gba_url == url:
            consolePath = libraryPath + "/gba"
        elif gc_url == url:
            consolePath = libraryPath + "/gc"
        elif nds_url == url:
            consolePath = libraryPath + "/nds"
        elif n3ds_url == url:
            consolePath = libraryPath + "/n3ds"
        elif wii_url == url:
            consolePath = libraryPath + "/wii"
        elif wiiu_url == url:
            consolePath = libraryPath + "/wiiu"
        elif psx_url == url:
            consolePath = libraryPath + "/psx"
        elif ps2_url == url:
            consolePath = libraryPath + "/ps2"
        elif psp_url == url:
            consolePath = libraryPath + "/psp"
        elif psvita_url == url:
            consolePath = libraryPath + "/psvita"
        elif dc_url == url:
            consolePath = libraryPath + "/dreamcast"
        else:
            print("URL not recognized. Can't create console path.")

        print(f"Console path: {consolePath}")
        console = os.path.basename(os.path.normpath(consolePath))

        if not os.path.exists(consolePath):
            os.makedirs(consolePath)
        else:
            print("Console path dir already exists, skipping mkdir.")

        print(f"Creating download files for {len(zip_links)} games")
        
        for link in zip_links:
            filename = Path(link.text).stem
            with open(f"{consolePath}/{filename}.py", "w") as f:
                f.write(
                    "import os\n"
                    "import requests\n"
                    "import zipfile\n"
                    "import py7zr\n"
                    "\n\n"
                    f"if '{console}' in str(os.path.abspath(__file__)):\n"
                    f"    if '{console}' == 'wiiu':\n"
                    f"        file_path = '{roms_dir}{console}/roms'\n"
                     "    else:\n"
                    f"        file_path = '{roms_dir}{console}'\n"
                    "else:\n"
                     "     print('Current directory not recognized.')\n"
                    f"download_response = requests.get('{url}/{link['href']}')\n"
                     "if download_response.status_code == 200:\n"
                    f"    with open(file_path + '/' + \"{link.text}\", 'wb') as f:\n"
                     "        f.write(download_response.content)\n"
                     "    print('Download successful.')\n"
                    f"    downloaded_file = file_path + '/' + \"{link.text}\"\n"
                     "    if downloaded_file.endswith('.zip'):\n"
                     "        with zipfile.ZipFile(downloaded_file, 'r') as f:\n"
                     "            f.extractall(file_path)\n"
                     "        os.remove(downloaded_file)\n"
                     "    elif downloaded_file.endswith('.7z'):\n"
                     "        with py7zr.SevenZipFile(downloaded_file, mode='r') as f:\n"
                     "            f.extractall(path=file_path)\n"
                     "        os.remove(downloaded_file)\n"
                     "else:\n"
                     "    print('Failed to download.')\n"
                )
                
    else:
        print("Request failed..")


def addLibrary():
    xmlPath = os.path.expanduser(systems_xml_path)
    print(f"Systems XML Path: {xmlPath}")
    with open(xmlPath, "r") as xml_file:
        xml_content = xml_file.read()

    libraryContent = f"""
        <system>
            <name>romlibrary</name>
            <fullname>ROM Library</fullname>
            <path>%ROMPATH%/romlibrary</path>
            <extension>.py</extension>
            <command>/bin/bash {os.path.expanduser("~/rom-library/download.sh")} "%ROM%"</command>
            <theme>library</theme>
        </system>
    """

    startTag = xml_content.find("<systemList>")
    endTag = xml_content.find("</systemList>")

    if libraryContent not in xml_content:
        if startTag != -1 and endTag != -1:
            xml_content_modified = xml_content[:endTag] + libraryContent + xml_content[endTag:]
            with open(xmlPath, "w") as xml_file:
                xml_file.write(xml_content_modified)
        else:
            print("Unable to find valid es_systems.xml")
    else:
        print("<system> entry already added to es_systems.xml.")


# Initialize ROM Library in es_systems.xml then export download ROM python scripts for each system
addLibrary()

for url in rom_urls:
    if url not in "XXXXXXX":
        read_files(url)
