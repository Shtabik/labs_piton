import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import warnings

# Импорт модели
from statsmodels.tsa.statespace.sarimax import SARIMAX
from pathlib import Path


# НАСТРОЙКИ И КОНСТАНТЫ
warnings.filterwarnings("ignore")
INPUT_PATH = Path("lab_4_part_5.xlsx")
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# 1) ЗАГРУЗКА И ОЧИСТКА
def load_and_clean(path: Path) -> pd.DataFrame:
    print(f"🔹 Загрузка данных из {path}...")

    # Часто в таких файлах заголовки на 2-й строке (header=1), проверяем это
    try:
        df = pd.read_excel(path, header=1)
    except Exception as e:
        print(f"Ошибка чтения файла: {e}")
        return pd.DataFrame()

    # Переименование колонок для удобства (убираем пробелы и кириллицу из ключей)
    cols_map = {
        'Дата': 'Date',
        'Год': 'Year',
        'Год-мес': 'Raw_YearMonth',
        'точка': 'Point',
        'бренд': 'Brand',
        'товар': 'Product',
        'Количество': 'Quantity',
        'Продажи': 'Sales',
        'Себестоимость': 'Cost'
    }

    df = df.rename(columns=cols_map)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Удаляем строки, где нет даты (иногда в Excel попадают пустые строки в конце)
    df = df.dropna(subset=['Date'])

    for col in ['Quantity', 'Sales', 'Cost']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)


    # Защита от деления на ноль
    df['AvgPrice'] = np.where(df['Quantity'] > 0, df['Sales'] / df['Quantity'], 0)
    df['Profit'] = df['Sales'] - df['Cost']

    # Создаем нормальный столбец Месяц-Год для группировки (тип Period)
    df['MonthPeriod'] = df['Date'].dt.to_period('M')

    print(f"Данные загружены. Строк: {len(df)}")
    return df


# 2) СТАТИСТИКА И АНАЛИЗ
def compute_metrics(df: pd.DataFrame):
    print("🔹 Расчет метрик...")

    if df.empty:
        print("DataFrame пуст, расчет метрик невозможен.")
        return pd.DataFrame()

    # --- Анализ по ТОВАРАМ ---
    product_summary = df.groupby("Product").agg({
        "Quantity": "sum",
        "Sales": "sum",
        "Cost": "sum",
        "Profit": "sum",
        "AvgPrice": "mean"
    })
    product_summary["Margin_%"] = (product_summary["Profit"] / product_summary["Sales"] * 100).round(2)

    # --- Анализ по ТОЧКАМ ---
    point_summary = df.groupby("Point").agg({
        "Sales": ["sum", "mean"],
        "Quantity": "sum",
        "Profit": "sum"
    })
    point_summary.columns = ['Total_Sales', 'Avg_Sales_Per_Transaction', 'Total_Qty', 'Total_Profit']

    # Сброс MultiIndex для удобства сохранения
    point_summary = point_summary.reset_index()

    # --- Сохранение в Excel (analysis_report.xlsx) ---
    try:
        with pd.ExcelWriter(OUTPUT_DIR / "analysis_report.xlsx", engine='openpyxl') as writer:
            product_summary.to_excel(writer, sheet_name="By_Product", index=True)
            point_summary.to_excel(writer, sheet_name="By_Point", index=False)
        print("Отчет сохранен в 'output/analysis_report.xlsx'")
    except Exception as e:
        print(f"Ошибка при сохранении analysis_report.xlsx: {e}")

    return product_summary

# 3) ВИЗУАЛИЗАЦИЯ
def beautify_dates(ax):
    """Вспомогательная функция для красивых дат на оси X"""
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))  # Шаг - 1 месяц
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  # Формат ГГГГ-ММ
    plt.xticks(rotation=45)


def plot_dynamics(df: pd.DataFrame):
    print("🔹 Построение графиков динамики...")

    # 1. Общий товарооборот
    # Группируем по Date (resample по месяцам), чтобы ось X была временной
    monthly_sales = df.set_index('Date').resample('M')['Sales'].sum()

    plt.figure(figsize=(10, 6))
    plt.plot(monthly_sales.index, monthly_sales.values, marker='o', linewidth=2, color='tab:blue')
    plt.title("Динамика общего товарооборота", fontsize=14)
    plt.ylabel("Продажи (ден. ед.)")
    plt.xlabel("Дата")
    plt.grid(True, linestyle='--', alpha=0.7)

    # Применяем форматирование дат
    ax = plt.gca()
    beautify_dates(ax)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "1_total_sales_trend.png")
    plt.close()

    # 2. Динамика по ТОЧКАМ (Top 5 для читаемости)
    top_points = df.groupby('Point')['Sales'].sum().nlargest(5).index
    df_top_points = df[df['Point'].isin(top_points)]

    pivot_points = df_top_points.pivot_table(index='MonthPeriod', columns='Point', values='Sales',
                                             aggfunc='sum').fillna(0)

    # Превращаем индекс обратно в timestamp для графика
    pivot_points.index = pivot_points.index.to_timestamp()

    plt.figure(figsize=(12, 6))
    for col in pivot_points.columns:
        plt.plot(pivot_points.index, pivot_points[col], marker='.', label=col)

    plt.title("Динамика продаж по Точкам (Топ-5)")
    plt.legend()
    plt.grid(True, alpha=0.5)
    ax = plt.gca()
    beautify_dates(ax)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "2_sales_by_point.png")
    plt.close()

