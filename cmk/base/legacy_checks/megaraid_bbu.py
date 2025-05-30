#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


# mypy: disable-error-code="var-annotated"

from cmk.agent_based.legacy.v0_unstable import LegacyCheckDefinition
from cmk.agent_based.v2 import State
from cmk.plugins.broadcom_storage.lib.megaraid import check_state

check_info = {}

# Agent output not included since it has almost 100 lines
# it's available in our archive or fh's bitbucket

# Load a fake controller with known good values for the most
# important parameters only and try to define their importance
megaraid_bbu_refvalues = {
    "Remaining Capacity Low": ("No", 1),  # nolearn
    "I2c Errors Detected": ("No", 1),
    "Temperature": ("OK", 2),
    "Pack is about to fail & should be replaced": ("No", 1),
    "Charging Status": ("None", 1),  # nolearn
    "Battery State": ("Operational", 2),  # nolearn
    "Learn Cycle Status": ("OK", 1),
    "Learn Cycle Active": ("No", 0),
    "Battery Pack Missing": ("No", 2),
    "Battery Replacement required": ("No", 1),
    "Over Temperature": ("No", 2),
    "Over Charged": ("No", 1),
    "Voltage": ("OK", 2),  # nolearn
    "isSOHGood": ("Yes", 2),
}


def megaraid_bbu_parse(string_table):
    controllers = {}
    current_hba = None
    for line in string_table:
        joined = " ".join(line)
        if ":" not in joined:
            continue  # skip garbage lines
        name, data = joined.split(":")
        name = name.strip()
        data = data.strip()

        # Scan each controller into its own dictionary
        if name in ["BBU status for Adapter", "BBU status for Adpater"]:
            item = f"/c{data}"
            current_hba = {}
            controllers[item] = current_hba
            # Add it under the old item name. Not discovered, but can be used when checking
            legacy_item = data
            controllers[legacy_item] = current_hba
        elif current_hba is not None:
            # We lose the numerical temperature here
            # (same key is used twice in output of megacli)
            # TODO: Fix the code and remove the pragma below!
            current_hba[name] = data
    return controllers


def discover_megaraid_bbu(section):
    # Items changed from e.g. '2' to '/c2' for consistency.
    # Only discover the new-style items.
    # The old items are kept in section, so that old services using them will still produce results
    yield from ((name, {}) for name in section if name.startswith("/c"))


def check_megaraid_bbu(item, _no_params, section):
    if (controller := section.get(item)) is None:
        return

    # get current charge level
    charge_level = controller.get("Relative State of Charge", "not reported for this controller")
    yield 0, f"Charge: {charge_level}"
    if (capacity := controller.get("Full Charge Capacity")) is not None:
        yield 0, f"Capacity: {capacity}"

    if controller.get("Learn Cycle Active") == "Yes":
        yield 0, "No states to check (controller is in learn cycle)"
        return

    yielded = False
    # verify defined important parameters to current level
    for varname, (refvalue, refstate) in megaraid_bbu_refvalues.items():
        if (value := controller.get(varname)) is None:
            # handle controller types that don't have certain values
            # if your bbu chipset fails and you still get a partial response this will lead
            # to a false result. but people asked for it :>
            continue

        # Some controllers report "Optimal" instead of "Operational"
        if value == "Optimal":
            continue

        # Some controllers do not output Temperature: OK and Voltage: OK.
        if varname in ["Temperature", "Voltage"] and value[0].isdigit():
            continue

        r = check_state(State(refstate), varname, value, refvalue)
        if r.state is not State.OK:
            yielded = True
            yield int(r.state), r.summary

    if not yielded:
        yield 0, "All states as expected"


check_info["megaraid_bbu"] = LegacyCheckDefinition(
    name="megaraid_bbu",
    parse_function=megaraid_bbu_parse,
    service_name="RAID BBU %s",
    discovery_function=discover_megaraid_bbu,
    check_function=check_megaraid_bbu,
)
