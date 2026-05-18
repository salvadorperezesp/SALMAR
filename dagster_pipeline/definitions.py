

from dagster import (
    Definitions,
    define_asset_job,
    ScheduleDefinition,
    AssetSelection,
)
from dagster_pipeline.assets import (
    datos_crudos,
    datos_procesados,
    muestra_entrenamiento,
    modelo_entrenado,
    reporte_evaluacion,
)

pipeline_vuelos = define_asset_job(
    name="pipeline_vuelos",
    selection=AssetSelection.all(),
    description="Pipeline completo: carga → limpieza → muestra → entrenamiento → evaluación",
)

schedule_semanal = ScheduleDefinition(
    job=pipeline_vuelos,
    cron_schedule="0 6 1 1 *",  # cada 1 de enero a las 6:00 AM
    name="schedule_semanal_vuelos",
)

defs = Definitions(
    assets=[
        datos_crudos,
        datos_procesados,
        muestra_entrenamiento,
        modelo_entrenado,
        reporte_evaluacion,
    ],
    jobs=[pipeline_vuelos],
    schedules=[schedule_semanal],
)
