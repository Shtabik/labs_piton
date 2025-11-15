import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LinearRegression
from statsmodels.tsa.statespace.sarimax import SARIMAX

from pathlib import Path


INPUT_PATH = Path("lab_4_part_5.xlsx")
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


# -------------------------------------------------------
# 1) ЗАГРУЗКА И ОЧИСТКА
# -------------------------------------------------------
def load_and_clean(path: Path) -> pd.DataFrame:
    print("Loading and cleaning data...")

    # файл начинается со второй строки
    df = pd.read_excel(path, header=1)

    # Переименование колонок
    df = df.rename(columns={
        'Дата': 'Date',
        'Год': 'Year',
        'Год-мес': 'YearMonth',
        'точка': 'Point',
        'бренд': 'Brand',
        'товар': 'Product',
        'Количество': 'Quantity',
        'Продажи': 'Sales',
        'Себестоимость': 'Cost'
    })

    # Приведение типов
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
    df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
    df['Cost'] = pd.to_numeric(df['Cost'], errors='coerce')

    # Вычисляем derived-поля
    df['AvgPrice'] = df['Sales'] / df['Quantity']
    df['Profit'] = df['Sales'] - df['Cost']

    print("Data loaded. Rows:", len(df))
    return df


# -------------------------------------------------------
# 2) СТАТИСТИКА И МЕТРИКИ
# -------------------------------------------------------
def compute_metrics(df: pd.DataFrame):
    print("Computing metrics...")

    summary = df.groupby("Product").agg({
        "Quantity": "sum",
        "Sales": "sum",
        "Cost": "sum",
        "Profit": "sum",
        "AvgPrice": "mean"
    })

    summary["Margin"] = summary["Profit"] / summary["Sales"]

    summary.to_excel(OUTPUT_DIR / "summary_products.xlsx")
    print("Saved summary_products.xlsx")

    return summary


# -------------------------------------------------------
# 3) ВИЗУАЛИЗАЦИИ
# -------------------------------------------------------
def plot_sales_by_month(df: pd.DataFrame):
    print("Plotting monthly sales...")

    monthly = df.groupby("YearMonth")["Sales"].sum()

    plt.figure(figsize=(12, 5))
    monthly.plot()
    plt.title("Динамика общего товарооборота")
    plt.xlabel("Год-месяц")
    plt.ylabel("Продажи")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "sales_total_trend.png")
    plt.close()


def plot_products(df: pd.DataFrame):
    print("Plotting per-product trends...")

    for product in df["Product"].unique():
        temp = df[df["Product"] == product].groupby("YearMonth")["Sales"].sum()

        plt.figure(figsize=(12, 5))
        temp.plot()
        plt.title(f"Динамика продаж: {product}")
        plt.xlabel("Год-месяц")
        plt.ylabel("Продажи")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / f"trend_{product}.png")
        plt.close()


# -------------------------------------------------------
# 4) ПРОГНОЗЫ
# -------------------------------------------------------
def forecast_sales_per_product(df: pd.DataFrame):
    print("Forecasting...")

    forecast_results = {}

    for product in df["Product"].unique():
        temp = df[df["Product"] == product].groupby("Date")["Sales"].sum().asfreq("MS")

        temp = temp.fillna(method="ffill").fillna(0)

        model = SARIMAX(temp, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
        model_fit = model.fit(disp=False)

        future = model_fit.forecast(6)
        forecast_results[product] = future

        plt.figure(figsize=(12, 5))
        temp.plot(label="Исторические продажи")
        future.plot(label="Прогноз")
        plt.title(f"Прогноз продаж: {product}")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / f"forecast_{product}.png")
        plt.close()

    # сохранить в файл
    writer = pd.ExcelWriter(OUTPUT_DIR / "forecast.xlsx")
    for prod, series in forecast_results.items():
        df_out = pd.DataFrame({"Forecast": series})
        df_out.to_excel(writer, sheet_name=str(prod))
    writer.close()

    print("Saved forecast.xlsx")


# -------------------------------------------------------
# MAIN
# -------------------------------------------------------
def main():
    df = load_and_clean(INPUT_PATH)

    compute_metrics(df)
    plot_sales_by_month(df)
    plot_products(df)
    forecast_sales_per_product(df)

    print("\nAll processing complete! Check /output folder.")


if __name__ == "__main__":
    main()
