import fastf1 as f1
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns


# session = f1.get_session(2024, "Japan", "Qualifying")
# lap_info = session.load(weather=False, telemetry=False)

#Qualifying Session Load
Q_session = f1.get_session(2024, "Monza", "Q")
Q_session.load(telemetry=False, laps=False, weather=False)
df_qualifying = Q_session.results[["Abbreviation", "Position"]]
df_qualifying.rename(columns={"Position" : "QPosition"}, inplace = True)

#Race Session Load
R_session = f1.get_session(2024, "Monza", "Race")
R_session.load(telemetry=False, laps=False, weather=False)
df_Race = R_session.results[["TeamName", "Abbreviation", "Position", "Status"]]

#Combined DataFrame
df_mixed = pd.merge(df_Race, df_qualifying, on='Abbreviation')
print(df_mixed)

#Plot:
#To set only 2 markers, grouped by team.
df_mixed['DriverMarker'] = df_mixed.groupby('TeamName').cumcount()

#For 1 unit length grid line:
x_min, x_max = int(df_mixed['QPosition'].min()), int(df_mixed['QPosition'].max())
y_min, y_max = int(df_mixed['Position'].min()), int(df_mixed['Position'].max())

# plt.style.use('ggplot')
plt.figure(figsize=(10, 7))
sns.scatterplot(
    data=df_mixed,
    x="QPosition",
    y="Position",
    hue="TeamName",          
    style="DriverMarker", 
    s=100,                   
    edgecolor="black"        
)

#Invert axises since negative correlation between best place and position 
#e.x. 1st is the best position but smallest in terms of integer
plt.gca().invert_xaxis()
plt.gca().invert_yaxis()

plt.title("Qualifying vs Race Results - Monza 2024")
plt.xlabel("Qualifying Position")
plt.ylabel("Race Finish Position")
plt.grid(True)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small', title="Driver/Team")
plt.tight_layout()
plt.xticks(range(x_min, x_max + 1))
plt.yticks(range(y_min, y_max + 1))
plt.show()
