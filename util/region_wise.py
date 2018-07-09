import pandas as pd
path = r'./x_y.csv'

data = pd.read_csv(path)
print(data.head(1))

ctr = {}
for i in range(13894):
    try:
        ctr[data.loc[i]['region']] += 1
    except:
        ctr[data.loc[i]['region']] = 1

df = pd.DataFrame(data={"region": list(ctr.keys()), "total": list(ctr.values())})
df.to_csv("./region_wise.csv", sep=',',index=False)
