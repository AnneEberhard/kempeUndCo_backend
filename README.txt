Vor import von Ahnenblatt CSV: 
    run check_encoding_csv.py to check the UTF encoding (is usually UTF-16)
    run clean_ahnenblatt_source.py to clean the headers of sonderzeichen and change to UTF-8
    then run import via django admin panel
    saved data set: Person-2024-08-02_1_model_unaltered

CAVE: After changing the model / adding fields etc. do an export of the data to ensure smooth import on the server

Dates:
1. add model field confidential
2. run set_confidentiality.py on cleaned ahnenblatt source 
    (clean_and_set_confidentiality.py will moved none-conform date into notes - saved data set is Person-2024-08-02_2_clean_added_confident)
3. BEWARE not switching Charfield to Datefield as content WILL BE LOST
4. add new datefields birth_date_formatted and death_date_formatted -> migrate
5. run migrate_dates.py
    saved data set: Person-2024-08-03_3_added_formatted_date (includes also updated paths)
    data set includes three new fields: confidential and 2 formatted date fields
6. admin.py changed so that formatted date fills automatically

To upload media files based on Ahnenblatt Datei:
 1. upload files in media/images folder (händisch)
 2. run rename_and_update_paths.py (on root level!)
    every image file now renamed based on id and image object numer
    (update_media_path.py verschiebt nur nach media Ordner, ohne Umbenennung)
    (Person-2024-08-03_1_updated_paths has non-conform dates in notes, extra field: confidential)
    saved data set: Person-2024-08-03_2_addded_conf_upated_path (extra field: confidential)

Added family_tree
1. updated model with field family_tree 1 and 2 and choices -> migrate
2. run update_family_trees.py to fill all data sets with 'kempe' as family 1 for starters
    saved data set: Person-2024-08-03_4_stammbaum_kempe_all
    (includes new fields: confidential, birth_date_formatted, death_date_formatted, family_tree_1, family_tree_2)


