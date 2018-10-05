#!/bin/bash

if [ -n "${SONAR_TOKEN:-}" ]; then
  SONAR_OPTS="${SONAR_OPTS} -Dsonar.login=${SONAR_TOKEN}"
fi

if [ -n "${CIRCLE_SHA1:-}" ]; then
  SONAR_OPTS="${SONAR_OPTS} -Dsonar.projectVersion=${CIRCLE_SHA1}"
fi

if [ "$CIRCLE_BRANCH" = "develop" ]; then
  SONAR_OPTS="${SONAR_OPTS} -Dsonar.analysis.mode=publish"
else
  if [ "$CIRCLE_PULL_REQUEST" != "" ]; then
    PR=$(echo -n $CIRCLE_PULL_REQUEST | tail -c 2)
    SONAR_OPTS="${SONAR_OPTS} -Dsonar.pullrequest.key=${PR}"
    SONAR_OPTS="${SONAR_OPTS} -Dsonar.pullrequest.base=develop"
    SONAR_OPTS="${SONAR_OPTS} -Dsonar.pullrequest.branch=${CIRCLE_BRANCH}"
    SONAR_OPTS="${SONAR_OPTS} -Dsonar.pullrequest.endpoint=https://api.github.com/"
    SONAR_OPTS="${SONAR_OPTS} -Dsonar.pullrequest.provider=GitHub"
    SONAR_OPTS="${SONAR_OPTS} -Dsonar.pullrequest.github.repository=TyVik/geopuzzle"
    SONAR_OPTS="${SONAR_OPTS} -Dsonar.pullrequest.github.token.secured=${GITHUB_TOKEN}"
  fi
fi

echo $SONAR_OPTS

sonar-scanner $SONAR_OPTS
