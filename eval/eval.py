import json
import os

e_types_list =  [
  "Pests and diseases", "Grain and oil crops", "Medicinal plants", "Livestock and poultry diseases",
  "Livestock and poultry", "Fruits and vegetables", "Agricultural production and operation entities", "Infected crop parts",
  "Soil type", "Agronomic techniques", "Fertilizer", "Physical control", "Feed additives",
  "Flowers", "Phenological period", "Gas", "Chemical control", "Pesticide", "Tea",
  "Agricultural control", "Veterinary drug", "Edible fungi", "Biological control", "Forage", "Aquatic animals"
]
e_types_list = [etype.lower() for etype in e_types_list]
# print(e_types_list)

def has_duplicate(tmp_list):
    if tmp_list == []:
        return False
    #去重复
    if type(tmp_list[0]) == str:
        if len(tmp_list) == len(set(tmp_list)):
            return False
        else:
            return True
    if type(tmp_list[0]) == list:
        tmp = []
        for t in tmp_list:
            if t not in tmp:
                tmp.append(t)
        if len(tmp_list) == len(tmp):
            return False
        else:
            return True

def get_correct_list_from_response_list(target_list, response_list):
    """
    target_list 和 response_list 均有可能包含重复的 item
    """
    res = []
    if not has_duplicate(response_list):
        res = [item for item in response_list if item in target_list]
    else:
        if not has_duplicate(target_list):
            # 去重
            uni_response_list = []
            for item in response_list:
                if item not in uni_response_list:
                    uni_response_list.append(item)
            res = [item for item in uni_response_list if item in target_list]
        else:
            res = []
            processed_item_list = []
            for item in response_list:
                if item not in processed_item_list:
                    processed_item_list.append(item)

                    num_item = response_list.count(item)
                    if num_item == 1:  # not duplicate
                        if item in target_list:
                            res.append(item)
                    else:  # duplicate
                        if item in target_list:
                            num_item_in_target = target_list.count(item)
                            num_item_correct = min([num_item, num_item_in_target])
                            res += [item] * num_item_correct
    return res

def soft_match(predict, target_list):
    """
    soft match: 字符串重叠
    """
    pred = predict.strip()
    if len(target_list) == 0:
        return pred
    
    for target_item in target_list:
        target_item = target_item.lower().strip()
        # 检查是否存在边界重叠
        if target_item in pred or pred in target_item:
            return target_item

#标注一致性计算
def calculate_cohens_kappa(tp, fp, fn):
    """计算 Cohen’s Kappa"""
    # 总样本数 N
    N = 48783 #数目见process.py处理test_bio.txt文件
    # 计算 TN
    tn = N - (tp + fp + fn)

    # 计算 p_o（观察一致性）
    p_o = (tp + tn) / N
    # 计算 p_e（期望一致性）
    p_true_0 = (tn + fp) / N
    p_true_1 = (tp + fn) / N
    p_pred_0 = (tn + fn) / N
    p_pred_1 = (tp + fp) / N
    p_e = (p_true_0 * p_pred_0) + (p_true_1 * p_pred_1)

    # 计算 Kappa
    kappa = (p_o - p_e) / (1 - p_e) if (1 - p_e) != 0 else 0

    return kappa

def calculate_kappa_per_type(entity_type, boundaries):
    """
    计算某个类别的 Cohen’s Kappa 系数。
    :param entity_type: 实体类别名称
    :param boundaries: 存储 TP、FP、FN 的字典
    :param num_entity: 总实体数
    :return: 该类别的 Cohen’s Kappa
    """
    if entity_type not in boundaries:
        print(f"Entity type '{entity_type}' not found in boundaries.")
        return None

    tp = boundaries[entity_type]["tp"]
    fp = boundaries[entity_type]["fp"]
    fn = boundaries[entity_type]["fn"]
    
    N = 48783 #数目见process.py处理test_bio.txt文件
    # 计算 TN
    tn = N - (tp + fp + fn)
    
    # 计算 P_o（观察一致性）
    p_o = (tp + tn) / N

    # 计算 p_e（期望一致性）
    p_true_0 = (tn + fp) / N
    p_true_1 = (tp + fn) / N
    p_pred_0 = (tn + fn) / N
    p_pred_1 = (tp + fp) / N
    p_e = (p_true_0 * p_pred_0) + (p_true_1 * p_pred_1)

    # 计算 Kappa
    kappa = (p_o - p_e) / (1 - p_e) if (1 - p_e) != 0 else 0

    return kappa


