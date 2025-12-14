import os
import random
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker
from statsmodels.tsa.statespace.sarimax import SARIMAX

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
warnings.filterwarnings("ignore")

# Настройки
OUTPUT_DIR = "outputs_ru"
os.makedirs(OUTPUT_DIR, exist_ok=True)
CSV_PATH = os.path.join(OUTPUT_DIR, "s7_tickets_v3.csv")
sns.set(style="whitegrid", palette="muted")
plt.rcParams['figure.figsize'] = (12, 6)

# Фиксация случайности
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)

# 1. Генерация данных
def generate_synthetic_s7_direct_ru(start_date="2021-01-01", end_date="2024-12-31", n_records_per_day=40):
    print("Генерация синтетических данных и расчет статусов...")
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    all_dates = pd.date_range(start, end, freq="D")

    origins = ["Шереметьево (SVO)", "Домодедово (DME)", "Пулково (LED)", "Пашковский (KRR)",
               "Толмачево (OVB)", "Платов (ROV)", "Внуково (VKO)", "Иркутск (IKT)"]
    destinations = ["Шереметьево (SVO)", "Пулково (LED)", "Анталья (AYT)", "Кольцово (SVX)",
                    "Казань (KZN)", "Курумоч (KUF)", "Владикавказ (OGZ)", "Владивосток (VVO)"]

    payment_methods = ["Банковская карта", "SberPay/MirPay", "Наличные", "Счет на оплату", "СБП"]
    passenger_types = ["Взрослый", "Ребенок", "Младенец"]
    booking_classes = ["Эконом", "Премиум", "Бизнес"]

    passenger_ids_pool = list(range(1, 5001))

    records = []
    for d in all_dates:
        season_factor = 1.0
        if d.month in (6, 7, 8):
            season_factor = 1.5
        elif d.month == 12:
            season_factor = 1.3
        elif d.month in (1, 2):
            season_factor = 0.8

        if d.dayofweek == 4: season_factor *= 1.2

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

            # Присваиваем ID сразу
            p_id = random.choice(passenger_ids_pool)

            records.append({
                "Дата_покупки": purchase_date,
                "Пассажир_ID": p_id,
                "Аэропорт_вылета": origin,
                "Аэропорт_прилета": dest,
                "Сегментов": segments,
                "Класс_бронирования": cls,
                "Стоимость_руб": fare,
                "Способ_оплаты": payment,
                "Тип_пассажира": p_type
            })

    df = pd.DataFrame(records)

    # --- ВНУТРЕННЯЯ ЛОГИКА СТАТУСОВ ---

    print("   -> Расчет статусов лояльности...")
    flights_per_passenger = df["Пассажир_ID"].value_counts()

    def get_status(flights):
        if flights < 5:
            return "Нет статуса"
        elif flights < 15:
            return "Серебро"
        elif flights < 30:
            return "Золото"
        else:
            return "Платина"


    id_to_status = flights_per_passenger.map(get_status)
    df["Статус_лояльности"] = df["Пассажир_ID"].map(id_to_status)

    return df

# 2. Загрузка

def load_data():
    if os.path.exists(CSV_PATH):
        print(f"Загрузка данных из {CSV_PATH}...")
        df = pd.read_csv(CSV_PATH)
    else:
        df = generate_synthetic_s7_direct_ru()
        df.to_csv(CSV_PATH, index=False)

    df["Дата_покупки"] = pd.to_datetime(df["Дата_покупки"])
    df["Месяц"] = df["Дата_покупки"].dt.to_period("M").dt.to_timestamp()
    days_map = {0: 'Пн', 1: 'Вт', 2: 'Ср', 3: 'Чт', 4: 'Пт', 5: 'Сб', 6: 'Вс'}
    df["День_недели"] = df["Дата_покупки"].dt.dayofweek.map(days_map)

    return df


# 3. Функции сохранения статистики
def save_statistics(df):
    print("Расчет и сохранение статистики...")

    # --- А. ЧИСЛЕННЫЕ ДАННЫЕ ---
    numeric_df = df.select_dtypes(include=[np.number])
    if "Пассажир_ID" in numeric_df.columns:
        numeric_df = numeric_df.drop(columns=["Пассажир_ID"])

    # Базовая статистика
    num_stats = numeric_df.describe().T

    # Добавляем МОДУ
    modes = numeric_df.mode().iloc[0]
    num_stats['Мода'] = modes

    num_stats.rename(columns={
        "count": "Количество", "mean": "Среднее", "std": "Стд_отклонение",
        "min": "Минимум", "max": "Максимум", "50%": "Медиана"
    }, inplace=True)


    num_stats = num_stats.reset_index().rename(columns={'index': 'Параметр'})
    num_file = os.path.join(OUTPUT_DIR, "stats_numerical_general.csv")
    num_stats.to_csv(num_file, index=False)
    print(f"-> Численная статистика (с модой) сохранена: {num_file}")

    # --- Б. КАТЕГОРИАЛЬНЫЕ ДАННЫЕ ---
    cat_df = df.select_dtypes(include=['object'])

    if not cat_df.empty:
        cat_stats = cat_df.describe().T

        # Добавляем долю в процентах
        cat_stats['Доля_моды_%'] = (cat_stats['freq'] / cat_stats['count'] * 100).round(2)

        # Переименовываем столбцы научно
        cat_stats.rename(columns={
            "count": "Объем_выборки",
            "unique": "Количество_уникальных",
            "top": "Мода (самое_популярное)",
            "freq": "Частота_моды"
        }, inplace=True)


        cat_stats = cat_stats.reset_index().rename(columns={'index': 'Параметр'})
        cat_file = os.path.join(OUTPUT_DIR, "stats_category_general.csv")
        cat_stats.to_csv(cat_file, index=False)
        print(f"-> Категориальная статистика сохранена: {cat_file}")


