import os
import requests
import yaml
from bs4 import BeautifulSoup
from pathlib import Path

roms_dir = "/run/media/SN01T/Emulation/roms/"
systems_xml_path = "~/ES-DE/custom_systems/es_systems.xml"
rom_urls =  {}

with open(os.path.expanduser("rom-urls.yml")) as stream:
    try:
        rom_urls = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

def read_files(console, url):
    print(f"Creating download files for {console}")
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

        consolePath = f"{roms_dir}romlibrary/{console}"
        if not os.path.exists(consolePath):
            os.makedirs(consolePath)
        else:
            print("Console path dir already exists, skipping mkdir.")
        print(f"Console path: {consolePath}")
        
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

for console_key, url in rom_urls.items():
    if url not in "XXXXXXX":
        console = console_key.split("_")[0]
        read_files(console, url)
