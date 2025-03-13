from TheGreatFilter import extract_main_news


# Test Model against a file 
def TestModel(filePath, eps, samples, metric):
    with open(filePath, "r") as file:
        newsLines = file.read().split("\n")
        predictedLines = extract_main_news(newsLines[0], eps, samples, metric)
        newsLines.pop(0)
        correct = 0
        falsePositives = 0
        falseIncluded = []
        for line in predictedLines:
            if line in newsLines:
                correct += 1
            else:
                falsePositives += 1
                falseIncluded.append(line)
                # print(f"[Falsely Included] : {line}")
        newsAccuracy = (correct / len(newsLines)) * 100
        noiseAccuracy = (correct / (correct+falsePositives)) * 100
        return noiseAccuracy, newsAccuracy, falseIncluded