# 4. Визуализация
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
    pivot_routes = routes.pivot(index="Аэропорт_прилета", columns="Аэропорт_вылета", values="count").fillna(0)
    plt.figure(figsize=(12, 10))
    sns.heatmap(pivot_routes, annot=True, fmt=".0f", cmap="YlGnBu", linewidths=.5)
    plt.title("Тепловая карта загруженности маршрутов")
    plt.xticks(rotation=45, ha='center')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "2_routes_heatmap.png"))
    plt.close()


def plot_seasonality(df):
    df['Номер_месяца'] = df['Дата_покупки'].dt.month
    month_names = ["Янв", "Фев", "Мар", "Апр", "Май", "Июн", "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"]

    monthly_mean = df.groupby('Номер_месяца')['Стоимость_руб'].mean()
    plt.figure(figsize=(12, 6))
    bars = plt.bar(monthly_mean.index, monthly_mean.values, color="skyblue")
    plt.title("Средняя стоимость билетов по месяцам")
    plt.xlabel("Месяц")
    plt.ylabel("Средняя стоимость, руб")
    plt.xticks(monthly_mean.index, [month_names[m - 1] for m in monthly_mean.index])
    plt.bar_label(bars, fmt="%.0f", padding=5)

    y_min = monthly_mean.min() - 500
    y_max = monthly_mean.max() + 500
    plt.ylim(y_min, y_max)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "3_seasonality_bar.png"))
    plt.close()


def plot_payment_analysis(df):
    pay_counts = df["Способ_оплаты"].value_counts()
    pay_mean = df.groupby("Способ_оплаты")["Стоимость_руб"].mean().sort_values(ascending=False)

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    axes[0].pie(pay_counts, labels=pay_counts.index, autopct='%1.1f%%', startangle=140,
                colors=sns.color_palette("pastel"))
    axes[0].set_title("Доля способов оплаты")

    sns.barplot(x=pay_mean.index, y=pay_mean.values, ax=axes[1], palette="viridis")
    y_min = pay_mean.min() - 500
    y_max = pay_mean.max() + 500
    axes[1].set_ylim(y_min, y_max)
    axes[1].set_title("Средний чек по способу оплаты")
    axes[1].tick_params(axis='x', rotation=15)

    for i, v in enumerate(pay_mean.values):
        axes[1].text(i, v, f"{int(v)} ₽", ha='center', va='bottom', fontsize=10)

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


def plot_loyalty_status(df):
    plt.figure(figsize=(10, 6))
    counts = df["Статус_лояльности"].value_counts()
    ax = sns.barplot(x=counts.index, y=counts.values, palette="coolwarm")
    plt.title("Распределение пассажиров по статусам лояльности")
    for container in ax.containers:
        ax.bar_label(container)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "bonus_loyalty_status.png"))
    plt.close()


def plot_day_of_week(df):
    plt.figure(figsize=(10, 5))
    order = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    counts = df["День_недели"].value_counts()
    ax = sns.barplot(x=counts.index, y=counts.values, order=order, palette="autumn")
    plt.title("В какие дни недели чаще всего покупают билеты?")
    for container in ax.containers:
        ax.bar_label(container)
    y_min = counts.min() - 500
    y_max = counts.max() + 500
    plt.ylim(y_min, y_max)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "bonus_day_of_week.png"))
    plt.close()


def run_forecast(monthly_df):
    if len(monthly_df) < 12:
        print("Мало данных для прогноза.")
        return

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
            print(f"-> Прогноз '{title}' сохранен в {filename}")
        except Exception as e:
            print(f"Ошибка прогноза {title}: {e}")

    make_sarima(monthly_df["Выручка"], "Выручка (руб)", "6_forecast_revenue.png")
    make_sarima(monthly_df["Продажи_шт"], "Количество билетов (шт)", "6_forecast_tickets.png")


# MAIN
def main():
    # 1. Загрузка (теперь статус уже внутри датасета)
    df = load_data()
    print(f"Данные готовы. Записей: {len(df)}")

    # 2. Сохранение статистики (раздельной и правильной)
    save_statistics(df)

    # 3. Графики
    monthly_data = plot_dynamics(df)
    plot_airports_heatmap(df)
    plot_seasonality(df)
    plot_payment_analysis(df)
    plot_passenger_class(df)
    plot_loyalty_status(df)
    plot_day_of_week(df)
    run_forecast(monthly_data)

    print(f"\nГотово! Все файлы в папке: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()