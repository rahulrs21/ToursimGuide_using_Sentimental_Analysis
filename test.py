# import pandas as pd
#
# df = pd.read_csv("b1.csv", usecols=['Rating', 'Place', 'Sub_Place', 'Review'],dtype={'Rating': 'int32', 'Place': 'str', 'Sub_Place': 'str', 'Review': 'str'})
#
#
#
# rating = df["Rating"]
# place_type = df["Place"]
# place_name = df["Sub_Place"]
# review = df["Review"]
#
# lis1 = [rating, place_type, place_name, review]
#
# review_sec =  []
# review_rev = []
#
# count=-1
#
# ex=[]
#
# for i in review:
#     review_rev.append(i)
#
# for i in rating:
#     review_sec.append(i)
#
#
# for i in place_name:
#        count = count+1
#        if(i == "Mangalore"):
#            ex.append(count)
#
# final_lis = []
# k_count = 0
# for k in ex:
#      answer = str(review_sec[ex[k_count]]) +" "+ str(review_rev[ex[k_count]])
#      k_count=k_count+1
#      print(answer)
#      final_lis.append(answer)
#





# st = "sfgdfs"
#
# user = 'sfgdfs'
# if(user == 'sfgdfs'):
#     print("true")



# name= "raup"
# v=name.capitalize()
# print(v)

data=[['aafa', 'dgdgd'], ['195errd7', 'fdgd'], ['dfd', 'sssds'], ['dgfdf', 'dfdfssr'], ['gfg', 'fhfgg'], ['sfg', 'jhg']]

year=[]
contenst=[]

# for i in data:
#     year.append(str(i[0]))
#     contenst.append(str(i[1]))
#
# print(year)
# print(contenst)
#
# list1 =['1 : This is most wonderful place that I spent a great time with my family', '4 : Nice ', '3 : Wonderful place forever', '5 : Wonderful nature ', '5 : Krishna Mutt tempe is the best place forever....']
# str1 = '\n'.join(list1)
# # for i in str1:
# #     if(i == ','):
# #         print
# print(str1)

# name_of_place = "Mangalore"
# lis = ["asf","adsf","ijn","Mangalore"]
#
#
# num1=0
# for i in lis:
#     if(name_of_place != lis[num1]):
#         num1=num1+1


"""
class Node:
    def __init__(self):
        self.m_children_nodes = {}
        self.m_total_word_so_far = ''
        self.m_current_letter = ''
        self.m_curr_index = 0
    def add_word(self, word, word_so_far = '', curr_index = -1):
        self.m_word = word
        self.m_curr_index = curr_index
        if self.m_curr_index >= 0:
            self.m_current_letter = self.m_word[self.m_curr_index]
            self.m_total_word_so_far = word_so_far + self.m_word[self.m_curr_index]

        if self.m_curr_index + 1 < len(self.m_word):
            if self.m_word[self.m_curr_index+1] not in self.m_children_nodes:
                self.m_children_nodes[self.m_word[self.m_curr_index+1]] = Node()
                self.m_children_nodes[self.m_word[self.m_curr_index+1]].add_word( \
                    self.m_word, self.m_total_word_so_far, self.m_curr_index + 1)
            else:
                self.m_children_nodes[self.m_word[self.m_curr_index+1]].add_word( \
                    self.m_word, self.m_total_word_so_far, self.m_curr_index + 1)

    def auto_complete_word(self, str):
        if len(str) > 0 and str[0] in self.m_children_nodes:
            self.m_children_nodes[str[0]].auto_complete_word(str[1:])
        if len(str) == 0:
            print("auto complete :")
            self.print_tree()

    def print_tree(self):
        if self:
            if len(self.m_children_nodes) == 0:
                print('word :', self.m_total_word_so_far)
            else:
                for i in self.m_children_nodes:
                    self.m_children_nodes[i].print_tree()

words = ["den", "dear", "do", "disco", "mangalore", "mysore"]

root = Node()
for word in words:
    root.add_word(word)

root.print_tree()

print('de :')
root.auto_complete_word('de')

for i in range(5):
    my_str = input("enter the letters to auto-complete : \n")
    root.auto_complete_word(my_str)

"""

pp = ['apple', 1, 'banana']
print(pp[1])
pp.append('tomato')
print(pp)