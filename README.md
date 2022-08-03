PLAY - запустить проигрывание видео
PAUSE - поставить видео на паузу
STOP - остановить проигрывание видео

File -> New video - Выбрать новое видео для редактора
File -> Save - Сохранить текущее видео

Edit -> Undo - Откатить изменение
Edit -> Redo - Вернуть изменение обратно

Actions -> Start writting - Начать запись действий
Actions -> Stop writting - Остановить запись действий
Actions -> Save - Сохранить последовательность действий для будущего применения
Actions -> Load - Загрузить последовательность действий и выполнить её

Действия:
1) Изменить скорость - вписать значение новой скоростb в окно слева от кнопки "Set speed" и нажать кнопку "Set speed"(Два окна левее означают гранцы применения). Значение скорости должно быть положительным. Если оставить значение в окне слева "1", то ничего не произойдёт при нажатии кнопки. Чем ближе значение новой скорости к "0", тем дольше происходит обработка, поэтому не рекомендуется ставить слишком низкие значения.

2) Повернуть изображение - вписать градус поворота против часовой стрелки в окно слева от кнопки "Rotate" и нажать кнопку "Rotate". Выбор флага "Reshape" означает будет ли расширение видео подстраиваться под новую картинку. По умолчанию расширение видео не меняется, поэтому часть картинки обрезается при повороте.

3) Вырезать фрагмент - в два окна слева от кнопки "Cut" вписать левые и правые границы фрагмента, который надо вырезать. Значение в кадрах. Значение левого окна должно быть >= 0 и < значения в правом окне. Значение правого окна должно быть <= количества кадров в видео и > значения в левом окне. По умолчанию в правом окне записано значение равное количеству кадров.

4) Вставить статическое изображение - для начала выбрать изображение для вставки нажав кнопку "Choose photo", затем в окна слева от кнопки "Add photo" вписать левую и правую границу в кадрах. После чего нажать кнопку "Add photo". Значения в окнах выставляются аналогично действию "Вырезать фрагмент"

5) Склеить фрагменты - выбрать второй фрагмент нажав кнопку "Choose fragment", после чего нажать кнопку "Put on the left" или "Put on the right" - вставить второй фрагмент слева или справа от текущего видео. Расширение полученного видео всегда равно расширению первого исходного видео.

6) Кроп - снизу от окна с видео списать границы кропа по горизонтали, справа от окна с видео границы кропа по вертикали. После чего нажать кнопку "Crop". Значения границ должны быть неотрицательными, не должны превышать количество пикселей в видео по текущей оси, и лева граница должна быть < правой и верхняя < нижней соотвественно.

