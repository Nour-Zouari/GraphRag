import csv
from neo4j import GraphDatabase

# --- Config Neo4j ---
uri = "bolt://localhost:7687"
user = "neo4j"
password = "123456789"
driver = GraphDatabase.driver(uri, auth=(user, password))

# ----------------------
# Fonction pour normaliser les noms
# ----------------------
def normalize_text(text):
    return text.strip().upper() if isinstance(text, str) else ""

# ----------------------
# Importer les allergies depuis CSV
# ----------------------
def import_patient_allergies(csv_path):
    with driver.session() as session:
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                patient_name = normalize_text(row['nom_patient'])
                allergen_name = normalize_text(row['nom_allergie'])

                # MERGE patient
                session.run(
                    "MERGE (p:PATIENT {name:$patient_name})",
                    patient_name=patient_name
                )

                # MERGE allergen
                session.run(
                    "MERGE (a:ALLERGENE {name:$allergen_name})",
                    allergen_name=allergen_name
                )

                # MERGE relation patient -> allergen
                session.run(
                    """
                    MATCH (p:PATIENT {name:$patient_name})
                    MATCH (a:ALLERGENE {name:$allergen_name})
                    MERGE (p)-[:A_ALLERGIE]->(a)
                    """,
                    patient_name=patient_name,
                    allergen_name=allergen_name
                )

if __name__ == "__main__":
    csv_file = "data/processed/patient_allergies.csv"
    import_patient_allergies(csv_file)
    print("Import terminé : patients et allergies ajoutés à Neo4j.")
