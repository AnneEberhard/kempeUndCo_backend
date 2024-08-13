Vor import von Ahnenblatt CSV: 
    run python script_check_encoding_csv.py to check the UTF encoding (is usually UTF-16)
    run python script_clean_ahnenblatt_source.py to clean the headers of sonderzeichen and change to UTF-8
    then run import via django admin panel
    saved data set: Person-2024-08-02_1_model_unaltered

CAVE: After changing the model / adding fields etc. do an export of the data to ensure smooth import on the server

Dates:
1. add model field confidential
2. run python script_set_confidentiality.py on cleaned ahnenblatt source 
    (clean_and_set_confidentiality.py will moved none-conform date into notes - saved data set is Person-2024-08-02_2_clean_added_confident)
3. BEWARE not switching Charfield to Datefield as content WILL BE LOST
4. add new datefields birth_date_formatted and death_date_formatted -> migrate
5. run python script_migrate_dates.py
    saved data set: Person-2024-08-03_3_added_formatted_date (includes also updated paths)
    data set includes three new fields: confidential and 2 formatted date fields
6. admin.py changed so that formatted date fills automatically

To upload media files based on Ahnenblatt Datei:
 1. upload files in media/images folder (händisch)
 2. run python script_rename_and_update_paths.py (on root level!)
    every image file now renamed based on id and image object numer
    (script_update_media_path.py verschiebt nur nach media Ordner, ohne Umbenennung)
    (Person-2024-08-03_1_updated_paths has non-conform dates in notes, extra field: confidential)
    saved data set: Person-2024-08-03_2_addded_conf_upated_path (extra field: confidential)

Added family_tree
1. updated model with field family_tree 1 and 2 and choices -> migrate
2. run python script_update_family_trees.py to fill all data sets with 'kempe' as family 1 for starters
    saved data set: Person-2024-08-03_4_stammbaum_kempe_all
    (includes new fields: confidential, birth_date_formatted, death_date_formatted, family_tree_1, family_tree_2)

Related data
1. new class to use foreignkey relations
2. started with motther, father and spouses
3. run python script_migrate_person_to_related_data.py to migrate info from person dataset to relatedData data set
4. added four manytomany fields for children aus 4 potential marriages
5. run python script_migrate_children_to_related_data.py
6. new created fields in related data now excluded in person admin
saved data sets: Person-2024-08-04, RelatedData-2024-08-04
OPEN: shall change of new dataset also induce change data in old??
OPEN: Family Status in Ahnenblatt - was ist was?
CAVE: RelatedData renamed Relation for usability reasons
saved data set (includes created and modiefied fields):
    Person-2024-08-04 _2_relation_and_creation
    Relation-2024-08-04 _2_relation_and_creation

ADMIN View
1. moved exported fields to resources.py
2. excluded view of not used fields in person (or double with now related data, such as father)
3. changed admin.py view von exclude to fieldsets

Created by and last modified
1. added to person model:
    creation_date, last_modified_date, created_by, last_modified_by
2. modified admin.py by switching logic for formatted dates to models.py
3. run python script_update_created_by.py to fill all existing fields with user
saved data set: Person-2024-08-04_3_created_by_filled

Add new person: 
1. refn will now be added automatically qhen saved and is readonly field
2. limited sex to choices F, M, D
3. name is now readonly and will be generated from prefix, given name, nick_name and surname (if existing)

Clean up relation: duplicates in some cases for spouses and children lists
1. run python script_cleanup_duplicate_spouses.py
saved data set: Relation-2024-08-05_1_spouses_cleaned_up
2. run python script_cleanup_duplicate_children.py
saved data set: Relation-2024-08-05_2_children_cleaned_up


Backup:
    exclude = ('fath_name', 'fath_refn', 'moth_name', 'moth_refn',
                'uid', 'marr_spou_name_1', 'marr_spou_refn_1', 'fam_husb_1',
                'fam_wife_1', 'marr_date_1', 'marr_plac_1', 'fam_chil_1',
                'fam_marr_1', 'fam_stat_1',
                'marr_spou_name_2', 'marr_spou_refn_2', 'fam_husb_2', 'fam_wife_2', 'marr_date_2',
                'marr_plac_2', 'fam_chil_2', 'fam_marr_2', 'fam_stat_2',
                'marr_spou_name_3', 'marr_spou_refn_3', 'fam_husb_3', 'fam_wife_3', 'marr_date_3',
                'marr_plac_3', 'fam_chil_3', 'fam_marr_3', 'fam_stat_3',
                'marr_spou_name_4', 'marr_spou_refn_4', 'fam_husb_4', 'fam_wife_4', 'marr_date_4',
                'marr_plac_4', 'fam_chil_4', 'fam_marr_4', 'fam_stat_4', 'chan_date', 'chan_date_time' )

Created discussions
db_backup.sqlite3 created

WITH REGARD TO ACCOUNTS/USERS
username ist mandatory due to DRF admin basis, but will be automatically generated if the user is created in the frontend.
if the user is created in the backend, choose a username that is not yet existent
all interaction with frontend users is in the frontend (activation infos, reset passwort etc.)
added two family possibilities for user to be assigned to - regard the frontend later on
