# first line: 480
@memory.cache
def callKSearch ():
    print('findKValueNow!!!')
    global countPercentageList
    countPercentageList = []
    global storeAllMetricsList
    storeAllMetricsList = []
    global sortShepCorrList
    sortShepCorrList = []
    global GatherSafe
    GatherSafe = []
    global GatherBorder
    GatherBorder = []
    global GatherRare
    GatherRare = []
    global GatherOut
    GatherOut = [] 
    global UMAPModalStore
    UMAPModalStore = []
    global MaxValue
    MaxValue = []
    global MaxIndex
    MaxIndex = []

    kValuesAll = [5,6,7,8,9,10,11,12,13]
    mDistanceAll = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
    dataNP = XData.to_numpy()
    D_highSpace = distance.squareform(distance.pdist(dataNP))

    for val in kValuesAll:
        safeIndCounter = []
        borderlineIndCounter = []
        rareIndCounter = []
        outIndCounter = []
        countPercentage = []
        
        nbrs = NearestNeighbors(n_neighbors=val, metric="euclidean", n_jobs = -1).fit(XData)
        distances, indices = nbrs.kneighbors(XData)

        summarizePerc = []
        for idx, el in enumerate(indices):
            computePer = -1
            for each in el:
                if (yData[idx] == yData[each]):
                    computePer = computePer + 1
            summarizePerc.append(computePer)

        for i, el in enumerate(summarizePerc):
            if (el >= (0.8 * val)):
                safeIndCounter.append(i)
            elif (el >= (0.5 * val)):
                borderlineIndCounter.append(i)
            elif (el >= (0.2 * val)):
                rareIndCounter.append(i)
            else:
                outIndCounter.append(i)
        
        percsafeIndCounter = len(safeIndCounter) / (len(safeIndCounter)+len(borderlineIndCounter)+len(rareIndCounter)+len(outIndCounter))
        percborderlineIndCounter = len(borderlineIndCounter) / (len(safeIndCounter)+len(borderlineIndCounter)+len(rareIndCounter)+len(outIndCounter))
        percrareIndCounter = len(rareIndCounter) / (len(safeIndCounter)+len(borderlineIndCounter)+len(rareIndCounter)+len(outIndCounter))
        percoutIndCounter = len(outIndCounter) / (len(safeIndCounter)+len(borderlineIndCounter)+len(rareIndCounter)+len(outIndCounter))

        countPercentage.append(percsafeIndCounter*100)
        countPercentage.append(percborderlineIndCounter*100)
        countPercentage.append(percrareIndCounter*100)
        countPercentage.append(percoutIndCounter*100)

        countPercentageList.append(countPercentage)
        
        metricShepCorr = []
        for dis in mDistanceAll:
            SearchUMAP = FunUMAPAll(XData, val, dis)
            D_lowSpace = distance.squareform(distance.pdist(SearchUMAP))
            resultShep = shepard_diagram_correlation(D_highSpace, D_lowSpace) 
            metricShepCorr.append(resultShep*100)
        storeAllMetricsList.append(metricShepCorr)
        sortShepCorr = sorted(range(len(metricShepCorr)), key=lambda k: metricShepCorr[k], reverse=True)[0]
        sortShepCorrList.append(sortShepCorr)

        max_value = max(metricShepCorr)
        max_index = metricShepCorr.index(max_value)
        UMAPModal = FunUMAP(XData, val, mDistanceAll[max_index])
        UMAPModalStore.append(UMAPModal)
        GatherSafe.append(safeIndCounter)
        GatherBorder.append(borderlineIndCounter)
        GatherRare.append(rareIndCounter)
        GatherOut.append(outIndCounter)
        MaxValue.append(max_value)
        MaxIndex.append(max_index)

    return [countPercentageList,sortShepCorrList,storeAllMetricsList,UMAPModalStore,GatherSafe,GatherBorder,GatherRare,GatherOut,MaxValue,MaxIndex]