# 4) ПРОГНОЗИРОВАНИЕ
def forecast_sales(df: pd.DataFrame):
    print("🔹 Прогнозирование продаж по товарам...")

    forecast_data = []  # Список для сбора всех прогнозов

    # Добавляем данные для записи по листам в Excel, чтобы сохранить исходные ряды
    all_forecast_series = {}

    # Берем топ-10 товаров по продажам
    top_products = df.groupby("Product")["Sales"].sum().nlargest(10).index.tolist()

    for product in top_products:
        # Подготовка ряда
        temp = df[df["Product"] == product].set_index("Date")
        # Ресемплинг по месяцам (M) и заполнение нулями пропусков
        ts = temp["Sales"].resample("MS").sum().fillna(0)

        if len(ts) < 6 or ts.sum() == 0:
            # Пропускаем, если слишком мало данных или продажи равны нулю
            continue

        try:
            # SARIMAX
            model = SARIMAX(ts, order=(1, 1, 1), seasonal_order=(0, 1, 1, 12),
                            enforce_stationarity=False, enforce_invertibility=False)
            model_fit = model.fit(disp=False)

            forecast_steps = 6
            forecast = model_fit.get_forecast(steps=forecast_steps)

            # Ряд для сохранения
            forecast_series = forecast.predicted_mean.round(2)
            all_forecast_series[product] = forecast_series  # Сохраняем для Excel

            # Сбор данных для сводной таблицы
            for date, val in zip(forecast_series.index, forecast_series.values):
                forecast_data.append({
                    "Product": product,
                    "Date": date,
                    "Forecast_Sales": round(val, 2)
                })

            # Визуализация (остается как было)
            plt.figure(figsize=(10, 5))
            plt.plot(ts.index, ts.values, label='История', marker='o')
            plt.plot(forecast_series.index, forecast_series.values, label='Прогноз', marker='o', linestyle='--',
                     color='red')
            plt.title(f"Прогноз: {product}")
            plt.legend()
            plt.grid(True, alpha=0.6)

            ax = plt.gca()
            beautify_dates(ax)

            plt.tight_layout()
            safe_name = str(product).replace("/", "_").replace("\\", "_")
            plt.savefig(OUTPUT_DIR / f"forecast_{safe_name}.png")
            plt.close()

        except Exception as e:
            print(f"Не удалось построить прогноз для {product}: {e}")

    # --- Сохраняем табличные результаты ---
    if all_forecast_series:
        try:
            # Используем явный ExcelWriter для записи нескольких листов
            with pd.ExcelWriter(OUTPUT_DIR / "forecast_results.xlsx", engine='openpyxl') as writer:
                # 1. Сводная таблица
                fc_df = pd.DataFrame(forecast_data)
                fc_df.to_excel(writer, sheet_name="Summary_Table", index=False)

                # 2. Прогнозы по каждому товару
                for prod, series in all_forecast_series.items():
                    # Создаем DataFrame из серии для удобной записи на лист
                    df_out = series.rename("Forecast_Sales").to_frame()
                    df_out.to_excel(writer, sheet_name=f"FC_{prod[:28]}")  # Ограничиваем имя листа

            print("Файл прогнозов сохранен: output/forecast_results.xlsx")

        except Exception as e:
            print(f"Ошибка при сохранении forecast_results.xlsx: {e}")

    else:
        print("Прогнозы не были сформированы (возможно, мало данных или была ошибка в моделировании).")


# MAIN
def main():
    # 1. Загрузка
    if not INPUT_PATH.exists():
        print(f"Файл {INPUT_PATH} не найден! Пожалуйста, положите файл рядом со скриптом.")
        # ГЕНЕРАЦИЯ ТЕСТОВЫХ ДАННЫХ (если файла нет)
        print("Создаю тестовый датасет для демонстрации...")
        dates = pd.date_range(start="2021-01-01", periods=24, freq="ME")  # 2 года
        data = []
        for d in dates:
            for p in ['Товар А', 'Товар Б']:
                data.append(
                    [d, d.year, f"{d.year}-{d.month:02d}", 'Магазин 1', 'Бренд X', p, np.random.randint(10, 100),
                     np.random.randint(1000, 5000), np.random.randint(500, 2000)])

        df_dummy = pd.DataFrame(data,
                                columns=['Дата', 'Год', 'Год-мес', 'точка', 'бренд', 'товар', 'Количество', 'Продажи',
                                         'Себестоимость'])
        # Добавляем пустую строку сверху как в оригинале
        with pd.ExcelWriter(INPUT_PATH) as writer:
            pd.DataFrame(["Header Info"]).to_excel(writer, index=False, header=False)
            df_dummy.to_excel(writer, startrow=1, index=False)
        print("Тестовый файл создан. Перезапустите анализ.")

    df = load_and_clean(INPUT_PATH)

    if not df.empty:
        # 2. Метрики
        compute_metrics(df)
        # 3. Графики
        plot_dynamics(df)
        # 4. Прогноз
        forecast_sales(df)

        print("\nГотово! Проверьте папку 'output'.")


if __name__ == "__main__":
    main()