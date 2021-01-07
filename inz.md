# Kontenery

* docker

Konteneryzacja polega na tym, że umożliwia uruchomienie wskazanych procesów aplikacji w wydzielonych kontenerach, które z punktu widzenia aplikacji są odrębnymi instancjami środowiska uruchomieniowego. 
Każdy kontener posiada wydzielony obszar pamięci, odrębny interface sieciowy z własnym prywatnym adresem IP oraz wydzielony obszar na dysku, na którym znajduje się zainstalowany 
obraz systemu operacyjnego i wszystkich zależności / bibliotek potrzebnych do działania aplikacji.
Z pomocą przychodzi Docker, który pozwala zbudować środowisko deweloperskie bez wirtualizacji i przy odrobinie szczęścia bez większego wysiłku związanego z instalacją oprogramowania. 

Przewagi konteneryzacji nad wirtualizacją:
* możliwość uruchomienia aplikacji w wydzielonym kontenerze, bez konieczności emulowania całej warstwy sprzętowej i systemu operacyjnego. 
* oszczędność w wykorzystaniu zasobów, docker uruchamia w kontenerze tylko proces/y aplikacji, powoduje to lepsze zarządzanie zasobami sprzętowych, 
    co przy rozproszonych aplikacjach instalowanych do tej pory na kilkunastu bądź kilkudziesięciu wirtualnych maszynach przynosi oszczędności zasobów.
* niezależność, kontenery działają niezależnie od siebie i do chwili, w której świadomie wskażemy zależność pomiędzy nimi, nic o sobie nie wiedzą.
    (np. chcemy dla naszej aplikacji uruchomić bazę danych, aby to zrobić uruchamiamy kolejny kontener z bazą i tworzymy połączenie sieciowe pomiędzy kontenerami.)


Docker jest otwarto źródłowe oprogramowanie służące do tworzenia wirtualizacji na poziomie systemu operacyjnego (tzw. „konteneryzacji”), szczególnie w środowiskach chmurowych.
Obecnie Docker z powodzeniem zastępuje klasyczną wirtualizację oferowaną przez rozwiązania typu VMware lub XEN.  Docker pozwala wykorzystywać gotowe obrazy zainstalowanych systemów, 
aplikacji i baz danych, które zostały wczeniej przygotowane i umieszczone w publicznym rejestrze.
Rejestr jest dostępny za darmo i zawiera obrazy oficjalnie budowane przez opiekunów / twórców konkretnych rozwiązań: https://hub.docker.com/explore/. Dzięki temu, jeśli chcemy używać PostgreSQL, Redis czy RubyOnRails.
jest duża szansa na to, że gotowy obraz będziemy mogli pobrać z repozytorium i nie tracić czasu na jego przygotowanie. Jeśli jednak nie znajdziemy tego czego szukamy, 
to zawsze możemy zbudować własny obraz bazując na jednym z bardziej generycznych zawierających tylko zainstalowany system operacyjny (Ubuntu, Fedora) lub zainstalowane środowisko uruchomieniowe (Java, Python czy ASP.NET).

Mechanizm budowana obrazów kontenerów możemy wykorzystać w drugą stronę i dostarczać nasze konkretne aplikacje w postaci obrazów. Bez względu na technologię wykorzystaną w aplikacji, 
obraz kontenera będzie dostarczany w identyczny sposób co upraszcza procedury instalacyjne. W zasadzie każda instalacja może ograniczyć się do pobrania wskazanych obrazów na środowisko docelowe i ich uruchomienie. 
Administratorzy środowisk nie muszą być nawet do końca świadomi co uruchamiają, a przy odrobinie szczęścia sam proces dostarczania aplikacji może zostać zautomatyzowany przez odpowiednie narzędzia.

Docker-compose
// napisać o docker compose


Korzyści używania dockera dla programistów:
* łatwość tworzenia środowisk deweloperskich,
* uproszczenie procesów dostarczania gotowych aplikacji na docelowe środowiska
* łatwość zarządzania wieloma środowiskami w obrębie jednego systemu operacyjnego
* automatyzacja procesu deploymentu aplikacji


Na koniec najważniejsze: 
Docker działa tylko na jądrze Linux i pozwala uruchamiać tylko aplikacje przeznaczone dla Linux’a, ale dla wszystkich użytkowników Windows i Mac jest przygotowane narzędzie Docker Toolbox, 
które pozwala zainstalować Docker’a w minimalnej maszynie wirtualnej pod kontrolą VirtualBox’a.

