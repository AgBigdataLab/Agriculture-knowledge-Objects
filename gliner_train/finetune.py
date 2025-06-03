import json
import random
import os
os.environ["TOKENIZERS_PARALLELISM"] = "true"
os.environ["CUDA_VISIBLE_DEVICES"] = "3"
import torch
from gliner import GLiNERConfig, GLiNER
from gliner.training import Trainer, TrainingArguments
from gliner.data_processing.collator import DataCollatorWithPadding, DataCollator
from gliner.utils import load_config_as_namespace
from gliner.data_processing import WordsSplitter, GLiNERDataset


model_path = r"/home/zhaochenyun/zcy/AgriNER/2_baseline/model/models--gliner-community--gliner_large-v2.5/snapshots/3b3bcaeacf8b0b63f957564c069f06b9a0585f8e"
model = GLiNER.from_pretrained(model_path,local_files_only=True)  
data_collator = DataCollator(model.config, data_processor=model.data_processor, prepare_labels=True)

# Optional: compile model for faster training
model.to("cuda")
print("done")


train_dataset_path = "gliner_train.json"
test_dataset_path = "gliner_test.json"

with open(train_dataset_path, "r") as f:
    train_dataset = json.load(f)
    
with open(test_dataset_path, "r") as f:
    test_dataset = json.load(f)
    
# # calculate number of epochs
num_steps = 500
batch_size = 4
data_size = len(train_dataset)
num_batches = data_size // batch_size
num_epochs = max(1, num_steps // num_batches)

training_args = TrainingArguments(
    output_dir="models",
    learning_rate=5e-6,
    weight_decay=0.01,
    others_lr=1e-5,
    others_weight_decay=0.01,
    lr_scheduler_type="cosine", #cosine
    warmup_ratio=0.1,
    per_device_train_batch_size=batch_size,
    per_device_eval_batch_size=batch_size,
    focal_loss_alpha=0.75,
    focal_loss_gamma=2,
    num_train_epochs=num_epochs,
    evaluation_strategy="steps",
    save_steps = 100,
    save_total_limit=10,
    dataloader_num_workers = 0,
    use_cpu = False,
    report_to="wandb",
    )

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    tokenizer=model.data_processor.transformer_tokenizer,
    data_collator=data_collator,
)

trainer.train()