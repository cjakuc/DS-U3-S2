import os
import sqlite3
import pandas as pd

# Save the filepath for the DB to a variable
DB_FILEPATH = os.path.join(os.path.dirname(__file__), "rpg_db.sqlite3")

# Intanstiate the connection
connection = sqlite3.connect(DB_FILEPATH)
# print("CONNECTION:", connection)

# Instantiate the cursor
cursor = connection.cursor()
# print("CURSOR:", cursor)

# Question 1: How many total characters are there?
query = """
SELECT
	count(distinct character_id) as character_count
FROM
	charactercreator_character
"""

result = cursor.execute(query).fetchone()
print("How many total characters are there?", result[0])

# Question 2: How many of each specific subclass?
charachter_types_items = ['charactercreator_mage',
                    'charactercreator_thief',
                    'charactercreator_cleric',
                    'charactercreator_fighter']
subclasses = ['mage','thief','cleric','fighter']

print("How many of each specific subclass?")
i = 0
for items in charachter_types_items:
    subclass_query = f"""
    SELECT
        count(distinct character_ptr_id) as subclass_count
    FROM
        {items}
     """
    subclass_result = cursor.execute(subclass_query).fetchone()
    print(f"There are {subclass_result[0]} charcters of subclass {subclasses[i]}")
    i += 1

# Question 3: How many total items
item_query = """
SELECT
	count(distinct item_id) as item_count
FROM
	armory_item
"""

item_result = cursor.execute(item_query).fetchone()
print("How many total items are there?", item_result[0])

# Question 4: How many of the items are weapons? How many are not?
weapon_query = """
SELECT
	count(distinct item_ptr_id) as weapon_count
FROM
	armory_weapon
"""

weapon_result = cursor.execute(weapon_query).fetchone()
print(f"In all the items, there are {weapon_result[0]} weapons and {item_result[0]-weapon_result[0]} non-weapons")

# Question 5: How many items does each character have?
print("How many items does each character have? (First 20 Rows")

char_item_query = """
SELECT
	character_id
	,count(distinct item_id) as item_count
FROM
	charactercreator_character_inventory
GROUP BY 
	character_id
LIMIT 20
"""

char_item_result = cursor.execute(char_item_query).fetchall()
char_item_df = pd.DataFrame(char_item_result, columns = ['Character_ID','Item_Count'])
char_item_df = char_item_df.set_index('Character_ID')

print(char_item_df)

# Question 6: How many weapons does each character have? (First 20 rows)
# print("How many weapons does each character have? (First 20 rows)")

# char_weapon_query = """
# SELECT
# 	ch.character_id
# 	,count(distinct ch.item_id) as item_count
# 	,count(distinct armory_weapon.item_ptr_id) as weapon_count
# FROM
# 	charactercreator_character_inventory as ch
# GROUP BY 
# 	ch.character_id
# LEFT JOIN armory_item ON armory_item.item_id = ch.item_id
# LEFT JOIN armory_weapon ON armory_item.item_id = armory_weapon.item_ptr_id
# LIMIT 20
# """

# Question 7: On average, how many items does each character have?
print("On average, how many items does each character have?")

ch_avg_items_query = """
SELECT
	character_id
	,count(distinct item_id) as item_count
FROM
	charactercreator_character_inventory
GROUP BY 
	character_id
"""

avg_char_item_result = cursor.execute(ch_avg_items_query).fetchall()
avg_char_item_df = pd.DataFrame(avg_char_item_result, columns = ['Character_ID','Item_Count'])
avg_char_item_df = avg_char_item_df.set_index('Character_ID')
avg_char_item = avg_char_item_df['Item_Count'].mean()

print(f"The average item count is {avg_char_item:,.2f}")

# Question 8: On average, how many weapons does each chararacter have
# print("On average, how many weapons does each character have?")