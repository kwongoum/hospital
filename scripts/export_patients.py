import csv
import xmlrpc.client
from pathlib import Path


# ============================================================
# 1. Configuration de la connexion à Odoo
# ============================================================

url = "http://localhost:8069"
db = "hospi_db"
username = "admin1.it@hospital.com"
password = "Psswrd3214"


# ============================================================
# 2. Connexion à Odoo
# ============================================================

common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")

uid = common.authenticate(
    db,
    username,
    password,
    {}
)

if not uid:
    print("Échec de l'authentification à Odoo.")
    exit()


print(f"Connexion réussie. User ID : {uid}")


# ============================================================
# 3. Connexion au service Object d'Odoo
# ============================================================

models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")


# ============================================================
# 4. Lire les patients depuis Odoo
# ============================================================

patients = models.execute_kw(
    db,
    uid,
    password,
    "hospital.patient",
    "search_read",
    [[]],
    {
        "fields": [
            "name",
            "age",
            "gender",
        ]
    }
)


print(f"Nombre de patients récupérés : {len(patients)}")


# ============================================================
# 5. Écrire les patients dans un fichier CSV
# ============================================================

# Enregistrer le CSV dans le même dossier que ce script
csv_file = Path(__file__).resolve().parent / "patients.csv"

with open(csv_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["id", "name", "age", "gender"]
    )

    writer.writeheader()
    writer.writerows(patients)

print(f"Export terminé : {csv_file}")