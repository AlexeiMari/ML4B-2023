### einzelne Grafik je nach Filter
activity_filter = st.selectbox("Select the Activity", pd.unique(df["Aktivität"]))
df_selection = df[df["Aktivität"] == activity_filter]
if activity_filter == 'Laufen':
    bar_laufen = px.bar(
    df_selection,
    x='Aktivität',
    orientation='v',
    title='Aktivitäten',
    color_discrete_sequence=['#2ECC71'],
    template='plotly_white'
    )
    st.plotly_chart(bar_laufen)
elif activity_filter == 'Idle':
    bar_idle = px.bar(
    df_selection,
    x='Aktivität',
    orientation='v',
    title='Aktivitäten',
    color_discrete_sequence=['#2ECC71'],
    template='plotly_white'
    )
    st.plotly_chart(bar_idle)
elif activity_filter == 'U-Bahn':
    bar_ubahn = px.bar(
    df_selection,
    x='Aktivität',
    orientation='v',
    title='Aktivitäten',
    color_discrete_sequence=['#2ECC71'],
    template='plotly_white'
    )
    st.plotly_chart(bar_ubahn)
elif activity_filter == 'Auto':
    bar_auto = px.bar(
    df_selection,
    x='Aktivität',
    orientation='v',
    title='Aktivitäten',
    color_discrete_sequence=['#2ECC71'],
    template='plotly_white'
    )
    st.plotly_chart(bar_auto)
elif activity_filter == 'Fahrrad':
    bar_fahrrad = px.bar(
    df_selection,
    x='Aktivität',
    orientation='v',
    title='Aktivitäten',
    color_discrete_sequence=['#2ECC71'],
    template='plotly_white'
    )
    st.plotly_chart(bar_fahrrad)



### Balkendiagramm für die gemockten Daten

df = pd.DataFrame(data)  # DataFrame mit Aktivitäten und Reihenfolge

# Aktivitäten und Farben
aktivitaeten = df['Aktivität'].unique()
farben = ['#3D7A3F', '#EB7A27', '#B4393C', '#FBB024', '#7A5803']

# Erstellen der Figure und Axes
fig, ax = plt.subplots()

# Schleife über die Aktivitäten
startpunkt = 0
bar_hoehe = 0.01
for idx, aktivitaet in enumerate(aktivitaeten):
    farbe = farben[idx]
    
    # Zählen der Häufigkeit der Aktivität
    haeufigkeit = df[df['Aktivität'] == aktivitaet].shape[0]

    # Beschriftung der Aktivität
    mittelpunkt = startpunkt + haeufigkeit / 2
    ax.text(mittelpunkt, bar_hoehe, aktivitaet, ha='center', va='bottom', color='white')

    # Anzahl der Aktivitäten innerhalb des Balkens
    ax.text(startpunkt + 0.5 * haeufigkeit, bar_hoehe / 2, str(haeufigkeit), ha='center', va='center', color='white')
    
    # Einfärben des Strahls entsprechend der Häufigkeit
    ax.bar(startpunkt, bar_hoehe, width=haeufigkeit, color=farbe, align='edge')
    
    # Aktualisierung des Startpunkts für die nächste Aktivität
    startpunkt += haeufigkeit

# Anpassung der Achsen
ax.set_xlim(0, startpunkt)
ax.set_ylim(0,0)
ax.axis('off')

st.pyplot(fig)



#fortbewegungsgraph

        st.subheader("Dein Fortbewegungsgraph")
        output_string = ""
        import graphviz
        graph = graphviz.Digraph()
        i = 0
        if len(prediction_data) > 1:
            while i < len(prediction_data) -1:
                graph.edge((prediction_data[i][0] + " " + str(prediction_data[i][1]) + " min"), (prediction_data[i+1][0] + " " + str(prediction_data[i+1][1]) + " min"))
                i += 1
            graph.edge(prediction_data[i][0] + " " + str(prediction_data[i][1]) + " min", "End")
        else:
            graph.edge(prediction_data[i][0] + " " + str(prediction_data[i][1]) + " min", "End")
        #st.write(output_string)
        graph.attr(bgcolor="#282C34")
        graph.node_attr.update(style='filled', color='white', fontcolor='black')  # Kreise weiß einfärben
        graph.edge_attr.update(color='white')  # Pfeile weiß einfärben
        st.graphviz_chart(graph)
