# encoding: utf-8
from psychopy import core, visual

# tworzymy okno
window = visual.Window(monitor='testMonitor')

# tworzymy skalę z domyślnymi ustawieniami
scale = visual.RatingScale(window)


# prosta funkcja do wyświetlania skali póki badany nie podjemie decyzji
def show_rating_scale(scale, window):
    # wyświetlaj dopóki brak decyzji
    while scale.noResponse:
        scale.draw()
        window.flip()

    # pobierz ze skali dane dotyczące odpowiedzi
    rating = scale.getRating()
    rt = scale.getRT()
    history = scale.getHistory()

    # zwracamy zebrane dane
    return rating, rt, history


# wyświetlamy pierwszą skalę i wyświetlamy zebrane dane
# (decyzję, czas decyzji oraz historię wyborów)
rating, rt, history = show_rating_scale(scale, window)
print(rating, rt, history)


# tworzymy różne skale
# --------------------

# słownik klawiszy nawigacyjnych, z których będziemy
# korzystać w każdej skali
navig = dict(leftKeys='f', rightKeys = 'j', acceptKeys='space')

# skala z pięcioma stopniami, kursor zaczyna na pozycji 4
scale2 = visual.RatingScale(window, low=1, high=5, markerStart=4, **navig)

# skala z trzema słowami do wyboru, zdefiniowany kolor markera
scale3 = visual.RatingScale(window, choices=['jamnik', 'kaczka', 'wombat'],
                            markerColor='cornflowerblue', markerStart=1,
                            **navig)

# skala z innym kursorem (glow - czyli taki gaussowski rozbłysk)
scale4 = visual.RatingScale(window, lineColor='green', noMouse=True,
                            textFont='Consolas', marker='glow', **navig)


# wyświetl każdą skalę i zbierz dane
# ----------------------------------
for sc in [scale2, scale3, scale4]:
    rating, rt, history = show_rating_scale(sc, window)
    print(rating, rt, history)

# cleanup i zamykamy
core.quit()
