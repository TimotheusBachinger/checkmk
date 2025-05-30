#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import pytest

from cmk.notification_plugins.cisco_webex_teams import _cisco_webex_teams_msg


@pytest.mark.parametrize(
    "context, result",
    [
        (
            {
                "PARAMETER_URL_PREFIX_1": "automatic_http",
                "MONITORING_HOST": "localhost",
                "OMD_SITE": "testsite",
                "HOSTURL": "/view?key=val",
                "SERVICEURL": "/view?key=val2",
                "HOSTNAME": "site1",
                "SERVICEDESC": "first",
                "SERVICESTATE": "CRITICAL",
                "NOTIFICATIONTYPE": "PROBLEM",
                "HOSTADDRESS": "127.0.0.1",
                "SERVICEOUTPUT": "Service Down",
                "WHAT": "SERVICE",
                "CONTACTNAME": "John,Doe",
                "LONGDATETIME": "Wed Sep 19 15:29:14 CEST 2018",
            },
            {
                "markdown": "#### Service PROBLEM notification"
                "  \nHost: [site1](http://localhost/testsite/view?key=val) (IP: 127.0.0.1)"
                "  \nService: [first](http://localhost/testsite/view?key=val2)"
                "  \nState: CRITICAL"
                "  \n#### Additional Info"
                "  \nService Down"
                "  \nPlease take a look: @John, @Doe"
                "  \nCheck_MK notification: Wed Sep 19 15:29:14 CEST 2018"
            },
        ),
        (
            {
                "PARAMETER_URL_PREFIX_1": "automatic_https",
                "MONITORING_HOST": "localhost",
                "OMD_SITE": "testsite",
                "HOSTURL": "/view?key=val",
                "HOSTNAME": "site1",
                "HOSTSTATE": "DOWN",
                "HOSTOUTPUT": "Manually set to Down by cmkadmin",
                "NOTIFICATIONTYPE": "PROBLEM",
                "HOSTADDRESS": "127.0.0.1",
                "WHAT": "HOST",
                "CONTACTNAME": "John",
                "LONGDATETIME": "Wed Sep 19 15:29:14 CEST 2018",
            },
            {
                "markdown": "#### Host PROBLEM notification"
                "  \nHost: [site1](https://localhost/testsite/view?key=val) (IP: 127.0.0.1)"
                "  \nState: DOWN  \n#### Additional Info"
                "  \nManually set to Down by cmkadmin"
                "  \nPlease take a look: @John"
                "  \nCheck_MK notification: Wed Sep 19 15:29:14 CEST 2018"
            },
        ),
    ],
)
def test_cisco_webex_teams_message(context: dict[str, str], result: dict[str, str]) -> None:
    msg = _cisco_webex_teams_msg(context)
    assert msg == result
