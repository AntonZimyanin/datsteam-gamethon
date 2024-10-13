import requests
import math
import time

auth_token = '670516cb9d5a9670516cb9d5ae'
url = 'https://games-test.datsteam.dev/play/magcarp/player/move'

headers = {
    'X-Auth-Token': auth_token,
}


data = {
    "transports": [
    ]
}


def postRequest(jsonData = data): 
    
    headers = {
        'X-Auth-Token': auth_token,
    }

    return requests.post(url, json=jsonData, headers=headers)

def calculate_distance(transport, bounty):
    """Calculate the Euclidean distance between a transport and a bounty."""
    return math.sqrt((transport['x'] - bounty['x']) ** 2 + (transport['y'] - bounty['y']) ** 2)

def calculate_direction(transport, bounty):
    """Calculate the direction vector to set the acceleration toward the bounty."""
    dx = bounty['x'] - transport['x']
    dy = bounty['y'] - transport['y']
    magnitude = math.sqrt(dx**2 + dy**2)
    
    # Normalize the direction and scale by a factor if desired (e.g., max acceleration)
    if magnitude != 0:
        return {"x": dx / magnitude, "y": dy / magnitude}
    else:
        return {"x": 0, "y": 0}

# Run the code 100 times with a 0.4-second delay
for _ in range(100):

    response = postRequest()

    # Parse the JSON response
    response_data = response.json()

    # Extract "transports" and "bounties"
    transports = response_data.get("transports", [])
    bounties = response_data.get("bounties", [])

    closest_bounties = {}

    # Iterate over each transport to find the closest bounty and adjust their acceleration
    for transport in transports:
        closest_bounty = None
        min_distance = float('inf')  # Initialize with a large value

        for bounty in bounties:
            distance = calculate_distance(transport, bounty)
            if distance < min_distance:
                min_distance = distance
                closest_bounty = bounty

        # Calculate acceleration toward the closest bounty
        direction = calculate_direction(transport, closest_bounty)
        transport['acceleration'] = direction

        closest_bounties[transport['id']] = closest_bounty

    # Prepare the updated data for the transport move request
    updated_data = {
        "transports": [
            {
                "id": transport['id'],
                "acceleration": transport['acceleration'],
                "activateShield": False,  # Assuming you may want to deactivate the shield while moving
                "attack": transport['acceleration']  # Attack in the direction of movement, if desired
            }
            for transport in transports
        ]
    }

    # Make the updated move request
    # response = requests.post(url, json=updated_data, headers=headers)
    
    response = postRequest(updated_data)

    # Print the transport coordinates and the closest bounty
    for transport in transports:
        transport_id = transport['id']
        transport_x = transport['x']
        transport_y = transport['y']
        closest_bounty = closest_bounties[transport_id]
        acceleration = transport['acceleration']

        print(f"Transport ID: {transport_id} - Coordinates: ({transport_x}, {transport_y}) - Closest Bounty: {closest_bounty} - New Acceleration: {acceleration}")

    # Wait for 0.4 seconds before the next iteration
    time.sleep(0.4)



def activate_shield_if_needed(transport, enemies):
    for enemy in enemies:
        distance = calculate_distance(transport, enemy)
        transport_id = transport['id']
        print(f"Расстояние до врага: {distance}")
        
        if distance <= 200:
            postRequest(data={id: transport_id})
            transport["activateShield"] = True
            print("Щит активирован!")
            break  # Если расстояние меньше 200, щит активируется, и больше не проверяем
        
        
        
        
import itertools

def calculate_distance(x1, y1, x2, y2):
    """Вычисление Евклидова расстояния между двумя точками."""
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def is_enemy(transport, enemy):
    """Проверить, находится ли враг в пределах 200 единиц от транспорта."""
    distance = calculate_distance(transport['x'], transport['y'], enemy['x'], enemy['y'])
    return distance <= 200

def is_weak_enemy(transport, enemy):
    """Проверить, слабее ли враг (имеет меньше здоровья, чем транспорт)."""
    return enemy["health"] < transport["health"]

def is_anomaly_nearby(transport, anomaly):
    """Проверить, находится ли аномалия в пределах её радиуса влияния от транспорта."""
    distance = calculate_distance(transport['x'], transport['y'], anomaly['x'], anomaly['y'])
    return distance <= anomaly['effectiveRadius']

