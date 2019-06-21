#! /bin/bash
#
# NATS Queue with Configuration
# =============================================================================
# Run docker image  in a new container.
# This is NOT run in "detached" (-d) mode.
# =============================================================================

IMAGE_NAME="nats-adroffner"
TAG="latest"

DOCKERFILE=Dockerfile

FULL_IMAGE_NAME="${IMAGE_NAME}:${TAG}"

docker run --rm -ti -p 4222:4222 $FULL_IMAGE_NAME -D