def print_metrics(tp, fp, fn, task, align=8):
    p, r, f1 = 0.0, 0.0, 0.0

    if tp + fp != 0:
        p = 1.0 * tp / (tp + fp)
    if tp + fn != 0:
        r = 1.0 * tp / (tp + fn)
    if p + r != 0.0:
        f1 = 2.0 * p * r / (p + r)
        
    print(("{} | p: {:.4f}, r: {:.4f}, f1: {:.4f} | tp: {:4d}, fp: {:4d}, fn: {:4d}, tp+fn: {:4d}\n".format(
        task.ljust(align),
        round(p, 4),
        round(r, 4),
        round(f1, 4),
        tp,
        fp,
        fn,
        tp+fn,
        )
    ))

    

## metric
## report overall metric
def report_metric(result_file,e_types_list):
    # print(e_types_list)
    with open(result_file, 'r', encoding='utf-8') as fr:
        data = json.load(fr)
    # ## per type
    hard_boundaries = dict()
    soft_boundaries = dict()
    for key in e_types_list:
        hard_boundaries[key] = {"tp": 0, "fp": 0, "fn": 0}
        soft_boundaries[key] = {"tp": 0, "fp": 0, "fn": 0}
         
    ## statistics
    invalid_count = 0
    num_undefined_type = 0
    num_entity = 0
    tp_ner_strict = 0
    fp_ner_strict = 0
    fn_ner_strict = 0
    tp_ner_strict_soft_match = 0
    fp_ner_strict_soft_match = 0
    fn_ner_strict_soft_match = 0

    for example in data:
        ## target
        strict_target_list = []
        boundaries_target_list = []

        ## per type 计算每种实体的边界匹配，目标实体类型分类存储
        boundaries_target_list_dict = {}
        for key in e_types_list:
            boundaries_target_list_dict[key] = []
        # print(example["label"])
        for ent_type,ent_names in example["label"].items():
            ent_type = ent_type.lower()
            for ent_name in ent_names:
                ent_name = ent_name.lower() #小写
                strict_target_list.append([ent_type, ent_name])
                boundaries_target_list.append(ent_name)
                if ent_type in boundaries_target_list_dict:
                    boundaries_target_list_dict[ent_type].append(ent_name)
                num_entity += 1

        ## predict
        strict_predict_list = []
        boundaries_predict_list = []
        strict_predict_list_soft_match = []
        boundaries_predict_list_soft_match = []
        
        # per type
        boundaries_predict_list_dict = {}
        boundaries_predict_list_soft_match_dict = {}
        for key in e_types_list:
            boundaries_predict_list_dict[key] = []
            boundaries_predict_list_soft_match_dict[key] = []
        
        if isinstance(example["response"], str):
            try:
                # 尝试将字符串解析为字典
                example["response"] = json.loads(example["response"])
            except json.JSONDecodeError as e:
                # print(f"Failed to decode JSON: {e}")
                invalid_count += 1  # 错误标注输出数量加1
                print(f"解析错误: {example['response']}")
                example["response"] = {}
                
        elif isinstance(example["response"], list):
                invalid_count += 1  # 错误标注输出数量加1
                print(f"解析错误: {example['response']}")
                example["response"] = {}
        
        # print(example["response"])
        for ent_type, entities in example["response"].items():
            ent_type = ent_type.replace("_", " ").lower()#####匹配实体类型的书写格式
            # print(entities)
            if entities is not None:
                for ent_name in entities:
                    if not isinstance(ent_name, str):  # 如果 ent_name 是字典类型
                        # print(f"ent_name type: {type(ent_name)}, value: {ent_name}")
                        invalid_count += 1  # 错误标注数量加1
                        continue  # 跳过这条标注
                
                    ent_name = ent_name.lower() #小写转换
                    strict_predict_list.append([ent_type, ent_name])
                    boundaries_predict_list.append(ent_name)
                    # print(strict_predict_list)
                    if ent_type in boundaries_predict_list_dict:
                        boundaries_predict_list_dict[ent_type].append(ent_name)
                    else:
                        print("未定义的实体类型：",ent_type)
                        #未定义的实体类型预测
                        num_undefined_type += 1

                    ## soft match
                    ent_name = soft_match(ent_name, boundaries_target_list)
                    strict_predict_list_soft_match.append([ent_type, ent_name])
                    boundaries_predict_list_soft_match.append(ent_name)

                    # per type
                    if ent_type in e_types_list:
                        boundaries_predict_list_soft_match_dict[ent_type].append(ent_name)
        ## hard-match 
        strict_correct_list = get_correct_list_from_response_list(strict_target_list, strict_predict_list)
        # print(strict_correct_list)
        tp_ner_strict += len(strict_correct_list)
        fp_ner_strict += len(strict_predict_list) - len(strict_correct_list)
        fn_ner_strict += len(strict_target_list) - len(strict_correct_list)


        ## soft-match
        strict_correct_list_soft_match = get_correct_list_from_response_list(strict_target_list, strict_predict_list_soft_match)
        
        tp_ner_strict_soft_match += len(strict_correct_list_soft_match)
        fp_ner_strict_soft_match += len(strict_predict_list_soft_match) - len(strict_correct_list_soft_match)
        fn_ner_strict_soft_match += len(strict_target_list) - len(strict_correct_list_soft_match)
        
        ## per type
        for key in e_types_list:
            cur_correct = get_correct_list_from_response_list(boundaries_target_list_dict[key], boundaries_predict_list_dict[key])
            hard_boundaries[key]["tp"] += len(cur_correct)
            hard_boundaries[key]["fp"] += len(boundaries_predict_list_dict[key]) - len(cur_correct)
            hard_boundaries[key]["fn"] += len(boundaries_target_list_dict[key]) - len(cur_correct)

            cur_correct_soft = get_correct_list_from_response_list(boundaries_target_list_dict[key], boundaries_predict_list_soft_match_dict[key])
            soft_boundaries[key]["tp"] += len(cur_correct_soft)
            soft_boundaries[key]["fp"] += len(boundaries_predict_list_soft_match_dict[key]) - len(cur_correct_soft)
            soft_boundaries[key]["fn"] += len(boundaries_target_list_dict[key]) - len(cur_correct_soft)
    print("#sentence: {}, #entity: {}, #undefined type: {}, #invalid label: {}".format(len(data), num_entity, num_undefined_type, invalid_count))
    
    #print 严格匹配和模糊匹配
    # print(tp_ner_strict)
    print_metrics(tp_ner_strict, fp_ner_strict, fn_ner_strict, "NER-strict-hardMatch", align=25)
    # 计算 Cohen's Kappa
    kappa_score = calculate_cohens_kappa(tp_ner_strict, fp_ner_strict, fn_ner_strict)
    print(f"Strict Cohen’s Kappa: {kappa_score:.4f}")
    
    print_metrics(tp_ner_strict_soft_match, fp_ner_strict_soft_match, fn_ner_strict_soft_match, "NER-soft-softMatch", align=25)
    kappa_score = calculate_cohens_kappa(tp_ner_strict_soft_match, fp_ner_strict_soft_match, fn_ner_strict_soft_match)
    print(f"Soft Cohen’s Kappa: {kappa_score:.4f}")
    return hard_boundaries,soft_boundaries


