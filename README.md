# Agriculture-knowledge-Objects
本项目旨在面向农业领域科技文献，实现细粒度专业领域**知识对象的识别与抽取**，并使用streamlit构建原型进行**结果的可视化呈现**。
## 农业知识对象识别数据集<br>（Agricultural Scientific Literature Knowledge Object Recognition Dataset，Agri-KORD）
`Agri-KORD` 是一个面向农业领域知识对象识别任务的数据集，旨在支持基于大语言模型（LLMs）对农业知识对象的理解、抽取与分析。<br>
本数据集共包含 **25 种农业知识对象类型**，涵盖作物、病虫害、防控方法等多个方面，具体类型如下：
```python
[
  "Pests and diseases", "Grain and oil crops", "Medicinal plants", "Livestock and poultry diseases","Livestock and poultry", "Fruits and vegetables", "Agricultural production and operation entities", "Infected crop parts", "Soil type", "Agronomic techniques", "Fertilizer", "Physical control", "Feed additives","Flowers", "Phenological period", "Gas", "Chemical control", "Pesticide", "Tea","Agricultural control", "Veterinary drug", "Edible fungi", "Biological control", "Forage", "Aquatic animals"
]
```
## gliner_train
用于训练 GLiNER 模型的代码，包括数据预处理、模型微调以及实体识别任务结果。
### 🔗 模型权重下载

由于 GitHub LFS 限额限制，训练后的模型权重未直接保存在仓库中。
你可以通过以下链接下载我们微调后的模型：
📦 [点击下载模型（Google Drive）](https://drive.google.com/drive/folders/1OCNPxt-CbG2qnh3U5x3ZY8cRNti6KilU?usp=sharing)

### 🗂️ 文件说明
| 文件/目录 | 描述 |
|-----------|------|
| `gliner_dataprocess.py` | GLiNER 模型训练用数据预处理脚本 |
| `finetune.py`           | GLiNER 模型微调主程序 |
| `gliner_output.json`    | 使用原始 `gliner_large-v2.5` 模型进行零样本实体识别的输出结果 |
| `gliner_ft_output.json` | 使用微调后的 `gliner_large-v2.5` 模型生成的输出结果 |
| `gliner_train.json`     | 用于微调的训练数据 |
| `gliner_test.json`      | 用于模型测试的数据 |

### 🧪 快速运行测试
```bash
python gliner_train/test.py
```

## eval
模型评估代码：指标P、R、F1
评估方式包含精确匹配和模糊匹配两种设置，其中：
- 精确匹配：实体边界和实体类型均正确识别
- 模糊匹配：只要求实体类型正确，实体边界可存在包含关系
