'''Analyze collected data'''
from pathlib import Path
import json

from loguru import logger

def analyze_collected_data():
    '''Print stats'''
    data_dir = Path("../data")

    # Stats to collect
    total_movies = 0
    years_distribution = {}
    genres = set()
    directors = set()
    missing_fields = {
        "year": 0,
        "director": 0,
        "main_cast": 0,
        "music_director": 0,
        "producer": 0,
        "genres": 0,
        "plot_themes": 0,
        "awards": 0
    }

    # Process each JSON file
    for json_file in data_dir.glob("*.json"):
        if json_file.name == "processed_pages.json":
            continue

        total_movies += 1
        data = json.loads(json_file.read_text())

        # Check years
        if data.get("year"):
            years_distribution[data["year"]] = years_distribution.get(data["year"], 0) + 1
        else:
            missing_fields["year"] += 1

        # Collect genres
        if data.get("genres"):
            genres.update(data["genres"])
        else:
            missing_fields["genres"] += 1

        # Add directors
        if data.get("director"):
            directors.add(data["director"])
        else:
            missing_fields["director"] += 1

        # Check other missing fields
        for field in missing_fields:
            if not data.get(field):
                missing_fields[field] += 1

    # Log analysis
    logger.info(f"Total movies collected: {total_movies}")
    logger.info("Years distribution:")
    for year in sorted(years_distribution.keys()):
        logger.info(f"{year}: {years_distribution[year]} movies")

    logger.info(f"Unique genres found: {len(genres)}")
    logger.info(f"Genres: {genres}")

    logger.info(f"Unique directors found: {len(directors)}")

    logger.info("Missing fields analysis:")
    for field, count in missing_fields.items():
        percentage = (count / total_movies) * 100
        logger.info(f"{field}: {count} movies ({percentage:.1f}%)")

if __name__ == "__main__":
    analyze_collected_data()
