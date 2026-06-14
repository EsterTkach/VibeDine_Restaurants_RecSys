import pickle
with open("models/cf_model.pkl", "rb") as f:
    model = pickle.load(f)
    


print(model.keys())

print(type(model["user_item_matrix"]))
print(type(model["item_user_matrix"]))

print(model["user_item_matrix"].shape)
print(model["item_user_matrix"].shape)