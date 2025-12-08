"""
:codeauthor: Georg Pfuetzenreuter <mail+salt@georg-pfuetzenreuter.net>
"""

from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from saltext.apache.modules import suse_apache

SAMPLE_A2ENMOD_L_OUTPUT = "actions alias auth_basic authn_core authn_file authz_host authz_groupfile authz_core authz_user autoindex cgi dir env expires include log_config mime negotiation setenvif ssl socache_shmcb userdir reqtimeout apparmor proxy proxy_fcgi remoteip rewrite"


@pytest.fixture
def configure_loader_modules():
    return {suse_apache: {}}


def test_check_mod_enabled():
    """
    Test if mod_enabled() finds if specified modules are enabled.
    """

    with patch.dict(
        suse_apache.__salt__,
        {"cmd.run": MagicMock(return_value=SAMPLE_A2ENMOD_L_OUTPUT)},
    ):
        assert suse_apache.check_mod_enabled("rewrite")


def test_check_mod_enabled_not():
    """
    Test if mod_enabled() finds if specified modules are not enabled.
    """

    with patch.dict(
        suse_apache.__salt__,
        {"cmd.run": MagicMock(return_value=SAMPLE_A2ENMOD_L_OUTPUT)},
    ):
        assert not suse_apache.check_mod_enabled("status")


def test_a2enmod():
    """
    Test if a2enmod() enables specified modules.
    """

    with patch.dict(
        suse_apache.__salt__,
        {"cmd.retcode": MagicMock(return_value=0)},
    ):
        assert suse_apache.a2enmod("status") == {
            "Name": "Apache2 Enable Mod",
            "Mod": "status",
            "Status": "Mod status enabled",
        }


def test_a2dismod():
    """
    Test if a2dismod() disables specified modules.
    """

    with patch.dict(
        suse_apache.__salt__,
        {"cmd.retcode": MagicMock(return_value=0)},
    ):
        assert suse_apache.a2dismod("status") == {
            "Name": "Apache2 Disable Mod",
            "Mod": "status",
            "Status": "Mod status disabled",
        }