def calculate_metrics(entity_type, boundaries):
    """
    计算并输出某种实体类型的精确度、召回率和F1分数。
    :param entity_type: 实体类型的名称（字符串）
    :param boundaries: 包含TP、FP、FN的字典
    """
    if entity_type not in boundaries:
        print(f"Entity type '{entity_type}' not found in boundaries.")
        return
    
    tp = boundaries[entity_type]["tp"]
    fp = boundaries[entity_type]["fp"]
    fn = boundaries[entity_type]["fn"]

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    return precision, recall, f1


####输入数据格式
#输入文件需同时包含真实标签label和预测标签response，匹配方式包含严格匹配和模糊匹配，计算微观F1（Micro F1）
# eval_data = [
#     {
#         "label": {
#             "Agronomic techniques": [
#                 "Cover cropping"
#             ],
#             "Pests and diseases": [
#                 "Huanglongbing"
#             ]
#         },
#         "response": {
#             "Agronomic techniques": [
#                 "Cover cropping"
#             ]
#         }
#     }
# ]

eval_data = r"/Users/yunyunzhao/Desktop/01/Agri_NER/gliner_train/gliner_ft_output.json"
#eval        
hard_boundaries,soft_boundaries = report_metric(eval_data, e_types_list)
##严格匹配不考虑大小写差异、空格或其他字符变化
##模糊匹配 部分重叠或相似 

#实体类型
for entity_type in e_types_list:
    p,r,f1 = calculate_metrics(entity_type,soft_boundaries)
    print("Entity Type: {}, Precision: {:.4f}, Recall: {:.4f}, F1 Score: {:.4f}".format(entity_type, p, r, f1))

    # kappa = calculate_kappa_per_type(entity_type, soft_boundaries)
    # print("Entity Type: {}, Precision: {:.4f}, Recall: {:.4f}, F1 Score: {:.4f}, Cohen's Kappa: {:.4f}".format(
    #     entity_type, p, r, f1, kappa if kappa is not None else 0.0
    # ))