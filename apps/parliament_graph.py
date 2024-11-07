import math
import matplotlib.pyplot as plt
import pandas as pd

# Function to sort tuples based on their second element
def Sort_Tuple(tup):
    return sorted(tup, key=lambda x: x[1])

def parlamentary_Coord(df, angle_total=210, rows=9, ratio=7, initial='NAME'):
    arco_total = 0
    angles = []
    for i in range(rows):
        arco_total += math.pi * int(ratio + i)
    for i in range(rows):
        arco_radio = math.pi * int(ratio + i)
        angles.append(angle_total / round(arco_radio / (arco_total / len(df)), 0))
    coord = []
    for a in range(len(angles)):
        current_angle = angles[a] / 2
        for i in range(int(round(angle_total / angles[a], 0))):
            coord.append((ratio + a, current_angle))
            current_angle += angles[a]
    coord = Sort_Tuple(coord)
    # Ensure the lengths match exactly with the DataFrame length
    coord = coord[:len(df)]
    df["radio"] = [x[0] for x in coord]
    df["tetha"] = [x[1] for x in coord]
    df["INITIAL"] = df[initial].apply(lambda x: x[0]) # Only for text in marker chart
    return df

# Function to adjust seat counts dynamically to match the exact number required
def adjust_seat_distribution(seat_distribution, target_seats):
    current_seats = sum(seat_distribution.values())
    while current_seats != target_seats:
        difference = target_seats - current_seats
        key_to_adjust = max(seat_distribution, key=seat_distribution.get)
        seat_distribution[key_to_adjust] += difference
        current_seats = sum(seat_distribution.values())
        return seat_distribution

def parliament_graph_generator(positive_value, target_seats):
    # Scaling the seat distribution to fit a target of 648 seats
    seat_distribution = {
     'Positive': int(round(positive_value / (target_seats+2) * target_seats)),
     'Negative': int(round((target_seats-positive_value) / (target_seats+2) * target_seats))
    }

    # Adjust the seat distribution to exactly match the target number of seats
    seat_distribution = adjust_seat_distribution(seat_distribution, target_seats)

    # Color mapping for the parties
    party_colors = {
     'Negative': '#DC241F',
     'Positive': '#6AB023',
    }

    # Generating the dataset based on the adjusted seat distribution
    data = {
     'NAME': [],
     'PARTY': [],
     'COLOR': []
    }

    # Fill the data dictionary with repeated party entries based on seat counts
    for party, seats in seat_distribution.items():
        for i in range(int(seats)):
            data['NAME'].append(f"{party[:1]}{i+1}")
            data['PARTY'].append(party)
            data['COLOR'].append(party_colors[party])

    # Create DataFrame
    df = pd.DataFrame(data)
    # Sort the data by party to ensure correct grouping in the chart
    df = df.sort_values(by=['PARTY'], ascending=True)
    # Apply parliamentary coordinates function with 9 rows
    df = parlamentary_Coord(df, angle_total=210, rows=9, ratio=6)
    # Convert angles to radians for Matplotlib
    df['theta'] = df['tetha'].apply(lambda x: math.radians(x))
    # Plotting with Matplotlib
    plt.figure(figsize=(23.4, 18.2)) # Increased figure size to make the chart larger
    ax = plt.subplot(111, polar=True)
    # Scatter plot with increased marker size and no edge color
    scatter = ax.scatter(df['theta'], df['radio'], c=df['COLOR'], s=300, edgecolors=None, alpha=.75)
    # Marker size increased by 30%

    # Add labels to seats with initials
    for idx, row in df.iterrows():
        ax.text(row['theta'], row['radio'], row['INITIAL'], ha='center', va='center', fontsize=7,color='black')
    # Adjust the plot appearance for better visual balance
    ax.set_ylim(0, max(df['radio']) + 1)
    ax.set_yticklabels([]) # Remove radial axis labels
    ax.set_xticklabels([]) # Remove angular axis labels
    ax.grid(False) # Remove grid lines




    ax.spines['polar'].set_visible(False) # Remove polar spine
    # Correct the chart orientation to match Plotly's alignment
    ax.set_theta_offset(math.radians(345)) # Adjust the angle to make it symmetrical
    # Add a legend to show party colors
    handles = [plt.Line2D([0], [0], marker='o', color='w', label=party, markersize=15, markerfacecolor=color) for party, color in party_colors.items()]
    plt.legend(handles=handles, loc='upper right', bbox_to_anchor=(1.2, 1), fontsize=12,
    frameon=False) # Increased fontsize to 12
    # Title and display
    plt.title('Parliamentary Chart', va='bottom', fontsize=16)

    return plt