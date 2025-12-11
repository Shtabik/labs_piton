import os
import random
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Отключаем предупреждения для чистоты вывода
warnings.filterwarnings("ignore")

# -----------------------------
# Настройки
# -----------------------------
OUTPUT_DIR = "outputs_ru"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Настройка стилей для графиков
sns.set(style="whitegrid", palette="muted")
plt.rcParams['figure.figsize'] = (12, 6)

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)

# ИСПРАВЛЕНИЕ: Теперь CSV сохраняется внутри папки outputs_ru
CSV_PATH = os.path.join(OUTPUT_DIR, "s7_tickets.csv")

# Словари для перевода
TRANSLATION_MAP = {
    "booking_class": {"economy": "Эконом", "premium": "Премиум", "business": "Бизнес"},
    "passenger_type": {"adult": "Взрослый", "child": "Ребенок", "infant": "Младенец"},
    "payment_method": {
        "card": "Банковская карта", "apple_pay": "SberPay/MirPay",
        "google_pay": "SberPay/MirPay", "cash": "Наличные", "bank_transfer": "Счет на оплату"
    },
    "loyalty_status": {"silver": "Серебро", "gold": "Золото", "none": "Нет статуса"}
}


# -----------------------------
# 1. Генерация данных (на русском)
# -----------------------------
def generate_synthetic_s7_ru(start_date="2021-01-01", end_date="2024-12-31", n_records_per_day=40):
    print("Генерация синтетических данных...")
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    all_dates = pd.date_range(start, end, freq="D")

    origins = ["SVO", "DME", "LED", "KRR", "OVB", "ROV", "VKO", "IKT"]
    destinations = ["SVO", "LED", "AYT", "SVX", "KZN", "KUF", "OGZ", "VVO"]

    payment_methods = ["Банковская карта", "SberPay/MirPay", "Наличные", "Счет на оплату", "СБП"]
    passenger_types = ["Взрослый", "Ребенок", "Младенец"]
    booking_classes = ["Эконом", "Премиум", "Бизнес"]
    loyalty_statuses = ["Нет статуса", "Серебро", "Золото", "Платина"]

    records = []
    for d in all_dates:
        season_factor = 1.0
        if d.month in (6, 7, 8):
            season_factor = 1.5
        elif d.month == 12:
            season_factor = 1.3
        elif d.month in (1, 2):
            season_factor = 0.8

        # Добавим эффект пятницы (люди чаще летают)
        if d.dayofweek == 4:  # 4 = Пятница
            season_factor *= 1.2

        n = max(1, int(n_records_per_day * (0.8 + np.random.rand() * 0.4) * season_factor))

        for _ in range(n):
            origin = random.choice(origins)
            dest = random.choice([c for c in destinations if c != origin])
            purchase_date = d + pd.Timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))

            base_fare = np.random.normal(9000, 3500)
            cls = random.choices(booking_classes, weights=[0.8, 0.15, 0.05])[0]
            if cls == "Премиум":
                base_fare *= 1.7
            elif cls == "Бизнес":
                base_fare *= 4.0

            segments = random.choice([1, 1, 1, 2])
            fare = max(1500, int(base_fare * (1 + 0.1 * segments)))

            payment = random.choices(payment_methods, weights=[0.6, 0.15, 0.05, 0.1, 0.1])[0]
            p_type = random.choices(passenger_types, weights=[0.85, 0.12, 0.03])[0]
            loyalty = random.choices(loyalty_statuses, weights=[0.85, 0.1, 0.04, 0.01])[0]

            records.append({
                "Дата_покупки": purchase_date,
                "Аэропорт_вылета": origin, "Аэропорт_прилета": dest,
                "Сегментов": segments, "Класс_бронирования": cls,
                "Стоимость_руб": fare, "Способ_оплаты": payment,
                "Тип_пассажира": p_type, "Статус_лояльности": loyalty
            })

    return pd.DataFrame(records)


