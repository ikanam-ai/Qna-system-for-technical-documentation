from transformers import RobertaModel, RobertaTokenizer


tokenizer = RobertaTokenizer.from_pretrained('ai-forever/ruRoberta-large')


def tokenize_function(texts):
    return tokenizer(texts, padding=True, truncation=True, return_tensors="pt")

class TextDataset(Dataset):
    def __init__(self, texts, labels):
        self.texts = texts
        self.labels = labels
        self.tokenizer = RobertaTokenizer.from_pretrained('ai-forever/ruRoberta-large')

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]
        tokens = self.tokenizer(text, padding='max_length', truncation=True, return_tensors="pt", max_length=128)
        input_ids = tokens['input_ids'].squeeze()
        attention_mask = tokens['attention_mask'].squeeze()
        token_type_ids = tokens.get('token_type_ids', torch.zeros_like(input_ids))
        return input_ids, attention_mask, token_type_ids, label

def collate_fn(batch):
    input_ids, attention_mask, token_type_ids, labels = zip(*batch)
    input_ids = torch.nn.utils.rnn.pad_sequence(input_ids, batch_first=True, padding_value=tokenizer.pad_token_id)
    attention_mask = torch.nn.utils.rnn.pad_sequence(attention_mask, batch_first=True, padding_value=0)
    token_type_ids = torch.nn.utils.rnn.pad_sequence(token_type_ids, batch_first=True, padding_value=0)
    labels = torch.tensor(labels)
    return input_ids, attention_mask, token_type_ids, labels



def get_embeddings(model, dataloader):
    model.eval()
    embeddings = []
    labels_list = []
    with torch.no_grad():
        for batch in dataloader:
            input_ids, attention_mask, token_type_ids, labels = batch
            input_ids = input_ids.to(device)
            attention_mask = attention_mask.to(device)
            token_type_ids = token_type_ids.to(device)
            labels = labels.to(device)

            embed = model.get_embed(input_ids, attention_mask, token_type_ids)
            embeddings.append(embed.cpu().numpy())
            labels_list.extend(labels.cpu().numpy())

    return np.vstack(embeddings), np.array(labels_list)