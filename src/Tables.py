class Tables:
    sample = """
    CREATE TABLE IF NOT EXISTS shopping_cart (
    userid text PRIMARY KEY,
    item_count int,
    last_update_timestamp timestamp
    );
    """

    all = [sample]