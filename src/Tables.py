class Tables:
    sample = """
    CREATE TABLE IF NOT EXISTS shopping_cart (
        userid text PRIMARY KEY,
        item_count int,
        last_update_timestamp timestamp
    );
    """
    meal_by_id = """
    CREATE TABLE IF NOT EXISTS meal_by_id (
        meal_id uuid PRIMARY KEY,
        meal_type text,
        provider text,
        pickup_time int,
    );
    """

    all = [sample, meal_by_id]


