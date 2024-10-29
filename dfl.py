import torch
import torch.nn as nn
import torch.optim as optim
import copy

# Define a simple model
class SimpleModel(nn.Module):
    def __init__(self):
        super(SimpleModel, self).__init__()
        self.fc = nn.Linear(10, 1)
    
    def forward(self, x):
        return self.fc(x)

# Function to train model on local data
def train_local(model, data, epochs=5):
    optimizer = optim.SGD(model.parameters(), lr=0.01)
    criterion = nn.MSELoss()
    
    for _ in range(epochs):
        optimizer.zero_grad()
        outputs = model(data)
        loss = criterion(outputs, torch.ones_like(outputs))
        loss.backward()
        optimizer.step()
    
    return model

# Function to average models
def average_models(models):
    averaged_model = copy.deepcopy(models[0])
    for param in averaged_model.parameters():
        param.data.zero_()
    
    for model in models:
        for param, avg_param in zip(model.parameters(), averaged_model.parameters()):
            avg_param.data += param.data / len(models)
    
    return averaged_model

# Simulate decentralized federated learning
def decentralized_federated_learning(num_nodes, rounds):
    # Initialize models for each node
    node_models = [SimpleModel() for _ in range(num_nodes)]
    
    # Simulate data for each node
    node_data = [torch.randn(100, 10) for _ in range(num_nodes)]
    
    for round in range(rounds):
        print(f"Round {round + 1}")
        
        # Train local models
        for i in range(num_nodes):
            node_models[i] = train_local(node_models[i], node_data[i])
        
        # Simulate peer-to-peer communication and model averaging
        for i in range(num_nodes):
            # Randomly select peers to communicate with
            peers = torch.randperm(num_nodes)[:3].tolist()
            peer_models = [node_models[j] for j in peers if j != i]
            peer_models.append(node_models[i])
            
            # Average models with peers
            node_models[i] = average_models(peer_models)
    
    return node_models

# Run decentralized federated learning
final_models = decentralized_federated_learning(num_nodes=5, rounds=10)
