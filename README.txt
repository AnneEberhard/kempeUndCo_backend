Vor import von Ahnenblatt CSV: 
    run check_encoding_csv.py to check the UTF encoding (is usually UTF-16)
    run clean_ahnenblatt_source.py to clean the headers of sonderzeichen and change to UTF-8
    then run import via django admin panel

CAVE: After changing the model / adding fields etc. do an export of the data to ensure smooth import on the server

Dates:
1. add model field clean_and_set_confidentiality
2. run clean_and_set_confidentiality.py on cleaned ahnenblatt source
3. BEWARE not switching Charfield to Datefield as content WILL BE LOST
4. instead: convert_birth_and_death_date.py???

To upload media files based on Ahnenblatt Datei:
 1. charfield anstelle von filefield (migrieren) (Nicht notwendig ab Sicherung cleaned dates)
 2. händisch upload der files in den media/images ordner
 3. durchführen des skriptes update_media_path.py (auf der root Ebene!)
 4. alle obje_file Felder in FileFields (migrieren) (Nicht notwendig ab Sicherung cleaned dates)
 danach persons exportiert als csv und als json

To rename all media files to ensure clean naming
1. rename_and_update_paths.py
every image file now renamed based on id and image object numer
