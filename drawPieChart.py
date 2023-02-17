import numpy as np
import matplotlib.pyplot as plt

# # Data for the pie chart
# labels = ['2', '3', '4', '5', '6', '7']
# sizes = [340, 269, 186, 66, 13, 4]
colors = ['#F652A0', '#001065', '#C23899', '#8A268D', '#51197C' ,'#C23899']

# # Create the pie chart
# fig1, ax1 = plt.subplots()
# ax1.pie(sizes,labels=labels, labeldistance=0.6, colors=colors, autopct='%1.1f%%',pctdistance=1.4, startangle=90, counterclock=False)

# # Add a title to the chart
# ax1.set_title("Depth of Bloated Transitive Dependencies")

# # Display the chart
# plt.show()

fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

recipe = ["2:  38.7%",
          "7:  0.5%",
          "3:  30.6%",
          "4:  21.2%",
          "5:  7.5%",
          "6:  1.5%",
]

data = [340, 4, 269, 186, 66, 13]

wedges, texts = ax.pie(data, colors=colors, wedgeprops=dict(width=0.5), startangle=-20)

bbox_props = dict(fc="w", ec="k", lw=0.72)
kw = dict(arrowprops=dict(arrowstyle="-"),
          bbox=bbox_props, zorder=0, va="center")

for i, p in enumerate(wedges):
    ang = (p.theta2 - p.theta1)/2. + p.theta1
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))
    horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
    connectionstyle = f"angle,angleA=0,angleB={ang}"
    kw["arrowprops"].update({"connectionstyle": connectionstyle})
    ax.annotate(recipe[i], xy=(x, y), xytext=(1.5*np.sign(x), 1.4*y),
                horizontalalignment=horizontalalignment, **kw)

ax.set_title("Depth of Bloated Transitive Dependencies", y=1.2)

plt.show()