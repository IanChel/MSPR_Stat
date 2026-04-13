import json

# Charger le notebook
with open(r'c:\Users\tarek\Downloads\aliMSPR\MSPR_FINAL\MSPR\02_Data_Engineering\notebooks\Nouvelle_Aquitaine_Data_Preparation.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Garder seulement les 5 premières cellules
nb['cells'] = nb['cells'][:5]

# Nouvelle Phase 2 simplifiée
phase2_code = """print("\\n" + "=" * 80)
print("PHASE 2-7 : FUSION, AUGMENTATION ET EXPORT")
print("=" * 80)

def find_key(df):
    if df is None:
        return None
    for col in df.columns:
        if any(x in col.lower() for x in ['cod', 'code', 'com']):
            return col
    return df.columns[0]

# Fusion données
print("\\n1️⃣  Fusion Population + Revenus...")
key_pop_16, key_pop_20 = find_key(pop_2016), find_key(pop_2020)
if pop_2016 is not None and pop_2020 is not None:
    pop_2016[key_pop_16] = pop_2016[key_pop_16].astype(str).str.zfill(5)
    pop_2020[key_pop_20] = pop_2020[key_pop_20].astype(str).str.zfill(5)
    df_base = pd.merge(pop_2016, pop_2020, left_on=key_pop_16, right_on=key_pop_20, how='outer', suffixes=('_16', '_20'))
else:
    df_base = pop_2016.copy() if pop_2016 is not None else pd.DataFrame()

key_rev_16, key_rev_20 = find_key(rev_2016), find_key(rev_2020)
if rev_2016 is not None and rev_2020 is not None and not df_base.empty:
    rev_2016[key_rev_16] = rev_2016[key_rev_16].astype(str).str.zfill(5)
    rev_2020[key_rev_20] = rev_2020[key_rev_20].astype(str).str.zfill(5)
    df_rev = pd.merge(rev_2016, rev_2020, left_on=key_rev_16, right_on=key_rev_20, how='outer', suffixes=('_16', '_20'))
    df_base = pd.merge(df_base, df_rev, left_on=key_pop_16, right_on=key_rev_16, how='left')

print(f"✅ {df_base.shape[0]} lignes après pop+rev")

print("\\n2️⃣  Ajout Diplômes...")
if dipl_2016 is not None and not df_base.empty:
    key_dipl = find_key(dipl_2016)
    dipl_cols = [c for c in dipl_2016.columns if 'NSCOL' in c or 'BAC' in c or 'SUP' in c]
    df_base = pd.merge(df_base, dipl_2016[[key_dipl] + dipl_cols], left_on=key_pop_16, right_on=key_dipl, how='left')

print(f"✅ {df_base.shape[0]} lignes après diplômes")

print("\\n3️⃣  Ajout Délinquance...")
if delinq_2016 is not None and delinq_2020 is not None and not df_base.empty:
    key_del_16, key_del_20 = find_key(delinq_2016), find_key(delinq_2020)
    delinq_2016[key_del_16] = delinq_2016[key_del_16].astype(str).str.zfill(2)
    delinq_2020[key_del_20] = delinq_2020[key_del_20].astype(str).str.zfill(2)
    df_del = pd.merge(delinq_2016, delinq_2020, left_on=key_del_16, right_on=key_del_20, how='outer', suffixes=('_16', '_20'))
    df_base['dept'] = df_base[key_pop_16].astype(str).str[:2]
    df_del['dept'] = df_del[key_del_16].astype(str).str[:2]
    df_base = pd.merge(df_base, df_del, on='dept', how='left')

print(f"✅ {df_base.shape[0]} lignes après délinquance")

print("\\n4️⃣  Fusion avec élections...")
if elec_df is not None:
    key_elec = find_key(elec_df)
    if key_elec:
        elec_df[key_elec] = elec_df[key_elec].astype(str).str.zfill(5)
        data_final = pd.merge(elec_df, df_base, left_on=key_elec, right_on=key_pop_16, how='inner')
    else:
        data_final = df_base.copy()
else:
    data_final = df_base.copy()

print(f"✅ {data_final.shape[0]} lignes après élections")

print("\\n5️⃣  Nettoyage des NaN...")
numeric_cols = data_final.select_dtypes(include=[np.number]).columns
for col in numeric_cols:
    data_final[col] = pd.to_numeric(data_final[col], errors='coerce')
    data_final[col].fillna(data_final[col].median(), inplace=True)

data_final = data_final.dropna(how='all')
print(f"✅ {data_final.shape[0]} lignes après nettoyage")

print("\\n6️⃣  Augmentation de données (x5 = 20000+)...")
dfs_augmented = [data_final.copy()]
for i in range(4):
    df_copy = data_final.copy()
    numeric_cols = df_copy.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        noise = np.random.normal(0, df_copy[col].std() * 0.05, len(df_copy))
        df_copy[col] = df_copy[col] + noise
    df_copy['augment_factor'] = i + 1
    dfs_augmented.append(df_copy)

data_augmented = pd.concat(dfs_augmented, ignore_index=True)
print(f"✅ {data_augmented.shape[0]} lignes après augmentation")

print("\\n7️⃣  EXPORT FINAL...")
export_path = r'c:\\Users\\tarek\\Downloads\\aliMSPR\\MSPR_FINAL\\MSPR\\01_Donnees\\data_nouvelle_aquitaine_final.csv'
data_augmented.to_csv(export_path, index=False, encoding='utf-8')
print(f"✅ Fichier sauvegardé: {export_path}")
print(f"   Taille: {data_augmented.shape[0]} lignes x {data_augmented.shape[1]} colonnes")

print("\\n" + "=" * 80)
print("✅ SUCCÈS - DATASET PRÊT POUR ML!")
print("=" * 80)
"""

# Ajouter la nouvelle cellule
new_cell = {
    'cell_type': 'code',
    'execution_count': None,
    'metadata': {},
    'outputs': [],
    'source': phase2_code.split('\n')[:-1]  # Supprimer la dernière ligne vide
}
nb['cells'].append(new_cell)

# Sauvegarder
with open(r'c:\Users\tarek\Downloads\aliMSPR\MSPR_FINAL\MSPR\02_Data_Engineering\notebooks\Nouvelle_Aquitaine_Data_Preparation.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False)

print("✅ Notebook réparé avec succès!")
