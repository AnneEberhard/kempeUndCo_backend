Vor import von Ahnenblatt CSV: 
    run check_encoding_csv.py to check the UTF encoding (is usually UTF-16)
    run clean_ahnenblatt_source.py to clean the headers of sonderzeichen and change to UTF-8
    then run import via django admin panel

CAVE: After changing the model / adding fields etc. do an export of the data to ensure smooth import on the server

To upload media files:
 1. charfield anstelle von filefield (migrieren)
 2. händisch upload der fieles in den media/images ordner
 3. durchführen des skriptes update_media_path.py (auf der root Ebene!)
 4. alle obje_file Felder in FileFields (migrieren)
 danach persons exportiert als csv und als json
