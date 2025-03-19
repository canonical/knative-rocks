# Copyright 2024 Canonical Ltd.
# See LICENSE file for licensing details.

import pytest
import subprocess
import logging

from charmed_kubeflow_chisme.rock import CheckRock


@pytest.mark.abort_on_fail
def test_rock():
    """Test rock."""
    check_rock = CheckRock("rockcraft.yaml")
    rock_image = check_rock.get_name()
    rock_version = check_rock.get_version()
    LOCAL_ROCK_IMAGE = f"{rock_image}:{rock_version}"
    logging.info("start")
    # assert the rock contains the expected files
    subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "--entrypoint",
            "/bin/bash",
            LOCAL_ROCK_IMAGE,
            "-c",
            "ls -la /var/run/ko",
        ],
        check=True,

    )
    logging.info("start")
    subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "--entrypoint",
            "/bin/bash",
            LOCAL_ROCK_IMAGE,
            "-c",
            "ls -la /ko-app/controller",
        ],
        check=True,
    )
    logging.info("start")
    # check for SSL cert file
    subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "--entrypoint",
            "/bin/bash",
            LOCAL_ROCK_IMAGE,
            "-c",
            "ls -la /etc/ssl/certs/ca-certificates.crt",
        ],
        check=True,
    )
    logging.info("start")