# type: ignore
# flake8: noqa
#
#
#
#
#
#
#
#
#
#
#
#
#
# Setup and data loading
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

# Set Data file path
data_file = "../input/children-in-cci/data.xlsx"

# Set Map file path
shp_file = "../input/west-bengal-district-shape-files/District_shape_West_Bengal.shp"

# Set style
sns.set_theme(style="white")

```
#
#
#
# Read the Excel file (assuming the file is in the working directory)
df_cci_count = pd.read_excel(data_file, sheet_name="CCI_Count")

# Load the shapefile for West Bengal
west_bengal_map = gpd.read_file(shp_file)

# Merge the West Bengal map with the CCI data
merged_df = west_bengal_map.merge(df_cci_count, left_on = "NAME", right_on = "District")

# Calculate the "Homes" total and create a custom label for each district
merged_df["Homes"] = (
    merged_df["Children Home"] +
    merged_df["Children Home CWSN"] +
    merged_df["Observation Home"] +
    merged_df["Special Home/ Place of Safety"]
)

# Reproject the data to UTM Zone 45N (EPSG:32645)
merged_df = merged_df.to_crs(epsg = 32645)

# Calculate Total
merged_df["Total"] = (
    merged_df["Homes"] + 
    merged_df["Specialized Adoption Agency"] + 
    merged_df["Open Shelter"]
)
merged = merged_df

# Plotting
fig, ax = plt.subplots(figsize=(12, 16))
merged.plot(
    column='Total',
    cmap='Blues',
    edgecolor='black',
    linewidth=0.3,
    ax=ax,
    legend=False,
    legend_kwds={'label': "No. of CCIs", 'orientation': "horizontal", 'pad': 0.01}
)

# Add labels
for idx, row in merged.iterrows():
    label = f"{row['NAME']}\nHomes: {int(row['Homes'])}\nSAA: {int(row['Specialized Adoption Agency'])}\nOS: {int(row['Open Shelter'])}"
    plt.annotate(text=label, xy=(row.geometry.centroid.x, row.geometry.centroid.y),
        horizontalalignment='center', fontsize=10, fontweight='bold', color='black')

ax.set_axis_off()
plt.title(
    "District-wise Distribution of PAB Approved CCI Units in West Bengal\nData as of September 2024", 
    fontsize=15,
    fontweight='bold',
    color='#2c3e50'
)
plt.show()
#
#
#
#
#
# Read the Excel file with sheet name specified (assuming the file is in the working directory)
df_child_category <- read_excel(data_file, sheet = "Child_Category")

# Calculate percentage of occupancy
df_child_category <- df_child_category %>%
    mutate(perc = `No. of Children` / sum(`No. of Children`)) %>%
    mutate(labels = scales::percent(perc))

# Set the figure size
options(repr.plot.width = 12, repr.plot.height = 10)

# Create the pie chart
ggplot(df_child_category, aes(x = "", y = `No. of Children`, fill = Category)) +
    geom_bar(stat = "identity", width = 1, color = "white") + # Add white borders for clarity
    coord_polar("y", start = 0) +
    theme_void() + # Use a minimal theme
    geom_label(
        aes(label = labels),
        position = position_stack(vjust = 0.5),
        size = 8, # Increase label size
        color = "black", # White text for better contrast
        fontface = "bold", # Bold text
        show.legend = FALSE # Hide labels from legend
    ) +
    scale_fill_brewer(palette = "Set3") + # Use a colorblind-friendly palette
    labs(
        title = "Category of Children",
        subtitle = "Distribution of Children by Category", # Add a subtitle
        fill = "Category" # Legend title
    ) +
    theme(
        plot.title = element_text(hjust = 0.5, size = 18, face = "bold", color = "#2c3e50"), # Customize title
        plot.subtitle = element_text(hjust = 0.5, size = 12, color = "#7f8c8d"), # Customize subtitle
        plot.caption = element_text(hjust = 1, size = 10, color = "#7f8c8d"), # Customize caption
        legend.position = "right", # Place legend on the right
        legend.title = element_text(size = 12, face = "bold"), # Customize legend title
        legend.text = element_text(size = 10) # Customize legend text
    )
#
#
#
#
#
# Read the excel file with sheet name for children under purview
df_child_purview <- read_excel(data_file, sheet = "PurviewCCI")

# Reshape the data for ggplot2 (convert to long format)
df_long <- df_child_purview %>%
    pivot_longer(cols = c(Girls, Boys, Total), names_to = "Category", values_to = "Count")

# Create the bar chart
ggplot(df_long, aes(x = as.factor(FY), y = Count, fill = Category)) +
    geom_bar(stat = "identity", position = "dodge", width = 0.4) + # Use "dodge" to place bars side by side
    coord_flip() +
    labs(
        title = "Children Facilitated through Govt. & NGO run Homes",
        x = "",
        y = "",
        fill = "Category"
    ) +
    theme_minimal() + # Use a minimal theme
    theme(
        plot.title = element_text(hjust = 0.5, size = 16, face = "bold"), # Center and style the title
        axis.text.x = element_text(size = 12), # Adjust x-axis text size
        axis.text.y = element_text(size = 12), # Adjust y-axis text size
        legend.position = "bottom" # Place the legend at the top
    )
#
#
#
#
#
# Read the excel file with sheet name for children under purview
df_formal_edu <- read_excel(data_file, sheet = "FormalEdRatio")
df_formal_edu <- mutate(df_formal_edu, percentage = scales::percent(average))

# Create the line graph
ggplot(df_formal_edu, aes(x = FY, y = average, group = 1)) +
    geom_line(color = "#1f78b4", linewidth = 1.5) + # Use a blue color for the line
    geom_point(color = "#33a02c", size = 4) + # Use a green color for the points
    geom_text(
        aes(label = percentage),
        size = 4,
        color = "black",
        fontface = "bold" # Make labels bold
    ) +
    labs(
        title = "Average Percentage of Children (6-18 Years) Enrolled in Formal Education",
        subtitle = "Data from Financial Year 2017-18 to 2023-24", # Add a subtitle
        x = "Financial Year",
        y = NULL # Remove y-axis label
    ) +
    theme_minimal() + # Use a minimal theme
    theme(
        plot.title = element_text(hjust = 0.5, size = 12, face = "bold", color = "#2c3e50"), # Customize title
        plot.subtitle = element_text(hjust = 0.5, size = 10, color = "#7f8c8d"), # Customize subtitle
        plot.caption = element_text(hjust = 1, size = 10, color = "#7f8c8d"), # Customize caption
        axis.text.x = element_text(size = 8, color = "#2c3e50"), # Customize x-axis text
        axis.text.y = element_blank(), # Remove y-axis text
        axis.title.y = element_blank(), # Remove y-axis title
        axis.ticks.y = element_blank(), # Remove y-axis ticks
        axis.line.y = element_blank(), # Remove y-axis line
        panel.grid.major.x = element_line(color = "#bdc3c7", linetype = "dotted"), # Add dotted grid lines for x-axis
        panel.grid.minor.x = element_blank(), # Remove minor x-axis grid lines
        panel.grid.major.y = element_blank(), # Remove major y-axis grid lines
        panel.grid.minor.y = element_blank(), # Remove minor y-axis grid lines
        legend.position = "bottom", # Place the legend at the bottom
        plot.background = element_rect(fill = "#f0f0f0", color = NA), # Light gray background
        panel.background = element_rect(fill = "white", color = NA) # White panel background
    )
#
#
#
#
#
# Read the excel file with sheet name for children under purview
df_vocational_edu <- read_excel(data_file, sheet = "VocationalTraining")
df_vocational_edu <- mutate(df_vocational_edu, percentage = scales::percent(average))

# Create the line graph
ggplot(df_vocational_edu, aes(x = FY, y = average, group = 1)) +
    geom_line(color = "#1f78b4", linewidth = 1.5) + # Use a blue color for the line
    geom_point(color = "#33a02c", size = 4) + # Use a green color for the points
    geom_text(
        aes(label = percentage),
        size = 4,
        color = "black",
        fontface = "bold" # Make labels bold
    ) +
    labs(
        title = "Average Percentage of Children (above 11 years) Enrolled in Vocational Training",
        subtitle = "Data from Financial Year 2017-18 to 2023-24", # Add a subtitle
        x = "Financial Year",
        y = NULL # Remove y-axis label
    ) +
    theme_minimal() + # Use a minimal theme
    theme(
        plot.title = element_text(hjust = 0.5, size = 12, face = "bold", color = "#2c3e50"), # Customize title
        plot.subtitle = element_text(hjust = 0.5, size = 10, color = "#7f8c8d"), # Customize subtitle
        plot.caption = element_text(hjust = 1, size = 10, color = "#7f8c8d"), # Customize caption
        axis.text.x = element_text(size = 8, color = "#2c3e50"), # Customize x-axis text
        axis.text.y = element_blank(), # Remove y-axis text
        axis.title.y = element_blank(), # Remove y-axis title
        axis.ticks.y = element_blank(), # Remove y-axis ticks
        axis.line.y = element_blank(), # Remove y-axis line
        panel.grid.major.x = element_line(color = "#bdc3c7", linetype = "dotted"), # Add dotted grid lines for x-axis
        panel.grid.minor.x = element_blank(), # Remove minor x-axis grid lines
        panel.grid.major.y = element_blank(), # Remove major y-axis grid lines
        panel.grid.minor.y = element_blank(), # Remove minor y-axis grid lines
        legend.position = "bottom", # Place the legend at the bottom
        plot.background = element_rect(fill = "#f0f0f0", color = NA), # Light gray background
        panel.background = element_rect(fill = "white", color = NA) # White panel background
    )
#
#
#
