from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


### Der Quicksort Algorithmus
# Dies ist eine Hilfsmethode für den quickSort Algorithmus.
# Dem quickSort müssen wir jedes Mal die Parameter arr, low, high und comparator übergeben.
# arr = ist das von uns übergebene Array
# low = der Index des ersten Elements in unserem Array (NICHT den Wert)
# high = der Index des letzten Elements in unserem Array (NICHT den Wert)
# comparator = eine Hilfsfunktion mit deren Hilfe wir entscheiden, wonach wir sortieren wollen.

# Jedes Mal wenn wir ein Bild sortieren, müssen wir die oben genannten 4 Parameter angeben. Um Code-Duplikation zu
# vermeiden, existiert diese Hilfsfunktion.

# So müssen wir nur das Array und die Comparator Funktion übergeben, die Hilfsfunktion übernimmt den Rest.

def quickSortHelp(arr, comparator):
    quickSort(arr, 0, len(arr) - 1, comparator)


def quickSort(arr, low, high, comparator):
    # Wenn das übergebene Array nur noch ein Element hat
    if len(arr) == 1:
        # Dann soll das Array zurückgegeben werden
        return arr
    # Wenn der Index des kleinen Elements kleiner ist als der Index des größten Elements ist
    if low < high:
        # Dann wird die Variable pi definiert
        # Pi ist der Index an dem das Array in zwei geteilt wird. (die Stelle unseres Pivot Elements)
        # arr[pi] ist fertig sortiert
        # was genau partition macht, wird weiter unten erklärt.
        pi = partition(arr, low, high, comparator)

        # Seperately sort elements before partition and after partition
        # Nun wird rekursiv der quickSort Algorithmus erneut aufgerufen. Das Array wird in zwei Arrays geteilt
        # Das erste geht nun vom "ersten" Index zum Element kurz vorm Pivot Element
        quickSort(arr, low, pi - 1, comparator)
        # Das zweite geht vom Element direkt nach dem Pivot Element zum "letzten" Element
        quickSort(arr, pi + 1, high, comparator)
        # "ersten" und "letzten" sind in Anführungszeichen, da es sich nur beim ersten Aufruf um das tatsächlich erste
        # und tatsächich letzte handelt. Da der Algorithmus häufiger aufgerufen wird, wäre der Index von Low/High
        # natürlich auch an anderen Stellen

# Die Methode Partition ist die, die tatsächlich zwei Werte an zwei verschiedenen Stellen miteinander vergleicht
# Es werden die gleichen Parameter wie bei der QuickSort funktion übergeben
def partition(arr, low, high, comparator):
    # i : der Index des kleinsten Elements minus 1, also ganz Links vom Array (noch weiter)
    i = (low - 1)
    # pivot : Wert des Pivot Elements. Hier wird anhand der Comparator Funktion ein Int Wert erstellt, um damit die
    # anderen Elemente zu vergleichen
    pivot = comparator(arr[high])

    # für jeden Wert in diesem Array zwischen dem Index des ersten und des letzten Elements
    for j in range(low, high):
        # Wenn der Wert an der Stelle kleiner ist als das Pivot Element
        if comparator(arr[j]) <= pivot:
            # Soll i um eins vergrößert werden.
            i = i + 1
            # Nun werden die zwei Werte in ihren Positionen vertauscht, damit das bisher kleinste Element vom Wert
            # her ganz links steht.
            arr[i], arr[j] = arr[j], arr[i].copy()
    # Das Element was danach kommt, wird mit dem letzten Element vertauscht
    arr[i + 1], arr[high] = arr[high], arr[i + 1].copy()
    # Zurückgegeben wird i+1 damit wder Algorithmus an die nächste Stelle im Array geht.
    return (i + 1)


### Comparator = Unsere Vergleichsfunktion
# howBright gibt tatsächlich nur die Summe der drei RGB Werte wieder, um nach Helligkeit zu sortieren
def howBright(pixel):
    return int(pixel[0]) + int(pixel[1]) + int(pixel[2])

