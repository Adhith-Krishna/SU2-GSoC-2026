import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('results/history.csv', skipinitialspace=True)
df.columns = df.columns.str.strip().str.replace('"','')

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

axes[0].plot(df['Inner_Iter'], df['rms[P]'])
axes[0].set_xlabel('Iteration')
axes[0].set_ylabel('rms[P]')
axes[0].set_title('Pressure residual')
axes[0].grid(True)

axes[1].plot(df['Inner_Iter'], df['rms[k]'])
axes[1].set_xlabel('Iteration')
axes[1].set_ylabel('rms[k]')
axes[1].set_title('TKE residual')
axes[1].grid(True)

axes[2].plot(df['Inner_Iter'], df['rms[w]'])
axes[2].set_xlabel('Iteration')
axes[2].set_ylabel('rms[w]')
axes[2].set_title('Dissipation residual')
axes[2].grid(True)

plt.tight_layout()
plt.savefig('results/plots/convergence.png', dpi=150)
print("Saved convergence.png")
