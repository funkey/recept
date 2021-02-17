from recept import evaluate, read_events, smooth, model_filter
import numpy as np
import sys
import torch

if __name__ == '__main__':

    filename_train = sys.argv[1]
    filename_test = sys.argv[2]

    events = read_events(filename_train)
    gold_standard = smooth(events, 7, 5)

    input_size = 8
    batch_size = 32
    num_epochs = 10
    nonlinearity = torch.nn.ReLU

    X = np.array([
        events.x[i:i + input_size].astype(np.float32)
        for i in range(len(events.x) - input_size)
    ])
    Y = gold_standard.x[input_size:].astype(np.float32)

    # normalize data
    mean = np.mean(X, axis=1)
    for i in range(input_size):
        X[:,i] -= mean
    Y -= mean
    Y = np.expand_dims(Y, axis=1)

    dataset = list(zip(X, Y))

    dataloader = torch.utils.data.DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=True)

    model = torch.nn.Sequential(
        torch.nn.Linear(input_size, 128),
        nonlinearity(),
        torch.nn.Linear(128, 64),
        nonlinearity(),
        torch.nn.Linear(64, 32),
        nonlinearity(),
        torch.nn.Linear(32, 1)
    )

    loss = torch.nn.MSELoss()

    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)


    for epoch in range(num_epochs):

        running_loss = 0.0

        for i, (x, y) in enumerate(dataloader):
            optimizer.zero_grad()
            y_pred = model(x)
            l = loss(y_pred, y)
            l.backward()
            optimizer.step()
            running_loss += l.item()
            if (i % 10) == (10 - 1):
                print(f"{epoch}/{i}: {np.sqrt(l.item())}")
                running_loss = 0.0

    model.eval()
    # model_filtered = model_filter(events, model, input_size)
    # evaluate(model_filtered, gold_standard, show_plot=True, show_events=events)

    events = read_events(filename_test)
    gold_standard = smooth(events, 7, 5)
    model_filtered = model_filter(events, model, input_size)
    evaluate(model_filtered, gold_standard, show_plot=True, show_events=events)
