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
    reservation_by_meal = """
        CREATE TABLE IF NOT EXISTS reservation_by_meal (
            meal_id uuid PRIMARY KEY,
            client_name text,
            reservation_timestamp timestamp,
        );
    """

    all = [meal_by_id, reservation_by_meal]