# Eine andere Möglichkeit ist es, nur nach dem RotAnteil zu sortieren
def valueofRed(pixel):
    return int(pixel[0])

# Oder Gelb Wert
def valueofYellow(pixel):
    return int(pixel[1])

# Oder Blau Wert
def valueofBlue(pixel):
    return int(pixel[2])



### Convert -> Zeilenweise Sortierung
def convertRow(originalImage):
    # Gibt einfach nur die Metadaten des Bildes auf die Konsole wieder
    print(originalImage)
    # Das Bild wird zu einem Numpy Array umgewandelt
    data_array = np.asarray(originalImage)
    # Nun wird das Array nochmal kopiert, damit wir damit arbeiten können
    data_array_sortByRow = data_array.copy()
    # .jpg und .png unterscheiden sich in der Anzahl ihrer Farbkanäle.
    # .jpg hat drei (RGB) und .png hat vier (RGBA)
    # damit es zur Laufzeit nicht zu fehlern kommt, wird geschaut, wieviele Werte wir bekommen (3 oder 4)
    data_Format = len(data_array[0][0])
    # Die Breite und Höhe des Arrays wird durch die Bildgröße bestimmt
    width, height = originalImage.size
    # Nun wird ein Array erstellt wo die Pixel sortiert angeorndet sein werden
    converted_data_array = np.zeros((height, width, data_Format), dtype=np.uint8)

    # Hier wird tatsächlich sortiert und eingefügt
    # Für jede Zeile im Bild
    for i in range(height):
        # wird die noch unsortierte Zeile temporär in der Variable sortedRow gespeichert
        sortedRow = data_array_sortByRow[i].copy()
        # dann wird die methode quickSortHelp aufgerufen (die wiederrum quickSort aufruft) um zu vergleichen
        quickSortHelp(sortedRow, howBright)  # comparator ohne Klammern!
        # Nun wird in das von uns vorbereitete Array die sortierte Zeile eingefügt
        converted_data_array[i] = sortedRow

    # Schließlich wird ein Sortiertes Bild aus dem Array erstellt
    converted_image_row = Image.fromarray(converted_data_array, "RGBA"[:data_Format])
    # und dann angezeigt
    #converted_image_row.save('Bilder/row.PNG')
    return converted_image_row


### Convert -> By Column
def convertColumn(originalImage):
    # Gibt einfach nur die Metadaten des Bildes auf die Konsole wieder
    print(originalImage)
    # Das Bild wird zu einem Numpy Array umgewandelt. Dabei werden aber mit der Hilfmethode die Axen vertauscht, damit
    # wir an die Werte der jeweiligen Spalten kamen. Nach vielen Überlegungen war dies die einzige Möglichkeit, wie wir
    # an den Wert gekommen sind (die funktioniert hat)
    data_array = switchAxis(np.asarray(originalImage))
    # Nun wird das Array nochmal kopiert, damit wir damit arbeiten können
    data_array_sortByColumn = data_array.copy()
    # Hier wird wieder zwischen den Dateiformaten unterschieden
    data_Format = len(data_array[0][0])
    # Die Breite und Höhe des Arrays wird durch die Bildgröße bestimmt
    width, height = originalImage.size
    # Nun wird ein Array erstellt wo die Pixel sortiert angeorndet sein werden
    converted_data_array = np.zeros((width, height, data_Format), dtype=np.uint8)

    # Hier wird tatsächlich sortiert und eingefügt
    # Für jede Spalte im Bild
    for i in range(width):
        # wird die noch unsortierte Spalte temporär in der Variable sortedColumn gespeichert
        sortedColumn = data_array_sortByColumn[i].copy()
        # dann wird die methode quickSortHelp aufgerufen (die wiederrum quickSort aufruft) um zu vergleichen
        quickSortHelp(sortedColumn, howBright)
        # Nun wird in das von uns vorbereitete Array die sortierte Zeile eingefügt
        converted_data_array[i] = sortedColumn

    # Schließlich wird ein Sortiertes Bild aus dem Array erstellt. Dabei werden die Achsen auch wieder zurückgetauscht
    converted_image_column = Image.fromarray(switchAxis(converted_data_array), "RGBA"[:data_Format])
    # und dann angezeigt
    #converted_image_column.save('Bilder/column.PNG')
    return converted_image_column


