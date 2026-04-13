# Ejercicio Técnico — Data Integration Engineer

## Contexto

Este repositorio contiene un ejercicio técnico para el rol de **Data Integration Engineer**. El objetivo es construir un pipeline ETL productivo que consuma la API pública del Banco de México (Banxico), transforme los datos y los persista con plena observabilidad en cada capa.

El package `vmetrix` ya está construido y funcional. No es necesario modificarlo — está ahí para que puedas concentrarte en la lógica del pipeline, no en la infraestructura.

---

## Estructura del repositorio

```
├── vmetrix/                  # Package base — no modificar
│   ├── __init__.py           # Configura logging y expone los singletons
│   ├── banxico_api.py        # Cliente HTTP para la API SIE de Banxico
│   ├── config.py             # Loader de variables de entorno desde .env
│   ├── database.py           # Wrapper sobre DuckDB local
│   ├── database.sql          # Schema de LocalDb — agregar tus DDLs aquí
│   ├── db.duckdb             # Base de datos local
│   └── .env                  # Token de API (incluido solo para este ejercicio)
├── s3_datalake/              # Carpeta vacía — simula un bucket S3
├── img/
│   └── business_case.png     # Diagrama de arquitectura objetivo
├── code_examples.ipynb       # Ejemplos de uso del package — leer antes de empezar
├── interview.ipynb           # Enunciado del ejercicio — trabajar aquí
└── CLAUDE.md                 # Documentación técnica del repositorio
```

---

## Antes de empezar

Ejecuta las celdas de `code_examples.ipynb` para verificar que tienes conectividad con la API de Banxico y acceso a la base local. Si algo no funciona en ese notebook, no va a funcionar en el ejercicio.

El token de la API está en `vmetrix/.env` y es válido solo para este ejercicio.

---

## El ejercicio

Los requerimientos completos están en `interview.ipynb`. En resumen:

1. **Carga histórica** de cuatro securities financieros desde `2025-01-01` hasta hoy.
2. **Carga diaria incremental** con los valores vigentes del día.
3. **Estadísticas móviles** de 7 días por security.
4. **Almacenamiento RAW** de cada respuesta de la API en `s3_datalake/` como Parquet.
5. **Idempotencia**: ejecutar el pipeline dos veces produce el mismo estado final, sin duplicados.
6. **Logging** estructurado en cada etapa del pipeline.
7. **Justificación explícita** de cada decisión DuckDB vs Python en comentarios.

Los criterios de evaluación están ordenados por prioridad dentro del notebook.

---

## Reglas del juego

**Plazo**: tienes 72 horas desde que recibes este repositorio para entregar tu solución.

**Entrega**: haz un fork del repositorio y comparte el link antes de que venza el plazo. El código tiene que correr en tu ambiente al momento de la entrevista — no se acepta código que funcionaba antes pero no funciona durante la sesión.

**Herramientas**: puedes usar todo lo que usarías en tu trabajo real — internet, documentación, IA, librerías adicionales. No hay restricciones. Lo que se evalúa no es si usaste ayuda, sino si entiendes lo que produjiste.

**Ambiente**: trabaja en el ambiente que prefieras. El único requisito es que puedas ejecutar cualquier celda del notebook en vivo durante la entrevista sin preparación adicional.

---

## La entrevista

La sesión dura **80 minutos** y tiene tres partes:

**Revisión del código entregado — 20 minutos**
Explicas tu solución, las decisiones que tomaste y lo que cambiarías. Las preguntas se enfocan en el razonamiento detrás de las decisiones, no solo en el resultado.

**Extensión en vivo — 40 minutos**
Se presenta un requerimiento nuevo que no estaba en el ejercicio. Lo implementas en tu ambiente con acceso a todo lo que usaste antes. No hay restricciones adicionales.

**Preguntas de cierre — 20 minutos**
Preguntas abiertas sobre diseño, decisiones técnicas y criterio.

---

## Lo que se evalúa

En orden de importancia:

1. **Idempotencia** — el pipeline es reprocesable sin efectos secundarios.
2. **Criterio sobre herramientas** — la elección DuckDB vs Python en cada transformación es razonada y justificada, no mecánica.
3. **Calidad del código** — logging, modelo de datos, manejo de errores, consistencia de estilo.
4. **Autonomía bajo presión** — cómo razonas y decides durante la extensión en vivo, no solo si terminas.
5. **Autocrítica** — capacidad de identificar las limitaciones de tu propia solución.

---

## Preguntas

Si algo del enunciado no está claro, escribe antes de asumir. Una pregunta bien formulada ya dice algo sobre cómo trabajas.
