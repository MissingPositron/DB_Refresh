import pymongo
import os, re
import datetime
import time

myclient = pymongo.MongoClient("mongodb://localhost:27017")
# database
mydb = myclient['MT_checkout_list']
# collection
mycol = mydb['lists']

# base_url = r'C:\Users\shopfloor\Documents\test'
base_url = r'\\pops\Shared\Production Test Programs\TE_Checklist'
save_file = open('test.json', "w")

# Technology set
tech_set = ['BiCs3_128G_X3', 'BiCs3_256G_X3', 'BiCs3_512G_X3', 'BiCs4_1.33T_X4', 'BiCs4_256G_X3', 'BiCs4_512G_X3']

# function to remove unwanted item from list
def removeFromList(List, item):
	if item in List:
		List.remove(item)

# main function
if __name__ == '__main__':

	print('Start process...')
	start_time = time.time()

	for root, folders, files in os.walk(base_url):
			for folder in folders:
				if 'tb' in folder:
					lv1_full_path = os.path.join(root, folder)
					
					for tech in tech_set:
						if tech in lv1_full_path:
							technology = tech
							break  
						else:
						 	technology = 'Unknown'
					
					MtStage = 'MT2' if 'MT2' in lv1_full_path else 'MT1'

					tb_name = folder

					# get all the package and die info for this tb
					for pack_folder in os.listdir(lv1_full_path):
						lv2_full_path = os.path.join(lv1_full_path, pack_folder) 

						if os.path.isdir(lv2_full_path):
							print(lv2_full_path)
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
							folder_info = os.stat(lv2_full_path)
							date = time.asctime(time.localtime(folder_info.st_mtime))

							# description for the file lists
							file_list = ', '.join(contents)
							des = '\\'.join([lv2_full_path, file_list])

							# Operation with MongoDB
							# for new folder insert new item
							if (mycol.find_one({'tb_name': tb_name, 'package': package, 'die_stack': die_stack}) is None):
								new_item = { \
								'tech' : technology, \
								'MT_stage': MtStage, \
								'tb_name': tb_name, \
								'package': package, \
								'die_stack': die_stack, \
								'T5773_available': t5773, \
								'T5831_available': t5831, \
								'description': des, \
								'date': date
								}
								insert_status = mycol.insert_one(new_item)
								print(insert_status)

							# for old folder, if new file found, update the information
							elif (mycol.find_one({ \
								'tech' : technology, \
								'MT_stage': MtStage, \
								'tb_name': tb_name, \
								'package': package, \
								'die_stack': die_stack, \
								'T5773_available': t5773, \
								'T5831_available': t5831, \
								'description': des}) is None):

								try:
									old_item = mycol.find_one({'tech' : technology, 'MT_stage': MtStage, 'tb_name': tb_name, 'package': package, 'die_stack': die_stack})
									update_values = { "$set" : {"T5773_available": t5773, 'T5831_available': t5831, 'description': des, 'date':date}}
									update_status = mycol.update_one(old_item, update_values, upsert=False)
									print(update_status)
								except:
									print(lv2_full_path + " update database fail")



	print('Complete!')
	print("--- %s seconds ---" % (time.time() - start_time))