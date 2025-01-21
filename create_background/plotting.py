import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Data
data = {
    "Weapon": [
        "AK Rifle", "Sniper", "SMG", "AR Rifle", "VEK", "SCAR", "Shotgun",
        "Hunting", ".50 Cal Sniper", "VSS", "LMG", "Minigun", "Tactical Shotgun",
        "Crossbow", "Revolver", "Pistol", "Grenade", "Knife", "RPG", "Air Strike",
        "BGM", "Fists", "Rubber Chicken", "Laser Trip Mine", "G. Launcher",
        "Homing", "MG Turret", "Tank Minigun", "Heli Minigun"
    ],
    "Count": [
        27599, 20920, 11984, 10898, 10023, 10005, 7247, 6316, 6266, 6254,
        6144, 6062, 6026, 6017, 6007, 2374, 2275, 2251, 1535, 1082, 804,
        676, 286, 153, 124, 103, 71, 22, 10
    ]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Sort data by count
df = df.sort_values(by="Count", ascending=False)

# Set up the figure
plt.figure(figsize=(10, 8))
sns.set_theme(style="darkgrid")

# Plot a horizontal bar chart
sns.barplot(
    x="Count", 
    y="Weapon", 
    data=df, 
    palette="Purples_r"
)

# Add labels and title
plt.title("Weapon Usage Statistics", fontsize=16)
plt.xlabel("Count", fontsize=12)
plt.ylabel("Weapon", fontsize=12)

# Show the plot
plt.tight_layout()
plt.show()