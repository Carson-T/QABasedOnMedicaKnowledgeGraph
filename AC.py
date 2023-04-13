import os
import time
import ahocorasick
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

from collections import deque


class TrieNode:
    def __init__(self, char=''):
        self.char = char
        self.children = {}
        self.word_finished = False
        self.fail = None
        self.word_list = []


class AC_Automaton:
    def __init__(self):
        self.root = TrieNode()

    def insert_word(self, word):
        curr = self.root
        for c in word:
            if c not in curr.children:
                curr.children[c] = TrieNode()
            curr = curr.children[c]
        curr.word_finished = True
        curr.word_list.append(word)

    def build_fail_transitions(self):
        queue = deque([self.root])
        while queue:
            node = queue.popleft()
            for char, child in node.children.items():
                fail_node = node.fail
                while fail_node and char not in fail_node.children:
                    fail_node = fail_node.fail
                child.fail = fail_node.children.get(char, self.root) if fail_node else self.root
                queue.append(child)

    def search_patterns(self, text):
        results = []
        node = self.root
        for i, char in enumerate(text):
            while node and char not in node.children:
                node = node.fail
            if not node:
                node = self.root
                continue
            node = node.children[char]
            if node.word_finished:
                end_index = i
                results.extend(node.word_list)
        return results


@profile
def main():
    # text = "小儿慢性充血性脾肿大该怎么治疗，能吃黄瓜吗？"
    text = "纤维化综合征眼球穿孔伤痧气腮腺恶性肿瘤奈瑟卡他球菌肺炎牙宣老年期抑郁障碍结肠黑变病结核性阴道炎涎腺的未分化癌黑舌充血性脾肿大眼丹慢性自身免疫性甲状腺炎恶性胸腔积液小儿无脾综合征皮肤弓形体病胸锁关节脱位重症联合免疫缺陷皮肤神经瘤原发性肝内硬化综合征小儿先天性直肠肛门畸形褥疮"
    patterns = region_words

    start = time.time()
    ac = AC_Automaton()
    for word in patterns:
        ac.insert_word(word)
    ac.build_fail_transitions()
    # res = ac.search_patterns(text)
    print(ac.search_patterns(text))
    print("time:",time.time()-start)

main()