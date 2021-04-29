#!/usr/bin/env python3
# Copyright 2021 Jon Seager
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""Charm the service.

Refer to the following post for a quick-start guide that will help you
develop a new k8s charm using the Operator Framework:

    https://discourse.charmhub.io/t/4208
"""

import logging

from ops.charm import CharmBase
from ops.main import main
from ops.model import ActiveStatus

logger = logging.getLogger(__name__)


class HookTestCharm(CharmBase):
    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.httpbin_pebble_ready, self._on_httpbin_pebble_ready)
        self.framework.observe(self.on.stop, self._on_stop)
        self.framework.observe(self.on.remove, self._on_remove)

    def _on_stop(self, event):
        logger.info("REMOVE EVENT\nREMOVE EVENT\nREMOVE EVENT")

    def _on_remove(self, event):
        logger.info("REMOVE EVENT\nREMOVE EVENT\nREMOVE EVENT")

    def _on_httpbin_pebble_ready(self, event):
        """Define and start a workload using the Pebble API."""
        container = event.workload
        pebble_layer = {
            "services": {
                "httpbin": {
                    "override": "replace",
                    "summary": "httpbin",
                    "command": "gunicorn -b 0.0.0.0:80 httpbin:app -k gevent",
                    "startup": "enabled",
                    "environment": {},
                }
            },
        }
        container.add_layer("httpbin", pebble_layer, combine=True)
        container.autostart()
        self.unit.status = ActiveStatus()


if __name__ == "__main__":
    main(HookTestCharm)
