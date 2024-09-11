#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import dependencies
import pandas as pd
import numpy as np
pd.set_option('max_colwidth', 400)


# ### Extract the crowdfunding.xlsx Data

# In[4]:


# Read the data into a Pandas DataFrame
crowdfunding_info_df = pd.read_excel('./Resources/crowdfunding.xlsx')
crowdfunding_info_df.head()


# In[6]:


# Get a brief summary of the crowdfunding_info DataFrame.
crowdfunding_info_df.info()


# ### Create the Category and Subcategory DataFrames
# ---
# **Create a Category DataFrame that has the following columns:**
# - A "category_id" column that is numbered sequential form 1 to the length of the number of unique categories.
# - A "category" column that has only the categories.
# 
# Export the DataFrame as a `category.csv` CSV file.
# 
# **Create a SubCategory DataFrame that has the following columns:**
# - A "subcategory_id" column that is numbered sequential form 1 to the length of the number of unique subcategories.
# - A "subcategory" column that has only the subcategories. 
# 
# Export the DataFrame as a `subcategory.csv` CSV file.

# In[9]:


# Get the crowdfunding_info_df columns.
crowdfunding_info_df.columns


# In[11]:


# Assign the category and subcategory values to category and subcategory columns.
crowdfunding_info_df[['category','subcategory']] = crowdfunding_info_df['category & sub-category'].str.split('/',n=1,expand=True)
                                                                                     
crowdfunding_info_df


# In[13]:


# Get the unique categories and subcategories in separate lists.
categories = crowdfunding_info_df['category'].unique()
subcategories = crowdfunding_info_df['subcategory'].unique()

print(categories)
print(subcategories)


# In[15]:


# Get the number of distinct values in the categories and subcategories lists.
print(len(categories))
print(len(subcategories))


# In[17]:


# Create numpy arrays from 1-9 for the categories and 1-24 for the subcategories.
category_ids = np.arange(1, 10)
subcategory_ids = np.arange(1, 25)

print(category_ids)
print(subcategory_ids)


# In[19]:


# Use a list comprehension to add "cat" to each category_id. 
cat_ids = [f" cat{cat_id}" for cat_id in category_ids] 
# Use a list comprehension to add "subcat" to each subcategory_id.    
scat_ids = [f" subcat{scat_id}" for scat_id in subcategory_ids]
    
print(cat_ids)
print(scat_ids)


# In[21]:


# Create a category DataFrame with the category_id array as the category_id and categories list as the category name.
category_df = pd.DataFrame({
    'category_id' : cat_ids,
    'category' : categories    
})

# Create a category DataFrame with the subcategory_id array as the subcategory_id and subcategories list as the subcategory name.
subcategory_df = pd.DataFrame({
    'subcategory_id': scat_ids,
    'subcategory' : subcategories
})


# In[23]:


category_df


# In[25]:


subcategory_df


# In[27]:


# Export categories_df and subcategories_df as CSV files.
category_df.to_csv("./Resources/category.csv", index=False)

subcategory_df.to_csv("./Resources/subcategory.csv", index=False)


# ### Campaign DataFrame
# ----
# **Create a Campaign DataFrame that has the following columns:**
# - The "cf_id" column.
# - The "contact_id" column.
# - The “company_name” column.
# - The "blurb" column is renamed as "description."
# - The "goal" column.
# - The "goal" column is converted to a `float` datatype.
# - The "pledged" column is converted to a `float` datatype. 
# - The "backers_count" column. 
# - The "country" column.
# - The "currency" column.
# - The "launched_at" column is renamed as "launch_date" and converted to a datetime format. 
# - The "deadline" column is renamed as "end_date" and converted to a datetime format.
# - The "category_id" with the unique number matching the “category_id” from the category DataFrame. 
# - The "subcategory_id" with the unique number matching the “subcategory_id” from the subcategory DataFrame.
# - And, create a column that contains the unique four-digit contact ID number from the `contact.xlsx` file.
#  
# 
# Then export the DataFrame as a `campaign.csv` CSV file.
# 

