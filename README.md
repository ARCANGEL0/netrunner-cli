
# NETRUNNER_V3  
## Cyberpunk ncurses Menu for the CLI  
====================================
<br>

<img src="https://raw.githubusercontent.com/ARCANGEL0/netrunner-cli/refs/heads/master/netrunner.png" alt="NETRUNNER Screenshot" height="560" width="1450">
<br>

<div align="center">

[![GitHub watchers](https://img.shields.io/github/watchers/ARCANGEL0/netrunner-cli.svg?style=flat-square&color=4c1)](https://github.com/ARCANGEL0/netrunner-cli/watchers)
[![GitHub stars](https://img.shields.io/github/stars/ARCANGEL0/netrunner-cli.svg?style=flat-square&color=4c1)](https://github.com/ARCANGEL0/netrunner-cli/stargazers)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/ARCANGEL0/netrunner-cli.svg?style=flat-square&color=4c1)](https://github.com/ARCANGEL0/netrunner-cli/pulls)
[![GitHub issues](https://img.shields.io/github/issues/ARCANGEL0/netrunner-cli.svg?style=flat-square&color=4c1)](https://github.com/ARCANGEL0/netrunner-cli/issues)
[![GitHub forks](https://img.shields.io/github/forks/ARCANGEL0/netrunner-cli.svg?style=flat-square&color=4c1)](https://github.com/ARCANGEL0/netrunner-cli/network/members)

</div>

/// Inspired by Cyberpunk 2077’s hacking interface  
/// Simulates the NETTECH Breach Protocol minigame  
/// Launches an ncurses-powered interactive terminal dashboard  

A personal terminal startup project designed to simulate the hacking terminal from *Cyberpunk 2077*.  
Includes service management, system shortcuts, and a customizable curses menu — all wrapped in a retro-futuristic interface.

---

## :: Installation

Use the included installer script to set up required packages and tools.

```bash
git clone https://github.com/ARCANGEL0/netrunner-cli
cd netrunner-cli
chmod +x install.sh && ./install.sh
```


This will:  
- Install dependencies listed in the script  
- Add NETRUNNER to your `.bashrc` or `.zshrc`  
- Launch the minigame every time you open the terminal  
- Automatically install [Cool Retro Term](https://github.com/Swordfish90/cool-retro-term)

---

## :: Breach Protocol Minigame

The terminal interface is locked behind a matrix-style minigame.

- Buffer length: 8  
- Required sequence: Randomized  
- Attempts allowed: 3  
- CTRL key traps: Prevent unauthorized exit or backgrounding  
- On fail: Terminal access is denied

> Only those who breach the system may enter.

---
## :: Demonstration

![Demo Usage](https://raw.githubusercontent.com/ARCANGEL0/netrunner-cli/refs/heads/master/demo.gif)

## :: Interactive Menu

Once authenticated, the ncurses menu provides:

- Start/stop system services such as:
  - apache  
  - mysql  
  - tor  
  - proxies  
- Access to configuration files and scripts  
- Shortcuts to useful utilities and tools  
- Full user customization of commands and layout

Use it as a modular launch center for your workflow.

---

## :: Bypass Option

To skip the matrix challenge during startup:

> [ F3 ] → Bypass the minigame and access the menu directly.


For when you just need to dive in fast.

---

## :: Project Note

This script was created as a personal startup shell wrapper — inspired by *Cyberpunk 2077* and the aesthetic of Arasaka terminals.  
It's made for immersion, speed, and full system control. Modify and adapt freely to fit your needs.

---
## //::[❤️] Support

<div align="center">
  <center> 
    If you enjoy the project and want to support future development:

<a href='https://ko-fi.com/J3J7WTYV7' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://storage.ko-fi.com/cdn/kofi3.png?v=6' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>
<br>
<strong>Hack the world. Byte by Byte.</strong> ⛛
</center>
</div>
