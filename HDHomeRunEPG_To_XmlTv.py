
import argparse
import json
import logging
import os
import pytz
import re
import ssl
import sys
from typing import Optional
from tzlocal import get_localzone
import urllib.request
import xml.etree.ElementTree as ET

__author__ = "Incubus Victim"
__credits__ = ["Incubus Victim"]
__license__ = "GPL"
__version__ = "2.1.0"
__maintainer__ = "Incubus Victim"

def setup_logging(debug_mode: str) -> None:
    """Configure logging based on debug mode."""
    log_level = logging.INFO
    if debug_mode.lower() == "full":
        log_level = logging.DEBUG
    elif debug_mode.lower() == "off":
        log_level = logging.WARNING
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    return logger

def discover_device_auth(host: str) -> str:
    """Discover HDHomeRun device auth."""
    try:
        logger.info("Fetching HDHomeRun Web API Device Auth")
        with urllib.request.urlopen("http://%s/discover.json" % host) as response:
            data = json.loads(response.read().decode())
            for key in data:
                if "DeviceAuth" in key:
                    device_auth = data["DeviceAuth"]
                    logger.info("Discovered device auth: %s" % device_auth)
                    return device_auth
        logger.error("No devices found")
        sys.exit(1)
    except Exception as e:
        logger.error("Error discovering device: %s" % e)
        sys.exit(1)

def fetch_channels(host: str, device_auth: str) -> list:
    """Fetch EPG channels from HDHomeRun device."""
    channel_data = []
    logger.info("Fetching HDHomeRun Web API Lineup for auth %s" % device_auth)
    url = "http://%s/lineup.json" % host
    with urllib.request.urlopen(url) as response:
        channel_data = json.loads(response.read().decode())

    return channel_data

def fetch_xmltv_data(device_auth: str) -> list:
    """Fetch XMLTV data for a all device channels via the HDHomeRun API."""
    xml_str = ""
    
    try:
        context = ssl._create_unverified_context()
        url = "https://api.hdhomerun.com/api/xmltv?DeviceAuth=%s" % device_auth
        with urllib.request.urlopen(url, context=context) as response:
            content = response.read()

        # Decode + clean
        xml_str = content.decode('utf-8')
        
        # Remove XML declaration
        xml_str = re.sub(r'^\s*<\?xml[^>]*>\s*', '', xml_str, flags=re.DOTALL)
        
        # Fix common escaping issues from HDHomeRun
        xml_str = xml_str.replace(r"\'", "'")
        xml_str = xml_str.replace(r'\"', '"')
        xml_str = re.sub(r'\\t', '\t', xml_str)   # if literal \t appears
    
        return xml_str
    except Exception as e:
        logger.error("Error fetching XMLTV for all channels: %s" % (e))
        return xml_str
   

def get_channel_id_by_display_name(tree: ET.ElementTree, display_name: str) -> Optional[str]:
    """Find the channel ID where any <display-name> matches the given name."""
    if tree is None:
        return None
    
    root = tree.getroot() if hasattr(tree, 'getroot') else tree
    
    # Iterate through all channel elements
    for channel in root.findall('channel'):
        # Check all <display-name> children
        for name_elem in channel.findall('display-name'):
            if name_elem.text and name_elem.text.strip() == display_name.strip():
                channel_id = channel.get('id')
                if channel_id:
                    return channel_id
    
    return None

def process_xmltv_data(xml_str: str, channels: list) -> str:
    """Process the XMLTV data replacing the API channel ID with the lineup.json channel ID."""
    search_xml = ET.ElementTree(ET.fromstring(xml_str))

    for channel in channels:
        channel_to = channel.get("GuideNumber", "")
        channel_from = get_channel_id_by_display_name(search_xml, channel_to)
        if channel_from is not None:
            xml_str = xml_str.replace(channel_from, channel_to)

    return xml_str

def generate_xmltv(host: str, filename: str) -> None:
    """Generate XMLTV file from HDHomeRun EPG data."""
    # Initialize XMLTV root
    xmltv_root = ET.Element("tv")
    xmltv_root.set("source-info-name", "HDHomeRun")
    xmltv_root.set("generator-info-name", "HDHomeRunEPG_to_XmlTv")
    
    # Discover device authentication
    device_auth = discover_device_auth(host)

    # Fetch channel list
    channels = fetch_channels(host, device_auth)
    if not channels:
        logger.error("No channels retrieved. Exiting.")
        sys.exit(1)

    # Fetch XMLTV EPG data for all channels
    logger.info("HDHomeRun XMLTV Extraction Started")
    xmltv_root = fetch_xmltv_data(device_auth)
    logger.info("HDHomeRun XMLTV Extraction Completed")

    # Process the XMLTV EPG data so the channels match with the lineup.json channel list
    logger.info("HDHomeRun XMLTV Processing Started")
    xmltv_root = process_xmltv_data(xmltv_root, channels)
    logger.info("HDHomeRun XMLTV Processing Completed")
    
    # Write to XML file
    try:
        logger.info("Writing XMLTV to file " + filename + " Started")
        tree = ET.ElementTree(ET.fromstring(xmltv_root))
        ET.indent(tree, space="\t", level=0)
        tree.write(filename, encoding="UTF-8", xml_declaration=True)
        logger.info("Writing XMLTV to file %s Completed" % filename)
    except Exception as e:
        logger.error("Error writing XML file: %s" % e)
        sys.exit(1)

def env_int(name, default):
    try:
        return int(os.environ.get(name, default))
    except (TypeError, ValueError):
        return default
        
def main():
    """Main function to parse arguments and generate XMLTV file."""
    parser = argparse.ArgumentParser(
        add_help=False,
        description="Program to download the HDHomeRun device EPG in XMLTV format suitable for Jellyfin."
    )
    parser.add_argument("--help", action="store_true", help="Show the command parameters available.")
    parser.add_argument("--host",default=os.environ.get("HOST", "hdhomerun.local"),help='...')
    parser.add_argument("--filename",default=os.environ.get("FILENAME", "epg.xml"),help='...')
    parser.add_argument("--debug",default=os.environ.get("DEBUG", "on"),help='...')
    
    args = parser.parse_args()
    
    if args.help:
        parser.print_help()
        sys.exit(0)
    
    global logger
    logger = setup_logging(args.debug)
    
    generate_xmltv(args.host, args.filename)

# Initialize local timezone with fallback to UTC
try:
    LOCAL_TZ = get_localzone()
except Exception as e:
    logger.warning("Could not detect local timezone: %s. Falling back to UTC." % e)
    LOCAL_TZ = pytz.UTC

if __name__ == "__main__":
    main()