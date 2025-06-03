from gliner import GLiNER

# Initialize GLiNER with the base model
model = GLiNER.from_pretrained("/gliner/models/checkpoint-4802", load_tokenizer=True)  


# Sample text for entity prediction
text = """
Pesticide overuse in agricultural systems has resulted in the development of pest resistance, the impoverishment of soil microbiota, water pollution, and several human health issues. Nonetheless, farmers still depend heavily on these agrochemicals for economically viable production, given the high frequency at which crops are affected by pests. Phytopathogenic insects are considered the most destructive pests on crops. Botanical pesticides have gained attention as potential biopesticides and complements to traditional pesticides, owing to their biodegradability and low toxicity. Plant-based extracts are abundant in a wide variety of bioactive compounds, such as flavonoids, a class of polyphenols that have been extensively studied for this purpose because of their involvement in plant defense responses. The present review offers a comprehensive review of current research on the potential of flavonoids as insecticides for crop protection, addressing the modes and possible mechanisms of action underlying their bioactivity. The structure–activity relationship is also discussed. It also addresses challenges associated with their application in pest and disease management and suggests alternatives to overcome these issues.
"""

# Labels for entity prediction
# Most GLiNER models should work best when entity types are in lower case or title case
# labels = ["Person", "Award", "Date", "Competitions", "Teams"]
labels =  [
  "Pests and diseases", "Grain and oil crops", "Medicinal plants", "Livestock and poultry diseases",
  "Livestock and poultry", "Fruits and vegetables", "Agricultural production and operation entities", "Infected crop parts",
  "Soil type", "Agronomic techniques", "Fertilizer", "Physical control", "Feed additives",
  "Flowers", "Phenological period", "Gas", "Chemical control", "Pesticide", "Tea",
  "Agricultural control", "Veterinary drug", "Edible fungi", "Biological control", "Forage", "Aquatic animals"
]
# Perform entity prediction
entities = model.predict_entities(text, labels, threshold=0.5)

# Display predicted entities and their labels
for entity in entities:
    print(entity["text"], "=>", entity["label"])