// napisać o docker dla ARM (buildx)


* keras to otwarto źródłowa biblioteka do tworzenia sieci neuronowych. 
Głównym założeniem Keras'a jest uproszczenie tworzenia sieci neuronowych więc cała logika odpowiedzialna za faktyczne obliczenia i operacje są oddelegowywane do bibliotek takich jak TensorFlow oraz Theano.
Keras wykorzystuje ww. biblioteki jako backend, więc jest swego rodzaju nakładką na mniejabstrakcyjne biblioteki.

Zalety wykorzystania biblioteki Keras:

\begin{itemize}
\item uproszenie tworzenia sieci
\item szybkie tworzenie prototypów, łatwość experymentowania
\item przyśpieszenie pisania kodu odpowiedzialnego za architekturę sieci
\item niższy próg wejścia niż w bibliotekach takich jak TensorFlow lub Theano
\end{itemize}


* scipy to biblioteka otwarto źródłowa stworzona do wykonywania operacji matematycznyhc oraz przetwarzania danych.

Najważniejsze operacje matematyczne zaimplementowanie w obrębie biblioteki:
\begin{itemize}
\item całkowanie
\item różniczkowanie numeryczne
\item algorytmy rozwiązywania równań różniczkowych
\item algorytmy z algebry liniowej
\item transformaty Fouriera
\item przetwarzania sygnałów
\end{itemize}

SciPy należy używać w parze z biblioteką NumPy, pierwszy wykorzystujemy do szeroko-pojetych obliczeń, metod numerycznych, 
a drugi z pary pakiet do operacji na listach, macierzach takich jak sortowanie, grupowanie, oczyszczanie danych.



* sciKit-Learn to biblioteka otwarto źródłowa algorytmów uczeuczenia maszynowego. 

Została stworzona na bazie SciPy do konkretnych zastosowań, takich jak:

\begin{itemize}
\item przetwarzania obrazu
\item klasyfikacja danych
\item Clustering'u
\item badaniu modeli 
\end{itemize}
natomiast sama szybkość uczenia się (czy po prostu wykonywania algorytmów) nie sprawia żadnych problemów ze względu na wykorzystanie kompilatora Cython

# mechanizm sterowania torem jazdy

* otsu jest to algorytm służący do progowania obrazu (binaryzacji - konwersji obrazu w odcieniach szarości do obrazu binarnego)
Jest to metoda progowania globalnego, oparta na histogramie. Metoda polega na minimalizacji sumy ważonej wariancji dwóch klas (tła i obiektów pierwszego planu), co jest tożsame z maksymalizacją wariancji międzyklasowej.
Metoda Otsu jest metodą popularną, cenioną za prostotę i efektywność. Jest ona implementowana przez wiele środowisk obliczeniowych oraz bibliotek. 
Metoda szczególnie dobrze sprawdza się w przypadkach, gdy liczby pikseli tła i obiektów pierwszego planu są zbliżone.
Opublikowana została w 1979 roku, a jej autorem jest Nobuyuki Otsu. 




* histogram jest to jeden z graficznych sposobów przedstawiania rozkładu empirycznego cechy. 


Składa się z szeregu prostokątów umieszczonych na osi współrzędnych. 
Prostokąty te są z jednej strony wyznaczone przez przedziały klasowe (patrz: szereg rozdzielczy) wartości cechy, 
natomiast ich wysokość jest określona przez liczebności (lub częstości, ewentualnie gęstość prawdopodobieństwa) elementów wpadających do określonego przedziału klasowego.
Jeśli histogram pokazuje liczebności, a nie gęstość prawdopodobieństwa, wówczas szerokości przedziałów powinny być równe.

kroki:

1. transformacja do odcieni szarości

1. otsu

2. zmiana wymiarów zdj, transformacja do tablicy liczb
// wstawić wzór

3. histogram 
// suma ilość pikseli białych

4. wyliczenie kąta skrętu
// z danych histogramu



typy uczenia maszynowego:
Jak zatem widzicie jest mnóstwo rzeczy, które można rozwiązać za pomocą uczenia maszynowego. Najważniejsze jest, aby wiedzieć jakie dane mamy na wejściu i co chcemy osiągnąć. 
W zależności od problemu możemy wybrać odpowiedni rodzaj uczenia maszynowego, który chcemy dobrać. Można je podzielić na trzy główne rodzaje:

uczenie maszynowe rodzaje(machine learning types)

