import random
import time
class SentenceCorrector(object):
    def __init__(self, cost_fn, conf_matrix):
        self.conf_matrix = conf_matrix
        self.cost_fn = cost_fn
        self.inv_conf_matrix = {}
        for key in self.conf_matrix:
            self.inv_conf_matrix[key]=[]
        for key in self.conf_matrix.keys():
            for letter in self.conf_matrix[key]:
                self.inv_conf_matrix[letter].append(key)
        self.best_state = None 
        

    def permutations_word_conf_matrix(self, word):
        """
        :param word: str
        :return: list of str
        """

        list_letters= list(word)
        if(len(list_letters)==1):
            temp=[list_letters[0]]
            temp+=self.inv_conf_matrix[list_letters[0]]
            return temp
        else:
            list_permutations_n_1 = self.permutations_word_conf_matrix(word[1:]) 
            temp=[]
            for i in range(len(list_permutations_n_1)):
                temp.append(list_letters[0]+list_permutations_n_1[i])
                for j in range(len(self.inv_conf_matrix[list_letters[0]])):
                    temp.append(self.inv_conf_matrix[list_letters[0]][j]+list_permutations_n_1[i])
            return temp
    def permutations_1_changes(self,word):
        perms=[]
        list_letters=list(word)
        for i in range(len(word)):
            temp=list_letters.copy()
            for l in range(-1,len(self.inv_conf_matrix[list_letters[i]])):
                if(l==-1):
                    temp[i]=list_letters[i]
                else:
                    temp[i]=self.inv_conf_matrix[list_letters[i]][l]
                perms.append("".join(temp))
        return perms


    def permutations_2_changes(self, word,changed):
        """
        :param word: str
        :return: list of str
        """
        perms=[]
        list_letters=list(word)
        for i in range(len(word)):
            if(not changed[i]):
                for j in range(i+1,len(word)):
                    if(not changed[j]):
                        temp=list_letters.copy()
                        for l in range(-1,len(self.inv_conf_matrix[list_letters[i]])):
                            if(l==-1):
                                temp[i]=list_letters[i]
                            else:
                                temp[i]=self.inv_conf_matrix[list_letters[i]][l]
                            for m in range(-1,len(self.inv_conf_matrix[list_letters[j]])):
                                if(m==-1):
                                    temp[j]=list_letters[j]
                                else:
                                    temp[j]=self.inv_conf_matrix[list_letters[j]][m]
                                perms.append("".join(temp))
        return perms


    def permutations_3_changes(self, word,changed):
        """
        :param word: str
        :return: list of str
        """
        perms=[]
        list_letters=list(word)
        for i in range(len(word)):
            if(not changed[i]):
                for j in range(i+1,len(word)):
                    if(not changed[j]):
                        for k in range(j+1,len(word)):
                            if(not changed[k]):
                                temp=list_letters.copy()
                                for l in range(-1,len(self.inv_conf_matrix[list_letters[i]])):
                                    if(l==-1):
                                        temp[i]=list_letters[i]
                                    else:
                                        temp[i]=self.inv_conf_matrix[list_letters[i]][l]
                                    for m in range(-1,len(self.inv_conf_matrix[list_letters[j]])):
                                        if(m==-1):
                                            temp[j]=list_letters[j]
                                        else:
                                            temp[j]=self.inv_conf_matrix[list_letters[j]][m]
                                        for n in range(-1,len(self.inv_conf_matrix[list_letters[k]])):
                                            if(n==-1):
                                                temp[k]=list_letters[k]
                                            else:
                                                temp[k]=self.inv_conf_matrix[list_letters[k]][n]
                                            perms.append("".join(temp))
        return perms

    def changeArray(self,s1,s2,a):
        for k in range(len(s1)):
            if(s1[k]!=s2[k]):
                a[k]=True
        return a

    def search(self, start_state):

        """
        :param start_state: str Input string with spelling errors
        """

        start_time = time.time()

        self.best_state = start_state
        broken_into_words=start_state.split()
        number_of_words=len(broken_into_words)
        min_cost=self.cost_fn(start_state)
        change_array = []
        word_changed=[False for _ in range(number_of_words)]
        for i in range(number_of_words):
            arr_temp = [False for j in range(len(broken_into_words[i]))]
            change_array.append(arr_temp)
        permuts_word_ith=[[] for i in range(number_of_words)]

        counter=0
        while counter<10:
            counter+=1
            iter_start_state=self.best_state


            #running in forward direction
            curr_best_state=iter_start_state
            curr_best_state_broken=iter_start_state.split()
            curr_min_cost=self.cost_fn(iter_start_state)
            # print(counter,curr_best_state)

            for i in range(number_of_words):
                if(permuts_word_ith[i]==[] or word_changed[i]):
                    if(len(broken_into_words[i])==1):
                        permuts_word_ith[i] = self.permutations_1_changes(curr_best_state_broken[i])
                    else:
                        permuts_word_ith[i] = self.permutations_2_changes(curr_best_state_broken[i],change_array[i])
                
                for j in range(len(permuts_word_ith[i])):
                    curr_best_state_broken[i]=permuts_word_ith[i][j]
                    temp=' '.join(curr_best_state_broken)
                    cost=self.cost_fn(temp)
                    if cost<curr_min_cost:
                        curr_min_cost=cost
                        if(curr_min_cost<min_cost):
                            self.best_state=temp
                            min_cost=curr_min_cost
                        curr_best_state=temp
                curr_best_state_broken=curr_best_state.split()


            #running in backward direction
            curr_best_state=iter_start_state
            curr_best_state_broken=iter_start_state.split()
            curr_min_cost=self.cost_fn(iter_start_state)   

            for i in range(number_of_words-1,-1,-1):
                for j in range(len(permuts_word_ith[i])):
                    curr_best_state_broken[i]=permuts_word_ith[i][j]
                    temp=' '.join(curr_best_state_broken)
                    cost=self.cost_fn(temp)
                    if cost<curr_min_cost:
                        curr_min_cost=cost
                        if(curr_min_cost<min_cost):
                            self.best_state=temp
                            min_cost=curr_min_cost
                        curr_best_state=temp
                curr_best_state_broken=curr_best_state.split()   


            curr_best_state=self.best_state
            curr_min_cost=self.cost_fn(curr_best_state)
            curr_best_state_broken = curr_best_state.split() 

            for i in range(number_of_words):
                change_array[i] = self.changeArray(curr_best_state_broken[i],broken_into_words[i],change_array[i])
                for j in range(len(change_array[i])):
                    word_changed[i]=word_changed[i] or change_array[i][j]


 
            # print("HELLO")
            words_to_be_changed=[]
            for n in range(number_of_words):
                tmp_word=curr_best_state_broken[n]
                length_of_inv_conf_matrix=0
                run_count=0
                while(length_of_inv_conf_matrix==0 and run_count<100):
                    rand_index_in_word=random.randint(0,len(tmp_word)-1)
                    if(not change_array[n][rand_index_in_word]):
                        length_of_inv_conf_matrix=len(self.inv_conf_matrix[tmp_word[rand_index_in_word]])
                if(length_of_inv_conf_matrix==0):
                    continue
                rand_index_in_conf_matrix=random.randint(0,length_of_inv_conf_matrix-1)
                replaced_word=tmp_word[0:rand_index_in_word]+self.inv_conf_matrix[tmp_word[rand_index_in_word]][rand_index_in_conf_matrix]+tmp_word[rand_index_in_word+1:]
                new_sentence=' '.join(curr_best_state_broken[0:n]+[replaced_word]+curr_best_state_broken[n+1:])
                if(self.cost_fn(new_sentence)<=min_cost):
                    words_to_be_changed.append(n)
            # print(words_to_be_changed)
            random.shuffle(words_to_be_changed)
            # print(words_to_be_changed)


            for n in range(len(words_to_be_changed)):
                curr_best_state_broken=curr_best_state.split()
                x=words_to_be_changed[n]
                permuts_word_nth=self.permutations_3_changes(curr_best_state_broken[x],change_array[x])

                for j in range(len(permuts_word_nth)):
                    curr_best_state_broken[x]=permuts_word_nth[j]
                    temp=' '.join(curr_best_state_broken)
                    cost=self.cost_fn(temp)

                    if cost<curr_min_cost:
                        curr_min_cost=cost
                        if(curr_min_cost<min_cost):
                            self.best_state=temp
                            min_cost=curr_min_cost
                            permuts_word_ith[x]=[]
                        curr_best_state=temp

            compare_state = self.best_state.split() 

            for xyz in range(number_of_words):
                change_array[xyz] = self.changeArray(compare_state[xyz],broken_into_words[xyz],change_array[xyz])
                for xy in range(len(change_array[xyz])):
                    word_changed[xyz]=word_changed[xyz] or change_array[xyz][xy]      

        # print("DONE")
        # print(time.time()-start_time)