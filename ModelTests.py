from TheGreatFilter import extract_main_news

with open("Tests/Al-Jazeera.txt", "r") as file:
    newsLines = file.read().split("\n")
    predictedLines = extract_main_news(newsLines[0])
    newsLines.pop(0)
    correct = 0
    falsePositives = 0
    for line in predictedLines:
        if line in newsLines:
            correct += 1
        else: 
            falsePositives += 1
            print(f"[Falsely Included] : {line}")
    print(f"Inlucding News Accuracy  : {(correct/len(newsLines)) * 100:.2f}% ")
    print(f"Deleting Noise Accuracy : {(correct/(correct+falsePositives)) * 100:.2f}% ")
