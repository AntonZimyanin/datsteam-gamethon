import requests
from http_client import HttpClient
import math
import itertools
import time

from app.datsteam.math.math_func import calculate_distance, calculate_acceleration
from enemy import is_enemy, is_weak_enemy


def avoid_anomaly(anomaly, transport):
    """
    Функция для обхода аномалии.
    Например, увеличиваем координаты на некоторое расстояние, чтобы обойти.
    """
    avoid_distance = anomaly['radius'] * \
        2  # Обход на расстоянии двойного радиуса аномалии
    if transport['x'] < anomaly['x']:
        transport['x'] -= avoid_distance
    else:
        transport['x'] += avoid_distance
    if transport['y'] < anomaly['y']:
        transport['y'] -= avoid_distance
    else:
        transport['y'] += avoid_distance


def enemy_action(transport, enemies):
    for enemy in enemies:
        distance_to_enemy = enemy_calculate_distance(transport, enemy)
        if distance_to_enemy <= 200:
            if transport['attackCooldownMs'] == 0:  # Проверяем, что орудие готово
                print(f"Attacking enemy at distance {
                      distance_to_enemy} meters!")
                enemy['health'] -= 30  # Наносим урон
                # Устанавливаем КД в 5 секунд
                transport['attackCooldownMs'] = 5000
                return 'attack'  # Атакуем врага
            else:
                print(f"Attack on cooldown for {
                      transport['attackCooldownMs']} ms.")
    return None  # Нет врагов в пределах досягаемости

def is_anomaly_nearby(transport, anomaly):
    """Проверить, находится ли аномалия в пределах её радиуса влияния от транспорта."""
    distance = enemy_calculate_distance(transport, anomaly)
    return distance <= anomaly['effectiveRadius']


def move_transport(transport, destination_x, destination_y):
    """Функция для перемещения транспорта к заданной точке"""
    delta_x = destination_x - transport['x']
    delta_y = destination_y - transport['y']
    distance = math.sqrt(delta_x ** 2 + delta_y ** 2)

    # Проверим, если транспорт близко к цели, просто переместим его на место
    if distance < 1:
        transport['x'] = destination_x
        transport['y'] = destination_y
        return

    # Рассчитываем новые координаты транспорта на основании скорости и направления
    velocity_magnitude = math.sqrt(
        transport['velocity']['x'] ** 2 + transport['velocity']['y'] ** 2)

    if velocity_magnitude > 0:
        norm_x = delta_x / distance
        norm_y = delta_y / distance

        # Обновляем координаты транспорта в зависимости от его скорости
        transport['x'] += transport['velocity']['x'] * norm_x
        transport['y'] += transport['velocity']['y'] * norm_y

        print(f"Transport {transport['id']} moved to ({
              transport['x']}, {transport['y']})")


def find_nearest_bounty(transport, bounties):
    """Функция для нахождения ближайшей точки с баунти"""
    min_distance = float('inf')
    nearest_bounty = None

    for bounty in bounties:
        distance = calculate_distance(transport, bounty)
        if distance < min_distance:
            min_distance = distance
            nearest_bounty = bounty

    return nearest_bounty


def find_path(transports, bounties, enemies, anomalies, client):

    for transport in transports:
        # Уменьшаем кулдаун атаки
        if transport['attackCooldownMs'] > 0:
            transport['attackCooldownMs'] = max(
                0, transport['attackCooldownMs'] - 1000)

        nearest_bounty = find_nearest_bounty(transport, bounties)

        if nearest_bounty:
            print(f"Nearest bounty found at ({
                  nearest_bounty['x']}, {nearest_bounty['y']})")

            while calculate_distance(transport, nearest_bounty) > 1:
                action = enemy_action(transport, enemies)
                if action == 'shield':
                    transport['shieldLeftMs'] = max(
                        transport['shieldLeftMs'] - 1, 0)

                # Обходим аномалии
                for anomaly in anomalies:
                    if is_anomaly_nearby(transport, anomaly):
                        print(f"Avoiding anomaly: {anomaly['id']}")
                        avoid_anomaly(anomaly, transport)

                # Перемещаем транспорт
                move_transport(
                    transport, nearest_bounty['x'], nearest_bounty['y'])

                updated_data = {
                    "transports": [
                        {
                            "id": transport['id'],
                            "x": transport['x'],
                            "y": transport['y'],
                            "acceleration": dict(transport).get('acceleration'),
                        }
                    ]
                }
                client.post_request(updated_data)
                time.sleep(0.34)  # Задержка для обновления


while True:
    client = HttpClient()

    auth_token = '670516cb9d5a9670516cb9d5ae'
    url = 'https://games.datsteam.dev/play/magcarp/player/move'

    headers = {
        'X-Auth-Token': auth_token
    }

    response = requests.post(url, json={}, headers=headers)

    response_data = response.json()

    # Extract "transports", "bounties", and "enemies"
    transports = response_data.get("transports", [])
    bounties = response_data.get("bounties", [])
    enemies = response_data.get("enemies", [])
    anomalies = response_data.get("anomalies", [])

    find_path(transports, bounties, enemies, anomalies, client)
