import torch
from transformers import RobertaModel, RobertaTokenizer

class Model(torch.nn.Module):
    def __init__(self, num_classes):
        super(Model, self).__init__()
        self.l1 = RobertaModel.from_pretrained('ai-forever/ruRoberta-large')
        self.pre_classifier = torch.nn.Linear(1024, 512)
        self.dropout = torch.nn.Dropout(0.3)
        self.classifier = torch.nn.Linear(512, num_classes)

    def forward(self, input_ids, attention_mask, token_type_ids):
        output_1 = self.l1(input_ids=input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids)
        hidden_state = output_1[0]
        pooler = hidden_state[:, 0]
        pooler = self.pre_classifier(pooler)
        pooler = torch.nn.ReLU()(pooler)
        pooler = self.dropout(pooler)
        output = self.classifier(pooler)
        return output
    
    def get_embed(self, input_ids, attention_mask, token_type_ids):
        output_1 = self.l1(input_ids=input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids)
        hidden_state = output_1[0]
        pooler = hidden_state[:, 0]
        return pooler