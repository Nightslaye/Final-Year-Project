import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def generate_paragraph(borough_data):

    # Multiply percentages by 100 and round to 2 decimal places
    percentage_4_5 = borough_data['Percentage of income on mortgage (4.5%)'].values[0] * 100
    percentage_8_6 = borough_data['Percentage of income on mortgage (8.6%)'].values[0] * 100

    paragraph = f"- The average price of a mortgage in {borough_data['Borough'].values[0]} is £{borough_data['Average Price'].values[0]:.2f}\n"
    paragraph += f"- It is suggested by {borough_data['Source_Deposit'].values[0]} that the recommended deposit is 20%. This means for {borough_data['Borough'].values[0]} you will need a deposit of £{borough_data['Recommended deposit 20%'].values[0]:.2f}.\n"
    # Insert line about household income
    # Potentitally more information
    paragraph += "- Mortgages have varying terms but this tool uses the assumption that your mortgage is:\n"
    paragraph += "  - 25 years\n"
    paragraph += "  - Fixed at 4.5% for 5 years\n"
    paragraph += "  - Increases to 8.6% for the last 20 years\n"
    paragraph += f"- With this in mind, your monthly payments would be £{borough_data['Est. Monthly payments (4.5% fixed 5 years)'].values[0]:.2f} for the first 5 years increasing to £{borough_data['Est. Monthly payments (8.6% 20 years)'].values[0]:.2f} for the last 20. People typically remortgage after the fixed term is over in order to achieve better interest rates so this *can* be looked at as the worst case scenario as it does not account for salary increase nor a better interest rate.\n"
    paragraph += f"- With this in mind, for the first 5 years, {percentage_4_5:.2f}% of your salary will go towards solely your mortgage with after tax (including student loan plan 2, NI and income tax). After the fixed term is up, it will increase to {percentage_8_6:.2f}%.\n"

    return paragraph

def compare_boroughs(borough1, borough2, file_path):
    # Read the Excel file into a pandas DataFrame
    df = pd.read_excel(file_path)

    # Filter data for the specified boroughs
    borough1_data = df[df['Borough'] == borough1]

    borough2_data = df[df['Borough'] == borough2]

    #print("Paragraph for Borough 1:")
    global para_1
    para_1 = generate_paragraph(borough1_data)
    #print(para_1)
    #print("\nParagraph for Borough 2:")
    global para_2
    para_2 = generate_paragraph(borough2_data)
    #print(para_2)

    # Set up seaborn style
    sns.set(style="darkgrid")

    # Plotting
    fig, axes = plt.subplots(3, 2, figsize=(12, 12))

    # Average Price comparison
    sns.barplot(x=[borough1, borough2],
                y=[borough1_data['Average Price'].values[0], borough2_data['Average Price'].values[0]], ax=axes[0, 0],
                hue=[borough1, borough2], palette="Blues_d", legend=False)
    axes[0, 0].set_title('Average Price Comparison', fontsize=14)
    axes[0, 0].set_ylabel('Average Price', fontsize=12)

    # Estimated Mortgage Required comparison
    sns.barplot(x=[borough1, borough2], y=[borough1_data['Est. Mortgage required'].values[0],
                                           borough2_data['Est. Mortgage required'].values[0]], ax=axes[0, 1],
                hue=[borough1, borough2], palette="Greens_d", legend=False)
    axes[0, 1].set_title('Estimated Mortgage Required Comparison', fontsize=14)
    axes[0, 1].set_ylabel('Estimated Mortgage Required', fontsize=12)

    # Estimated Household Salary Required comparison
    sns.barplot(x=[borough1, borough2], y=[borough1_data['Est. Household Salary required'].values[0],
                                           borough2_data['Est. Household Salary required'].values[0]],
                ax=axes[1, 0], hue=[borough1, borough2], palette="Reds_d", legend=False)
    axes[1, 0].set_title('Estimated Household Salary Required Comparison', fontsize=14)
    axes[1, 0].set_ylabel('Estimated Household Salary Required', fontsize=12)

    # Percentage of income on mortgage comparison (4.5%)
    sns.barplot(x=[borough1, borough2], y=[borough1_data['Percentage of income on mortgage (4.5%)'].values[0],
                                           borough2_data['Percentage of income on mortgage (4.5%)'].values[0]],
                ax=axes[1, 1], hue=[borough1, borough2], palette="Oranges_d", legend=False)
    axes[1, 1].set_title('Percentage of Income on Mortgage (4.5%) Comparison', fontsize=14)

    # Interest Rates comparison (5 years and 20 years) - Line plot
    axes[2, 0].plot(['5 Year Rate', '20 Year Rate'],
                    [borough1_data['Est. Monthly payments (4.5% fixed 5 years)'].values[0],
                     borough1_data['Est. Monthly payments (8.6% 20 years)'].values[0]], marker='o', color='purple',
                    label=borough1)
    axes[2, 0].plot(['5 Year Rate', '20 Year Rate'],
                    [borough2_data['Est. Monthly payments (4.5% fixed 5 years)'].values[0],
                     borough2_data['Est. Monthly payments (8.6% 20 years)'].values[0]], marker='o', color='orange',
                    label=borough2)
    axes[2, 0].set_title('Interest Rates Comparison', fontsize=14)
    axes[2, 0].set_ylabel('Estimated Monthly Payments', fontsize=12)
    axes[2, 0].legend()

    # Interest Rates comparison percentage (5 years and 20 years) - Line plot
    axes[2, 1].plot(['5 Year Rate', '20 Year Rate'],
                    [borough1_data['Percentage of income on mortgage (4.5%)'].values[0],
                     borough1_data['Percentage of income on mortgage (8.6%)'].values[0]], marker='o', color='purple',
                    label=borough1)
    axes[2, 1].plot(['5 Year Rate', '20 Year Rate'],
                    [borough2_data['Percentage of income on mortgage (4.5%)'].values[0],
                     borough2_data['Percentage of income on mortgage (8.6%)'].values[0]], marker='o', color='orange',
                    label=borough2)
    axes[2, 1].set_title('Interest Rates Comparison (Percentage)', fontsize=14)
    axes[2, 1].set_ylabel('Percentage of Income on Mortgage (%)', fontsize=12)
    axes[2, 1].legend()

    # Adjust layout
    plt.tight_layout()
    plt.savefig(borough1+"_"+borough2+"_"+'comparison_chart.png')
    #plt.show()


# Example usage:
file_path = 'Mortgage_Data.xlsx'

#borough1 = input("Enter first borough name: ")
#borough2 = input("Enter second borough name: ")

#compare_boroughs(borough1, borough2, file_path) #replace borough1 & 2 with inputted values from folium_test
