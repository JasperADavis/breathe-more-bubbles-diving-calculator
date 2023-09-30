# Breathe More Bubbles | CS50P
#### Video Demo: https://youtu.be/DGpjk8S9PNI

## Purpose

This repository represents a Python project to fulfill the final project requirements for Harvard University's CS50P, Introduction to Programming with Python.
You may fork and incorporate in your own projects as long as they are not commerical in nature.

## Overview
This is a python program that runs calculations related to hypothetical scuba diving scenarios.
It currently consists of two sub-programs.

### Sub-Program 1: Depth Hazard Identification
This program allows users to identify potential hazards associated with specific gas blends at selected depths.

### Sub-Program 2: MOD Calculator
This program allows users to calculate the MOD (maximum operating depth) for a specific gas blend; if the specified blend is hypoxic (i.e. a gas blend where the proportion that is oxygen is under 18% at surface level pressures), it will also provide the minimum operating depth.

#### DISCLAIMER
All resulting calculations are hypothetical and are NOT to be exclusively used for actual scuba diving activity.
Scuba diving is a dangerous activity that requires appropriate training for the conditions and goals unique to each dive. Please consult with a medical professional before diving, and seek appropriate certification from an accredited diving agency.


## Instructions

### Dependencies

This program only makes use of the `sys` module for exiting via `sys.exit()` and `art` for generating the ASCII art displayed at the start of the program.

### Usage

The program can be executed from the command line using the `project.py` executable:

```
python project.py
```

Once the program begins, you'll be informed of the following:
`program may be ended at any time by pressing 'CTRL + D'`

After that, the user will get to select which specific sub-program to run.
The user is then asked to input a number representing what percentage by volume a specific gas will use. Each gas is presented, one at a time, until the full gas blend volume reaches 100%.

At this point, the paths diverge depending on the originally selected program.

#### Sub-Program 1: Depth Hazard Identification
If selecting program #1, Depth Hazard Identification, the user is prompted for the units that will be used to report depth.
The targeted depth is then provided by the user.

If `ft` was entered as the unit of measurement, the depth number is converted to meters for all relevant calculations (but don't worry, results will still be output in feet as well!).

A function converts the specified depth to the atmospheric pressure experienced at that depth underwater (specifically calculated using saltwater, not freshwater). This pressure is then multiplied by the earlier provided gas proportions to calculate the partial pressure of each gas at the specified depth.

These partial pressures are then run through a function that compares each gas's partial pressure to various gas-specific thresholds. If any thresholds are crossed, these hazards are logged. After all gases have been analyzed, all identified hazards are printed. If a specific gas's partial pressure was not deemed hazardous, you'll see the following report: `{specific_gas}: no hazards detected`.

#### Sub-Program 2: MOD Calculator
If selecting program #2, MOD Calculator, the user's previously selected blend of gases is run through a function that calculates the maximum operating depth achieveable with this blend before crossing a hazard threshold. This also supports using hypoxic gas blends (defined as those with an oxygen proportion under 18%). When a hypoxic blend is used, an alert is shown informing the user of as much, and the minimum operating depth is also provided. This minimum depth is the depth at which one could begin breathing this blend, as prior to that point, it would not provide enough oxygen.

#### Repeat?
After either program runs, the user is prompted with the opportunity to re-run the program. If the user enters `y`, the program runs from the top, otherwise, the program gracefully exits.

#### Testing
This project directory should also contain a file called `test_project.py`. Running this file performs a number of tests on the main file's functions using `Pytest`.


## FUTURE IMPROVEMENTS

### Planned Features
- Allow user to utilize pre-defined common gas mixes (e.g. EANitrox-32)
- Provide ability to specify starting altitude and whether water is saltwater or freshwater
- Implement graphical interface