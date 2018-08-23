
# coding: utf-8

# In[101]:


# Import modules
import os
import csv


# In[102]:


# Set up variables
total_votes = 0
polling_info = os.path.join("..", "PyPoll", "election_data.csv")
output_path = os.path.join("..", "PyPoll", "PyPoll.txt")
list_all_names = []
unique_names = []
correy_count = 0
khan_count = 0
li_count = 0
o_tooley_count = 0


# In[103]:


# Open csv; read it;
with open(polling_info, newline="") as poll_info:
    csvreader = csv.reader(poll_info, delimiter=",")
    csvheader = next(poll_info)
    for row in csvreader:
        total_votes += 1
        list_all_names.append(str(row[2]))
        if row[2] == "Correy":
            correy_count += 1
        elif row[2] == "Khan":
            khan_count += 1
        elif row[2] == "Li":
            li_count += 1
        elif row[2] == "O'Tooley":
            o_tooley_count += 1


# In[104]:


pov_correy = round(correy_count / total_votes * 100, 3)
pov_khan = round(khan_count / total_votes * 100, 3)
pov_li = round(li_count / total_votes * 100, 3)
pov_o_tooley = round(o_tooley_count / total_votes * 100, 3)


# In[105]:


# Run through list_all_names and create if stmt to print unique names into separate list
def unique(list):
	for x in list_all_names:
		if x not in unique_names:
			unique_names.append(x)

unique(list_all_names)
# In[106]:


# Make a list of the values and find the max to determine the winner
candidates_pov_list = [pov_khan, pov_correy, pov_li, pov_o_tooley]
winner_pov = max(candidates_pov_list)
candidates = ["Khan", "Correy", "Li", "O'Tooley"]
winner_index = candidates_pov_list.index(winner_pov)


# In[107]:


# Print election results to terminal
print("Election Results")
print("-------------------------")
print("Total votes: " + str(total_votes))
print("-------------------------")
print("Correy: " + str(pov_correy) + "% (" + str(correy_count) + ")")
print("Khan: " + str(pov_khan)+ "% (" + str(khan_count) + ")")
print("Li: " + str(pov_li)+ "% (" + str(li_count) + ")")
print("O'Tooley: " + str(pov_o_tooley)+ "% (" + str(o_tooley_count) + ")")
print("-------------------------")
print("Winner: " + str(candidates[winner_index]))
print("-------------------------")


# In[108]:


# Export as text file
# Open the file using "write" mode. Specify the variable to hold the contents
with open(output_path, 'w', newline='') as text_file:
    text_file.write("Election Results\n"
                    "------------------------------------------------\n"
                    "Total votes: " + str(total_votes) + "\n"
                    "------------------------------------------------\n"
                    "Correy: " + str(pov_correy) + "% (" + str(correy_count) + ")\n"
                    "Khan: " + str(pov_khan)+ "% (" + str(khan_count) + ")\n"
                    "Li: " + str(pov_li)+ "% (" + str(li_count) + ")\n"
                    "O'Tooley: " + str(pov_o_tooley)+ "% (" + str(o_tooley_count) + ")\n"
                    "------------------------------------------------\n"
                    "Winner: " + str(candidates[winner_index]) + "\n"
                    "------------------------------------------------\n")

