import pandas as pd
from neo4j import GraphDatabase

# ----------------------------
# Config Neo4j
# ----------------------------
uri = "bolt://localhost:7687"
user = "neo4j"
password = "123456789"
driver = GraphDatabase.driver(uri, auth=(user, password))

# ----------------------------
# Charger le CSV
# ----------------------------
df = pd.read_csv("data/processed/allergies_medicaments_clean.csv")

# ----------------------------
# Fonction d'import dans Neo4j
# ----------------------------
def import_allergies(tx, medicament_name, allergen_name):
    # S'assurer que le nœud allergène existe
    tx.run("""
        MERGE (a:ALLERGENE {name: $allergen_name})
    """, allergen_name=allergen_name)

    # Relier le médicament existant (recherche par name) au nœud allergène
    tx.run("""
        MATCH (m:MEDICAMENT {name: $med_name})
        MATCH (a:ALLERGENE {name: $allergen_name})
        MERGE (m)-[:CONTIENT_ALLERGENE]->(a)
    """, med_name=medicament_name, allergen_name=allergen_name)

# ----------------------------
# Import batch avec execute_write
# ----------------------------
with driver.session() as session:
    for _, row in df.iterrows():
        med_name = row["medicament"]
        allergen_name = row["allergen"]
        session.execute_write(import_allergies, med_name, allergen_name)

print("Import terminé dans Neo4j.")
