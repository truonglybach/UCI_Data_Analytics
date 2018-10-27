
# coding: utf-8

# In[149]:


# Import modules
import os
import csv


# In[150]:


# Create necessary variables
budget_data = os.path.join("..", "PyBank", "budget_data.csv")
output_path = os.path.join("..", "PyBank", "PyBank.txt")
months = 0
net_rev = 0


# In[151]:


# Create an empty list to store revenue per month
rev_per_month = []
list_of_dates = []


# In[152]:


# Open the file and read through it; skip over the header and begin to += 1
# for each month and net rev; as well as, appending each rev_per_month to its relevant list
with open(budget_data, newline='') as budget_ds:
    csvreader = csv.reader(budget_ds, delimiter=",")
    csv_header = next(budget_ds)
    for row in csvreader:
        months = months + 1
        net_rev = net_rev + int(row[1])
        rev_per_month.append(int(row[1]))
        list_of_dates.append(str(row[0]))


# In[153]:


# Find the difference btwn each item on my rev_per_month list
# Divide the sum of the differences by the number of total months
diff_btwn = [rev_per_month[i+1]-rev_per_month[i] for i in range(len(rev_per_month)-1)]
numerator = sum(diff_btwn)
avg_diff = numerator/months
# Round to two points, cause it's currency
r_avg_diff = round(avg_diff, 2)


# In[154]:


# Find max and min values in diff_btwn list;
# that being, the greatest inc/dec in profits
g_inc_profits = max(diff_btwn)
g_dec_profits = min(diff_btwn)

# In[155]:


# Refer to the diff_btwn list and retrieve its index;
# add to its value by 1 and search for the missing dates accordingly;
for value in diff_btwn:
    if (value == g_inc_profits):
        db_index_inc = diff_btwn.index(g_inc_profits)
    elif (value == g_dec_profits):
        db_index_dec = diff_btwn.index(g_dec_profits)
# Plus one because of finding diff in btwn rev
index_inc_rpm = db_index_inc + 1
index_dec_rpm = db_index_dec + 1


# In[156]:


# Read through list of dates and find appropriate date for rev
date_g_inc = list_of_dates[index_inc_rpm]
date_g_dec = list_of_dates[index_dec_rpm]


# In[157]:


# Print to terminal
print("Financial Analysis")
print("------------------------------------------------")
print("Total Months: " + str(months))
print("Net Revenue: " + "$" + str(net_rev))
print("Average Change: " + "$" + str(r_avg_diff))
print("Greatest Increase in Profits: " + str(date_g_inc) + " ($" + str(g_inc_profits) + ")")
print("Greatest Decrease in Profits: " + str(date_g_dec) + " ($" + str(g_dec_profits) + ")")


# In[169]:


# Export as text file
# Open the file using "write" mode. Specify the variable to hold the contents
with open(output_path, 'w', newline='') as text_file:
    text_file.write("Financial Analysis\n"
                   "------------------------------------------------\n"
                   "Total Months: " + str(months) + "\n"
                   "Net Revenue: " + "$" + str(net_rev) + "\n"
                   "Average Change: " + "$" + str(r_avg_diff) + "\n"
                   "Greatest Increase in Profits: " + str(date_g_inc) + " ($" + str(g_inc_profits) + ")\n"
                   "Greatest Decrease in Profits: " + str(date_g_dec) + " ($" + str(g_dec_profits) + ")\n")