# In[30]:


# Create a copy of the crowdfunding_info_df DataFrame name campaign_df. 
campaign_df = crowdfunding_info_df.copy()
campaign_df.head()


# In[32]:


# Rename the blurb, launched_at, and deadline columns.
campaign_df = campaign_df.rename(columns={'blurb' : 'description','launched_at':'launched_date',
                            'deadline':'end_date'})
campaign_df


# In[34]:


# Convert the goal and pledged columns to a `float` data type.
campaign_df[['goal','pledged']] = campaign_df[['goal','pledged']].astype(float)
campaign_df


# In[36]:


# Check the datatypes
campaign_df.dtypes


# In[38]:


# Format the launched_date and end_date columns to datetime format
from datetime import datetime as dt
campaign_df['launched_date'] = pd.to_datetime(campaign_df['launched_date']).dt.strftime('%Y-%m-%d')
campaign_df['end_date'] = pd.to_datetime(campaign_df['end_date']).dt.strftime('%Y-%m-%d')
campaign_df


# In[40]:


# Merge the campaign_df with the category_df on the "category" column and 
# the subcategory_df on the "subcategory" column.
campaign_merged_df = campaign_df.merge(category_df, on= 'category',how = 'left').merge(subcategory_df, on='subcategory',how = 'left')
 
campaign_merged_df.tail(10)


# In[42]:


# Drop unwanted columns
campaign_cleaned = campaign_merged_df.drop(['staff_pick','spotlight','category & sub-category','category','subcategory'],axis=1)
campaign_cleaned


# In[44]:


# Export the DataFrame as a CSV file. 
campaign_cleaned.to_csv("./Resources/campaign.csv", index=False)


# ### Extract the contacts.xlsx Data.

# In[47]:


# Read the data into a Pandas DataFrame. Use the `header=2` parameter when reading in the data.
contact_info_df = pd.read_excel('./Resources/contacts.xlsx', header=3)
contact_info_df.head()


# ### Create the Contacts DataFrame 
# ---
# **Create a Contacts DataFrame that has the following columns:**
# - A column named "contact_id"  that contains the unique number of the contact person.
# - A column named "first_name" that contains the first name of the contact person.
# - A column named "last_name" that contains the first name of the contact person.
# - A column named "email" that contains the email address of the contact person
# 
# Then export the DataFrame as a `contacts.csv` CSV file.

# ### Option 1: Use Pandas to create the contacts DataFrame.

# In[51]:


print(contact_info_df.columns)


# In[53]:


# Iterate through the contact_info_df and convert each row to a dictionary.
import json
dict_values = []

for i, row in contact_info_df.iterrows():
    #print(i)
    data = row['contact_info']
    converted_data = json.loads(data)
    row_values = [value for key, value in converted_data.items()]
    dict_values.append(row_values)
# Print out the list of values for each row.
print(dict_values)


# In[55]:


# Create a contact_info DataFrame and add each list of values, i.e., each row 
# to the 'contact_id', 'name', 'email' columns.
contact_df = pd.DataFrame(dict_values, columns=['contact_id','name','email'])
contact_df


# In[57]:


# Check the datatypes.
contact_df.info()


# In[59]:


# Create a "first"name" and "last_name" column with the first and last names from the "name" column. 
contact_df[['first_name','last_name']] = contact_df['name'].str.split(' ',n=1,expand=True)

# Drop the contact_name column
contact_df_clean = contact_df.drop(['name'],axis=1)
contact_df_clean


# In[61]:


# Reorder the columns
contact_df_clean = contact_df_clean[['contact_id','first_name','last_name','email']]
contact_df_clean


# In[63]:


# Check the datatypes one more time before exporting as CSV file.
contact_df_clean.info()


