GET_RANDOM_TRACK = """
    SELECT Name, Album, Artists, Path
    FROM TypedBaseItems
    WHERE Type = 'Audio'
    AND Path IS NOT NULL
    ORDER BY RANDOM()
    LIMIT 1;
"""
