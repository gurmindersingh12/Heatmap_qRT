import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# -------------------------
# 1. Load the Data
# -------------------------
# Read the CSV file containing p-values for treatment comparisons
file_path = "QPCR-results-p-values.csv"  # Ensure this file is in the same directory
p_values = pd.read_csv(file_path)

# -------------------------
# 2. Data Processing
# -------------------------
# Rename the column containing -log10(p-value) for consistency
p_values.rename(columns={"[-log10(p-value)]": "-log10(P-Value)"}, inplace=True)

# Pivot the dataset to create a matrix format suitable for heatmap visualization
heatmap_data = p_values.pivot(index="Group1", columns="Group2", values="-log10(P-Value)")

# -------------------------
# 3. Generate the Heatmap
# -------------------------
# Create the heatmap using Seaborn
fig, ax = plt.subplots(figsize=(10, 6))  # Adjust figure size
sns.heatmap(heatmap_data, cmap="coolwarm", annot=True, fmt=".2f", linewidths=0.5, 
            cbar_kws={"label": r"$-\log_{10}$(P-Value)"}, annot_kws={"size": 6}, ax=ax)  # Heatmap customization

# -------------------------
# 4. Customize Labels and Save Plot
# -------------------------
# Set axis labels
ax.set_xlabel("Treatment Groups", fontsize=14, fontweight='bold', color='black', labelpad=8)
ax.set_ylabel("Treatment Groups", fontsize=14, fontweight='bold', color='black', labelpad=8)

# Rotate x-axis labels for better readability
plt.xticks(rotation=90)

# Adjust layout to ensure labels are not cut off
plt.tight_layout()

# -------------------------
# 5. Save the Heatmap as SVG
# -------------------------
output_svg = "heatmap_p_values.svg"  # Output file name
plt.savefig(output_svg, format="svg", dpi=300, bbox_inches="tight")  # Save in high quality

# Show the plot
plt.show()

# Print confirmation message
print(f"Heatmap saved successfully as: {output_svg}")
