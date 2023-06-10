class Tables:
    meal_by_id = """
    CREATE TABLE IF NOT EXISTS meal_by_id (
        meal_id uuid PRIMARY KEY,
        meal_type text,
        provider text,
        pickup_time int,
        available boolean,
    );
    """
    reservations = """
        CREATE TABLE IF NOT EXISTS reservations (
            meal_id uuid,
            client_name text,
            provider text,
            pickup_time int,
            reservation_timestamp timestamp,
            PRIMARY KEY ((meal_id), client_name)
        );
    """
    all = [meal_by_id, reservations]
