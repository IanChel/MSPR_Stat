import json
import os

# Créer un notebook complètement nouveau et simple
notebook = {
    "cells": [
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["try:\n", "    import xlrd\n", "    import openpyxl\n", "except ImportError:\n", "    import sys\n", "    !{sys.executable} -m pip install xlrd openpyxl\n", "    print(\"Dépendances installées.\")"]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["# Analyse de la Région Nouvelle-Aquitaine : Préparation des Données\n", "Ce notebook regroupe et nettoie les données électorales, socio-économiques et de sécurité pour la région Nouvelle-Aquitaine."]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["import pandas as pd\n", "import numpy as np\n", "import os\n", "import warnings\n", "warnings.filterwarnings('ignore')\n", "\n", "base_path = r'c:\\Users\\tarek\\Downloads\\aliMSPR\\MSPR_FINAL'\n", "data_2016 = os.path.join(base_path, 'indicateur data 2016')\n", "data_2020 = os.path.join(base_path, 'indicateur data 2020')\n", "elec_file = os.path.join(base_path, 'MSPR', '01_Donnees', 'brut', 'nouvelle_aquitaine_2012_2017_tour1.csv')\n", "export_path = os.path.join(base_path, 'MSPR', '01_Donnees', 'data_nouvelle_aquitaine_final.csv')\n", "\n", "print(\"Chemins configurés.\")"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["def load_data(path, file):\n", "    full_path = os.path.join(path, file)\n", "    try:\n", "        if file.endswith('.csv'):\n", "            df = pd.read_csv(full_path, sep=';', encoding='utf-8', low_memory=False)\n", "            if len(df.columns) == 1:\n", "                df = pd.read_csv(full_path, sep=',', encoding='utf-8', low_memory=False)\n", "        else:\n", "            df = pd.read_excel(full_path, engine='openpyxl' if file.endswith('.xlsx') else None)\n", "        print(f'✅ {file}: {len(df)} lignes')\n", "        return df\n", "    except Exception as e:\n", "        print(f'❌ {file}: {e}')\n", "        return None\n", "\n", "print('CHARG DONNÉES 2016:')\n", "pop_2016 = load_data(data_2016, 'Population & emploi.csv')\n", "rev_2016 = load_data(data_2016, 'Revenus.xls')\n", "dipl_2016 = load_data(data_2016, 'Diplôme.xls')\n", "delinq_2016 = load_data(data_2016, 'Délinquance.csv')\n", "\n", "print('\\nCHARG DONNÉES 2020:')\n", "pop_2020 = load_data(data_2020, 'Population.xlsx')\n", "rev_2020 = load_data(data_2020, 'Revenus.xlsx')\n", "delinq_2020 = load_data(data_2020, 'Délinquance.xlsx')\n", "\n", "print('\\nCHARG ÉLECTIONS:')\n", "elec = load_data(os.path.dirname(elec_file), os.path.basename(elec_file))"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["print('\\n' + '='*80)\n", "print('PHASE: FUSION ET AUGMENTATION')\n", "print('='*80)\n", "\n", "def find_geo(df):\n", "    for col in df.columns:\n", "        if any(x in col.lower() for x in ['cod', 'code', 'com']):\n", "            return col\n", "    return df.columns[0]\n", "\n", "# Fusion Population\n", "print('\\n1. Fusion Population...')\n", "key16, key20 = find_geo(pop_2016), find_geo(pop_2020)\n", "pop_2016[key16] = pop_2016[key16].astype(str).str.zfill(5)\n", "pop_2020[key20] = pop_2020[key20].astype(str).str.zfill(5)\n", "df = pd.merge(pop_2016, pop_2020, left_on=key16, right_on=key20, how='outer', suffixes=('_16', '_20'))\n", "print(f'✅ {len(df)} lignes')\n", "\n", "# Fusion Revenus\n", "print('\\n2. Fusion Revenus...')\n", "k16, k20 = find_geo(rev_2016), find_geo(rev_2020)\n", "rev_2016[k16] = rev_2016[k16].astype(str).str.zfill(5)\n", "rev_2020[k20] = rev_2020[k20].astype(str).str.zfill(5)\n", "df_rev = pd.merge(rev_2016, rev_2020, left_on=k16, right_on=k20, how='outer', suffixes=('_16', '_20'))\n", "df = pd.merge(df, df_rev, left_on=key16, right_on=k16, how='left')\n", "print(f'✅ {len(df)} lignes')\n", "\n", "# Fusion Diplômes\n", "print('\\n3. Fusion Diplômes...')\n", "k_dipl = find_geo(dipl_2016)\n", "dipl_cols = [c for c in dipl_2016.columns if 'NSCOL' in c or 'BAC' in c]\n", "df = pd.merge(df, dipl_2016[[k_dipl] + dipl_cols], left_on=key16, right_on=k_dipl, how='left')\n", "print(f'✅ {len(df)} lignes')\n", "\n", "# Fusion Délinquance\n", "print('\\n4. Fusion Délinquance...')\n", "k_del_16, k_del_20 = find_geo(delinq_2016), find_geo(delinq_2020)\n", "delinq_2016[k_del_16] = delinq_2016[k_del_16].astype(str).str.zfill(2)\n", "delinq_2020[k_del_20] = delinq_2020[k_del_20].astype(str).str.zfill(2)\n", "df_del = pd.merge(delinq_2016, delinq_2020, left_on=k_del_16, right_on=k_del_20, how='outer', suffixes=('_16', '_20'))\n", "df['dept'] = df[key16].str[:2]\n", "df_del['dept'] = df_del[k_del_16].str[:2]\n", "df = pd.merge(df, df_del, on='dept', how='left')\n", "print(f'✅ {len(df)} lignes')\n", "\n", "# Fusion Élections\n", "print('\\n5. Fusion Élections...')\n", "k_elec = find_geo(elec)\n", "elec[k_elec] = elec[k_elec].astype(str).str.zfill(5)\n", "df = pd.merge(elec, df, left_on=k_elec, right_on=key16, how='inner')\n", "print(f'✅ {len(df)} lignes')\n", "\n", "# Nettoyage NaN\n", "print('\\n6. Nettoyage NaN...')\n", "numeric = df.select_dtypes(include=[np.number]).columns\n", "for col in numeric:\n", "    df[col] = pd.to_numeric(df[col], errors='coerce')\n", "    df[col].fillna(df[col].median(), inplace=True)\n", "print(f'✅ {len(df)} lignes')\n", "\n", "# Augmentation x5\n", "print('\\n7. Augmentation de données (x5)...')\n", "dfs = [df.copy()]\n", "for i in range(4):\n", "    df_aug = df.copy()\n", "    for col in numeric:\n", "        noise = np.random.normal(0, df[col].std() * 0.05, len(df))\n", "        df_aug[col] = df_aug[col] + noise\n", "    df_aug['aug_factor'] = i + 1\n", "    dfs.append(df_aug)\n", "df_final = pd.concat(dfs, ignore_index=True)\n", "print(f'✅ {len(df_final)} lignes après augmentation')\n", "\n", "# Export\n", "print('\\n8. Export CSV...')\n", "df_final.to_csv(export_path, index=False, encoding='utf-8')\n", "size_mb = os.path.getsize(export_path) / (1024*1024)\n", "print(f'✅ Sauvegardé: {export_path}')\n", "print(f'   Taille: {len(df_final)} lignes x {len(df_final.columns)} colonnes')\n", "print(f'   Poids: {size_mb:.2f} MB')\n", "\n", "print('\\n' + '='*80)\n", "print('✅ SUCCÈS - DATASET PRÊT POUR ML!')\n", "print('='*80)"]
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {
                "name": "ipython",
                "version": 3
            },
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.11.5"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

# Save notebook
nb_path = r'c:\Users\tarek\Downloads\aliMSPR\MSPR_FINAL\MSPR\02_Data_Engineering\notebooks\Nouvelle_Aquitaine_Data_Preparation.ipynb'
with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, ensure_ascii=False, indent=2)

print(f"✅ Notebook créé: {nb_path}")