Uczenie nadzorowane (Supervised Learning)
Możecie pomyśleć o tym, że jest analogiczne do tego, jak uczy się Jagoda albo Otylka :). Dostają informacje, jak należy coś rozwiązać od rodziców (Ja i Elwira) albo od „cioć” ze żłobka lub przedszkola.
Jest to najczęściej wykorzystywany rodzaj uczenia maszynowego. Sam w pracy modelując obecnie ryzyko kredytowe klientów (czy spłaca kredyt) na wejściu mam zbiór cech opisujących klientów oraz 
informacje kto spłacił a kto nie (odpowiedź / etykiety / target). Właśnie dlatego, że uczenie nadzorowane jest nazwane „nadzorowanym”.
uczenie maszynowe nadzorowane (machine learning supervised)
Przykładami takiego uczenia jest wszystko z punktu „Przykłady uczenia maszynowego” oznaczone jako 0/1. Ponadto inne wykorzystanie uczenia nadzorowanego to:
zdjęcie rentgenowskie i rozpoznajemy czy pacjent jest chory na zapalenie płuc,
tweet i rozpoznajemy sentyment czy jest obraźliwy,
rozpoznawanie konkretnych twarzy (np. Mirka :)).


Uczenie nienadzorowane (Unsupervised Learning):
Uczenie się bez nadzoru jest przeciwieństwem uczenia nadzorowanego. Czasami moje dziewczyny uczą się samodzielnie próbując odgadnąć pewne zależności. Czyli próbują dopasować pewne zależności bez prawidłowej odpowiedzi.
Przekładając to na modelowanie oznacza to, że na wejściu mamy same charakterystyki i nie narzucamy żadnych odpowiedzi czy coś jest np. dobre a coś złe. 
Algorytm ma na celu podczas procesu uczenia znaleźć samemu interesujące wzorce czy zależności. Po to jest to robione, aby potem człowiek (lub inteligentny algorytm) mógł wejść i zrozumieć nowo zorganizowane dane.
uczenie maszynowe nienadzorowane (machine learning unsupervised)
Przykładami może być:
segmentacja klientów (algorytmy grupowania, które podzielą klientów na podgrupy),
systemy rekomendacyjne (szukanie podobnych klientów i pokazywanie podobnych filmów / produktów),
redukcja wymiarów (zredukowanie 100 cech do 10 innych wartości nie mówiąc jak).
Dlaczego ta dziedzina uczenia jest moim zdaniem bardzo ciekawym obszarem? Ponieważ większość danych na świecie jest nieoznaczona! 
Można w tej sposób analizować terabajty nieoznaczonych danych, aby je lepiej rozumieć co może być źródłem potencjalnego zysku dla wielu branż.

Uczenie ze wzmocnieniem (Reinforcement Learning)
Ten rodzaj uczenia jest z jednej strony bardzo ciekawy ale z drugiej jest najtrudniejszy. W miarę łatwo można dostrzec różnicę pomiędzy uczeniem nienadzorowanym a nadzorowanym, 
natomiast różnica między uczeniem ze wzmocnieniem jest bardziej mglista.

Pomyślcie, że dzieci mogą się uczyć czegoś samodzielnie podobnie jak w przypadku uczenia nienadzorowanego. Jednak może się coś wydarzyć, że zostaną ukarane i zrozumieją by czegoś nie powtarzać, 
np. dotknięcie garnka z gotującą się zupą. Nie ostrzegając ich (nie robiąc uczenia nadzorowowanego :)) po pierwszym dotknięciu zapamiętają już, aby już tego nie robić.

W przypadku każdego problemu z uczeniem ze wzmocnieniem potrzebujemy agenta i środowiska oraz połączenia tych dwóch elementów za pomocą pętli informacji zwrotnej. 
Aby połączyć agenta ze środowiskiem w rzeczywistości dajemy mu zestaw określonych działań, które może podjąć. Te działania wpływają na środowisko, w którym jest osadzony. 
Aby połączyć środowisko z agentem, stale wysyłamy dwa sygnały do agenta: zaktualizowany stan i nagrodę (nasz sygnał wzmocnienia dla zachowania).

// aka sieci neuronowe i uczenie głębokie
Wstęp do sztucznej inteligencji:

