# CS50P
"""BREATHE MORE BUBBLES: Scuba Diving Planning Calculator"""

# IMPORTS
import sys
from art import text2art

# CONSTANTS
PROGRAM_NAME = "Breathe\nMore\nBubbles"
PROGRAMS = ["Depth Hazard Identification", "MOD Calculator"]
GASES_LIST = ["oxygen", "nitrogen", "helium", "hydrogen", "argon"]
HYPOXIC_THRESHOLD = 0.18
M_TO_FT = 3.28084
AMBIENT_PRESSURE = 1
ATM_TO_MBAR = 1013.25
ATM_TO_MMHG = 760
ATM_TO_PSI = 14.6959
MSW_TO_ATM = 0.1

# To Be Implemented
# MSW_TO_ATM = 0.099376327658525
# MIXED_GASES_LIST = ["air", "nitrox", "trimix", "heliox", "hydreliox", "hydrox", "argox"]
# GASES_LIST = ["oxygen", "nitrogen", "helium", "hydrogen", "argon", "neon"]


def main():
    # select which program to run
    program = select_program()
    print(f"Selected program: {program}\n")

    # select your gas mixture
    selected_gases = select_gasses()

    if program == "Depth Hazard Identification":
        # gather depth and units
        depth, units = get_depth()
        display_hazards(identify_hazards(depth, selected_gases))

    elif program == "MOD Calculator":
        MOD_calc(selected_gases)
    else:
        # room to expand functionality in the future
        print("Future programs to be implemented")

    # MAIN PROGRAM ENDING
    print()
    repeat = input("Repeat? (y/n): ").lower()
    if repeat != "y":
        sys.exit("Succesful completion")


def display_hazards(hazards_list):
    """Prints hazards from list in formatted table"""
    final_str = "IDENTIFIED HAZARDS:\n"
    for hazard in hazards_list:
        final_str += f"\n{hazard}"
    pr_print(final_str)
    print()


def MOD_calc(gases_dict):
    """Takes a gases dict and calculates the Maximum Operating Depth (MOD) for that mix before encountering a potential hazard"""
    # handle hypoxic blends (blends with oxygen proportion less than 18%, which aren't breathable at surface pressure)
    full_set_of_passes = 0
    if (o2_portion := (gases_dict["oxygen"] / 100)) < HYPOXIC_THRESHOLD:
        minimum_depth = min_depth(o2_portion)
        current_depth = minimum_depth - 1
        pr_print(
            f"CAUTION:\nHypoxic blend in use.\n\nMinimum Operating Depth: {minimum_depth:,.2f}m\n(based on oxygen proportion alone)"
        )
    else:
        current_depth = -1
    incrementing = True

    while incrementing:
        # get pressure, calc partial pressure for all gases, run through hazard ID function, if no hazards, increment depth; else, break
        current_depth += 1
        for message in identify_hazards(current_depth, gases_dict, verbose=False):
            if "no hazards detected" not in message:
                incrementing = False
                break
            full_set_of_passes += 1

    # return maximum depth calculated (before encountering hazard)
    # handles cases where hypoxic blend's min. depth already causes issues from a different gas (and is therefore not a useable blend)
    if full_set_of_passes >= len(gases_dict):
        max_depth = current_depth
        print("\nMaximum Operating Depth:")
        identify_hazards(max_depth, gases_dict)
        return max_depth
    else:
        identify_hazards(current_depth, gases_dict)
        pr_print("WARNING:\nNo safe depth for that specific mix of gases")
        return None


def min_depth(o2_portion):
    """Takes a proportion of gas mix that is oxygen and calculates minimum depth needed for a hypoxic blend to be breathable"""
    min_atm = HYPOXIC_THRESHOLD / o2_portion
    min_depth = absolute_pressure_to_depth(min_atm)
    return min_depth


def identify_hazards(depth, gases_dict, verbose=True):
    """Takes a specific depth and gas mix (as a gases dict) and returns potential hazards at respective partial pressure for each gas"""
    pressure = depth_to_absolute_pressure(depth)
    if verbose:
        pr_print(
            f"DEPTH & PRESSURE:\n\nDepth: {depth:,.2f}m ({(depth * M_TO_FT):,.2f}ft)\nPressure: {pressure:,.2f} atm"
        )

    adj_gases_dict = pp_of_gases(gases_dict, pressure)
    if verbose:
        display_gases(adj_gases_dict)
    return check_dangers(adj_gases_dict)


def select_program():
    """Prompts user to select which specific sub-program to run"""
    if len(PROGRAMS) == 1:
        return PROGRAMS[0], 0
    print("\nAvailable Programs:\n")
    for index, program in enumerate(PROGRAMS):
        print((index + 1), "-", program)
    print()
    while True:
        program = input("Program #: ")
        if program.isnumeric():
            program = int(program)
            if program > len(PROGRAMS) or program < 1:
                print("Not a valid selection")
            else:
                break
        else:
            print("Must input a positive number with no symbols or letters")
    return PROGRAMS[(program - 1)]


