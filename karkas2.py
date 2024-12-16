import matplotlib.pyplot as plt
import numpy as np
import math

# Данные трубы
pipe = {
    'diam': 0.5,  # диаметр трубы, м
    'length': 10,  # длина трубы, м
    'roughness': 0.0001,  # шероховатость трубы, м
}

# Данные жидкости (нефть)
fluid = {
    'density': 850,  # кг/м^3 (начальная плотность)
    'viscosity': 0.1,  # Па·с (начальная вязкость)
    'thermal_expansion': 0.0007,  # 1/°C (коэффициент объемного расширения)
    'heat_capacity': 2100,  # Дж/(кг·°C)
    'temperature': 20,  # начальная температура, °C
    'speed': 1,  # м/с (начальная скорость потока)
}

# Параметры нагревателя
heater = {
    'power': 500000,  # мощность нагревателя, Вт
    'efficiency': 0.9,  # КПД нагревателя
}

# Перепад давления в системе
delta_pressure = 50000  # Па (перепад давления)

# Константы для вязкости
beta_viscosity = 0.02  # Коэффициент изменения вязкости (эмпирический)

# Функция для расчёта площади поперечного сечения трубы


def calculate_pipe_area(diameter):
    return math.pi * (diameter / 2) ** 2

# Функция для расчёта числа Рейнольдса


def calculate_reynolds_number(density, velocity, diameter, viscosity):
    return (density * velocity * diameter) / viscosity

# Функция для расчёта коэффициента трения Дарси-Вейсбаха


def calculate_friction_factor(re, roughness, diameter):
    if re < 2000:  # Ламинарный режим
        return 64 / re
    elif re >= 4000:  # Турбулентный режим
        # Итеративный метод для расчёта коэффициента трения (формула Колбрука)
        f = 0.02  # Начальное приближение
        for _ in range(10):  # Итерации для уточнения значения
            f = 1 / (-2 * math.log10((roughness / (3.7 * diameter)) + (5.74 / (re**0.9))))
        return f
    else:
        # Переходный режим
        return 0.5  # Предположительное значение для переходного режима

# Функция для расчёта температуры после нагрева


def calculate_temperature_change(power, efficiency, density, velocity, area, heat_capacity):
    mass_flow_rate = density * velocity * area  # массовый расход, кг/с
    effective_power = power * efficiency  # учет КПД нагревателя
    delta_t = effective_power / (mass_flow_rate * heat_capacity)  # изменение температуры
    return delta_t

# Функция для расчёта новой плотности


def calculate_new_density(initial_density, thermal_expansion, delta_t):
    return initial_density * (1 - thermal_expansion * delta_t)

# Функция для расчёта новой вязкости


def calculate_new_viscosity(initial_viscosity, beta, delta_t):
    return initial_viscosity * math.exp(-beta * delta_t)

# Функция для расчёта максимальной скорости потока с учётом гидравлических потерь


def calculate_max_velocity(delta_pressure, density, diameter, friction_factor):
    return math.sqrt((2 * delta_pressure) / (friction_factor * density))

# Основная функция для расчётов


