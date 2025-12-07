import csv
from neo4j import GraphDatabase

# --- Config Neo4j ---
uri = "bolt://localhost:7687"
user = "neo4j"
password = "123456789"
driver = GraphDatabase.driver(uri, auth=(user, password))

# --- Chargement CSV nettoyé ---
def load_clean_csv(file_path="data/processed/clean_openfda_bdpm.csv"):
    records = []
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            drug_code = row["drug_code"]
            interactions = row["interactions"].split(";") if row["interactions"] else []
            interactions = [x for x in interactions if x != drug_code]  # éviter auto-liens
            records.append((drug_code, interactions))
    return records

# --- Fonctions pour Neo4j ---
def add_medicament(tx, code_cis):
    tx.run("MERGE (m:MEDICAMENT {code:$code})", code=code_cis)

def add_medicaments_batch(tx, codes):
    tx.run(
        "UNWIND $codes AS c "
        "MERGE (:MEDICAMENT {code:c})",
        codes=codes
    )

def add_interactions_batch(tx, drug_code, interaction_codes):
    tx.run(
        "MATCH (a:MEDICAMENT {code:$drug}) "
        "MATCH (b:MEDICAMENT) WHERE b.code IN $codes "
        "MERGE (a)-[:INTERAGIT_AVEC]->(b)",
        drug=drug_code,
        codes=interaction_codes
    )

# --- Import dans Neo4j ---
def import_to_neo4j(records):
    with driver.session() as session:
        for drug_code, interactions in records:
            session.execute_write(add_medicament, drug_code)

            if interactions:
                session.execute_write(add_medicaments_batch, interactions)
                session.execute_write(add_interactions_batch, drug_code, interactions)

if __name__ == "__main__":
    records = load_clean_csv()
    print(f"Import de {len(records)} médicaments dans Neo4j...")
    import_to_neo4j(records)
    print("Import terminé.")
