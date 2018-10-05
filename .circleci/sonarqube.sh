#!/bin/bash

if [ -n "${SONAR_TOKEN:-}" ]; then
  SONAR_OPTS="${SONAR_OPTS} -Dsonar.login=${SONAR_TOKEN}"
fi

if [ -n "${CIRCLE_SHA1:-}" ]; then
  SONAR_OPTS="${SONAR_OPTS} -Dsonar.projectVersion=${CIRCLE_SHA1}"
fi

if [ "$CIRCLE_BRANCH" = "develop" ]; then
  SONAR_OPTS="${SONAR_OPTS} -Dsonar.analysis.mode=publish -Dsonar.pullrequest.provider="
else
  PR=$(echo -n $CIRCLE_PULL_REQUEST | tail -c 2)
  SONAR_OPTS="${SONAR_OPTS} -Dsonar.pullrequest.key=${PR} -Dsonar.pullrequest.branch=${CIRCLE_BRANCH}"
fi

echo $SONAR_OPTS

sonar-scanner $SONAR_OPTS
