import torch
import torch.nn as nn
import torchvision.models as models


class EncoderCNN(nn.Module):
    def __init__(self, embed_size):
        super(EncoderCNN, self).__init__()
        resnet = models.resnet50(pretrained=True)
        for param in resnet.parameters():
            param.requires_grad_(False)
        
        modules = list(resnet.children())[:-1]
        self.resnet = nn.Sequential(*modules)
        self.embed = nn.Linear(resnet.fc.in_features, embed_size)

    def forward(self, images):
        features = self.resnet(images)
        features = features.view(features.size(0), -1)
        features = self.embed(features)
        return features
    

class DecoderRNN(nn.Module):
    def __init__(self, embed_size, hidden_size, vocab_size, num_layers=1):
        ''' Initialize the layers of this model.'''
        super(DecoderRNN, self).__init__()
        
        self.hidden_dim = hidden_size
        self.num_layers = num_layers

        # embedding layer that turns words into a vector of a specified size
        self.word_embeddings = nn.Embedding(vocab_size, embed_size)

        # the LSTM takes embedded features+word_embeddings (of a specified size) as inputs 
        # and outputs hidden states of size hidden_dim
        self.lstm = nn.LSTM(embed_size, hidden_size, num_layers, batch_first=True)

        # the linear layer that maps the hidden state output dimension 
        # to the number of words in the vocabulary
        # the last layer gives the probability of the next word
        self.hidden2vocab = nn.Linear(hidden_size, vocab_size)
  

    def forward(self, features, captions):
        ''' Define the feedforward behavior of the model.'''
        # create embedded word vectors for each word in a sentence
        # remove end-word to avoid the network to predict it when seeing end-word
        embeds = self.word_embeddings(captions[:, :-1])

        # append caption embeds to the end of feature vector
        # after embedding, caption have shape (batch_size, caption_len, embedding_dim)
        # because of that, it is necessary to insert one dimension to the image's features
        # features will have shape (batch_size, 1, features_len)
        lstm_input = torch.cat((features.unsqueeze(dim=1), embeds), 1)

        # the lstm takes in our embeddings and hiddent state
        lstm_out, _ = self.lstm(lstm_input)

        # get the scores for the most likely words
        word_outputs = self.hidden2vocab(lstm_out)
        #word_scores = F.log_softmax(word_outputs, dim=1)
        
        return word_outputs
        

    def sample(self, inputs, states=None, max_len=20):
        " accepts pre-processed image tensor (inputs) and returns predicted sentence (list of tensor ids of length max_len) "
        captions = []

        # initialize hidden state if not provided        
        hidden = states
        if not states:
            # The axes dimensions are (n_layers, batch_size, hidden_dim)
            hidden = (torch.randn(self.num_layers, 1, self.hidden_dim).to(inputs.device),
                      torch.randn(self.num_layers, 1, self.hidden_dim).to(inputs.device))

        for i in range(max_len):
            # first input to lstm is the image features
            lstm_out, hidden = self.lstm(inputs, hidden)
            # outputs shape (1, 1, vocab_size)
            outputs = self.hidden2vocab(lstm_out.squeeze(1))
                                    
            word_id = outputs.argmax(dim=1)
            # get the most probable word
            captions.append(word_id.item())
            
            # the next inputs are the words in the caption
            # so embedde the words
            inputs = self.word_embeddings(word_id).unsqueeze(1)
        return captions
            
            
