# Copyright 2024 Canonical Ltd.
# See LICENSE file for licensing details.

import pytest
import subprocess

from charmed_kubeflow_chisme.rock import CheckRock


@pytest.mark.abort_on_fail
def test_rock():
    """Test rock."""
    check_rock = CheckRock("rockcraft.yaml")
    rock_image = check_rock.get_name()
    rock_version = check_rock.get_version()
    LOCAL_ROCK_IMAGE = f"{rock_image}:{rock_version}"

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

    subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "--entrypoint",
            "/bin/bash",
            LOCAL_ROCK_IMAGE,
            "-c",
            "ls -la /ko-app/ingress",
        ],
        check=True,
    )

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
    # ensure no "readOnlyRootFilesystem: true" in the manifests
    subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "--entrypoint",
            "/bin/bash",
            LOCAL_ROCK_IMAGE,
            "-c",
            # A. if grep found the string (test should fail) then grep returns 0.
            # But we want the test to fail, so we do && to return exit code 1
            # B. if grep did NOT find the string (test should succecced) then grep returns 1.
            # But we want the test to succeed, so in this case the && is not calculated,
            # since we have a failing exit code and || exit 0 happens
            'grep -ri "readOnlyRootFilesystem: true" /var/run/ko && exit 1 || exit 0',
        ],
        check=True,
    )