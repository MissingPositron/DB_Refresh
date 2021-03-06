import pymongo
import os, re
import datetime

myclient = pymongo.MongoClient("mongodb://localhost:27017")
# database
mydb = myclient['tb_list_test']
# collection
mycol = mydb['lists']

# base_url = r'C:\Users\shopfloor\Documents\test'
base_url = r'\\pops\Shared\Production Test Programs\TE_Checklist\BiCs4_512G_X3\Advantest_Common_Code\Checked_Out_Evidence_For_Each_Test_Item'

# some basic data
products = []

# function to remove unwanted item from list
def removeFromList(List, item):
	if item in List:
		List.remove(item)

# get all the folders with full path
for tb_folder in os.listdir(base_url):
	lv1_full_path = os.path.join(base_url, tb_folder)
	if os.path.isdir(lv1_full_path) and 'tb' in lv1_full_path:
		tb_name = tb_folder 
		
		# get all the package and die info for this tb
		for pack_folder in os.listdir(lv1_full_path):
			lv2_full_path = os.path.join(lv1_full_path, pack_folder) 
				
			if os.path.isdir(lv2_full_path):
				contents = os.listdir(lv2_full_path)
				# jump empty folders
				if len(contents) == 0:
					continue

				# get die infor
				pack_info = pack_folder.split('_')
				die_stack = ''.join([item for item in pack_info if re.match(r'^[\d]*D', item)])
				
				# clear the pack_info
				clear_list = ['T5773', '5773', 't5773', 'T5831', '5831' , 't5831', '512G', '256G']
				for i in clear_list:
					removeFromList(pack_info, i)				
				removeFromList(pack_info, die_stack) 
				package = '_'.join(pack_info)
				
				# platform 
				t5773_file = [item for item in contents if '5773' in os.path.join(lv2_full_path, item)]
				t5831_file = [item for item in contents if '5831' in os.path.join(lv2_full_path, item)]
				t5773 = len(t5773_file) > 0
				t5831 = len(t5831_file) > 0

				# # Year - Month - Day
				date = datetime.date.today().strftime("%Y-%m-%d")

				new_item = { \
					'tb_name': tb_name, \
					'package': package, \
					'die_stack': die_stack, \
					'T5773_available': t5773, \
					'T5831_available': t5831, \
					'description': ', '.join(contents) \
				}
				
				# insert new item
				if (mycol.find_one(new_item) is None):
					new_item['date'] = date
					insert_status = mycol.insert_one(new_item)
					print(insert_status)
				