# -----------------------------
# 2. Загрузка и предобработка
# -----------------------------
def load_data():
    if os.path.exists(CSV_PATH):
        print(f"Загрузка данных из {CSV_PATH}...")
        df = pd.read_csv(CSV_PATH)

        rename_dict = {
            "purchase_datetime": "Дата_покупки", "origin": "Аэропорт_вылета",
            "destination": "Аэропорт_прилета", "segments": "Сегментов",
            "booking_class": "Класс_бронирования", "fare": "Стоимость_руб",
            "payment_method": "Способ_оплаты", "passenger_type": "Тип_пассажира",
            "loyalty_status": "Статус_лояльности"
        }
        df.rename(columns=rename_dict, inplace=True)

        for col, mapping in TRANSLATION_MAP.items():
            ru_col = rename_dict.get(col, col)
            if ru_col in df.columns and df[ru_col].iloc[0] in mapping.keys():
                df[ru_col] = df[ru_col].map(mapping).fillna(df[ru_col])
    else:
        df = generate_synthetic_s7_ru()
        df.to_csv(CSV_PATH, index=False)

    df["Дата_покупки"] = pd.to_datetime(df["Дата_покупки"])
    df["Месяц"] = df["Дата_покупки"].dt.to_period("M").dt.to_timestamp()

    # Дни недели для аналитики
    days_map = {0: 'Пн', 1: 'Вт', 2: 'Ср', 3: 'Чт', 4: 'Пт', 5: 'Сб', 6: 'Вс'}
    df["День_недели"] = df["Дата_покупки"].dt.dayofweek.map(days_map)

    return df


# -----------------------------
# 3. Визуализация и Анализ
# -----------------------------

def plot_dynamics(df):
    monthly = df.groupby("Месяц").agg({"Стоимость_руб": "sum", "Аэропорт_вылета": "count"}).rename(
        columns={"Стоимость_руб": "Выручка", "Аэропорт_вылета": "Продажи_шт"}
    )
    fig, ax1 = plt.subplots(figsize=(14, 6))

    color = 'tab:blue'
    ax1.set_xlabel('Месяц')
    ax1.set_ylabel('Выручка (руб)', color=color)
    ax1.plot(monthly.index, monthly['Выручка'], color=color, linewidth=2, marker='o')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{x / 1e6:.1f}М'))

    ax2 = ax1.twinx()
    color = 'tab:orange'
    ax2.set_ylabel('Количество билетов (шт)', color=color)
    ax2.plot(monthly.index, monthly['Продажи_шт'], color=color, linestyle='--', linewidth=2)
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title("Динамика продаж и объема перевозок S7")
    fig.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "1_dynamics_revenue_tickets.png"))
    plt.close()
    return monthly


def plot_airports_heatmap(df):
    routes = df.groupby(["Аэропорт_вылета", "Аэропорт_прилета"]).size().reset_index(name="count")
    pivot_routes = routes.pivot(index="Аэропорт_вылета", columns="Аэропорт_прилета", values="count").fillna(0)
    plt.figure(figsize=(10, 8))
    sns.heatmap(pivot_routes, annot=True, fmt=".0f", cmap="YlGnBu", linewidths=.5)
    plt.title("Тепловая карта загруженности маршрутов")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "2_routes_heatmap.png"))
    plt.close()


def plot_seasonality(df):
    df['Номер_месяца'] = df['Дата_покупки'].dt.month
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='Номер_месяца', y='Стоимость_руб', data=df, palette="coolwarm", showfliers=False)
    plt.title("Распределение стоимости билетов по месяцам")
    plt.xlabel("Месяц (1=Январь)")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "3_seasonality_boxplot.png"))
    plt.close()


