import os

# base_url = r'C:\Users\shopfloor\Documents\test'
base_url = r'\\pops\Shared\Production Test Programs\TE_Checklist\BiCs4_512G_X3\Advantest_Common_Code\Checked_Out_Evidence_For_Each_Test_Item'
for tb_folder in os.listdir(base_url):
    print(tb_folder)