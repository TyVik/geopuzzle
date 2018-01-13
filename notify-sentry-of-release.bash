#!/bin/bash -ex

# Create a Sentry API key with project:write permissions from under your Sentry organization's settings.
# Set the following environment variables.

# SENTRY_TOKEN         (Required) Sentry Token
# SENTRY_ORGANIZATION    (Optional) Slug (aka name) for the Sentry organization.
#                           If not provided, this script assumes Sentry matches Bitbucket organization.
#                           Example: "demo"
# SENTRY_PROJECT         (Optional) Slug (aka name) for the Sentry project.
#                           If not provided, this script assumes Sentry matches Bitbucket repository.
#                           Example: "ZeroDivisionError"
# BITBUCKET_COMMIT       (Provided) Commit SHA that triggered the build.

curl https://sentry.io/api/0/organizations/${SENTRY_ORGANIZATION}/releases/ \
    -H "Authorization: Bearer ${SENTRY_TOKEN}" \
    -X POST \
    -H "Content-Type:application/json" \
    -d "{\"version\":\"${BITBUCKET_COMMIT}\",\"ref\":\"${BITBUCKET_BRANCH}\",\"projects\": [\"${SENTRY_PROJECT}\"]}"