def check_dangers(gases_dict):
    """examines selected gases to identify hazards at specified depth (pressure)"""
    hazards = []

    gases_selected = list(gases_dict)

    for gas in GASES_LIST:
        if gas in gases_selected:
            ppGas = gases_dict[gas]

            if gas == "oxygen":
                if ppGas >= 1.6:
                    message = "central nervous system oxygen toxicity: seizure, convulsions, unconsciousness"
                elif ppGas >= 1.4:
                    message = "potential for central nervous system oxygen toxicity"
                elif ppGas <= 0.0:
                    message = "apoxia"
                elif ppGas < 0.18:
                    message = "hypoxia"
                else:
                    message = "no hazards detected"
            elif gas == "nitrogen":
                if ppGas >= 7.9:
                    message = "severe narcosis: hallucinations & unconsciousness"
                elif ppGas >= 3.16:
                    message = "narcosis: serious impairment of judgement, focus, decision-making, coordination"
                else:
                    message = "no hazards detected"
            elif gas == "helium":
                if ppGas >= 15.82:
                    message = (
                        "severe narcosis: hallucinations & unconsciousness"
                    )
                else:
                    message = "no hazards detected"
            elif gas == "hydrogen":
                if ppGas >= 29.6:
                    message = "narcosis: hallucinations, disorientation, confusion"
                else:
                    message = "no hazards detected"
            elif gas == "argon":
                if ppGas >= 1.7:
                    message = "narcosis: serious impairment of judgement, focus, decision-making, coordination"
                else:
                    message = "no hazards detected"
            hazards.append(f"{gas}: {message}")

    return hazards


def ft_to_m(num: float, unit="ft"):
    """Converts number in feet to number in meters"""
    unit = unit.lower()
    if unit == "m":
        return num
    elif unit == "ft":
        return num / M_TO_FT
    else:
        return "Invalid unit provided"


def get_depth():
    """Prompts user for unit (meters or feet) and selected depth, then returns depth in meters"""
    while True:
        units = input("Select Units ('m' or 'ft'): ").lower()
        if units in ["m", "ft", ""]:
            break
    while True:
        try:
            depth = float(input("Input depth: "))
        except ValueError:
            print("Must provide a numerical value (no letters or symbols)")
        else:
            if units != "m" and units != "":
                depth = ft_to_m(depth)
            break

    return depth, units


def depth_to_absolute_pressure(depth: float):
    """Takes depth in meters (sea water) and returns barometric pressure in atm"""
    hydrostatic_pressure = depth * MSW_TO_ATM
    return hydrostatic_pressure + AMBIENT_PRESSURE


def absolute_pressure_to_depth(atm: float):
    """Takes hydrostatic pressure (in atm) and returns depth at which that hydrostatic pressure is present"""
    depth = (atm - 1) / MSW_TO_ATM
    return depth


def select_gasses():
    """Allows user to select combination of gases used in breathing mix"""
    pr_print(
        "For each gas, input fractional proportion of total volume (e.g. 100 = 100%, 32 = 32%)"
    )
    print()
    total_volume = 100.00
    current_volume = 0.00
    gases_with_proportion = {}
    while True:
        for gas in GASES_LIST:
            if current_volume == total_volume:
                break
            else:
                while True:
                    while True:
                        try:
                            print(f"Volume remaining: {total_volume - current_volume}%")
                            if gas != "oxygen":
                                while True:
                                    result = float(
                                        input(f"Proportional % of {gas}: ").replace("%", "")
                                    )
                                    if result >= 0:
                                        break
                                    else:
                                        print("negative numbers aren't allowed")
                            else:
                                while True:
                                    result = float(
                                        input(f"Proportional % of {gas}: ").replace(
                                            "%", ""
                                        )
                                    )
                                    if result > 0:
                                        break
                                    pr_print("No oxygen is a non-starter")
                        except ValueError:
                            print(
                                "You must enter a non-negative number; no letters or symbols ('0' is fine, except for oxygen)"
                            )
                        else:
                            break
                    if current_volume + result > total_volume:
                        print("\nThat takes more than 100% of the available volume")
                    else:
                        current_volume += result
                        break
            if result != 0:
                gases_with_proportion[gas] = result
        if current_volume < total_volume:
            print("\nYou have unallocated space\nPlease try again")
        else:
            break
    display_selected_blend(gases_with_proportion)
    return gases_with_proportion


def display_selected_blend(unadj_gases_dict):
    """Prints gas and proporitons, one line at a time in nicely formatted table"""
    final_str = "SELECTED BLEND:\n"
    # print("Selected Blend:")
    for gas in unadj_gases_dict:
        final_str += f"\n{gas.capitalize()}: {unadj_gases_dict[gas]}%"
    pr_print(final_str)
    print()


def display_gases(gases_dict):
    """Prints gas and respective partial pressure, one line at a time in nicely formatted table"""
    final_str = "PARTIAL PRESSURES:\n"
    for gas in gases_dict:
        final_str += (
            f"\npartial pressure of {gas.capitalize()}: {gases_dict[gas]:,.2f} atm"
        )
    pr_print(final_str)
    print()


def pp_of_gases(gases_dict, pressure):
    """Takes dictionary of gases mix, multiplies by the ATM pressure to return a dict with partial pressures of each gas."""
    adj_gases_dict = {}
    for gas in gases_dict:
        adj_gases_dict[gas] = (gases_dict[gas] * pressure) / 100.0
    return adj_gases_dict


def pr_print(text):
    """Takes input string and prints nicely formatted table with borders; handles multi-line blocks of text"""
    lines = text.split("\n")

    if len(lines) == 1:
        length = len(text)
        border = "+" + ("-" * (length + 2)) + "+"
        print(f"{border}\n| {text} |\n{border}")
    else:
        max_length = 0
        for line in lines:
            if len(line) > max_length:
                max_length = len(line)
        border = "+" + ("-" * (max_length + 2)) + "+"
        print(border)
        for line in lines:
            differential = max_length - len(line)
            if differential == 0:
                print(f"| {line} |")
            else:
                print(f"|" + " " + line + (" " * (differential + 1) + "|"))
        print(border)


if __name__ == "__main__":
    print(text2art(PROGRAM_NAME.upper()))
    pr_print("program may be ended at any time by pressing 'CTRL + D'")
    while True:
        try:
            main()
        except EOFError:
            sys.exit("\n\nUser manually ended the program")
