from django.contrib.postgres.indexes import GinIndex


class GinIndexTrgrm(GinIndex):
    def create_sql(self, model, schema_editor, using=''):
        statement = super().create_sql(model, schema_editor)
        statement.template = 'CREATE INDEX %(name)s ON %(table)s%(using)s (%(columns)s gin_trgm_ops)%(extra)s%(condition)s'
        return statement
