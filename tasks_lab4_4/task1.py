# analyze_s7.py (исправленный и устойчивый вариант)
import os
import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.statespace.sarimax import SARIMAX

# -----------------------------
# Настройки
# -----------------------------
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

sns.set(style="whitegrid")
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)

CSV_PATH = "s7_tickets.csv"

# -----------------------------
# Вспомогательные: генерация синтетики (если нужно)
# -----------------------------
def generate_synthetic_s7(start_date="2021-01-01", end_date="2024-12-31", n_records_per_day=30):
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    all_dates = pd.date_range(start, end, freq="D")

    origins = ["SVO", "DME", "LED", "KRR", "OVB", "ROV", "VKO"]
    destinations = ["SVO", "LED", "AYT", "SVX", "KZN", "KUF", "EGO"]
    payment_methods = ["card", "apple_pay", "google_pay", "cash", "bank_transfer"]
    passenger_types = ["adult", "child", "infant"]
    booking_classes = ["economy", "premium", "business"]

    records = []
    for d in all_dates:
        season_factor = 1.0
        if d.month in (6,7,8):
            season_factor = 1.4
        elif d.month == 12:
            season_factor = 1.2
        elif d.month in (1,2):
            season_factor = 0.9

        n = max(1, int(n_records_per_day * (0.7 + np.random.rand()*0.6) * season_factor))
        for _ in range(n):
            origin = random.choice(origins)
            dest = random.choice([c for c in destinations if c != origin])
            purchase_date = d + pd.Timedelta(hours=random.randint(0,23), minutes=random.randint(0,59))
            segments = random.choice([1,1,1,2])
            base_fare = np.random.normal(8000, 3000)
            cls = random.choices(booking_classes, weights=[0.8, 0.15, 0.05])[0]
            if cls == "premium":
                base_fare *= 1.6
            elif cls == "business":
                base_fare *= 3.5
            promo = np.random.choice([1.0, 0.8, 0.9, 1.2], p=[0.75, 0.05, 0.15, 0.05])
            fare = max(500, int(base_fare * (1 + 0.05*segments) * promo))
            payment = random.choices(payment_methods, weights=[0.7, 0.08, 0.07, 0.1, 0.05])[0]
            p_type = random.choices(passenger_types, weights=[0.9, 0.08, 0.02])[0]
            loyalty = random.choices(["silver", "gold", "none"], weights=[0.12, 0.03, 0.85])[0]
            if loyalty != "none" and np.random.rand() < 0.15:
                fare = int(fare * 1.2)
            records.append({
                "purchase_datetime": purchase_date,
                "origin": origin,
                "destination": dest,
                "segments": segments,
                "booking_class": cls,
                "fare": fare,
                "payment_method": payment,
                "passenger_type": p_type,
                "loyalty_status": loyalty
            })
    df = pd.DataFrame(records)
    df["date"] = pd.to_datetime(df["purchase_datetime"]).dt.date
    df["month"] = pd.to_datetime(df["purchase_datetime"]).dt.to_period("M").dt.to_timestamp()
    df["year"] = pd.to_datetime(df["purchase_datetime"]).dt.year
    return df

# -----------------------------
# 1) Загрузка или генерация данных
# -----------------------------
if os.path.exists(CSV_PATH):
    print("Найден s7_tickets.csv — загружаю реальный датасет.")
    df = pd.read_csv(CSV_PATH, parse_dates=["purchase_datetime"], dayfirst=False, infer_datetime_format=True)
    # Приводим purchase_datetime к datetime на всякий случай
    df["purchase_datetime"] = pd.to_datetime(df["purchase_datetime"], errors="coerce")
    # Удаляем строки с некорректной датой
    nbad = df["purchase_datetime"].isna().sum()
    if nbad:
        print(f"Внимание: {nbad} строк с некорректным purchase_datetime удалено.")
        df = df.dropna(subset=["purchase_datetime"]).copy()
    # Если столбца month нет — создаём
    df["month"] = pd.to_datetime(df["purchase_datetime"]).dt.to_period("M").dt.to_timestamp()
    df["date"] = pd.to_datetime(df["purchase_datetime"]).dt.date
    df["year"] = pd.to_datetime(df["purchase_datetime"]).dt.year
else:
    print("Реальный CSV не найден — генерирую синтетические данные (пример).")
    df = generate_synthetic_s7(start_date="2021-01-01", end_date="2024-12-31", n_records_per_day=40)

print(f"Размер датасета: {df.shape}")
print(df.head())

# -----------------------------
# 2) Описательная статистика
# -----------------------------
desc = df[["fare", "segments"]].describe(percentiles=[0.25, 0.5, 0.75]).T
desc.to_csv(os.path.join(OUTPUT_DIR, "descriptive_stats.csv"))
print("\nОписательная статистика (fare, segments):")
print(desc)

# -----------------------------
# 3) Месячная агрегация — убедительная конвертация month -> datetime
# -----------------------------
monthly = df.groupby("month").agg(
    revenue=pd.NamedAgg(column="fare", aggfunc="sum"),
    tickets=pd.NamedAgg(column="fare", aggfunc="count")
).reset_index()

# ВАЖНЫЙ ФИКС: явно привести month к datetime (если это не так)
monthly["month"] = pd.to_datetime(monthly["month"], errors="coerce")
monthly = monthly.dropna(subset=["month"]).sort_values("month").reset_index(drop=True)

# Создаём корректный временной ряд с частотой начала месяца
monthly_ts = monthly.set_index("month").asfreq("MS")
monthly_ts["revenue"] = monthly_ts["revenue"].interpolate()  # интерполируем пропуски

monthly.to_csv(os.path.join(OUTPUT_DIR, "monthly_revenue_tickets.csv"), index=False)

