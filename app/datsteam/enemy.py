from math_func import calculate_distance


def is_enemy(transport, enemy):
    """Check if the enemy is within a distance of 200 units from the transport."""
    distance = calculate_distance(transport, enemy)
    print(f"Distance to enemy: {distance}")
    
    return distance <= 200


def is_weak_enemy(transport, enemy):
    """Check if the enemy has less health than the transport, meaning it is weaker."""
    return enemy["health"] < transport["health"]
