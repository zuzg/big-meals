class Tables:
    meal_by_id = """
    CREATE TABLE IF NOT EXISTS meal_by_id (
        meal_id uuid PRIMARY KEY,
        meal_type text,
        provider text,
        pickup_time int,
        is_available boolean,
    );
    """
    reservations = """
        CREATE TABLE IF NOT EXISTS reservations (
            meal_id uuid PRIMARY KEY,
            client_name text,
            provider text,
            pickup_time int,
            reservation_timestamp timestamp,
        );
    """

    all = [meal_by_id, reservations]