# Hilfsmethode zu convertColumn
def switchAxis(data_array):
    # Diente Kontrollzwecken ob alles funktioniert
    # print("started switchAxis")
    # Es wird ein Array erstellt in das die vertauschten Werte eingefügt werden. Es spiegelt quasi das übergebene Array
    # wieder, nur verdreht
    switched_data_array = np.zeros((len(data_array[0]), len(data_array), len(data_array[0][0])), dtype=np.uint8)
    for i in range(len(data_array)):
        for j in range(len(data_array[i])):
            #Hier wird vertauscht bzw. eingefügt
            switched_data_array[j][i] = data_array[i][j]
    # print("finished switchAxis")
    # Und hier wird zurückgegeben
    return switched_data_array


### Convert -> Continuously
def convertContinuously(originalImage):
    # Gibt einfach nur die Metadaten des Bildes auf die Konsole wieder
    print(originalImage)
    # Das Bild wird zu einem Numpy Array umgewandelt.
    data_array = np.asarray(originalImage)
    # Hier wird wieder zwischen den Dateiformaten unterschieden
    data_Format = len(data_array[0][0])
    # Die Breite und Höhe des Arrays wird durch die Bildgröße bestimmt
    width, height = originalImage.size

    # Wir formtieren das Array um in neue Dimensionen
    # -> statt vorher ein 3D Array gehabt zu haben, haben wir jetzt ein 2D Array
    # dies wird erreicht mit der Methode .reshape
    data_array_sortContinuously = data_array.reshape(width * height, data_Format).copy()
    # Jetzt wird der Sortieralgorithmus auf das gesamte Bild angewandt, nicht mehr nur auf Zeile/Spalte
    quickSortHelp(data_array_sortContinuously, howBright)
    # Jetzt wird das 2D Array wieder in ein 3D Array zurückgewandelt
    converted_data_array = data_array_sortContinuously.reshape(height, width, data_Format)
    # Schließlich wird ein sortiertes Bild erstellt
    converted_image_continously = Image.fromarray(converted_data_array, "RGBA"[:data_Format])
    # Und angezeigt
    #converted_image_continously.save('Bilder/continous.PNG')
    return converted_image_continously

#### Aufruf Pixelsorting
# Bild laden
original = Image.open('Bilder/Beispiel.PNG')

# Runterskalieren des Bildes
factor = 0.25
width, height = original.size
width, height = int(width * factor), int(height * factor)
original = original.resize((width, height))

# Nun kann man sehen, wie sortiert wird!
# Hinweis: convertContinuously dauert etwas länger :( Da hilft es den Faktor mit dem Skaliert wird anzupassen damit
# das Bild kleiner wird

def convert(originalImage):
    original = originalImage
    convertedImageRow = convertRow(originalImage)
    print("Zeilenweise fertig sortiert")

    convertedImageColumn = convertColumn(originalImage)
    print("Spaltenweise fertig sortiert")

    convertedImageContinuously = convertContinuously(originalImage)
    print("Kontinuierlich fertig sortiert")

    # Darstellung in Plot View
    fig, axs = plt.subplots(2, 2)

    axs[0][0].imshow(original)
    axs[0][0].set_title("Orginalbild")
    axs[0][0].axis('off')

    axs[0][1].imshow(convertedImageRow)
    axs[0][1].set_title("Zeilenweise sortiert")
    axs[0][1].axis('off')

    axs[1][0].imshow(convertedImageColumn)
    axs[1][0].set_title("Spaltenweise sortiert")
    axs[1][0].axis('off')

    axs[1][1].imshow(convertedImageContinuously)
    axs[1][1].set_title("Kontinuirlich sortiert")
    axs[1][1].axis('off')

    fig.tight_layout()
    plt.show()

convert(original)
