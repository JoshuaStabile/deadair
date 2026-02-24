GET_RANDOM_TRACK = """
    SELECT Name, Album, Artists, Path
    FROM BaseItems
    WHERE UnratedType = 'Music'
    AND Path IS NOT NULL
    ORDER BY RANDOM()
    LIMIT 1;
"""
