import os
import requests
from bs4 import BeautifulSoup
from pathlib import Path

roms_dir = '/run/media/SN01T/Emulation/roms/'
systems_xml_path = '~/ES-DE/custom_systems/es_systems.xml'

# Based on the actual ROM download url, change the url below to correct urls.
snes_url   = 'XXXXXXX'
nes_url    = 'XXXXXXX'
n64_url    = 'XXXXXXX'
gb_url     = 'XXXXXXX'
gbc_url    = 'XXXXXXX'
gba_url    = 'XXXXXXX'
gc_url     = 'XXXXXXX'
nds_url    = 'XXXXXXX'
n3ds_url   = 'XXXXXXX'
wii_url    = 'XXXXXXX'
wiiu_url   = 'XXXXXXX'
psx_url    = 'XXXXXXX'
ps2_url    = 'XXXXXXX'
psp_url    = 'XXXXXXX'
psvita_url = 'XXXXXXX'
dc_url     = 'XXXXXXX'
rom_urls = [
    snes_url, nes_url, n64_url, gb_url, gbc_url, gba_url ,gc_url, nds_url,
    n3ds_url, wii_url, wiiu_url, psx_url, ps2_url, psp_url, psvita_url, dc_url
]

def read_files(url):
    # Send a GET request to the URL
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find al the <a> tags with href attributes
        links = soup.find_all('a', href=True)
        print(f'Response received from url {url} with {len(links)} unfiltered links')

        usaTag = '(USA'
        filteredWords = ['(Beta)', '(Beta 1)', '(Beta 2)', '(Beta 3)', '(Rev 1)', '(Arcade)', '(Proto)', '(Proto 1)', '(Proto 2)', '(Sample)', '(Rev 2)', '(Rev 3)', '(Competition Cart', '(Pirate)', '(Demo)']
        accepted_file_extensions = ['.zip', '.7z', '.wua']

        # Filter only USA full version files + allowed extensions - excluded words
        zip_links = []
        for link in links:
            if not any(w in link.text for w in filteredWords) and any(extension in link['href'] for extension in accepted_file_extensions) and usaTag in link.text:
                zip_links.append(Path(link.text).stem)

        libraryPath = f'{roms_dir}romlibrary'
        print(f'Library path: {libraryPath}')
        if not os.path.exists(libraryPath):
            os.makedirs(libraryPath)
        else:
            print(f'Library path already exists, skipping mkdir.')

        if snes_url in url:         
            consolePath = libraryPath + '/snes'
        elif nes_url in url:
            consolePath = libraryPath + '/nes'
        elif n64_url in url:
            consolePath = libraryPath + '/n64'
        elif gb_url in url:
            consolePath = libraryPath + '/gb'
        elif gbc_url in url:
            consolePath = libraryPath + '/gbc'
        elif gba_url in url:
            consolePath = libraryPath + '/gba'
        elif gc_url in url:
            consolePath = libraryPath + '/gc'
        elif nds_url in url:
            consolePath = libraryPath + '/nds'
        elif n3ds_url in url:
            consolePath = libraryPath + '/n3ds'
        elif wii_url in url:
            consolePath = libraryPath + '/wii'
        elif wiiu_url in url:
            consolePath = libraryPath + '/wiiu'
        elif psx_url in url:
            consolePath = libraryPath + '/psx'
        elif ps2_url in url:
            consolePath = libraryPath + '/ps2'
        elif psp_url in url:
            consolePath = libraryPath + '/psp'
        elif psvita_url in url:
            consolePath = libraryPath + '/psvita'
        elif dc_url in url:
            consolePath = libraryPath + '/dreamcast'
        else:
            print('URL not recognized. Can\'t create console path.')

        print(f'Console path: {consolePath}')

        if not os.path.exists(consolePath):
            os.makedirs(consolePath)
        else:
            print('Console path dir already exists, skipping mkdir.')

        print(f'Creating download files for {len(zip_links)} games')
        
        for title in zip_links:
            with open(consolePath + '/' + title + '.py', 'w') as f:
                f.write(
                    'import os\n'
                    'import requests\n'
                    'from bs4 import BeautifulSoup\n'
                    'from pathlib import Path\n'
                    'import zipfile\n'
                    'import py7zr\n'
                    '\n'
                    'if \'snes\' in str(os.path.abspath(__file__)):\n'
                    f'   url = \'{snes_url}\'\n'
                    f'   file_path = \'{roms_dir}snes\'\n'
                    'elif \'nes\' in str(os.path.abspath(__file__)):\n'
                    f'   url = \'{nes_url}\'\n'
                    f'   file_path = \'{roms_dir}nes\'\n'
                    'elif \'n64\' in str(os.path.abspath(__file__)):\n'
                    f'   url = \'{n64_url}\'\n'
                    f'   file_path = \'{roms_dir}n64\'\n'
                    'elif \'gb\' in str(os.path.abspath(__file__)):\n'
                    f'   url = \'{gb_url}\'\n'
                    f'   file_path = \'{roms_dir}gb\'\n'
                    'elif \'gbc\' in str(os.path.abspath(__file__)):\n'
                    f'   url = \'{gbc_url}\'\n'
                    f'   file_path = \'{roms_dir}gbc\'\n'
                    'elif \'gba\' in str(os.path.abspath(__file__)):\n'
                    f'   url = \'{gba_url}\'\n'
                    f'   file_path = \'{roms_dir}gba\'\n'
                    'elif \'gc\' in str(os.path.abspath(__file__)):\n'
                    f'   url = \'{gc_url}\'\n'
                    f'   file_path = \'{roms_dir}gc\'\n'
                    'elif \'nds\' in str(os.path.abspath(__file__)):\n'
                    f'   url = \'{nds_url}\'\n'
                    f'   file_path = \'{roms_dir}nds\'\n'
                    'elif \'n3ds\' in str(os.path.abspath(__file__)):\n'
                    f'   url = \'{n3ds_url}\'\n'
                    f'   file_path = \'{roms_dir}n3ds\'\n'
                    'elif \'wii\' in str(os.path.abspath(__file__)):\n'
                    f'   url = \'{wii_url}\'\n'
                    f'   file_path = \'{roms_dir}wii\'\n'
                    'elif \'wiiu\' in str(os.path.abspath(__file__)):\n'
                    f'   url = \'{wiiu_url}\'\n'
                    f'   file_path = \'{roms_dir}wiiu\'\n'
                    'elif \'psx\' in str(os.path.abspath(__file__)):\n'
                    f'   url = \'{psx_url}\'\n'
                    f'   file_path = \'{roms_dir}psx\'\n'
                    'elif \'ps2\' in str(os.path.abspath(__file__)):\n'
                    f'   url = \'{ps2_url}\'\n'
                    f'   file_path = \'{roms_dir}ps2\'\n'
                    'elif \'psp\' in str(os.path.abspath(__file__)):\n'
                    f'   url = \'{psp_url}\'\n'
                    f'   file_path = \'{roms_dir}psp\'\n'
                    'elif \'psvita\' in str(os.path.abspath(__file__)):\n'
                    f'   url = \'{psvita_url}\'\n'
                    f'   file_path = \'{roms_dir}psvita\'\n'
                    'elif \'dreamcast\' in str(os.path.abspath(__file__)):\n'
                    f'   url = \'{dc_url}\'\n'
                    f'   file_path = \'{roms_dir}dreamcast\'\n'
                    'else:\n'
                    '   print(\'Current directory not recognized.\')\n'
                    '\n'
                    'response = requests.get(url)\n'
                    '\n'
                    'if response.status_code == 200:\n'
                    '   soup = BeautifulSoup(response.content, \'html.parser\')\n'
                    '   links = soup.find_all(\'a\', href=True)\n'
                    '\n'
                    '   zip_links = []\n'
                    '   for link in links:\n'
                   f'       if any(extension in link[\'href\'] for extension in {accepted_file_extensions}):\n'
                    '           zip_links.append(link)\n'
                    '\n'
                    '   for link in zip_links:\n'
                    '       link_text = Path(link.text).stem\n'
                    '       if link_text in str(os.path.basename(__file__)).rstrip(\'.py\'):\n'
                    '           full_url = url + \'/\' + link[\'href\']\n'
                    '           download_response = requests.get(full_url)\n'
                    '           if download_response.status_code == 200:\n'
                    '               with open(file_path + \'/\' + link.text, \'wb\') as f:\n'
                    '                   f.write(download_response.content)\n'
                    '               print(\'Download successful.\')\n'
                    '\n'
                    '               downloaded_file = file_path + \'/\' + link.text\n'
                    '               if downloaded_file.endswith(\'.zip\'):\n'
                    '                   with zipfile.ZipFile(downloaded_file, \'r\') as f:\n'
                    '                       f.extractall(file_path)\n'
                    '                   os.remove(downloaded_file)\n'
                    '               elif downloaded_file.endswith(\'.7z\'):\n'
                    '                   with py7zr.SevenZipFile(downloaded_file, mode=\'r\') as f:\n'
                    '                       f.extractall(path=file_path)\n'
                    '                   os.remove(downloaded_file)\n'
                    '               break\n'
                    '           else:\n'
                    '               print(\'Failed to download.\')\n'
                    '               break\n'
                    'else:\n'
                    '   print(\'Game not found in HTML.\')\n'
                )
                
    else:
        print('Request failed..')


def addLibrary():
    xmlPath = os.path.expanduser(systems_xml_path)
    print(f'Systems XML Path: {xmlPath}')
    with open(xmlPath, 'r') as xml_file:
        xml_content = xml_file.read()

    libraryContent = f'''
        <system>
            <name>romlibrary</name>
            <fullname>ROM Library</fullname>
            <path>%ROMPATH%/romlibrary</path>
            <extension>.py</extension>
            <command>/bin/bash {os.path.expanduser('~/rom-library/download.sh')} '%ROM%'</command>
            <theme>library</theme>
        </system>
    '''

    startTag = xml_content.find('<systemList>')
    endTag = xml_content.find('</systemList>')

    if libraryContent not in xml_content:
        if startTag != -1 and endTag != -1:
            xml_content_modified = xml_content[:endTag] + libraryContent + xml_content[endTag:]
            with open(xmlPath, 'w') as xml_file:
                xml_file.write(xml_content_modified)
        else:
            print('Unable to find valid es_systems.xml')
    else:
        print('<system> entry already added to es_systems.xml.')


# Initialize ROM Library in es_systems.xml then export download ROM python scripts for each system
addLibrary()

for url in rom_urls:
    if url not in 'XXXXXXX':
        read_files(snes_url)
