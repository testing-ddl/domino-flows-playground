#!/usr/bin/env bash
##
## Helper script to run generate_artifacts.generate_artifacts_with_netapp_volume_exports
## with the specified netapp volume. The script parses the netapp volume id from
## the input netapp volume URL, and creates a new workflow file with this netapp
## volume id injected into it via sed.
##

NETAPP_VOLUME_ID=$(basename "${1%/*}")
sed "s/NETAPP_VOLUME_ID_TEMPLATE/$NETAPP_VOLUME_ID/g" generate_artifacts.py > generate_artifacts_with_netapp_volume_exports.py
pyflyte run --remote generate_artifacts_with_netapp_volume_exports.py generate_artifacts_with_netapp_volume_exports
