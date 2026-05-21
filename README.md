# Teen Mental Health EDA

Proyecto de analisis exploratorio de datos sobre habitos digitales, descanso, actividad fisica y salud mental en adolescentes.

## Objetivo

El objetivo es estudiar patrones asociados a la variable `depression_label`, prestando atencion a:

- Uso diario de redes sociales.
- Horas de sueno y uso de pantallas antes de dormir.
- Nivel de estres, ansiedad y adiccion.
- Rendimiento academico y actividad fisica.
- Diferencias por variables categoricas como genero, plataforma y nivel de interaccion social.

## Estructura del proyecto

```text
proyecto-github-01/
|-- data/
|   |-- raw/
|   |   `-- Teen_Mental_Health_Dataset.csv
|   `-- processed/
|       `-- teen_mental_health_processed.csv
|-- notebooks/
|   `-- 01_teen_mental_health_eda.ipynb
|-- src/
|   |-- cleaning.py
|   |-- features.py
|   |-- io.py
|   |-- utils.py
|   `-- viz.py
|-- main.py
|-- requirements.txt
`-- README.md
```

## Instalacion

Desde la raiz del proyecto:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecucion

Para generar el dataset procesado:

```bash
python main.py
```

El archivo resultante se guarda en:

```text
data/processed/teen_mental_health_processed.csv
```

## Notebook principal

El analisis limpio y presentable esta en:

```text
notebooks/01_teen_mental_health_eda.ipynb
```

Incluye:

- Carga y validacion inicial del dataset.
- Limpieza de datos y conversion de tipos.
- Feature engineering.
- Analisis descriptivo.
- Distribuciones y correlaciones.
- Comparacion de variables frente a `depression_label`.
- Pruebas chi-cuadrado y Cramer's V para variables categoricas.

## Principales conclusiones iniciales

- El dataset contiene 1200 registros y no presenta nulos ni duplicados en la version original revisada.
- La variable `depression_label` esta muy desbalanceada: aproximadamente un 2.6% de registros positivos.
- Las correlaciones lineales mas destacadas con `depression_label` son positivas para horas diarias en redes sociales, estres y ansiedad, y negativa para horas de sueno.
- En las variables categoricas analizadas, las pruebas chi-cuadrado no muestran una asociacion fuerte con `depression_label` en esta muestra.

## Nota

Este EDA es exploratorio. Las asociaciones observadas no implican causalidad y conviene interpretar los resultados teniendo en cuenta el desbalance de la variable objetivo.
