from typing import List
import os
import time
from memory_profiler import profile
cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
disease_path = os.path.join(cur_dir, 'dict/disease.txt')
department_path = os.path.join(cur_dir, 'dict/department.txt')
check_path = os.path.join(cur_dir, 'dict/check.txt')
drug_path = os.path.join(cur_dir, 'dict/drug.txt')
food_path = os.path.join(cur_dir, 'dict/food.txt')
producer_path = os.path.join(cur_dir, 'dict/producer.txt')
symptom_path = os.path.join(cur_dir, 'dict/symptom.txt')
deny_path = os.path.join(cur_dir, 'dict/deny.txt')
# 加载特征词
disease_wds= [i.strip() for i in open(disease_path,encoding='utf-8') if i.strip()]
department_wds= [i.strip() for i in open(department_path,encoding='utf-8') if i.strip()]
check_wds= [i.strip() for i in open(check_path,encoding='utf-8') if i.strip()]
drug_wds= [i.strip() for i in open(drug_path,encoding='utf-8') if i.strip()]
food_wds= [i.strip() for i in open(food_path,encoding='utf-8') if i.strip()]
producer_wds= [i.strip() for i in open(producer_path,encoding='utf-8') if i.strip()]
symptom_wds= [i.strip() for i in open(symptom_path,encoding='utf-8') if i.strip()]
region_words = set(department_wds + disease_wds + check_wds + drug_wds + food_wds + producer_wds + symptom_wds)
deny_words = [i.strip() for i in open(deny_path,encoding='utf-8') if i.strip()]


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word_end = False
        self.word_list = []


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str):
        curr = self.root
        for c in word:
            if c not in curr.children:
                curr.children[c] = TrieNode()
            curr = curr.children[c]
        curr.is_word_end = True
        curr.word_list.append(word)

    def search(self, text: str) -> List[str]:
        result = []
        curr = self.root
        n = len(text)
        for i in range(n):
            c = text[i]
            if c not in curr.children:
                continue
            j = i
            while j < n and text[j] in curr.children:
                curr = curr.children[text[j]]
                if curr.is_word_end:
                    result.extend(curr.word_list)
                j += 1
            curr = self.root
        return result

@profile
def main():
    text = "纤维化综合征眼球穿孔伤痧气腮腺恶性肿瘤奈瑟卡他球菌肺炎牙宣老年期抑郁障碍结肠黑变病结核性阴道炎涎腺的未分化癌黑舌充血性脾肿大眼丹慢性自身免疫性甲状腺炎恶性胸腔积液小儿无脾综合征皮肤弓形体病胸锁关节脱位重症联合免疫缺陷皮肤神经瘤原发性肝内硬化综合征小儿先天性直肠肛门畸形褥疮"
    # text = "小儿慢性充血性脾肿大脱囊先天性喉喘鸣"
    patterns = region_words
    start = time.time()
    trie = Trie()
    for pattern in patterns:
        trie.insert(pattern)
    print(trie.search(text))
    print("time:",time.time()-start)


main()