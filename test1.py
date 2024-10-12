import math
import itertools

def calculate_distance(x1, y1, x2, y2):
    """Вычисление Евклидова расстояния между двумя точками."""
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def find_shortest_path(transport, bounties):
    """
    Найти кратчайший маршрут для сбора всех наград, начиная с положения транспорта.
    """
    # Начальное положение транспорта
    start_x, start_y = transport['x'], transport['y']
    
    # Список всех bounties с их координатами
    bounty_coords = [(b['x'], b['y']) for b in bounties]
    
    # Перебор всех возможных маршрутов через все награды
    min_path = None
    min_length = float('inf')
    
    for perm in itertools.permutations(bounty_coords):
        # Начинаем с транспорта и идем по маршруту, состоящему из всех bounties
        path = [(start_x, start_y)] + list(perm)
        total_length = 0
        
        # Рассчитываем длину маршрута
        for i in range(len(path) - 1):
            total_length += calculate_distance(path[i][0], path[i][1], path[i + 1][0], path[i + 1][1])
        
        # Сравниваем длину с минимальной на текущий момент
        if total_length < min_length:
            min_length = total_length
            min_path = path
    
    return min_path, min_length

# Пример данных
transport = {
    "anomalyAcceleration": {"x": 1.2, "y": 1.2},
    "attackCooldownMs": 0,
    "deathCount": 0,
    "health": 100,
    "id": "00000000-0000-0000-0000-000000000000",
    "selfAcceleration": {"x": 1.2, "y": 1.2},
    "shieldCooldownMs": 0,
    "shieldLeftMs": 0,
    "status": "alive",
    "velocity": {"x": 1.2, "y": 1.2},
    "x": 1,
    "y": 1
}

bounties = [
    {"points": 100, "radius": 10, "x": 1, "y": 1},
    {"points": 100, "radius": 10, "x": 2, "y": 2},
    {"points": 100, "radius": 10, "x": 3, "y": 3},
    {"points": 100, "radius": 10, "x": 5, "y": 5}
]

# Поиск кратчайшего маршрута
path, length = find_shortest_path(transport, bounties)

print("Оптимальный путь для сбора наград:", path)
print("Общая длина пути:", length)