# podziały sztucznej inteligencji
* uczenie głębokie ( uczenie hierarchiczne ) - klasa algorytmów uczenia maszynowego
    podstawowe złożenia

    * Rozwijanie struktury hierarchicznej i reprezentację podstawowych i wtórnych cech,
    reprezentujących różne poziomy abstrakcji.

    * Wykorzystują wiele warstw neuronów różnych rodzajów w celu stopniowej ekstrakcji cech i 
    ich transformacji w celu osiągnięcia hierarchii cech wtórnych/pochodnych, 
    które prowadzą do lepszych wyników zbudowanych na ich podstawie sieci neuronowych. 
    W ten sposób próbują określić bardziej skomplikowane cechy na podstawie prostszych cech.

    * Stosują różne strategie uczenia nadzorowanego i nienadzorowanego dla różnych warstw,

    * Stopniowo rozwijają i aktualizują strukturę sieci dopóki występuje znacząca poprawa wyników 
    działania sieci.


    Architektury głebokie:


? sieci konwolucyjne

problem zanikowego gradientu
//
W przypadku wykorzystania strategii uczących wykorzystujących metody gradientowe
dla wielu warstw (np. sieci MLP) zwykle natrafiamy na problem zanikającego gradientu,
ponieważ pochodne są z przedziału [0, 1], więc wielokrotne przemnażanie prowadzi
do bardzo małych liczb prowadząc do coraz mniejszych zmian wag w warstwach coraz dalej
położonych od wyjścia sieci, stosując np. propagację wsteczną błędów.
Ten problem może zostać rozwiązany za pomocą treningu
wstępnego i strategii końcowego dostrojenia, które najpierw
trenują model warstwa po warstwie w nienadzorowany
sposób (np. używając głębokiego autoenkodera), a następnie
wykorzystujemy algorytm propagacji wstecznej do dostrojenia sieci.
//
* rozwiązanie relu = Rektyfikowane Jednostki Liniowe
    Możemy również wykorzystać jednostki ReLU
    w celu wyeliminowania problemu zanikającego
    gradientu.
    Jednostki ReLU są zdefiniowane jako:
    f(x) = max(0, x) zamiast funkcji logistycznej.
    Strategia wykorzystująca jednostki ReLU oparta jest na uczeniu pewnych cech
    dzięki rzadszym aktywacjom tych jednostek.
    Inną korzyścią jest to, że proces uczenia przebiega zwykle szybciej
* Technika Regularyzacji Opuszczeń
    Można wykorzystać też technikę regularyzacji opuszczeń,
    która wybiera do aktualizacji tylko te neurony z różnych
    warstw, które są najlepiej przystosowane.
    Ta technika zapobiega przeuczeniu sieci neuronowych,
    zapobiega psuciu wag dobrze przystosowanych do innych
    wzorców, jak również przyspiesza proces nauki.