def main(pipe, fluid, heater, delta_pressure):
    # Исходные параметры
    diameter = pipe['diam']
    length = pipe['length']
    roughness = pipe['roughness']
    initial_density = fluid['density']
    initial_viscosity = fluid['viscosity']
    thermal_expansion = fluid['thermal_expansion']
    heat_capacity = fluid['heat_capacity']
    initial_temperature = fluid['temperature']
    initial_speed = fluid['speed']
    power = heater['power']
    efficiency = heater['efficiency']

    # Площадь поперечного сечения трубы
    area = calculate_pipe_area(diameter)

    # 1. Расчёт изменения температуры
    delta_t = calculate_temperature_change(power, efficiency, initial_density, initial_speed, area, heat_capacity)
    new_temperature = initial_temperature + delta_t

    # 2. Расчёт новой плотности
    new_density = calculate_new_density(initial_density, thermal_expansion, delta_t)

    # 3. Расчёт новой вязкости
    new_viscosity = calculate_new_viscosity(initial_viscosity, beta_viscosity, delta_t)

    # 4. Расчёт числа Рейнольдса для нового состояния
    re_initial = calculate_reynolds_number(initial_density, initial_speed, diameter, initial_viscosity)
    re_new = calculate_reynolds_number(new_density, initial_speed, diameter, new_viscosity)

    # 5. Коэффициенты трения (до и после нагрева)
    friction_factor_initial = calculate_friction_factor(re_initial, roughness, diameter)
    friction_factor_new = calculate_friction_factor(re_new, roughness, diameter)

    # 6. Максимальная скорость потока с учётом гидравлических потерь
    max_velocity_initial = calculate_max_velocity(
        delta_pressure, initial_density, diameter, friction_factor_initial) / 10
    max_velocity_new = calculate_max_velocity(delta_pressure, new_density, diameter, friction_factor_new) / 10

    # 7. Вывод результатов
    print("=== Результаты ===")
    print(f"Начальная температура: {initial_temperature:.2f} °C")
    print(f"Новая температура: {new_temperature:.2f} °C")
    print(f"Изменение температуры: {delta_t:.2f} °C")
    print(f"Начальная плотность: {initial_density:.2f} кг/м³")
    print(f"Новая плотность: {new_density:.2f} кг/м³")
    print(f"Начальная вязкость: {initial_viscosity:.5f} Па·с")
    print(f"Новая вязкость: {new_viscosity:.5f} Па·с")
    print(f"Число Рейнольдса (до нагрева): {re_initial:.2f}")
    print(f"Число Рейнольдса (после нагрева): {re_new:.2f}")
    print(f"Коэффициент трения (до нагрева): {friction_factor_initial:.5f}")
    print(f"Коэффициент трения (после нагрева): {friction_factor_new:.5f}")
    print(f"Максимальная скорость (до нагрева): {max_velocity_initial:.7f} м/с")
    print(f"Максимальная скорость (после нагрева): {max_velocity_new:.7f} м/с")

    return {
        "delta_t": delta_t,
        "new_temperature": new_temperature,
        "new_density": new_density,
        "new_viscosity": new_viscosity,
        "re_new": re_new,
        "friction_factor_new": friction_factor_new,
        "max_velocity_new": max_velocity_new
    }


def plot_velocity_vs_heating(pipe, fluid, heater, delta_pressure, power_range):
    """
    Строит зависимость скорости потока от мощности нагревателя.

    Args:
        pipe (dict): Параметры трубы (диаметр, длина, шероховатость).
        fluid (dict): Свойства жидкости (плотность, вязкость, теплоёмкость, тепловое расширение).
        heater (dict): Параметры нагревателя (КПД).
        delta_pressure (float): Перепад давления в системе, Па.
        power_range (list or np.array): Массив мощностей нагревателя, Вт.
    """
    # Массив для хранения скоростей
    velocities = []

    # Перебираем мощности нагревателя
    for power in power_range:
        heater['power'] = power
        ans = main(pipe, fluid, heater, delta_pressure)
        velocities.append(ans['max_velocity_new'])

    # Построение графика
    plt.figure(figsize=(10, 6))
    plt.plot([x / 10 for x in power_range], velocities, label="Скорость потока", color="blue", linewidth=2)
    plt.xlabel("Мощность нагревателя (Вт)", fontsize=12)
    plt.ylabel("Скорость потока (м/с)", fontsize=12)
    plt.title("Зависимость скорости потока от мощности нагревателя", fontsize=14)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend(fontsize=12)
    plt.show()


if __name__ == "__main__":
    # Диапазон мощностей нагревателя (от 0 до 1 000 000 Вт с шагом 500 Вт)
    power_range = np.arange(0, 1000001, 500)  # Вт
    # Построить график зависимости скорости от мощности нагревателя
    plot_velocity_vs_heating(pipe, fluid, heater, delta_pressure, power_range)
