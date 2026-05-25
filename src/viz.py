import matplotlib.pyplot as plt
import seaborn as sns


def _save_or_show(output_path=None) -> None:
    if output_path:
        plt.savefig(output_path, dpi=160, bbox_inches="tight")
        plt.close()
    else:
        plt.show()


def plot_correlation_matrix(df, numeric_cols=None):
    """Muestra una matriz de correlacion para columnas numericas."""
    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include="number").columns

    plt.figure(figsize=(12, 8))
    corr = df[numeric_cols].corr()

    sns.heatmap(
        corr,
        annot=True,
        cmap="coolwarm",
        fmt=".2f",
        linewidths=0.5,
    )

    plt.title("Correlation Matrix")
    plt.tight_layout()
    _save_or_show()


def plot_depression_vs_social_media(df):
    """Compara horas de redes sociales segun etiqueta de depresion."""
    plt.figure(figsize=(8, 5))

    sns.boxplot(
        data=df,
        x="depression_label",
        y="daily_social_media_hours",
    )

    plt.title("Depression vs Social Media Usage")
    plt.xlabel("Depression label")
    plt.ylabel("Daily social media hours")
    plt.tight_layout()
    _save_or_show()


def plot_numeric_distributions(df, numeric_cols=None):
    """Muestra histogramas de las variables numericas."""
    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include="number").columns

    df[numeric_cols].hist(figsize=(16, 12), bins=20)
    plt.tight_layout()
    _save_or_show()


def plot_depression_rate_by_category(df, categorical_cols, target="depression_label"):
    """Grafica la tasa media de depresion por variable categorica."""
    fig, axes = plt.subplots(1, len(categorical_cols), figsize=(6 * len(categorical_cols), 5))

    if len(categorical_cols) == 1:
        axes = [axes]

    for ax, col in zip(axes, categorical_cols):
        depression_rate = (
            df.groupby(col, observed=True)[target]
            .mean()
            .sort_values(ascending=False)
            .reset_index()
        )
        sns.barplot(data=depression_rate, x=col, y=target, ax=ax)
        ax.set_title(f"{col} vs depression rate")
        ax.set_ylabel("Depression rate")
        ax.tick_params(axis="x", rotation=25)

    plt.tight_layout()
    _save_or_show()


def save_target_distribution(df, output_path, target="depression_label") -> None:
    plt.figure(figsize=(7, 5))
    sns.countplot(data=df, x=target)
    plt.title("Distribution of depression_label")
    plt.xlabel("Depression label")
    plt.ylabel("Frequency")
    plt.tight_layout()
    _save_or_show(output_path)


def save_numeric_distributions(df, output_path, numeric_cols=None) -> None:
    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include="number").columns

    df[numeric_cols].hist(figsize=(16, 12), bins=20)
    plt.suptitle("Numeric Variable Distributions", y=1.02, fontsize=16)
    plt.tight_layout()
    _save_or_show(output_path)


def save_correlation_matrix(df, output_path, numeric_cols=None) -> None:
    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include="number").columns

    plt.figure(figsize=(13, 9))
    corr = df[numeric_cols].corr()
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.title("Correlation Matrix")
    plt.tight_layout()
    _save_or_show(output_path)


def save_numeric_vs_target(df, output_path, target="depression_label") -> None:
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    variables_to_compare = [
        "daily_social_media_hours",
        "sleep_hours",
        "stress_level",
        "anxiety_level",
    ]

    for ax, col in zip(axes.ravel(), variables_to_compare):
        sns.boxplot(data=df, x=target, y=col, ax=ax)
        ax.set_title(f"{col} vs {target}")

    plt.tight_layout()
    _save_or_show(output_path)


def save_depression_rate_by_category(
    df,
    output_path,
    categorical_cols,
    target="depression_label",
) -> None:
    fig, axes = plt.subplots(1, len(categorical_cols), figsize=(6 * len(categorical_cols), 5))

    if len(categorical_cols) == 1:
        axes = [axes]

    for ax, col in zip(axes, categorical_cols):
        depression_rate = (
            df.groupby(col, observed=True)[target]
            .mean()
            .sort_values(ascending=False)
            .reset_index()
        )
        sns.barplot(data=depression_rate, x=col, y=target, ax=ax)
        ax.set_title(f"{col} vs depression rate")
        ax.set_ylabel("Depression rate")
        ax.tick_params(axis="x", rotation=25)

    plt.tight_layout()
    _save_or_show(output_path)


def save_cramers_v_by_category(report_df, output_path) -> None:
    plt.figure(figsize=(8, 5))
    sns.barplot(data=report_df, x="feature", y="cramers_v")
    plt.title("Cramer's V by Categorical Feature")
    plt.xlabel("Feature")
    plt.ylabel("Cramer's V")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    _save_or_show(output_path)