# In[65]:


# Export the DataFrame as a CSV file. 
contact_df_clean.to_csv("./Resources/contacts.csv", encoding='utf8', index=False)


# ### Option 2: Use regex to create the contacts DataFrame.

# In[68]:


contact_info_df_copy = contact_info_df.copy()
contact_info_df_copy.head()


# In[70]:


# Extract the four-digit contact ID number.
contact_info_df_copy['contact_id'] = contact_info_df_copy['contact_info'].str.extract(r'(\d{4})')
contact_info_df_copy


# In[72]:


# Check the datatypes.
contact_info_df_copy.dtypes


# In[74]:


# Convert the "contact_id" column to an int64 data type.
contact_info_df_copy['contact_id'] = pd.to_numeric(contact_info_df_copy['contact_id'])
contact_info_df_copy.info()


# In[76]:


# Extract the name of the contact and add it to a new column.
contact_info_df_copy['name'] = contact_info_df_copy['contact_info'].str.extract(r'([^nameil"\s][A-Za-z]+\s[A-Za-z]+)')
contact_info_df_copy


# In[78]:


# Extract the email from the contacts and add the values to a new column.
contact_info_df_copy['email'] = contact_info_df_copy['contact_info'].str.extract(r'"(\S+@\S+)"}')
contact_info_df_copy


# In[80]:


# Create a copy of the contact_info_df with the 'contact_id', 'name', 'email' columns.
contact_info_df_copy2 = contact_info_df_copy[['contact_id','name','email']].copy()
contact_info_df_copy2


# In[82]:


# Create a "first"name" and "last_name" column with the first and last names from the "name" column. 
contact_info_df_copy2[['first_name','last_name']] = contact_info_df_copy2['name'].str.split(' ',n=1,expand = True)
contact_info_df_copy2
# Drop the contact_name column
contact_df_clean2 = contact_info_df_copy2.drop(['name'],axis=1)
contact_df_clean2


# In[84]:


# Reorder the columns
contact_df_clean2 = contact_info_df_copy2[['contact_id','first_name','last_name','email']]


# In[86]:


# Check the datatypes one more time before exporting as CSV file.
contact_df_clean2.info()


# In[88]:


# Export the DataFrame as a CSV file. 
# contacts_df_clean.to_csv("Resources/contacts.csv", encoding='utf8', index=False)


# ## EXTRACT TRANSFORM AND LOAD using sqlalchemy

# In[91]:


get_ipython().system('pip install psycopg2')


# In[95]:


pip install --upgrade sqlalchemy


# In[133]:


import psycopg2
import pandas as pd
from sqlalchemy import create_engine
# username = 'postgres'
# password = 'postgres'
# hostname = 'localhost'
# port = '5432'
# db = 'etl'


# In[135]:


engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/etl')


# In[137]:


pd.read_sql('select * from campaign', engine)


# In[103]:


campaign_df = pd.read_csv('./Resources/campaign.csv')


# In[105]:


campaign_df.to_sql( 'campaign', con=engine, if_exists = 'replace' )


# In[107]:


category_df = pd.read_csv('./Resources/category.csv')


# In[111]:


category_df


# In[109]:


category_df.to_sql('category', con=engine, if_exists = 'replace')


# In[113]:


pd.read_sql('select * from category', engine)


# In[115]:


subcategory_df = pd.read_csv('./Resources/subcategory.csv')


# In[117]:


subcategory_df


# In[121]:


subcategory_df.to_sql('subcategory', con=engine, if_exists = 'replace')


# In[123]:


pd.read_sql('select * from subcategory', engine)


# In[125]:


contacts_df = pd.read_csv('./Resources/contacts.csv')


# In[127]:


contacts_df


# In[129]:


contacts_df.to_sql('contacts', con=engine , if_exists = 'replace')


# In[131]:


pd.read_sql('select * from contacts', engine)


# In[ ]:




