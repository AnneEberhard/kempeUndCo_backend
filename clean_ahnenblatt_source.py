import csv

# Mapping der originalen Header zu den Modell-Feldern
header_mapping = {
    "#REFN": "refn",
    "NAME": "name",
    "FATH.NAME": "fath_name",
    "FATH.#REFN": "fath_refn",
    "MOTH.NAME": "moth_name",
    "MOTH.#REFN": "moth_refn",
    "_UID": "uid",
    "SURN": "surn",
    "GIVN": "givn",
    "SEX": "sex",
    "OCCU": "occu",
    "CHAN.DATE": "chan_date",
    "CHAN.DATE.TIME": "chan_date_time",
    "BIRT.DATE": "birt_date",
    "BIRT.PLAC": "birt_plac",
    "DEAT.DATE": "deat_date",
    "DEAT.PLAC": "deat_plac",
    "NOTE": "note",
    "CHR.DATE": "chr_date",
    "CHR.PLAC": "chr_plac",
    "BURI.DATE": "buri_date",
    "BURI.PLAC": "buri_plac",
    "NAME._RUFNAME": "name_rufname",
    "NAME.NPFX": "name_npfx",
    "SOUR": "sour",
    "NAME.NICK": "name_nick",
    "NAME._MARNM": "name_marnm",
    "CHR.ADDR": "chr_addr",
    "RELI": "reli",
    "MARR.SPOU.NAME.1": "marr_spou_name_1",
    "MARR.SPOU.#REFN.1": "marr_spou_refn_1",
    "FAM.HUSB.1": "fam_husb_1",
    "FAM.WIFE.1": "fam_wife_1",
    "MARR.DATE.1": "marr_date_1",
    "MARR.PLAC.1": "marr_plac_1",
    "FAM.CHIL.1": "fam_chil_1",
    "FAM.MARR.1": "fam_marr_1",
    "FAM._STAT.1": "fam_stat_1",
    "FAM._MARR.1": "fam_marr_1",
    "MARR.SPOU.NAME.2": "marr_spou_name_2",
    "MARR.SPOU.#REFN.2": "marr_spou_refn_2",
    "FAM.HUSB.2": "fam_husb_2",
    "FAM.WIFE.2": "fam_wife_2",
    "MARR.DATE.2": "marr_date_2",
    "MARR.PLAC.2": "marr_plac_2",
    "FAM.CHIL.2": "fam_chil_2",
    "FAM.MARR.2": "fam_marr_2",
    "FAM._STAT.2": "fam_stat_2",
    "FAM._MARR.2": "fam_marr_2",
    "MARR.SPOU.NAME.3": "marr_spou_name_3",
    "MARR.SPOU.#REFN.3": "marr_spou_refn_3",
    "FAM.HUSB.3": "fam_husb_3",
    "FAM.WIFE.3": "fam_wife_3",
    "MARR.DATE.3": "marr_date_3",
    "MARR.PLAC.3": "marr_plac_3",
    "FAM.CHIL.3": "fam_chil_3",
    "FAM.MARR.3": "fam_marr_3",
    "FAM._STAT.3": "fam_stat_3",
    "FAM._MARR.3": "fam_marr_3",
    "MARR.SPOU.NAME.4": "marr_spou_name_4",
    "MARR.SPOU.#REFN.4": "marr_spou_refn_4",
    "FAM.HUSB.4": "fam_husb_4",
    "FAM.WIFE.4": "fam_wife_4",
    "MARR.DATE.4": "marr_date_4",
    "MARR.PLAC.4": "marr_plac_4",
    "FAM.CHIL.4": "fam_chil_4",
    "FAM.MARR.4": "fam_marr_4",
    "FAM._STAT.4": "fam_stat_4",
    "FAM._MARR.4": "fam_marr_4",
    "OBJE.FILE.1": "obje_file_1",
    "OBJE.TITL.1": "obje_titl_1",
    "OBJE.FILE.2": "obje_file_2",
    "OBJE.TITL.2": "obje_titl_2",
    "OBJE.FILE.3": "obje_file_3",
    "OBJE.TITL.3": "obje_titl_3",
    "OBJE.FILE.4": "obje_file_4",
    "OBJE.TITL.4": "obje_titl_4",
    "OBJE.FILE.5": "obje_file_5",
    "OBJE.TITL.5": "obje_titl_5",
    "OBJE.FILE.6": "obje_file_6",
    "OBJE.TITL.6": "obje_titl_6",
}

def clean_csv(input_file, output_file):
    with open(input_file, mode='r', encoding='utf-16') as infile, open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
        reader = csv.DictReader(infile, delimiter='\t')
        # Überprüfen, ob die Header korrekt gemappt werden können
        if not all(header in header_mapping for header in reader.fieldnames):
            print("Some headers are not mapped correctly.")
            return
        
        # Neue Header basierend auf dem Mapping
        new_fieldnames = [header_mapping[header] for header in reader.fieldnames]
        
        writer = csv.DictWriter(outfile, fieldnames=new_fieldnames, delimiter=',')
        writer.writeheader()
        
        for row in reader:
            new_row = {header_mapping[key]: value for key, value in row.items()}
            writer.writerow(new_row)
    
    print(f"CSV file cleaned and saved as {output_file}")

# Beispielaufruf des Skripts
input_file = 'Stammfolge Kempe 2264.csv'  # Pfad zur Originaldatei
output_file = 'kempe_cleaned_source_file.csv'  # Pfad zur bereinigten Datei
clean_csv(input_file, output_file)