def avoid_anomaly(anomaly, transport):
    """
    Функция для обхода аномалии.
    Например, увеличиваем координаты на некоторое расстояние, чтобы обойти.
    """
    avoid_distance = anomaly['radius'] * 2  # Обход на расстоянии двойного радиуса аномалии
    if transport['x'] < anomaly['x']:
        transport['x'] -= avoid_distance
    else:
        transport['x'] += avoid_distance
    if transport['y'] < anomaly['y']:
        transport['y'] -= avoid_distance
    else:
        transport['y'] += avoid_distance

    print(f"Обход аномалии {anomaly['id']} в ({anomaly['x']}, {anomaly['y']}). Новые координаты транспорта: ({transport['x']}, {transport['y']})")

def enemy_action(transport, enemies):
    for enemy in enemies:
        if is_enemy(transport, enemy):
            if is_weak_enemy(transport, enemy):
                print(f"Ramming weak enemy: {enemy['id']}")
                return 'attack'  # Атакуем слабого врага
            else:
                print(f"Activating shield due to enemy: {enemy['id']}")
                return 'shield'  # Активируем щит от сильного врага
    return None  # Нет врагов в пределах досягаемости

def find_shortest_path(transport, bounties, enemies, anomalies):
    """
    Найти оптимальный маршрут для сбора наград, принимая в расчет врагов и аномалии.
    """
    start_x, start_y = transport['x'], transport['y']
    
    # Список всех bounties с их координатами и очками
    bounty_coords = [(b['x'], b['y'], b['points']) for b in bounties]
    
    min_path = None
    min_score_weighted_length = float('inf')

    for perm in itertools.permutations(bounty_coords):
        path = [(start_x, start_y)] + [(x, y) for x, y, points in perm]
        total_length = 0
        transport_copy = transport.copy()  # Копируем состояние транспорта для этого маршрута
        
        # Рассчитываем длину маршрута с учетом врагов и аномалий
        for i in range(len(path) - 1):
            x1, y1 = path[i]
            x2, y2 = path[i + 1]
            total_length += calculate_distance(x1, y1, x2, y2)
            
            # Проверяем врагов на пути
            action = enemy_action(transport_copy, enemies)
            if action == 'shield':
                transport_copy['shieldLeftMs'] = max(transport_copy['shieldLeftMs'] - 1, 0)
            elif action == 'attack':
                transport_copy['x'], transport_copy['y'] = x2, y2
                print(f"Transport {transport_copy['id']} attacks and moves to ({x2}, {y2})")
            
            # Проверяем аномалии на пути и обходим их при необходимости
            for anomaly in anomalies:
                if is_anomaly_nearby(transport_copy, anomaly):
                    print(f"Avoiding anomaly: {anomaly['id']}")
                    avoid_anomaly(anomaly, transport_copy)
        
        # Общая сумма очков за маршрут
        total_points = sum([points for x, y, points in perm])
        
        # Взвешиваем результат: минимизация длины, максимизация очков
        if total_points > 0:
            score_weighted_length = total_length / total_points
        else:
            score_weighted_length = total_length
        
        # Сравниваем взвешенное расстояние с минимальным
        if score_weighted_length < min_score_weighted_length:
            min_score_weighted_length = score_weighted_length
            min_path = path
    
    return min_path, min_score_weighted_length

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
    {"points": 200, "radius": 10, "x": 2, "y": 2},
    {"points": 300, "radius": 10, "x": 3, "y": 3},
    {"points": 500, "radius": 10, "x": 5, "y": 5}
]

enemies = [
    {"id": "enemy1", "health": 80, "x": 2, "y": 2},
    {"id": "enemy2", "health": 120, "x": 4, "y": 4},
]

anomalies = [
    {"id": "anomaly1", "effectiveRadius": 3, "radius": 2, "x": 3, "y": 3, "strength": 100},
    {"id": "anomaly2", "effectiveRadius": 4, "radius": 2, "x": 4, "y": 4, "strength": 50},
]

# Поиск оптимального маршрута
path, weighted_length = find_shortest_path(transport, bounties, enemies, anomalies)

print("Оптимальный путь для сбора наград:", path)
print("Взвешенная длина маршрута:", weighted_length)
