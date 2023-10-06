from datetime import datetime

import matplotlib.pyplot as plt
import openpyxl


def plotCreator(threadTimes):
    # Assuming threadTimes is a list of (x, y) pairs
    # Extract keys and corresponding value3
    keys = list(threadTimes.keys())
    value3 = [item[2] for item in threadTimes.values()]

    # Create a new Excel workbook and select the active sheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    for index, value in enumerate(value3, start=1):
        sheet.cell(row=index, column=1, value=value)  # Write each value to a separate column in the first row
    # workbook.save("excel/times of %2d users %2d.xlsx" % len(value3), % str(datetime.now()))
    current_time = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    workbook.save(f"excel/times of {len(value3)} users {current_time}.xlsx")

    # Create a bar plot
    plt.plot(range(len(value3)), value3, '1', color='black')  # bar for bar plot
    # Set x-ticks to display sorted keys
    # plt.xticks([keys[0], keys[-1]])
    # # Set x-ticks to display sorted keys
    # plt.yticks()
    # Set labels for the x and y axes
    plt.xlabel('Users simultaneous accessing Firebase')
    plt.ylabel('Response time in seconds')

    # Set a title for the plot
    plt.title('Social Firebase Database Response Times')

    plt.savefig(f"plots/times of {len(value3)} users {current_time}.png", dpi=300, bbox_inches='tight')
    # Show the plot
    plt.show()
