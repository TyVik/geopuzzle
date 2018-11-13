#!/bin/sh

set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
	CREATE DATABASE template_postgis;
	UPDATE pg_database SET datistemplate = TRUE WHERE datname = 'template_postgis';
EOSQL

for DB in template_postgis "$POSTGRES_DB"; do
	echo "Loading PostGIS extensions into $DB"
	psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname="$DB" <<-EOSQL
		CREATE EXTENSION IF NOT EXISTS postgis;
		CREATE EXTENSION IF NOT EXISTS postgis_topology;
		CREATE EXTENSION IF NOT EXISTS postgis_sfcgal;
		CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;
		CREATE EXTENSION IF NOT EXISTS address_standardizer;
		CREATE EXTENSION IF NOT EXISTS postgis_tiger_geocoder;
	EOSQL
done