def plot_payment_analysis(df):
    pay_counts = df["Способ_оплаты"].value_counts()
    pay_mean = df.groupby("Способ_оплаты")["Стоимость_руб"].mean().sort_values(ascending=False)
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    axes[0].pie(pay_counts, labels=pay_counts.index, autopct='%1.1f%%', startangle=140,
                colors=sns.color_palette("pastel"))
    axes[0].set_title("Доля способов оплаты")
    sns.barplot(x=pay_mean.index, y=pay_mean.values, ax=axes[1], palette="viridis")
    axes[1].set_title("Средний чек по способу оплаты")
    axes[1].tick_params(axis='x', rotation=45)
    for i, v in enumerate(pay_mean.values):
        axes[1].text(i, v + 100, f"{int(v)} ₽", ha='center', va='bottom', fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "4_payment_analysis.png"))
    plt.close()


def plot_passenger_class(df):
    plt.figure(figsize=(10, 6))
    ax = sns.countplot(data=df, x="Класс_бронирования", hue="Тип_пассажира", palette="Set2")
    plt.title("Распределение пассажиров по классам")
    for container in ax.containers:
        ax.bar_label(container)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "5_passenger_class_structure.png"))
    plt.close()


# НОВАЯ ФУНКЦИЯ: Популярность дней недели
def plot_day_of_week(df):
    plt.figure(figsize=(10, 5))
    order = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    counts = df["День_недели"].value_counts()
    sns.barplot(x=counts.index, y=counts.values, order=order, palette="autumn")
    plt.title("В какие дни недели чаще всего покупают билеты?")
    plt.ylabel("Количество билетов")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "bonus_day_of_week.png"))
    plt.close()


# ОБНОВЛЕННАЯ ФУНКЦИЯ: Прогноз (теперь два графика: Выручка и Билеты)
def run_forecast(monthly_df):
    if len(monthly_df) < 12:
        print("Мало данных для прогноза.")
        return

    # Вспомогательная функция, чтобы не дублировать код
    def make_sarima(series, title, filename):
        try:
            model = SARIMAX(series, order=(1, 1, 1), seasonal_order=(1, 1, 0, 12),
                            enforce_stationarity=False, enforce_invertibility=False)
            res = model.fit(disp=False)
            fc = res.get_forecast(steps=6)
            mean = fc.predicted_mean
            conf = fc.conf_int()

            plt.figure(figsize=(12, 6))
            plt.plot(series.index, series, label='История')
            plt.plot(mean.index, mean, label='Прогноз', color='red', marker='o')
            plt.fill_between(conf.index, conf.iloc[:, 0], conf.iloc[:, 1], color='pink', alpha=0.3)
            plt.title(f"Прогноз: {title}")
            plt.legend()
            plt.grid(True)
            plt.savefig(os.path.join(OUTPUT_DIR, filename))
            plt.close()
            print(f"-> Прогноз '{title}' построен.")
        except Exception as e:
            print(f"Ошибка прогноза {title}: {e}")

    # 1. Прогноз денег
    make_sarima(monthly_df["Выручка"], "Выручка (руб)", "6_forecast_revenue.png")
    # 2. Прогноз количества билетов (НОВОЕ)
    make_sarima(monthly_df["Продажи_шт"], "Количество билетов (шт)", "6_forecast_tickets.png")


# -----------------------------
# MAIN
# -----------------------------
def main():
    df = load_data()
    print(f"Данные готовы. Записей: {len(df)}")

    # Статистика
    desc = df[["Стоимость_руб", "Сегментов"]].describe().T
    desc.to_csv(os.path.join(OUTPUT_DIR, "stats_general.csv"))
    print(desc)

    monthly_data = plot_dynamics(df)  # График 1
    plot_airports_heatmap(df)  # График 2
    plot_seasonality(df)  # График 3
    plot_payment_analysis(df)  # График 4
    plot_passenger_class(df)  # График 5

    # Запуск новых функций
    plot_day_of_week(df)  # БОНУС: График дней недели
    run_forecast(monthly_data)  # ОБНОВЛЕНО: Прогноз и выручки, и билетов

    print(f"\nГотово! Все файлы в папке: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()