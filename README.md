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
## eval
模型评估代码：指标P、R、F1
评估方式包含精确匹配和模糊匹配两种设置，其中：
- 精确匹配：实体边界和实体类型均正确识别
- 模糊匹配：只要求实体类型正确，实体边界可存在包含关系
