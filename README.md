# SignalAudit

A comprehensive Windows desktop application for WiFi network analysis, monitoring, and management. SignalAudit provides real-time signal strength visualization, network diagnostics, and automated connection management.

## Overview

SignalAudit is a powerful WiFi analyzer that leverages Windows native commands to deliver detailed insights into wireless networks in your vicinity. Built with Python and CustomTkinter, it offers a modern, intuitive interface for both casual users and network professionals.

## Key Features

### Network Discovery and Analysis

- **Nearby WiFi Discovery**: Automatically detect all WiFi access points within range
- **Current Network Analysis**: Detailed information about your active WiFi connection
- **Signal Strength Monitoring**: Real-time signal strength measurements with visual graphs
- **Comprehensive Network Details**: View SSID, BSSID, authentication type, encryption, channel, frequency, and more

### Real-Time Monitoring

- **Live Signal Graphs**: Dynamic curves showing signal strength evolution over time
- **Signal Quality Metrics**: Monitor signal strength in percentage and dBm
- **Channel Utilization**: Track channel usage and identify congestion (shown as percentage)
- **Connected Stations**: View the number of devices connected to each access point
- **Available Capacity**: Monitor network capacity and bandwidth availability

### Connection Management

- **Smart Connection**: Automatically connect to the strongest available WiFi network
- **Signal-Based Sorting**: Sort networks by signal strength for optimal selection
- **Profile Creation**: Create and save Windows WiFi profiles for quick reconnection
- **Quick Disconnect**: Easily disconnect from current WiFi network

### Network Information Display

For each detected network, SignalAudit displays:

- Network name (SSID)
- Network type (Infrastructure/Ad-hoc)
- Authentication method (WPA2-Personal, Open, etc.)
- Encryption protocol (CCMP, AES, etc.)
- BSSID (MAC address of the access point)
- Signal strength (percentage and absolute value)
- Radio type (802.11n, 802.11ac, 802.11ax)
- Frequency band (2.4 GHz, 5 GHz)
- Channel number
- BSS load statistics
- Channel utilization percentage
- Connected stations count
- Available capacity
- Supported and basic data rates (Mbits/s)

## System Requirements

- **Operating System**: Windows 10 or Windows 11
- **Privileges**: Administrator rights (required for WiFi profile management and connection operations)
- **Hardware**: WiFi adapter with driver support for network statistics

## Installation

### Windows Installer (Recommended)

Download the latest stable release from the Releases page and run the installer:

**https://github.com/nour-nejia/SignalAudit/releases/tag/v1.0.0**

1. Download `SignalAudit_Installer.exe` from the release page
2. Run the installer and follow the wizard
3. Launch SignalAudit from the Start Menu or Desktop shortcut

### Run from Source

1. Clone the repository:
```bash
git clone https://github.com/yourusername/signalaudit.git
cd signalaudit
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python signalaudit.py
```

**Note**: Running from source requires Python 3.8 or higher.

## Usage Guide

### Main Interface Buttons

**Découvrir Wi-Fi à proximité** (Discover Nearby WiFi)
- Scans for all available WiFi networks in range
- Displays comprehensive information for each network
- Updates the network list with current data

**Analyser Wi-Fi actuel** (Analyze Current WiFi)
- Shows detailed information about your currently connected network
- Displays signal quality, channel usage, and connection statistics
- Useful for troubleshooting connection issues

**Trier Wi-Fi par signal décroissant** (Sort WiFi by Decreasing Signal)
- Organizes detected networks by signal strength
- Helps identify the strongest available networks
- Automatically refreshes the display with sorted results

**Se connecter au Wi-Fi le plus puissant** (Connect to Strongest WiFi)
- Automatically connects to the network with the highest signal strength
- Creates a Windows profile if needed
- Ideal for quick connections in new environments

**Se déconnecter du Wi-Fi** (Disconnect from WiFi)
- Safely disconnects from the current WiFi network
- Releases the network adapter for new connections

**Tous les AP** (All Access Points)
- Displays a complete list of all detected access points
- Shows detailed statistics for each AP
- Blue button for comprehensive network overview

**AP Connecté** (Connected AP)
- Shows information specific to your current connection
- Displays real-time connection quality metrics
- Red button for quick access to current network status
- 
### Technology Stack

- **UI Framework**: CustomTkinter (modern, customizable tkinter widgets)
- **Data Visualization**: Matplotlib (for real-time signal graphs)
- **System Integration**: Windows CMD commands (netsh, network adapters)
- **Build Tool**: Nuitka (Python to native executable compilation)
- **Installer**: Inno Setup (professional Windows installer creation)

### Core Components

- **WiFi Scanner**: Interfaces with Windows WLAN API via netsh commands
- **Signal Analyzer**: Processes and interprets WiFi signal data
- **Graph Engine**: Renders real-time signal strength curves
- **Profile Manager**: Creates and manages Windows WiFi profiles
- **Connection Handler**: Manages network connections and disconnections

## Building from Source

To compile SignalAudit into a standalone executable:

1. Install Nuitka:
```bash
pip install nuitka
```

2. Compile the application:
```bash
python -m nuitka --standalone --windows-disable-console --enable-plugin=tk-inter signalaudit.py
```

3. The compiled executable will be in the `signalaudit.dist` folder

To create the installer, use Inno Setup with the provided configuration script.

## Troubleshooting

### Application won't start
- Ensure you're running Windows 10 or 11
- Right-click and select "Run as administrator"
- Check if your WiFi adapter is enabled

### No networks detected
- Verify your WiFi adapter is turned on
- Check if Windows WiFi service is running
- Try running the application as administrator

### Cannot connect to networks
- Administrator privileges are required for connection operations
- Ensure the network is within range and not hidden
- Check if the network requires additional authentication (captive portal)

### Graphs not displaying
- Verify matplotlib is properly installed
- Check if there's sufficient signal data collected
- Try rescanning the networks

## Known Limitations

- Windows-only application (uses Windows-specific networking commands)

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
6. 
## Acknowledgments

- CustomTkinter for the modern UI framework
- The Python community for excellent networking libraries
- Windows WLAN API documentation and community resources
----
**Note**: This application is designed for legitimate network analysis and troubleshooting purposes. Always ensure you have permission before analyzing or connecting to WiFi networks.
