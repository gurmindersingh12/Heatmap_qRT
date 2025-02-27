import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load Data
expression_data = pd.read_csv("expression_data.csv")
p_values = pd.read_csv("p_values.csv")

# Define time points order and treatment colors
time_order = ["0hpi", "12hpi", "24hpi", "48hpi", "72hpi"]
treatment_colors = {"B": "#d73027", "Y": "#4575b4", "D": "#74add1", "N": "#fdae61"}
legend_labels = {"B": "Ptr ToxB", "Y": "YPD", "D": "Water", "N": "NIC"}

# Set up figure
fig, ax = plt.subplots(figsize=(12, 6))
bar_width = 0.2
x = np.arange(len(time_order))
bar_positions = {}

# Plot bars with error bars
for i, (treatment, label) in enumerate(legend_labels.items()):
    subset = expression_data[expression_data['Treatment'] == treatment]
    bars = ax.bar(x + i * bar_width, subset['Expression'], width=bar_width, label=label,
                  color=treatment_colors[treatment],
                  yerr=[subset['Expression'] - subset['Exp. Lower Error Bar'], 
                        subset['Exp. Upper Error Bar'] - subset['Expression']],
                  capsize=5, error_kw={'elinewidth': 1.5, 'capthick': 1.5})
    bar_positions[treatment] = bars

# Annotate significance
annotated_pairs = {}
spacing_factor = 0.08
for _, row in p_values.iterrows():
    time_idx = time_order.index(row['Time1'])
    t1, t2 = row['Treatment1'], row['Treatment2']
    stars = row['Stars']
    
    if t1 in bar_positions and t2 in bar_positions:
        x1 = x[time_idx] + list(legend_labels.keys()).index(t1) * bar_width
        x2 = x[time_idx] + list(legend_labels.keys()).index(t2) * bar_width
        y_max = max(expression_data.loc[(expression_data['Time'] == row['Time1']) & 
                                        (expression_data['Treatment'].isin([t1, t2]))]['Exp. Upper Error Bar']) * 1.1
        
        key = (row['Time1'], min(x1, x2), max(x1, x2))
        if key in annotated_pairs:
            y_max += annotated_pairs[key] * spacing_factor
            annotated_pairs[key] += 1
        else:
            annotated_pairs[key] = 1
        
        line_y = y_max + 0.08
        ax.plot([x1, x1, x2, x2], [line_y, line_y + 0.05, line_y + 0.05, line_y], color='black', lw=1)
        ax.text((x1 + x2) / 2, line_y + 0.05, stars, ha='center', fontsize=12, fontweight='bold', color='black')

# Customize plot
ax.set_xticks(x + bar_width * 1.5)
ax.set_xticklabels(time_order, color='black', fontsize=14)
ax.set_xlabel("Time Points (hpi; hours post-infiltration)", fontsize=18, fontweight='bold', color='black', labelpad=14)
ax.set_ylabel("Expression Level", fontsize=18, fontweight='bold', color='black', labelpad=14)

# Legend settings
legend = ax.legend(title="Treatments", fontsize=14, title_fontsize=16, facecolor='white', edgecolor='black', frameon=True)
legend.get_title().set_fontweight('bold')
for text in legend.get_texts():
    text.set_color("black")

# Remove gridlines and title
ax.grid(False)
ax.set_title("")
ax.tick_params(axis='both', colors='black')

# Save plot in SVG and TIFF formats
plt.savefig("expression_plot.svg", format="svg", dpi=600)
plt.savefig("expression_plot.tiff", format="tiff", dpi=600)

# Show plot
plt.show()