# -----------------------------
# 4) График — выручка по месяцам (корректный datetime индекс)
# -----------------------------
plt.figure(figsize=(12,5))
plt.plot(monthly_ts.index, monthly_ts["revenue"], marker="o")
plt.title("Месячная выручка")
plt.xlabel("Месяц")
plt.ylabel("Выручка (руб.)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "monthly_revenue.png"))
plt.show(block=False)
plt.close()

# -----------------------------
# 5) Топ аэропортов (по отправлениям и выручке)
# -----------------------------
top_orig = df["origin"].value_counts().rename_axis("origin").reset_index(name="departures")
top_orig.to_csv(os.path.join(OUTPUT_DIR, "top_origins.csv"), index=False)
plt.figure(figsize=(8,4))
sns.barplot(data=top_orig, x="origin", y="departures")
plt.title("Отправления по аэропортам (Top)")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "top_origins.png"))
plt.show(block=False)
plt.close()

rev_by_origin = df.groupby("origin")["fare"].sum().sort_values(ascending=False).reset_index()
rev_by_origin.to_csv(os.path.join(OUTPUT_DIR, "revenue_by_origin.csv"), index=False)
plt.figure(figsize=(8,4))
sns.barplot(data=rev_by_origin, x="origin", y="fare")
plt.title("Выручка по аэропортам отправления")
plt.ylabel("Выручка (руб.)")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "revenue_by_origin.png"))
plt.show(block=False)
plt.close()

# -----------------------------
# 6) Сезонность: декомпозиция
# -----------------------------
try:
    decomposition = seasonal_decompose(monthly_ts["revenue"], model="additive", period=12, extrapolate_trend='freq')
    fig = decomposition.plot()
    fig.set_size_inches(12,8)
    fig.suptitle("Декомпозиция месячной выручки (trend/seasonal/resid)", fontsize=14)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "decomposition_revenue.png"))
    plt.show(block=False)
    plt.close()
except Exception as e:
    print("Не удалось выполнить seasonal_decompose:", e)

# -----------------------------
# 7) Анализ по типам пассажиров / loyalty / payment (если есть)
# -----------------------------
if "passenger_type" in df.columns:
    pt_counts = df["passenger_type"].value_counts()
    pt_counts.to_csv(os.path.join(OUTPUT_DIR, "passenger_type_counts.csv"))
    plt.figure(figsize=(6,4))
    sns.barplot(x=pt_counts.index, y=pt_counts.values)
    plt.title("Типы пассажиров")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "passenger_types.png"))
    plt.show(block=False)
    plt.close()

if "loyalty_status" in df.columns:
    loy = df.groupby("loyalty_status")["fare"].agg(["count","mean","sum"]).reset_index()
    loy.to_csv(os.path.join(OUTPUT_DIR, "loyalty_stats.csv"), index=False)
    print("\nСтатистика по loyalty status:")
    print(loy)

if "payment_method" in df.columns:
    pay_stats = df.groupby("payment_method")["fare"].agg(["count","mean","sum"]).sort_values(by="count", ascending=False)
    pay_stats.to_csv(os.path.join(OUTPUT_DIR, "payment_stats.csv"))
    print("\nСтатистика по способам оплаты:")
    print(pay_stats)
    plt.figure(figsize=(8,4))
    sns.barplot(x=pay_stats.index, y=pay_stats["count"].values)
    plt.title("Количество платежей по методам оплаты")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "payment_method_counts.png"))
    plt.show(block=False)
    plt.close()

# -----------------------------
# 8) Простой прогноз: SARIMAX для месячной выручки
# -----------------------------
ts = monthly_ts["revenue"].copy()
if len(ts) < 12:
    print("Слишком мало точек для надёжного сезонного прогноза (меньше 12 месяцев).")
else:
    train = ts.iloc[:-6] if len(ts) > 6 else ts
    steps = 6
    print("\nОбучение SARIMAX на месячной выручке...")
    try:
        model = SARIMAX(train, order=(1,0,1), seasonal_order=(1,1,1,12),
                        enforce_stationarity=False, enforce_invertibility=False)
        res = model.fit(disp=False)
        fc = res.get_forecast(steps=steps)
        idx = pd.date_range(train.index[-1] + pd.offsets.MonthBegin(), periods=steps, freq="MS")
        fc_mean = pd.Series(fc.predicted_mean.values, index=idx)
        fc_conf = fc.conf_int()

        plt.figure(figsize=(12,5))
        plt.plot(ts.index, ts.values, label="История")
        plt.plot(fc_mean.index, fc_mean.values, label="Прогноз", marker="o")
        plt.fill_between(fc_conf.index, fc_conf.iloc[:,0], fc_conf.iloc[:,1], color="gray", alpha=0.3)
        plt.title("Прогноз месячной выручки (SARIMAX)")
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, "sarimax_forecast_revenue.png"))
        plt.show(block=False)
        plt.close()

        pd.DataFrame({"forecast": fc_mean}).to_csv(os.path.join(OUTPUT_DIR, "forecast_revenue_next6months.csv"))
        print("Прогноз сохранён.")
    except Exception as e:
        print("Ошибка при обучении SARIMAX:", e)

# -----------------------------
# 9) Краткий отчёт
# -----------------------------
report = {
    "total_revenue": int(df["fare"].sum()),
    "total_tickets": int(len(df)),
    "period_start": df["purchase_datetime"].min(),
    "period_end": df["purchase_datetime"].max()
}
print("\nКраткий отчёт:")
for k,v in report.items():
    print(f"{k}: {v}")

print(f"\nГрафики и CSV-файлы сохранены в папке: {OUTPUT_DIR}")
