import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime
import tabulate
import matplotlib.ticker as ticker


# required files
url_bundestag = "members_party_DOB.csv"
url_regierung = "bundesregierung.csv"
# url_germanPopulation = "https://service.destatis.de/bevoelkerungspyramide/data/15_bevoelkerungsvorausberechnung_daten.csv"
url_germanPopulation = "15_bevoelkerungsvorausberechnung_daten.csv" # local file

# members of parliament with DOB
membersOfParliament = pd.read_csv(url_bundestag)

# defining ages from date of birth
membersOfParliament["age"]=-(membersOfParliament["DOB year"]-datetime.today().year)
membersOfParliament.drop("Unnamed: 0",axis=1,inplace=True)

# members of Bundesregierung
bundesregierung = pd.read_csv(url_regierung)[["Partei","DOB"]]
bundesregierung["age"]=datetime.today().year-bundesregierung["DOB"]

# population of Germany by age
population_de_raw = pd.read_csv(url_germanPopulation,sep=";")
pop_2021 = pd.DataFrame([population_de_raw.iloc[142],
                         population_de_raw.iloc[143]]).transpose().iloc[4:].reset_index()
pop_2021["age"] = np.arange(100)
pop_2021["population"] = pop_2021[142] + pop_2021[143]
pop_2021.drop(["index",142,143],axis=1,inplace=True)

# defining some names and colors and font sizes
party_colors = {'CDU/CSU':'#151518',
                'AfD':'#00A2DE',
                'SPD':'#e3000f',
                'Bündnis 90/Die Grünen' : '#409A3C',
                'Die Linke':'#be3075',
                'fraktionslos':'#949494'}
party_names = list(party_colors.keys())
titleFontsize = 20

#### calculate histograms…
binWidth = 15 # 15 years is about one "generation" (roughly boomer, genX, millenials, genZ, genAlpha)
bins = np.arange(0,100,binWidth) # age bins
# …for each party, the whole Bundestag…
partyHists = {}
partyBins = {}
partyHists["Bundestag"], partyBins["Bundestag"] = np.histogram(membersOfParliament["age"],bins=bins)
partyHists["Bundestag"] = partyHists["Bundestag"]/partyHists["Bundestag"].sum() * 100 # normalizing
for party in party_names:
    masked = membersOfParliament[ membersOfParliament.Party==party ]
    partyHists[party], partyBins[party] = np.histogram(masked["age"],bins=bins)
    partyHists[party] = partyHists[party]/partyHists[party].sum() * 100 # normalizing
# …and for the population of Germany
popHist, popBins = np.histogram(pop_2021.age,bins=bins,weights=pop_2021.population)
popHist = popHist/popHist.sum() * 100 # normalizing

# plotting functions
def plotMembers():
    """Plots every member's age sorted by party affiliation. Also
    prints some information."""
    sns.set_style("darkgrid")
    fig, ax = plt.subplots(figsize=(12,4))
    sns.stripplot(x="Party", y="age",
                  data=membersOfParliament,
                  hue="Party", hue_order=party_names, palette=sns.color_palette(party_colors.values()),
                  order=party_names)
    ax.set_ylim(0,90) # show same age range as our "generations" later on.
    ax.yaxis.set_major_locator(ticker.MultipleLocator(15)) # tick age labels every 15 years

    # axis labels and title
    plt.xlabel('')
    plt.ylabel('Alter')
    plt.suptitle('Abgeordnete des 21. Bundestages nach Alter und Partei', fontsize=titleFontsize-8)
    plt.show()

    # print some addtional information
    oldest = membersOfParliament.age.max()
    youngest = membersOfParliament.age.min()
    print(f"\n\nDie jeweils jüngsten und ältesten Mitglieder in jeder Fraktion sind:")
    print(tabulate.tabulate(membersOfParliament.groupby("Party")["age"].describe()[["min","max"]].astype(int).transpose()[party_names],
                            headers='keys', tablefmt='psql'))

def plotDemographyVSgeneralPopulation(histogram, bins, title, color, position, ax, showpop=True):
    """Plot histogram of one given party. Optionally also the general
    German population in gray background."""
    ylabels = bins[:-1]
    ylabelsWords = ['Gen Alpha', 'Gen Z', 'Millenials', 'Gen X', 'Baby Boomer', 'Stumme Generation']
    ylabelPositions = np.arange(len(ylabels))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    if showpop:
        # general population
        ax.barh(ylabelPositions, -popHist, color='lightgrey')
        ax.barh(ylabelPositions, popHist, color='lightgrey')
    # party
    ax.barh(ylabelPositions, -histogram, color=color,alpha=0.5, label=title)
    ax.barh(ylabelPositions, histogram, color=color,alpha=0.5)
    # title and labels
    ax.set_title(f'{title}')
    ax.set_xlabel("")
    ax.tick_params(bottom=False)
    ax.set_xticklabels([])
    ax.set_xlim([-65,65])
    # put y-axis labels only left of the first and right of the last chart
    ax.set_yticks(ylabelPositions)
    ax.tick_params(left=False, right=False)
    if position=='first':
        ax.set_ylabel("Altersgruppe")
        ax.set_yticklabels([f"{a}–{a+binWidth-1}" for a in ylabels])
    elif position=='last':
        ax.yaxis.tick_right()
        ax.tick_params(right=False)
        ax.set_yticklabels(ylabelsWords)
    else:
        ax.set_yticklabels([])#ylabels)
    # write percentage in the middle
    for cohort in ylabelPositions:
        cohortPercentage = np.round(histogram[cohort])
        annotation = str(int(cohortPercentage))+"%" if cohortPercentage > 0 else ""
        ax.annotate(annotation,(0,cohort),
                    ha="center",va="center",fontweight="bold",color="black",size="large")


def plotGenerations_BTvsParties():
    """Plot histograms of generations in the Bundestag and individual fractions."""
    party_colors["Bundestag"]='#B7958B'
    plt.style.use('default')
    fig, axs = plt.subplots(nrows=1, ncols=7, figsize=(19,3))
    
    fig.suptitle('Altersstruktur der Fraktionen', fontsize=titleFontsize)
    for party, ax, figNo in zip(partyHists.keys(), axs.ravel(), np.arange(7)):
        if figNo==0:
            position='first'
        elif figNo==6:
            position='last'
        else:
            position=None
        plotDemographyVSgeneralPopulation(partyHists[party], bins, party, party_colors[party],position, ax)
        plt.tight_layout()


def plotGenerations_DEvsBTvsRegierung():
    """Plot histograms of generations in Germany, the Bundestag, and the Bundesregierung."""
    party_colors["Bundestag"]='#B7958B'
    plt.style.use('default')
    fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(19,3))
    
    fig.suptitle('Generationen in Deutschland, im Bundestag und in der Regierung', fontsize=titleFontsize)

    regHist, regBins = np.histogram(bundesregierung["age"],bins=bins)
    regHist = regHist/regHist.sum()*100 # normalize
    
    plotDemographyVSgeneralPopulation(popHist, bins, "Deutschland",
                                      "#ffcc3c",'first', axs[0], showpop=False)
    plotDemographyVSgeneralPopulation(partyHists["Bundestag"], bins, "Bundestag",
                                      party_colors["Bundestag"],None, axs[1])
    plotDemographyVSgeneralPopulation(regHist, bins, "Regierung",
                                      "#f4cfc4",'last', axs[2])

    plt.tight_layout()
    
