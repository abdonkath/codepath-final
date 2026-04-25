PET_CARE_GUIDES = {
    "dog": {
        "general": """
Dogs need daily exercise, fresh water, and regular feeding (2x/day for adults).
Routine vet checkups should happen once a year.
Dental cleaning is recommended every 6-12 months.
Nails should be trimmed every 3-4 weeks.
Baths are needed every 4-6 weeks depending on coat type.
Flea and tick prevention should be applied monthly.
Dogs are social animals and need daily interaction and playtime.
""",
        "golden retriever": """
Golden Retrievers are high-energy dogs needing 1-2 hours of exercise daily.
Their dense double coat requires brushing 2-3 times per week to prevent matting.
They are prone to hip dysplasia — joint supplements may be recommended by a vet.
Ear infections are common; ears should be checked and cleaned weekly.
Goldens are food-motivated and prone to obesity — monitor meal portions.
Socialization and obedience training should start early (8-16 weeks).
""",
        "poodle": """
Poodles require professional grooming every 6-8 weeks.
They are highly intelligent and need daily mental stimulation (puzzle toys, training).
Poodles need moderate daily exercise — 30-60 minutes of walking or play.
Ear hair grows into the ear canal and should be cleaned regularly to prevent infection.
They are hypoallergenic — good for owners with allergies.
""",
        "bulldog": """
Bulldogs are low-energy and need only 20-30 minutes of light exercise daily.
Their facial skin folds must be cleaned daily to prevent bacterial infections.
Bulldogs are prone to breathing issues — avoid exercise in hot or humid weather.
Weight management is critical; avoid overfeeding.
Dental hygiene is important — brush teeth 2-3 times per week.
""",
    },
    "cat": {
        "general": """
Cats are independent but need daily interaction and enrichment.
Fresh water and food should always be available (or scheduled 2x/day for wet food).
Litter box should be scooped daily and fully cleaned weekly.
Annual vet visits are recommended; indoor cats need core vaccines.
Cats need scratching posts to maintain claw health.
Dental disease is common — teeth brushing or dental treats help.
""",
        "persian": """
Persian cats have long, thick coats that require daily brushing to prevent tangles.
Their flat faces (brachycephalic) make them prone to breathing and eye issues.
Eye discharge is common — wipe eyes gently with a damp cloth daily.
Persians are calm and low-energy — short indoor play sessions are sufficient.
Regular professional grooming every 6-8 weeks is recommended.
""",
        "siamese": """
Siamese cats are highly vocal and social — they need lots of human interaction.
They are prone to respiratory infections and dental disease.
Daily playtime of 20-30 minutes helps prevent boredom and destructive behavior.
Siamese have short coats needing only weekly brushing.
They do better in pairs or with other pets to avoid loneliness.
""",
        "maine coon": """
Maine Coons are large, dog-like cats that enjoy interactive play and fetch.
Their semi-long coat needs brushing 2-3 times per week.
They are prone to hypertrophic cardiomyopathy (HCM) — annual cardiac screenings recommended.
Maine Coons love water and may play with their water bowl.
They need vertical space — tall cat trees and shelves are ideal.
""",
    },
    "other": {
        "general": """
Small animals (rabbits, guinea pigs, hamsters) need species-appropriate diet and housing.
Exotic pets (birds, reptiles) require specialized vet care — find an exotic animal vet.
All pets benefit from a clean, safe living environment and daily observation for health changes.
Regular weight checks help detect illness early in small animals.
Enrichment activities (toys, foraging, exploration) are important for mental health.
""",
        "rabbit": """
Rabbits need unlimited timothy hay, fresh leafy greens, and limited pellets daily.
Their enclosure should allow at least 3-4 hours of free roaming per day.
Rabbits are social — they do best in bonded pairs.
Nails need trimming every 4-6 weeks.
Rabbits cannot vomit — GI stasis is a medical emergency; watch for loss of appetite.
Annual vet visits with a rabbit-savvy vet are recommended.
""",
        "bird": """
Birds need a varied diet: pellets, fresh fruits, vegetables, and limited seeds.
Social interaction daily is critical — birds can develop depression if isolated.
Cage cleaning should happen weekly; food/water dishes daily.
Wing and nail trims every 2-3 months depending on species.
Birds are sensitive to fumes — never use non-stick cookware or aerosol sprays nearby.
""",
    },
}


def retrieve(species: str, breed: str = "") -> str:
    """Return care guide text for a given species and optional breed."""
    species = species.lower().strip()
    breed = breed.lower().strip()

    species_data = PET_CARE_GUIDES.get(species, PET_CARE_GUIDES["other"])
    general = species_data.get("general", "")
    breed_specific = species_data.get(breed, "")

    if breed_specific:
        return f"General {species} care:\n{general}\n\nBreed-specific care for {breed}:\n{breed_specific}"
    return f"General {species} care:\n{general}"
