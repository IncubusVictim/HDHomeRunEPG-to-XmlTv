"""
Program to download the current EPG from an HDHomeRun Quattro box for the next 7 days into
an XMLTV formatted file.

I developed this so I could easily update the EPG on a Jellyfin media server that was linked
to an HDHomeRun Quattro.  The HDHomeRun Quattro hardware automatically maintains the EPG for
the channels it has tuned in, so it made sense to use this.

The HDHomeRun Quattro has a limitation of just over 7 days EPG, so trying to go beyond that
is pointless.
"""

import argparse
import datetime
import re
import requests
from requests.adapters import HTTPAdapter
import ssl
import sys
import xml.etree.ElementTree as ET
import unicodedata

__author__ = "Samantha Little"
__credits__ = ["Samantha Little"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Samantha Little"

# Defaults
urlHost = "hdhomerun.local"
epgFilename = "epg.xml"
scheduleDurationInDays = 7
hoursIncrement = 3
showLogInfo = "on"

# Create an adapter that forces TLS v1.2
class TLS12Adapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        context.options |= ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3  # Disable older SSL versions
        context.minimum_version = ssl.TLSVersion.TLSv1_2  # Enforce TLS v1.2
        kwargs["ssl_context"] = context
        return super().init_poolmanager(*args, **kwargs)

def clean_text(text: str) -> str:
    # Removes control characters
    text = "".join(ch for ch in text if unicodedata.category(ch)[0]!="C")

    # Removes feature tags such as [S], [S,SL], [AD] and [HD]
    text = re.sub(r'\[[A-Z,]+\]', '', text)

    # Removes season/episode information
    text = re.sub(r'\(?[SE]?\d+\s?Ep\s?\d+[\d/]*\)?', '', text)

    return text.strip()

# Logging
def log(type, text):
    now = datetime.datetime.today()
    if (type == "INFO" and (showLogInfo == "on" or showLogInfo == "full")) or (type == "DETAIL" and showLogInfo == "full"):
        print(type + " (" + str(now)[0:19] + "): " + text)
def logError(text):
    log("ERROR", text)
def logInfo(text):
    log("INFO", text)
def logDetail(text):
    log("DETAIL", text)

# Set up the session with the custom TLS 1.2 adapter
session = requests.Session()
session.mount("https://", TLS12Adapter())

# Set up all the command line parameters
parser = argparse.ArgumentParser(add_help=False, description="Program to download the HDHomeRun device EPG and convert it to an XMLTV format suitable for Jellyfin.")
parser.add_argument("--help", action="store_true", help="Show the command parameters available.")
parser.add_argument("--host", help="The host name or IP address of the HDHomeRun server if different from \"hdhomerun.local\".")
parser.add_argument("--filename", help="The file path and name of the EPG to be generated. Defaults to epg.xml in the current directory.")
parser.add_argument("--days", help="The number of days in the future from now to obtain an EPG for. Defaults to 7 but will be restricted to a max of about 14 by the HDHomeRun device.")
parser.add_argument("--hours", help="The number of hours of guide interation to obtain. Defaults to 3 hours.")
parser.add_argument("--debug", help="Switch debug log message on, options are \"on\", \"full\" or \"off\". Defaults to \"on\"")
showHelp = False
try:
    args = parser.parse_args()
except:
    showHelp = True
if (showHelp or args.help):
    parser.print_help()
    sys.exit(0)
if (args.host != None):
    urlHost = args.host
if (args.filename != None):
    epgFilename = args.filename
if (args.days != None):
    scheduleDurationInDays = int(args.days)
if (args.hours != None):
    hoursIncrement = int(args.hours)
if (args.debug != None and args.debug.lower() == "on"):
    showLogInfo = "on"
if (args.debug != None and args.debug.lower() == "off"):
    showLogInfo = "off"
if (args.debug != None and args.debug.lower() == "full"):
    showLogInfo = "full"

# Construct the HDHomeRun info Url's
deviceUrl = "http://" + urlHost + "/discover.json"
lineUpUrl = "http://" + urlHost + "/lineup.json"

logInfo("---------- Fetching HDHomeRun Web API Device Auth ----------")

# Get DeviceAuth the HDHomeRun device info
deviceResp = requests.get(deviceUrl)
if deviceResp.status_code != 200:
    logInfo("Device infor request failed: (" + deviceResp.status_code + ") " + deviceResp.reason)
    sys.exit()
deviceJson = deviceResp.json()
deviceAuth = deviceJson["DeviceAuth"]

logInfo("---------- Fetching HDHomeRun Web API Lineup ----------")

# Get the HDHomeRun channel line up info
lineUpResp = requests.get(lineUpUrl)
if lineUpResp.status_code != 200:
    logInfo("Device infor request failed: (" + lineUpResp.status_code + ") " + lineUpResp.reason)
    sys.exit()
lineUpJson = lineUpResp.json()

logInfo("---------- HDHomeRun RPG Extraction Started ----------")

# Prepare to process the HDHomeRun Guide
timestamp1Day = 86400
timestampIncrementHrs = (timestamp1Day / 24) * hoursIncrement
nextTimestamp = int(datetime.datetime.today().timestamp())
maxTimestamp = int((datetime.datetime.today() + datetime.timedelta(days = scheduleDurationInDays)).timestamp())
guideData = {"AppName":"HDHomeRun","AppVersion":"20241007","DeviceAuth":deviceAuth,"Platform":"WINDOWS","PlatformInfo":{"Vendor":"Web"}}
guideHeader = {"Cache-Control":"no-cache","Content-Type":"multipart/form-data","Accept-Encoding":"gzip, deflate, br","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; WebView/3.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.22631"}

# Begin the EPG extraction from the HDHomeRun device
guideResp = session.post("https://api.hdhomerun.com/api/guide?DeviceAuth=" + deviceAuth + "&SynopsisLength=160", headers=guideHeader, data=guideData)
if deviceResp.status_code != 200:
    logInfo("HDHomeRun guide request failed: (" + deviceResp.status_code + ") " + deviceResp.reason)
    sys.exit()

baseGuideJson = guideResp.json()

nextTimestamp = int(nextTimestamp + timestampIncrementHrs)

# Loop for the next 6 days guide
while nextTimestamp <= maxTimestamp:
    
    logInfo("--> Processing from (" + str(nextTimestamp) + ") " + str(datetime.datetime.fromtimestamp(nextTimestamp)))

    guideResp = session.post("https://api.hdhomerun.com/api/guide?DeviceAuth=" + deviceAuth + "&SynopsisLength=160&Start=" + str(nextTimestamp), headers=guideHeader, data=guideData)
    if deviceResp.status_code != 200:
        logInfo("HDHomeRun guide request failed: (" + deviceResp.status_code + ") " + deviceResp.reason)
        sys.exit()

    reqGuideJson = guideResp.json()

    if reqGuideJson == None:
        break
    
    for reqChannel in reqGuideJson:

        channelText = reqChannel["GuideName"]
        if "Affiliate" in reqChannel:
            channelText = reqChannel["Affiliate"]

        logDetail("----> Processing channel: " + reqChannel["GuideNumber"] + " - " + channelText)

        baseChannel = {}
        for srchChannel in baseGuideJson:
            if srchChannel["GuideNumber"] == reqChannel["GuideNumber"]:
                baseChannel = srchChannel
                break
    
        if baseChannel != {}:

            for reqGuideItem in reqChannel["Guide"]:

                newGuideItem = {}
                for baseGuideItem in baseChannel["Guide"]:
                    if baseGuideItem["StartTime"] == reqGuideItem["StartTime"]:
                        newGuideItem = baseGuideItem
                        break

                if newGuideItem == {}:
                    baseChannel["Guide"].append(reqGuideItem)
                    logDetail("------> Appending: " + reqGuideItem["Title"] + " from " + str(reqGuideItem["StartTime"]) + " to " + str(reqGuideItem["EndTime"]))

    nextTimestamp = int(nextTimestamp + timestampIncrementHrs)

logInfo("---------- HDHomeRun RPG Extraction Completed ----------")

logInfo("---------- HDHomeRun XMLTV Transformation Started ----------")

tv = ET.Element("tv")
tv.set("generator-info-name", "HDHomeRun")
tv.set("generator-info-url", deviceUrl)

# Scan through all Channels adding them to the XML document
for reqChannel in baseGuideJson:

    # Channel
    channel = ET.SubElement(tv, "channel")
    channel.set("id", reqChannel["GuideNumber"])

    # Channel name
    guideName = reqChannel["GuideName"]
    for reqLineUp in lineUpJson:
        if reqLineUp["GuideNumber"] == reqChannel["GuideNumber"]:
            guideName = reqLineUp["GuideName"]
            break

    channelName = ET.SubElement(channel, "display-name")
    channelName.set("lang", "en")
    channelName.text = guideName

    # Channel logo url
    if "ImageURL" in reqChannel:
        channelLogo = ET.SubElement(channel, "icon")
        channelLogo.set("src", reqChannel["ImageURL"])
        channelLogo.text = ""

# Scan through all Programmes adding them to the XML document
for reqChannel in baseGuideJson:
    for reqGuide in reqChannel["Guide"]:

        # Programme
        programme = ET.SubElement(tv, "programme")
        startTime = datetime.datetime.fromtimestamp(reqGuide["StartTime"]).strftime("%Y%m%d%H%M%S +0000")
        endTime = datetime.datetime.fromtimestamp(reqGuide["EndTime"]).strftime("%Y%m%d%H%M%S +0000")
        programme.set("channel", reqChannel["GuideNumber"])
        programme.set("start", startTime)
        programme.set("stop", endTime)

        # Programme title
        title = ET.SubElement(programme, "title")
        title.set('lang', 'en')
        title.text = reqGuide["Title"]

        # Programme description
        if "Synopsis" in reqGuide:
            description = ET.SubElement(programme, "desc")
            description.set('lang', 'en')
            description.text = clean_text(reqGuide["Synopsis"])

        # Programme icon
        if "ImageURL" in reqGuide:
            icon = ET.SubElement(programme, "icon")
            icon.set("src", reqGuide["ImageURL"])

        # Programme series/episode detail
        if "EpisodeNumber" in reqGuide:
            episodeNumber = reqGuide["EpisodeNumber"]
            if "S" in episodeNumber and "E" in episodeNumber:
                seriesNo = episodeNumber[episodeNumber.index("S") + 1:episodeNumber.index("E")]
                episodeNo = episodeNumber[episodeNumber.index("E") + 1:]
                episode = ET.SubElement(programme, "episode-num")
                episode.set("system", "xmltv_ns")
                episode.text = "{Series}.{Episode}.0".format(Series=seriesNo, Episode=episodeNo)
            else:
                logError("Enable to process episode")
            episodeOS = ET.SubElement(programme, "episode-num")
            episodeOS.set("system", "onscreen")
            episodeOS.text = episodeNumber

            if "OriginalAirdate" in reqGuide:
                originalAirdate = reqGuide["OriginalAirdate"]
                episodeOAD = ET.SubElement(programme, "episode-num")
                episodeOAD.set("system", "original-air-date")
                episodeOAD.text = datetime.datetime.fromtimestamp(reqGuide["OriginalAirdate"]).strftime("%Y-%m-%d %H:%M:%S")

            if "EpisodeTitle" in reqGuide:
                episodeTitle = reqGuide["EpisodeTitle"]
                title.text = title.text + ": " + episodeTitle

        if "Filter" in reqGuide:
            for filter in reqGuide["Filter"]:
                category = ET.SubElement(programme, "category")
                category.set("lang", "en")
                category.text = filter

logInfo("---------- HDHomeRun XMLTV Transformation Completed ----------")

logInfo("---------- Writing XMLTV to file " + epgFilename + " Started ----------")

# Create the XMLTV file
data = ET.ElementTree(tv).write(epgFilename, encoding='utf-8')

logInfo("---------- Writing XMLTV to file " + epgFilename + " Completed ----------")
