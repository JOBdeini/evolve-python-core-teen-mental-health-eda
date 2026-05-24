# Teen Mental Health EDA

Proyecto de analisis exploratorio de datos sobre habitos digitales, descanso, actividad fisica y salud mental en adolescentes.

## Objetivo

El objetivo es estudiar patrones asociados a la variable `depression_label`, prestando atencion a:

- Uso diario de redes sociales.
- Horas de sueno y uso de pantallas antes de dormir.
- Nivel de estres, ansiedad y adiccion.
- Rendimiento academico y actividad fisica.
- Diferencias por variables categoricas como genero, plataforma y nivel de interaccion social.

## Preguntas de investigacion

Este EDA se organiza alrededor de tres preguntas principales:

1. Influye el uso de redes sociales en la salud mental de los usuarios adolescentes?
2. Que variables se repiten con mas frecuencia en los usuarios con `depression_label = 1` frente a los que no presentan esa etiqueta?
3. Cual es el perfil de usuario con mayor tendencia observada a presentar riesgo de depresion dentro de este dataset?

## Estructura del proyecto

```text
proyecto-github-01/
|-- data/
|   |-- raw/
|   |   `-- Teen_Mental_Health_Dataset.csv
|   `-- processed/
|       `-- teen_mental_health_processed.csv
|-- notebooks/
|   |-- 01_teen_mental_health_eda.ipynb
|   `-- 01_teen_mental_health_eda_original_copy.ipynb
|-- reports/
|   `-- figures/
|       |-- 01_target_distribution.png
|       |-- 02_numeric_distributions.png
|       |-- 03_correlation_matrix.png
|       |-- 04_numeric_vs_depression_label.png
|       |-- 05_depression_rate_by_category.png
|       `-- 06_cramers_v_by_category.png
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

## Ruta recomendada de revision

Para revisar el proyecto en GitHub, el orden recomendado es:

1. Leer este `README.md` para entender el objetivo, la estructura y las conclusiones principales.
2. Abrir `notebooks/01_teen_mental_health_eda.ipynb` para revisar el EDA completo, con codigo, tablas, graficas y conclusiones.
3. Consultar `reports/figures/` para ver las visualizaciones principales exportadas como imagenes.
4. Revisar `src/` para comprobar que la limpieza, el feature engineering y las utilidades estan modularizadas.
5. Ejecutar `python main.py` para regenerar el dataset procesado desde `data/raw/`.

## Notebook principal

El analisis limpio y presentable esta en:

```text
notebooks/01_teen_mental_health_eda.ipynb
```

La version previa se conserva como copia de respaldo en:

```text
notebooks/01_teen_mental_health_eda_original_copy.ipynb
```

Incluye:

- Carga y validacion inicial del dataset.
- Limpieza de datos y conversion de tipos.
- Feature engineering.
- Analisis descriptivo.
- Distribuciones y correlaciones.
- Comparacion de variables frente a `depression_label`.
- Pruebas chi-cuadrado y Cramer's V para variables categoricas.
- Interpretacion de resultados despues de las validaciones y graficas principales.

## Como queda documentado el EDA

El EDA queda documentado en tres niveles:

- `README.md`: resumen ejecutivo del proyecto, instrucciones de ejecucion y principales conclusiones.
- `notebooks/01_teen_mental_health_eda.ipynb`: analisis paso a paso, con codigo reproducible y outputs guardados.
- `reports/figures/`: graficas exportadas para facilitar la revision sin ejecutar el notebook.

## Visualizaciones

Las principales graficas del analisis se guardan tambien como imagenes en `reports/figures/`.

![Distribucion de depression_label](reports/figures/01_target_distribution.png)

![Matriz de correlacion](reports/figures/03_correlation_matrix.png)

![Variables numericas frente a depression_label](reports/figures/04_numeric_vs_depression_label.png)

## Respuesta a las preguntas de investigacion

### 1. Influye el uso de redes sociales en la salud mental?

El analisis muestra una asociacion entre mayor uso diario de redes sociales y `depression_label = 1`. El grupo con depresion registra una media aproximada de 6.72 horas diarias de redes sociales, frente a 4.48 horas en el grupo sin depresion. Ademas, todos los casos positivos aparecen dentro del grupo de usuarios intensivos, definido como 5 o mas horas diarias de uso.

La correlacion entre `daily_social_media_hours` y `depression_label` es positiva, aunque moderada. Por tanto, el dataset sugiere una relacion relevante, pero no permite afirmar causalidad. No se puede concluir que las redes sociales causen depresion; tambien podria ocurrir que usuarios con peor salud mental pasen mas tiempo en redes sociales.

### 2. Que variables se repiten en usuarios con depression_label = 1?

Las variables que mas diferencian al grupo con `depression_label = 1` son:

- Mayor uso diario de redes sociales.
- Menos horas de sueno.
- Mayor nivel de estres.
- Mayor nivel de ansiedad.
- Mayor `risk_score`.
- Peor categoria de calidad de sueno.

En cambio, edad, rendimiento academico, actividad fisica, screen time antes de dormir y addiction level no muestran diferencias tan claras en la comparacion directa de medias. Las variables categoricas originales muestran diferencias descriptivas leves: la tasa de depresion es algo mayor en mujeres y en usuarios de TikTok, pero las pruebas chi-cuadrado no muestran una asociacion fuerte para genero, plataforma o nivel de interaccion social.

### 3. Cual es el perfil de mayor tendencia observada?

Dentro de este dataset, el perfil con mayor tendencia observada a `depression_label = 1` combina varios factores:

- Usuario adolescente con 5 o mas horas diarias de redes sociales.
- Menor calidad de sueno, especialmente categoria `poor`.
- Niveles altos de estres y ansiedad.
- `risk_score` alto.
- Ligera mayor presencia descriptiva en mujeres y usuarios de TikTok, aunque sin evidencia estadistica fuerte en esta muestra.

La conclusion principal es que el riesgo no parece depender de una unica variable aislada, sino de la acumulacion de factores: uso intensivo de redes, peor descanso y mayor malestar emocional. El dataset contiene 1200 registros, no presenta nulos ni duplicados, y la clase positiva esta desbalanceada: aproximadamente un 2.6% de los registros tienen `depression_label = 1`.

## Nota

Este EDA es exploratorio. Las asociaciones observadas no implican causalidad y conviene interpretar los resultados teniendo en cuenta el desbalance de la variable objetivo.
