import os
import subprocess
import sys
from rpft.converters import create_flows
from rapidpro_abtesting.main import apply_abtests

def run_pipeline(
        sources, 
        model, 
        languages, 
        translation_repo, 
        outputpath, 
        select_phrases, 
        add_selectors,
        special_words, 
        ab_testing_sheet_ID = None, 
        dict_edits_sheet_ID = None, 
        SG_sheet_ID = None, 
        SG_flow_name = None,
        SG_path = None
        ):

    #####################################################################
    # Step 0: Fetch available PO files and convert to JSON
    #####################################################################

    for lang in languages:

        lang_name = lang["language"]
        lang_code = lang["code"]

        #Setup file to store the translations we retrieve from the translation repo
        translations_store_folder = os.path.join(outputpath, lang_name + "_translations")
        if not os.path.exists(translations_store_folder):
            os.makedirs(translations_store_folder)

        #Fetch all relevant translation files
        translations_fetch_folder = os.path.join(translation_repo, lang_code)
        for root, dirs, files in os.walk(translations_fetch_folder):
            for file in files:
                file_name, file_extension = os.path.splitext(file)
                if file_extension == ".po":
                    source_file_path = os.path.join(root, file)
                    dest_file_path = os.path.join(translations_store_folder, file_name + ".json")
                    subprocess.run(["node", "./node_modules/@idems/idems_translation_common/index.js", "convert", source_file_path, dest_file_path])

        #Merge all translation files into a single JSON that we can localise back into our flows
        subprocess.run(["node", "./node_modules/@idems/idems_translation_common/index.js", "concatenate_json", translations_store_folder, translations_store_folder, "merged_translations.json"])

    print("Step 0 complete, fetched all available translations and converted to json")

    for source in sources:

        #Load core file information

        source_file_name = source["filename"]
        spreadsheet_id  = source["spreadsheet_id"]
        crowdin_file_name = source["crowdin_name"]
        split_num = source["split_no"]

        #Setup output and temp files to store intermediary JSON files and log files
        if not os.path.exists(outputpath):
            os.makedirs(outputpath)

        #####################################################################
        #Step 1: Load google sheets and convert to RapidPro JSON
        #####################################################################

        output_file_name_1 = source_file_name + "_1"
        output_path_1 = os.path.join(outputpath, output_file_name_1 + ".json")

        create_flows([spreadsheet_id], output_path_1, "google_sheets", model)
        
        print("Step 1 complete, created " + output_file_name_1)

        #####################################################################
        # Step 2: Flow edits (for all deployments) and localization (changes specific to a deployment)
        #####################################################################

        input_path_2 = output_path_1

        if(ab_testing_sheet_ID):            
            output_file_name_2 = source_file_name + "_2"
            output_path_2 = os.path.join(outputpath, output_file_name_2 + ".json")

            apply_abtests(input_path_2, output_path_2, [ab_testing_sheet_ID], "google_sheets")
            print("Step 2 complete, added A/B tests and localization")
        else:
            output_path_2 = output_path_1
            print("Step 2 skipped, no AB testing sheet ID provided")        
 
        # Fix issues with _ui ?????not working?????
        # subprocess.run(["node", "./node_modules/@idems/idems-chatbot-tools/fix_ui.js", output_path_2, output_path_2])
        # print("Fixed _ui")

        ####################################################################
        # Step 3: Catch errors pre-translation
        ####################################################################

        input_path_3_1 = output_path_2
        output_file_name_3_1 = source_file_name + "_3_1"
        has_any_words_log = "3_has_any_words_check"

        subprocess.run(["node", "./node_modules/@idems/idems_translation_chatbot/index.js", "has_any_words_check", input_path_3_1, outputpath, output_file_name_3_1, has_any_words_log])

        input_path_3_2 = os.path.join(outputpath, output_file_name_3_1 + ".json")
        integrity_log = "3_integrity_log"
        excel_log_name = os.path.join(outputpath, "3_excel_log.xlsx")
        
        subprocess.run(["node", "./node_modules/@idems/idems_translation_chatbot/index.js", "overall_integrity_check", input_path_3_2, outputpath, integrity_log, excel_log_name])

        print("Step 3 complete, reviewed files pre-translation")

        #####################################################################
        # Step 4: Extract Text to send to translators
        #####################################################################

        input_path_4 = os.path.join(outputpath, output_file_name_3_1 + ".json")
        output_file_name_4 = crowdin_file_name
        output_path_4 = os.path.join(outputpath, "send_to_translators")

        #Setup output file to send to translators if it doesn't exist
        if not os.path.exists(output_path_4):
            os.makedirs(output_path_4)

        subprocess.run(["node", "./node_modules/@idems/idems_translation_chatbot/index.js", "extract_simple", input_path_4, output_path_4, output_file_name_4])

        print("Step 4 complete, extracted text for translation")

        #####################################################################
        # Step 5: Localise translations back into JSON files
        #####################################################################
        
        input_path_5 = os.path.join(outputpath, source_file_name + "_3_1.json")
        output_file_name_5 = source_file_name + "_5"

        for lang in languages:

            language = lang["language"]

            json_translation_path = os.path.join(outputpath, language + "_translations", "merged_translations.json")

            subprocess.run(["node", "./node_modules/@idems/idems_translation_chatbot/index.js", "localize", input_path_5, json_translation_path, language, output_file_name_5, outputpath])

        print("Step 5 complete, localised translations back into JSON")

        #####################################################################
        # step 6: text & translation edits for dictionaries
        #####################################################################

        input_path_6 = os.path.join(outputpath, output_file_name_5 + ".json")

        if(dict_edits_sheet_ID):            
            output_file_name_6 = source_file_name + "_6"
            output_path_6 = os.path.join(outputpath, output_file_name_6 + ".json")

            apply_abtests(input_path_2, output_path_2, [dict_edits_sheet_ID], "google_sheets")
            print("Step 6 complete, text & translation edits made for dictionaries")
        else:
            output_path_6 = input_path_6
            print("Step 6 skipped, no dict edits sheet ID provided") 

        #####################################################################
        # step 7: catch errors post translation 
        #####################################################################

        input_path_7_1 = output_path_6
        output_file_name_7_1 = source_file_name + "_7_1"
        has_any_words_log = "7_has_any_words_check"

        subprocess.run(["node", "./node_modules/@idems/idems_translation_chatbot/index.js", "has_any_words_check", input_path_7_1, outputpath, output_file_name_7_1,  has_any_words_log])

        input_path_7_2 = os.path.join(outputpath, output_file_name_7_1 + ".json")
        output_file_name_7_2 = source_file_name + "_7_2"
        fix_arg_qr_log = "7_arg_qr_log"
        
        subprocess.run(["node", "./node_modules/@idems/idems_translation_chatbot/index.js", "fix_arg_qr_translation", input_path_7_2, outputpath, output_file_name_7_2, fix_arg_qr_log])

        input_path_7_3 = os.path.join(outputpath, output_file_name_7_2 + ".json")
        integrity_log = "7_integrity_log"
        excel_log_name = os.path.join(outputpath,"8_excel_log.xlsx")
        
        subprocess.run(["node", "./node_modules/@idems/idems_translation_chatbot/index.js", "overall_integrity_check", input_path_7_3, "./output", integrity_log, excel_log_name])

        print("Step 7 complete, reviewed files post translation")

        #####################################################################
        # step 8: add quick replies to message text and translation
        #####################################################################

        input_path_8 = os.path.join(outputpath, output_file_name_7_2 + ".json")
        output_file_name_8 = source_file_name + "_8"

        #changes to be made here aroud length of strings.

        subprocess.run(["node", "./node_modules/@idems/idems_translation_chatbot/index.js", "move_quick_replies", input_path_8, select_phrases, output_file_name_8, outputpath, add_selectors, special_words])
        
        print("Step 8 complete, removed quick replies")

        #####################################################################
        # step 9: implement safeguarding
        #####################################################################
               
        input_path_9 = os.path.join(outputpath, output_file_name_8 + ".json")

        if(SG_path and SG_flow_name and SG_sheet_ID):
            output_file_name_9 = source_file_name + "_9"
            output_path_9 = os.path.join(outputpath, output_file_name_9)
            subprocess.run(["node", "./node_modules/@idems/safeguarding-rapidpro/srh_add_safeguarding_to_flows.js", input_path_9, SG_path, output_path_9, SG_sheet_ID, SG_flow_name])
            print("Added safeguarding")

            if "srh_safeguarding" in source_file_name:
                subprocess.run(["node", "./node_modules/@idems/safeguarding-rapidpro/srh_edit_redirect_flow.js", output_path_9, SG_path, output_path_9])
                print("Edited redirect sg flow")

            print("Step 9 complete, adding safeguarding flows")

        else:
            output_path_9 = input_path_9
            print("Step 9 skipped, no sareguarding details provided")

        #####################################################################
        # step 10. split files (if too big)?
        #####################################################################

        if(split_num>1):
            input_path_10 = output_path_9
            subprocess.run(["node", "./node_modules/@idems/idems-chatbot-tools/split_in_multiple_json_files.js", input_path_10, str(split_num)])

            print(f"Step 10 complete, split file in {split_num}")

        else:
            print("Step 10 skipped as file not specified to be split")


def process_safeguarding_words(input_file, output_path, output_name):

    #####################################################################
    #Fetch translated safeguarding words and turn into JSON
    #####################################################################

    #"./extract_keywords.py" has the rough script required to run this process, need to adapt as necessary

    print("Safeguarding word processing complete")