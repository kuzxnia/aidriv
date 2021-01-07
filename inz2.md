Sieci neuronowe

7.1.    Wprowadzenie do uczenia maszynowego
7.2.    Uczenie maszynowe
    7.2.1.    typy uczenia maszynowego

7.3.    Uczenie głębokie
    7.3.1.    Problemy
    7.3.2.    Rektyfikowane Jednostki Liniowe (ReLU)
    7.3.3.    Technika Regularyzacji Opuszczeń
    7.3.4.    podziały sztucznej inteligencji

7.4.    Architektury głębokie
    7.4.1.    Konwolucyjne sieci neuronowe (Convolutional Neural Network - CNN)


Sieci neuronowe


7.3.    Uczenie głęboki

    7.3.4.    podziały sztucznej inteligencji

7.4.    Architektury głębokie
    7.4.1.    Konwolucyjne sieci neuronowe (Convolutional Neural Network - CNN

        LeNet-5
        AlexNet
        ConvNet


\subsection{Architektury głębokie}

\subsubsection{Konwolucyjne sieci neuronowe (Convolutional Neural Network - CNN)}


    * Sieć konwolucyjna jest zwykle sekwencją warstw, które transformują jeden obraz danych
    do drugiego poprzez funkcję różniczkowalną (w celu umożliwienia wykorzystania algorytmu
    propagacji wstecznej błędów do dostrojenia parametrów sieci neuronowej.
    Składają się z jednej lub wielu warstw konwolucyjnych (typowych dla kroku próbkowania, określającego subwzorce),
    a następnie przez jedną lub w pełni połączone warstwy tak jak w klasycznej wielowarstwowej
    sieci, np. MLP, SVM, SoftMax itp. Głęboka sieć konwolucyjna zawiera wiele warstw.
    Sieci kowolucyjne są łatwe do uczenia, gdyż zawierają mniej parametrów (wykorzystując te
    same wagi) niż typowe sieci neuronowe z dokładnością
    do ilości warstw konwolucyjnych i ich rozmiaru.

    Ten rodzaj sieci neuronowych jest predestynowany do obliczeń na strukturach 2D (tj. obrazy).
    Sieci konwolucyjne CNNs (ConvNet) zwykle składają się z trzech typowych warstw:

    * Warstwa konwolucyjna zawierająca zbiór adaptowalnych filtrów, np. [5x5x3]

    * Warstwę łączenia,

    * W pełni połączoną sieć implementującą sieci MLP, SVM, czy SoftMax.

    

    Konwolucje pozwalają na ekstrakcję prostych cech w początkowych warstwach sieci, np. rozpoznają
    krawędzie o różnej orientacji lub różnokolorowe plamy, a następnie plastry, koła w kolejnych warstwach.
    Każda warstwa konwolucyjna zawiera cały zbiór filtrów
    (np. 8 filtrów), a każdy z nich generuje osobną mapę aktywacji 2D. Układamy te mapy aktywacyjne na stercie wzdłuż wymiaru głębokości sieci i produkujemy obraz wyjściowy.

    photo przykłady
    W każdej konwolucji możemy wyróżnić:
    * Ilość parametrów w każdej warstwie: Ilość kanałów * Ilość filtrów * szerokość filtra * wysokość filtra
    * Ilość jednostek ukrytych w każdej warstwie: Ilość filtrów * szerokość wzorca * wysokość wzorca


    Przykład sieci konwolucyjnej(na bazie architektury LeNet):
    1. Obraz wejściowy [32x32x3], gdzie trzeci parametr koduje kolor dla poszczególnych składowych from R, G, i B.

    2. Warstwa konwolucyjna oblicza wyjście dla neuronów podłączonych do lokalnych regionów w obrazie
    wejściowym, a każda warstwa wyznacza iloczyn skalarny (dot product) pomiędzy ich wagami i małym
    regionem w obrazie wejściowym. To może prowadzić do wyników zapisanych w np. 8 warstwach
    konwolucyjnych o tym samym rozmiarze, co zapisujemy jako [32x32x8] gdzie 8 to ilość filtrów konwolucyjnych.

    3. Warstawa ReLU (RELU) stosuje funkcję ReLU (określoną jako max(0,x)) z zerowym progiem. Wymiar klastra
    macierzy dla tej warstwy pozostaje niezmieniony wielkości, czyli [32x32x8] dla powyższego przykładu.

    4. Warstwa łączenia (POOL) służy do progresywnej redukcji rozmiaru przestrzennego do zredukowania ilości cech i złożoności obliczeniowej sieci. Przeprowadza operację próbkowania przestrzennego względem wysokości i szerokości (wyznaczając np. maksimum dla MaxPooling), co skutkuje wynikowym wymiarem np. [16x16x8].
    
Najczęściej w sieciach konwolucyjnych stosujemy warstwę MaxPool która przesuwa filtry 2x2 przez całą macierz wyciągając największą wartość z okna filtra i zapisuje ją do następnej mapy. Najważniejszy powód stosowania warstw łączących jest uchronienie modelu przed przeuczeniem. Czasami stosujemy też warstwę opuszczającą, która zastępuje warstwę łączącą. Należy być ostrożnym przy stosowaniu warstwy łączącej, szczególnie w zadaniach wizyjnych, gdyż może to spowodować utratę lokalnej wrażliwości modelu mimo zmniejszenia rozmiaru modelu.

5. Warstwa połączeń każdy-z-każdym (FCNN) oblicza wynik klasyfikacji, co skutkuje wymiarem wyjściowym, np. [1x1x5], dla 5 klas/kategorii, czyli po jednym neuronie wyjściowym dla każdej klasy. Ta warstwa uczona jest metodą uczenia nadzorowanego (zwykle jakąś metodą gradientową, np. propagacją wsteczną błędów) i jest połączona z poprzednią warstwą na zasadzie każdy-z-każdym.

kolejnymi warstwami konwolucyjnymi. Jej główną funkcją jest stopniowa redukcja wymiaru i ilości parametrów, jak również nakładu obliczeniowego. Pozwala również kontrolować przeuczenie się sieci ponieważ mniejsza ilość parametrów rzadziej prowadzi do przeuczenia. Warstwa łączenia typowo wykorzystuje operację Maksimum niezależnie dla każdego plastra wejściowego i przeskalowuje go przestrzennie (zmniejszając jego rozmiar). Najczęstszą formą łączenia jest wykorzystanie filtrów o wielkości 2x2 z krokiem 2, próbkujących każdy plaster wejściowy i redukując jego rozmiar czterokrotnie (każdy wymiar o połowę), odrzucając 75% aktywacji, ponieważ zawsze wybieramy jedno maksimum z 4 aktywacji w regionie wejściowym 2x2 w każdym plastrze.
    Głębokość jest zaś zachowana.

    przykładowe architektury konwolucyjne:
    LeNet
    *

AlexNet, GoogLeNet, , ResNet, VGGNet