* Konwolucyjne sieci neuronowe (Convolutional Neural Network - CNN)

    składają się z jednej
    lub wielu warstw konwolucyjnych (typowych dla kroku próbkowania, określającego subwzorce),
    a następnie przez jedną lub w pełni połączone warstwy tak jak w klasycznej wielowarstwowej
    sieci, np. MLP, SVM, SoftMax itp. Głęboka sieć konwolucyjna zawiera wiele warstw.
    Sieci kowolucyjne są łatwe do uczenia, gdyż zawierają mniej parametrów (wykorzystując te
    same wagi) niż typowe sieci neuronowe z dokładnością
    do ilości warstw konwolucyjnych i ich rozmiaru.

    Ten rodzaj sieci neuronowych jest predestynowany
    do obliczeń na strukturach 2D (tj. obrazy).

    potrafią stopniowo filtrować różne części
    danych uczących i wyostrzać ważne cechy w procesie dyskryminacji
    wykorzystanym do rozpoznawania lub klasyfikacji wzorców.

    * Sieć konwolucyjna jest zwykle sekwencją warstw, które transformują jeden obraz danych
    do drugiego poprzez funkcję różniczkowalną (w celu umożliwienia wykorzystania algorytmu
    propagacji wstecznej błędów do dostrojenia parametrów sieci neuronowej.
    Sieci konwolucyjne CNNs (ConvNet) zwykle składają się z trzech typowych warstw:

        * Warstwa konwolucyjna
        zawierająca zbiór
        adaptowalnych filtrów,
        np. [5x5x3]

        * Warstwę łączenia,

        * W pełni połączoną sieć
        implementującą sieci MLP,
        SVM, czy SoftMax.

    * Konwolucje pozwalają na ekstrakcję prostych cech w początkowych warstwach sieci, np. rozpoznają
    krawędzie o różnej orientacji lub różnokolorowe plamy, a następnie plastry, koła w kolejnych warstwach.
    Każda warstwa konwolucyjna zawiera cały zbiór filtrów
    (np. 8 filtrów), a każdy z nich generuje osobną mapę
    aktywacji 2D. Układamy te mapy aktywacyjne na stercie wzdłuż
    wymiaru głębokości sieci i produkujemy obraz wyjściowy.

    // photo przykłady

    W każdej konwolucji możemy wyróżnić:
    * Ilość parametrów w każdej warstwie: Ilość kanałów * Ilość filtrów * szerokość filtra * wysokość filtra
    * Ilość jednostek ukrytych w każdej warstwie: Ilość filtrów * szerokość wzorca * wysokość wzorca


    Przykład sieci konwolucyjnej:
    1. Obraz wejściowy [32x32x3], gdzie trzeci parametr koduje kolor dla poszczególnych składowych from R, G, i B.

    2. Warstwa konwolucyjna (CONV) oblicza wyjście dla neuronów podłączonych do lokalnych regionów w obrazie
    wejściowym, a każda warstwa wyznacza iloczyn skalarny (dot product) pomiędzy ich wagami i małym
    regionem w obrazie wejściowym. To może prowadzić do wyników zapisanych w np. 8 warstwach
    konwolucyjnych o tym samym rozmiarze, co zapisujemy jako [32x32x8] gdzie 8 to ilość filtrów konwolucyjnych.

    3. Warstawa ReLU (RELU) stosuje funkcję ReLU (określoną jako max(0,x)) z zerowym progiem. Wymiar klastra
    macierzy dla tej warstwy pozostaje niezmieniony wielkości, czyli [32x32x8] dla powyższego przykładu.

    4. Warstwa łączenia (POOL) przeprowadza operację próbkowania przestrzennego względem wysokości
    i szerokości (wyznaczając np. maksimum dla MaxPooling), co skutkuje wynikowym wymiarem np. [16x16x8].

    5. Warstwa połączeń każdy-z-każdym (FCNN) oblicza wynik klasyfikacji, co skutkuje wymiarem wyjściowym,
    np. [1x1x5], dla 5 klas/kategorii, czyli po jednym neuronie wyjściowym dla każdej klasy. Ta warstwa uczona
    jest metodą uczenia nadzorowanego (zwykle jakąś metodą gradientową, np. propagacją wsteczną błędów)
    i jest połączona z poprzednią warstwą na zasadzie każdy-z-każdym.


    * Warstwa łącząca (pooling layer) służy do progresywnej redukcji rozmiaru przestrzennego do
    zredukowania ilości cech i złożoności obliczeniowej sieci.

    Najczęściej w sieciach konwolucyjnych stosujemy warstwę MaxPool która that przesuwa filtry 2x2
    przez całą macierz wyciągając największą wartość z okna filtra i zapisuje ją do następnej mapy.
    Najważniejszy powód stosowania warstw łączących jest uchronienie modelu przed przeuczeniem.
    Czasami stosujemy też warstwę opuszczającą, która zastępuje warstwę łączącą.
    Należy być ostrożnym przy stosowaniu warstwy łączącej, szczególnie w zadaniach wizyjnych, gdyż
    może to spowodować utratę lokalnej wrażliwości modelu mimo zmniejszenia rozmiaru modelu.

    kolejnymi warstwami konwolucyjnymi. Jej główną funkcją jest stopniowa redukcja wymiaru i ilości
    parametrów, jak również nakładu obliczeniowego. Pozwala również kontrolować przeuczenie się sieci
    ponieważ mniejsza ilość parametrów rzadziej prowadzi do przeuczenia. Warstwa łączenia typowo
    wykorzystuje operację Maksimum niezależnie dla każdego plastra wejściowego i przeskalowuje go
    przestrzennie (zmniejszając jego rozmiar).
    Najczęstszą formą łączenia jest wykorzystanie filtrów o wielkości 2x2 z krokiem 2, próbkujących każdy
    plaster wejściowy i redukując jego rozmiar o czterokrotnie (każdy wymiar o połowę), odrzucając 75%
    aktywacji, ponieważ zawsze wybieramy jedno maksimum z 4 aktywacji w regionie wejściowym 2x2 w każdym plastrze.
    Głębokość jest zaś zachowana.

    przykładowe architektury konwolucyjne:

        AlexNet, GoogLeNet, LeNet, ResNet, VGGNet

* algorytm sterowania torem jazdy 
    // wypisać kroki

