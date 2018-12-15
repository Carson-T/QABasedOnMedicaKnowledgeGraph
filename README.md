# QABasedOnMedicaKnowledgeGraph
self-implement of disease centered Medical graph from zero to full and sever as question answering base. 从无到有搭建一个以疾病为中心的一定规模医药领域知识图谱，并以该知识图谱完成自动问答与分析服务。

# 项目介绍

知识图谱是目前自然语言处理的一个热门方向，本人参加了ccks2018会议，并得到一些收获，可以查看我的ccks2018参会总结(https://github.com/liuhuanyong/CCKS2018Summary )。  
与知识图谱相关的另一种形态，即事理图谱，本人在这方面也尝试性地积累了一些工作，可参考：(https://github.com/liuhuanyong/ComplexEventExtraction )  
关于知识图谱概念性的介绍就不在此赘述。目前知识图谱在各个领域全面开花，如教育、医疗、司法、金融等。本项目立足医药领域，以垂直型医药网站为数据来源，以疾病为核心，构建起一个包含7类规模为4.4万的知识实体，11类规模约30万实体关系的知识图谱。
本项目将包括以下两部分的内容：
1) 基于垂直网站数据的医药知识图谱构建
2) 基于医药知识图谱的自动问答

# 项目最终效果
话不多少，直接上图。以下两图是实际问答运行过程中的截图：
![image](https://github.com/liuhuanyong/QABasedOnMedicalKnowledgeGraph/blob/master/img/chat1.png)

![image](https://github.com/liuhuanyong/QABasedOnMedicalKnowledgeGraph/blob/master/img/chat2.png)

# 项目运行方式
1、配置要求：要求配置neo4j数据库及相应的python依赖包。neo4j数据库用户名密码记住，并修改相应文件。  
2、知识图谱数据导入：python build_medicalgraph.py，导入的数据较多，估计需要几个小时。  
3、启动问答：python chat_graph.py

# 以下介绍详细方案
# 一、医疗知识图谱构建
# 1.1 业务驱动的知识图谱构建框架
![image](https://github.com/liuhuanyong/QABasedOnMedicalKnowledgeGraph/blob/master/img/kg_route.png)

# 1.2 脚本目录
prepare_data/datasoider.py：网络资讯采集脚本  
prepare_data/datasoider.py：网络资讯采集脚本  
prepare_data/max_cut.py：基于词典的最大向前/向后切分脚本  
build_medicalgraph.py：知识图谱入库脚本    　　

# 1.3 医药领域知识图谱规模
1.3.1 neo4j图数据库存储规模
![image](https://github.com/liuhuanyong/QABasedOnMedicalKnowledgeGraph/blob/master/img/graph_summary.png)

1.3.2 知识图谱实体类型

| 实体类型 | 中文含义 | 实体数量 |举例 |
| :--- | :---: | :---: | :--- |
| Check | 诊断检查项目 | 3,353| 支气管造影;关节镜检查|
| Department | 医疗科目 | 54 |  整形美容科;烧伤科|
| Disease | 疾病 | 8,807 |  血栓闭塞性脉管炎;胸降主动脉动脉瘤|
| Drug | 药品 | 3,828 |  京万红痔疮膏;布林佐胺滴眼液|
| Food | 食物 | 4,870 |  番茄冲菜牛肉丸汤;竹笋炖羊肉|
| Producer | 在售药品 | 17,201 |  通药制药青霉素V钾片;青阳醋酸地塞米松片|
| Symptom | 疾病症状 | 5,998 |  乳腺组织肥厚;脑实质深部出血|
| Total | 总计 | 44,111 | 约4.4万实体量级|


1.3.3 知识图谱实体关系类型

| 实体关系类型 | 中文含义 | 关系数量 | 举例|
| :--- | :---: | :---: | :--- |
| belongs_to | 属于 | 8,844| <妇科,属于,妇产科>|
| common_drug | 疾病常用药品 | 14,649 | <阳强,常用,甲磺酸酚妥拉明分散片>|
| do_eat |疾病宜吃食物 | 22,238| <胸椎骨折,宜吃,黑鱼>|
| drugs_of |  药品在售药品 | 17,315| <青霉素V钾片,在售,通药制药青霉素V钾片>|
| need_check | 疾病所需检查 | 39,422| <单侧肺气肿,所需检查,支气管造影>|
| no_eat | 疾病忌吃食物 | 22,247| <唇病,忌吃,杏仁>|
| recommand_drug | 疾病推荐药品 | 59,467 | <混合痔,推荐用药,京万红痔疮膏>|
| recommand_eat | 疾病推荐食谱 | 40,221 | <鞘膜积液,推荐食谱,番茄冲菜牛肉丸汤>|
| has_symptom | 疾病症状 | 5,998 |  <早期乳腺癌,疾病症状,乳腺组织肥厚>|
| acompany_with | 疾病并发疾病 | 12,029 | <下肢交通静脉瓣膜关闭不全,并发疾病,血栓闭塞性脉管炎>|
| Total | 总计 | 294,149 | 约30万关系量级|

1.3.4 知识图谱属性类型

| 属性类型 | 中文含义 | 举例 |
| :--- | :---: | :---: |
| name | 疾病名称 | 喘息样支气管炎 |
| desc | 疾病简介 | 又称哮喘性支气管炎... |
| cause | 疾病病因 | 常见的有合胞病毒等...|
| prevent | 预防措施 | 注意家族与患儿自身过敏史... |
| cure_lasttime | 治疗周期 | 6-12个月 |
| cure_way | 治疗方式 | "药物治疗","支持性治疗" |
| cured_prob | 治愈概率 | 95% |
| easy_get | 疾病易感人群 | 无特定的人群 |


# 二、基于医疗知识图谱的自动问答
# 2.1 技术架构
![image](https://github.com/liuhuanyong/QABasedOnMedicalKnowledgeGraph/blob/master/img/qa_route.png)

# 2.2 脚本结构
question_classifier.py：问句类型分类脚本  
question_parser.py：问句解析脚本  
chatbot_graph.py：问答程序脚本  

# 2.3　支持问答类型

| 问句类型 | 中文含义 | 问句举例 |
| :--- | :---: | :---: |
| disease_symptom | 疾病症状| 乳腺癌的症状有哪些？ |
| symptom_disease | 已知症状找可能疾病 | 最近老流鼻涕怎么办？ |
| disease_cause | 疾病病因 | 为什么有的人会失眠？|
| disease_acompany | 疾病的并发症 | 失眠有哪些并发症？ |
| disease_not_food | 疾病需要忌口的食物 | 失眠的人不要吃啥？ |
| disease_do_food | 疾病建议吃什么食物 | 耳鸣了吃点啥？ |
| food_not_disease | 什么病最好不要吃某事物 | 哪些人最好不好吃蜂蜜？ |
| food_do_disease | 食物对什么病有好处| 鹅肉有什么好处？ |
| disease_drug | 啥病要吃啥药 | 肝病要吃啥药？ |
| drug_disease | 药品能治啥病 | 板蓝根颗粒能治啥病？ |
| disease_check | 疾病需要做什么检查 | 脑膜炎怎么才能查出来？|
| check_disease |　检查能查什么病 | 全血细胞计数能查出啥来？ |
| disease_prevent | 预防措施| 怎样才能预防肾虚？ |
| disease_lasttime | 治疗周期 | 感冒要多久才能好？ |
| disease_cureway | 治疗方式 | 高血压要怎么治？ |
| disease_cureprob | 治愈概率 | 白血病能治好吗？ |
| disease_easyget | 疾病易感人群 | 什么人容易得高血压？ |
| disease_desc | 疾病描述 | 糖尿病 |

# 问答结果展示

        用户:乳腺癌的症状有哪些？
        小勇: 乳腺癌的症状包括：乳腺癌的远处转移；胸痛；乳头溢液；乳头破碎；肝肿大；泌乳障碍；乳头内陷；乳房肿块；剧痛
        ******************************************************************************************
        用户:最近老流鼻涕怎么办？
        小勇: 症状流鼻涕可能染上的疾病有：枯草热；副流行性感冒；急性上呼吸道感染；硫化氢中毒；小儿衣原体肺炎；风寒感冒；慢性额窦炎；鼻源性头痛；人禽流行性感冒；小儿流行性喘憋性肺炎；病毒性感冒；慢性鼻炎；风热犯肺；感冒；顿呛；小儿急性上呼吸道感染；嗜酸细胞增多性非变态反应性鼻炎；干酪性鼻窦炎；下呼吸道感染；麻疹
        ******************************************************************************************
        用户:为什么有的人会失眠？
        小勇: 失眠可能的成因有：躯体疾病和服用药物可以影响睡眠，如消化不良，头痛，背痛，关节炎，心脏病，糖尿病，哮喘，鼻窦炎，溃疡病，或服用某些影响中枢神经的药物。
        由于生活方式引起睡眠问题也很常见，如饮用咖啡或茶叶，晚间饮酒，睡前进食或晚饭较晚造成满腹食物尚未消化，大量吸烟，睡前剧烈的体力活动，睡前过度的精神活动，夜班工作，白天小睡，上床时间不规律，起床时间不规律。
        可能的原因有压力很大，过度忧虑，紧张或焦虑，悲伤或抑郁，生气，容易出现睡眠问题。
        吵闹的睡眠环境，睡眠环境过于明亮，污染，过度拥挤。
        ******************************************************************************************
        用户:失眠有哪些并发症？
        小勇: 失眠的症状包括：心肾不交；神经性耳鸣；咽鼓管异常开放症；偏执狂；十二指肠胃反流及胆汁反流性胃炎；腋臭；黧黑斑；巨细胞动脉炎；Stargardt病；抑郁症；腔隙性脑梗死；甲状腺功能亢进伴发的精神障碍；紧张性头痛；胃下垂；心血虚；迷路震荡；口腔结核性溃疡；痰饮；游走性结节性脂膜炎；小儿脑震荡
        ******************************************************************************************
        用户:失眠的人不要吃啥？
        小勇: 失眠忌食的食物包括有：油条；河蚌；猪油（板油）；淡菜(鲜)
        ******************************************************************************************
        用户:耳鸣了吃点啥？
        小勇: 耳鸣宜食的食物包括有：南瓜子仁;鸡翅;芝麻;腰果
        推荐食谱包括有：紫菜芙蓉汤;羊肉汤面;油豆腐油菜;紫菜鸡蛋莲草汤;乌药羊肉汤;可乐鸡翅;栗子鸡翅;冬菇油菜心
        ******************************************************************************************
        用户:哪些人最好不好吃蜂蜜？
        小勇: 患有散发性脑炎伴发的精神障碍；情感性心境障碍；蝎螫伤；四肢淋巴水肿；农药中毒所致的精神障碍；肝错构瘤；细菌性肺炎；急性高原病；小儿颅后窝室管膜瘤；柯萨奇病毒疹；眼眶静脉性血管瘤；乙脑伴发的精神障碍；晚期产后出血；吸入性肺炎；腓总神经损伤；铍及其化合物引起的皮肤病；猝死型冠心病；彼得异常；过敏性急性小管间质性肾炎；小儿腹胀的人最好不要吃蜂蜜
        ******************************************************************************************
        用户:鹅肉有什么好处？
        小勇: 患有子宫内膜厚；呼吸疾病；肛肠病；闭经；丧偶后适应性障碍；宫颈外翻；巨球蛋白血症；急性颌下腺炎；锥体外系损害；腺样体炎；咳嗽；错构瘤；牙科病；子宫内膜炎；闭锁综合征；结膜炎；恶性淋巴瘤；足外翻；神经炎；病理性近视的人建议多试试鹅肉
        ******************************************************************************************
        用户:肝病要吃啥药？
        小勇: 肝病宜食的食物包括有：鹅肉;鸡肉;鸡肝;鸡腿
        推荐食谱包括有：小米红糖粥;小米蛋奶粥;扁豆小米粥;黄豆小米粥;人参小米粥;小米粉粥;鲜菇小米粥;芝麻小米粥
        肝病通常的使用的药品包括：恩替卡韦分散片；维生素C片；二十五味松石丸；拉米夫定胶囊；阿德福韦酯片
        ******************************************************************************************
        用户:板蓝根颗粒能治啥病？
        小勇: 板蓝根颗粒主治的疾病有流行性腮腺炎；喉痹；喉炎；咽部异感症；急性单纯性咽炎；腮腺隙感染；过敏性咽炎；咽囊炎；急性鼻咽炎；喉水肿；慢性化脓性腮腺炎；慢性咽炎；急性喉炎；咽异感症；鼻咽炎；锁喉痈；小儿咽喉炎；喉返神经损伤；化脓性腮腺炎；喉血管瘤,可以试试
        ******************************************************************************************
        用户:脑膜炎怎么才能查出来？
        小勇: 脑膜炎通常可以通过以下方式检查出来：脑脊液钠；尿常规；Fisher手指试验；颈项强直；脑脊液细菌培养；尿谷氨酰胺；脑脊液钾；脑脊液天门冬氨酸氨基转移酶；脑脊液病原体检查；硝酸盐还原试验
        ******************************************************************************************
        用户:怎样才能预防肾虚？
        小勇: 肾虚可能的成因有：1、多因房劳过度，或少年频繁手淫。2、思虑忧郁，损伤心脾，则病及阳明冲脉。3、恐惧伤肾，恐则伤肾。4、肝主筋，阴器为宗筋之汇，若情志不遂，忧思郁怒，肝失疏泄条达，则宗筋所聚无能。5、湿热下注，宗筋弛纵。
        肾虚是肾脏精气阴阳不足所产生的诸如精神疲乏、头晕耳鸣、健忘脱发、腰脊酸痛、遗精阳痿、男子不育、女子不孕、更年期综合征等多种病证的一个综合概念。关于肾虚形成的原因，可归结为两个方面，一为先天禀赋不足，二为后天因素引起。
        从引起肾虚的先天因素来看，首先是先天禀赋薄弱。《灵枢.寿天刚柔》篇说：“人之生也，有刚有柔，有弱有强。”由于父母体弱多病，精血亏虚时怀孕;或酒后房事怀孕;或年过五十精气力量大减之时怀孕;或男女双方年龄不够，身体发育不完全结婚，也就是早婚时怀孕，或生育过多，精血过度耗损;或妊娠期中失于调养，胎气不足等等都可导致肾的精气亏虚成为肾虚证形成的重要原因;其次，如果肾藏精功能失常就会导致性功能异常，生殖功能下降，影响生殖能力，便会引起下一代形体虚衰，或先天畸形、痴呆、缺陷、男子出现精少不育、早泄，女子出现闭经不孕、小产、习惯性流产等等。
        肾虚的预防措施包括：肾虚日常预防
        在预防方面，因起病与恣情纵欲有关的，应清心寡欲，戒除手淫;如与全身衰弱、营养不良或身心过劳有关的，应适当增加营养或注意劳逸结合，节制性欲。
        1、性生活要适度，不勉强，不放纵。
        2、饮食方面：无力疲乏时多吃含铁、蛋白质的食物，如木耳、大枣、乌鸡等;消化不良者多喝酸奶，吃山楂;平日护肾要多吃韭菜、海参、人参、乌鸡、家鸽等。
        3、经常进行腰部活动，这些运动可以健运命门，补肾纳气。还可多做一些刺激脚心的按摩，中医认为，脚心的涌泉穴是浊气下降的地方，经常按摩涌泉穴，可益精补肾、强身健体、防止早衰，并能舒肝明目，清喉定心，促进睡眠，增进食欲。
        4、充足的睡眠也是恢复精气神的重要保障，工作再紧张，家里的烦心事再多，到了该睡觉的时候也要按时休息。
        健康教育
        1、过度苦寒、冰凉的食物易伤肾，如芦荟、苦瓜、雪糕、鹅肉、啤酒进食过多都伤肾，应该多食黑色素含量高和温补性中药如黑米黑豆等。
        2、男性接触过多的洗涤剂也伤肾，家庭应少用洗涤剂清洗餐具及蔬果，以免洗涤剂残留物被过多摄入。
        3、适当运动可延缓衰老，但强度不宜太大，应选能力所及的运动项目，以促进血液循环，可改善血淤、气损等情况。散步、慢跑、快步走，或在鹅卵石上赤足适当行走，都会促进血液循环，对肾虚有辅助治疗作用。
        4、保持良好的作息习惯，尽量避免熬夜。
        5、积极参加户外运动，放松心情。
        6、不要给自己太大的压力，学会合理减压。
        ******************************************************************************************
        用户:感冒要多久才能好？
        小勇: 感冒治疗可能持续的周期为：7-14天
        ******************************************************************************************
        用户:高血压要怎么治？
        小勇: 高血压可以尝试如下治疗：药物治疗;手术治疗;支持性治疗
        ******************************************************************************************
        用户:白血病能治好吗？
        小勇: 白血病治愈的概率为（仅供参考）：50%-70%
        ******************************************************************************************
        用户:什么人容易得高血压？
        小勇: 高血压的易感人群包括：有高血压家族史，不良的生活习惯，缺乏运动的人群
        ******************************************************************************************
        用户:糖尿病
        小勇: 糖尿病,熟悉一下：糖尿病是一种比较常见的内分泌代谢性疾病。该病发病原因主要是由于胰岛素分泌不足，以及胰升高血糖素不适当地分泌过多所引起。多见于40岁以上喜食甜食而肥胖的病人，城市多于农村，常有家族史，故与遗传有关。少数病人与病毒感染和自身免疫反应有关。主要表现为烦渴、多饮、多尿、多食、乏力、消瘦等症状。生命的常见病，伴发高血压、冠心病、高脂血症等，严重时危及生命。
        中医学认为，肝主疏泄，关系人体接收机的升降与调畅，肝气郁滞则气机升降输布紊乱，肝失疏泄则血糖等精微物质不能随清阳之气输布于周身而郁滞于血中，出现高血糖或精微物质的输布紊乱，反见血糖升高，进一步导致血脂、蛋白等其它精微物质紊乱，引起其他合并症，治疗以疏肝调气为主，顺肝条达之性以恢复其生理功能，肝气条达，气机调畅，精微得以输布，糖被利用而血糖自然下降。
        另外，因糖尿病的发生和饮食有关，饮食控制的好坏直接影响着治疗的效果。再就是配合运动，注意调摄情志，再适当的配合中药治疗会取得良好的治疗效果。 
        ******************************************************************************************
        用户:全血细胞计数能查出啥来
        小勇: 通常可以通过全血细胞计数检查出来的疾病有成人类风湿性关节炎性巩膜炎；外阴-阴道-牙龈综合征；电击伤；老年收缩期高血压；小儿肝硬化；异常血红蛋白病；痴呆综合征；高血压病伴发的精神障碍；睾丸淋巴瘤；叶酸缺乏所致贫血；眼球内炎；不稳定血红蛋白病；类癌综合征；老年痴呆；急性淋巴管炎；宫颈妊娠；蚕食性角膜溃疡；低增生性急性白血病；交感性眼炎；原发性免疫缺陷病

# 总结
１、本项目完成了从无到有，以垂直网站为数据来源，构建起以疾病为中心的医疗知识图谱，实体规模4.4万，实体关系规模30万。并基于此，搭建起了一个可以回答18类问题的自动问答小系统,总共耗时3天。其中，数据采集与整理1天，知识图谱构建与入库0.5天，问答系统组件1.5天。总的来说，还是比较快速。      
2、本项目以业务驱动，构建医疗知识图谱，知识schema设计基于所采集的结构化数据生成(对网页结构化数据进行xpath解析)。    
3、本项目以neo4j作为存储，并基于传统规则的方式完成了知识问答，并最终以cypher查询语句作为问答搜索sql，支持了问答服务。  
4、本项目可以快速部署，数据已经放在data/medical.json当中，本项目的数据，如侵犯相关单位权益，请联系我删除。本数据请勿商用，以免引起不必要的纠纷。在本项目中的部署上，可以遵循项目运行步骤，完成数据库搭建，并提供搜索服务。  
5、本项目还有不足：关于疾病的起因、预防等，实际返回的是一大段文字，这里其实可以引入事件抽取的概念，进一步将原因结构化表示出来。这个可以后面进行尝试。    

If any question about the project or me ,see https://liuhuanyong.github.io/


如有自然语言处理、知识图谱、事理图谱、社会计算、语言资源建设等问题或合作，可联系我：    
1、我的github项目介绍：https://liuhuanyong.github.io  
2、我的csdn博客：https://blog.csdn.net/lhy2014  
3、about me:刘焕勇，中国科学院软件研究所，lhy_in_blcu@126.com  
