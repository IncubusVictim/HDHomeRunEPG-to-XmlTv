# HDHomeRun EPG converter to XMLTV file

<div align="right">
<a href="https://buymeacoffee.com/incubusvictim" target="_blank"><img align="top" src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a> <img align="top" src="https://github.com/IncubusVictim/HDHomeRunEPG-to-XmlTv/blob/main/bmc_qr.png" width="100" />
</div>

## Versions

The current version is v2.1 which this README.md file relates direct to.

The current version is always HDHomeRunEPG_To_XmlTv.py and the previous versions also exist for reference, but these are not recommended now as we have a Silicon Dust API to get the XMLTV data from.

## Fixes and Acknowledgments

[#5](https://github.com/IncubusVictim/HDHomeRunEPG-to-XmlTv/issues/5) - Many thanks to [@supitsmike] for fixing the bug where all episodes were showing as "New".<br/>
[#7](https://github.com/IncubusVictim/HDHomeRunEPG-to-XmlTv/issues/7) - Add the <new /> to help with NEXTPVR intepretting a new show correctly.<br/>
[#13](https://github.com/IncubusVictim/HDHomeRunEPG-to-XmlTv/issues/13) - Manys thanks to [@AcSlayter] for adding docker support.<br/>
[#14](https://github.com/IncubusVictim/HDHomeRunEPG-to-XmlTv/issues/14) - Many thanks to [@Sujeom] for fixing the status handling bug.<br/>
[#10](https://github.com/IncubusVictim/HDHomeRunEPG-to-XmlTv/issues/10) - The re-vamp in v2 has re-arranged all XMLTV elements to match the DTD more closely.<br/>
[#11](https://github.com/IncubusVictim/HDHomeRunEPG-to-XmlTv/issues/11) - The re-vamp in v2 has allowed me to attempt the location timezone detection properly.<br/>
[#12](https://github.com/IncubusVictim/HDHomeRunEPG-to-XmlTv/issues/12) - The re-vamp in v2 corrects the formatting of the XMLTV so it no longer is on a single line.<br/>
[#31](https://github.com/IncubusVictim/HDHomeRunEPG-to-XmlTv/issues/31) - Modified to utilise the HDHomeRun API that now gives 2 days worth of XMLTV data in a single call.

## Features

A Python program to download the current EPG provided by Silicon Dust's API for a HDHomeRun device you have at home.  The API provides 2 days worth of EPG in XMLTV format already, the only tweak I have had to make is with the Channel ID so it maps directly to the same channel on your device.  This has the effect in Jellyfin where no manual mapping is necessary for these channels.  This should work with some other HDHomeRun models, but I have only tested with the Quattro.

I developed this so I could easily update the EPG on a Jellyfin media server that was linked to an HDHomeRun Quattro.

<i><b>Version 2.1 Notes:</b> This latest version has removed all the manual processing necessary to shape the XMLTV produce as this is now given in its entirety by the Silicon Dust API.</i>

<i><b>NOTE 1:</b> The Binaries I have generated are purely for those that are not comfortable running the Python application.  All of the binaries run on my local hardware and OS's, but if you have any problems please send me a message and I will try my best to help out if I can.</i>

## Usage

```
python HDHomeRunEPG_To_XmlTv.py [--help] [--host <HOST>] [--filename <FILENAME>] [--debug <DEBUG>]
```

|      Parameter | Description     |
| -------------: | :-------------- |
| `--help`  | Show the command parameters available. |
| `--host <HOST>`  | The host name or IP address of the HDHomeRun server if different from "hdhomerun.local". |
| `--filename <FILENAME>` | The file path and name of the EPG to be generated. Defaults to epg.xml in the current directory. |
| `--debug <DEBUG>` | Switch debug log message on, options are "on", "full" or "off". Defaults to "on". This is usefuly to see the detail of all the programmes being retrieved, but will mak the app take longer to run. |

## Python Pre-requisites

To run the Python application as described in the [Usage](#usage) section above, you will need the following elements set up:

### Install Python

Install Python 3.9 or above onto your platform if it is not already available and ensure you can execute the following from you terminal/command/Powershell window:

```
python --version
```

If this returns the Python version you have it installed correctly.

### Install PIP

With Python installed you should have the PIP utility to install Python packages. If not check instructions for your platform.

```
pip --version
```

OR 

```
pip3 --version
```

### Install HDHomeRunEPG_To_XmlTv Python packages

Requirements are listed in the requirements.txt file. These can be installed using the following command:

```
pip install -r requirements.txt
```

### Running the HDHomeRunEPG_To_XmlTv Python app

Simply run the HDHomeRunEPG_To_XmlTv app on your platform, the following will produce an epg.xml file from your HDHomeRun.local device.

```
python HDHomeRunEPG_to_XmlTv.py
```

If you don't have the HDHomeRun.local address, use you IP address directly as follows:

```
python HDHomeRunEPG_to_XmlTv.py --host 192.168.68.102
```

## Binaries

Please find a <b>binaries</b> directory in the repository root that contains a PyInstaller built distibution that can be run independently on the platform it is built for.  Extract the relevant binary platform zip files onto your machine and run according to the instructions below:

### Debian Linux (#31 Tested)

To run the Debian Linux binary from a terminal window, put yourself in the binaries directory and run the following command with any parameters (as described above), e.g:

```
.\HDHomeRunEPG_To_XmlTv --host 192.168.1.100
```

If this fails and you need to make the HDHomeRunEPG_To_XmlTv runnable, type in the followwing before running it again:

```
chmod 755 HDHomeRunEPG_To_XmlTv
```

### Mac OS (#7 Tested) (TBC: When I have a working MacOS environment I will build this)

To run the Mac OS binary from a terminal window, put yourself in the binaries directory and run the following command with any parameters (as described above), e.g:

```
.\HDHomeRunEPG_To_XmlTv --host 192.168.1.100
```

If this fails and you need to make the HDHomeRunEPG_To_XmlTv runnable, type in the followwing before running it again:

```
chmod 755 HDHomeRunEPG_To_XmlTv
```

### Windows (#31 Tested)

To run the Windows binary from a terminal window, put yourself in the binaries directory and run the following command with any parameters (as described above), e.g:

```
.\HDHomeRunEPG_To_XmlTv --host 192.168.1.100
```

# Docker Usage

You can run this project using Docker. Here are the steps:

1. **Update the HDHomeRun host:**
	Edit the `HOST` environment variable in your `docker-compose.yml` file or set it directly in your Docker command. Example:
	```yaml
	environment:
	  - HOST=192.168.1.100
	```
	Or set it in your run command:
	```sh
	docker run --rm -e HOST=192.168.1.100 hdhomerun-epg
	```

2. **Build the Docker image:**
	```sh
	docker compose build
	```

3. **Start the container:**
	```sh
	docker compose up
	```

4. **Cron schedule:**
	The script is scheduled to run every day at 1am using cron inside the container:
	```cron
	0 1 * * *
	```
	This will automatically update the EPG file as specified by the `FILENAME` environment variable.

---

# Other Recommendations

A kind individual [@thekoma](https://github.com/thekoma/HDHomeRunEPG-to-XmlTv) has developed an API service that fetches and caches EPG from HDHomeRun devices the serves the data as an XMLTV output.
