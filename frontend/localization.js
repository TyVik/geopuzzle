'use strict';
import LocalizedStrings from "react-localization";


let localization = new LocalizedStrings({
    en: {
        capital: 'Capital',
        flag: 'Flag',
        coat_of_arms: 'Coat of arms',
        title: 'Title',
        area: 'Area',
        population: 'Population',
        currency: 'Currency',
        phone: 'Phone',
        found: 'Found',
        give_up: 'give up',
        once_again: 'once again',
        congratulations: 'Congratulations!',
        km2: 'sq. km.',
        loading: 'Loading...',
        start: 'Start',
        quizInitCaption: "I'll search the regions by",
        quizInitCheck: "Choose at least one option",
        network_error: "Connecting to server...",
    },
    ru: {
        capital: 'Столица',
        flag: 'Флаг',
        coat_of_arms: 'Герб',
        title: 'Название',
        area: 'Площадь',
        population: 'Население',
        currency: 'Валюта',
        phone: 'Телефонный код',
        found: 'Найдено',
        give_up: 'сдаюсь',
        once_again: 'ещё раз',
        congratulations: 'Поздравляем!',
        km2: 'кв. км.',
        loading: 'Загрузка...',
        start: 'Начали!',
        quizInitCaption: "Я буду искать регионы по",
        quizInitCheck: "Выберите хотя бы один вариант",
        network_error: "Соединение с сервером...",
    }
});

localization.setLanguage(window.__LANGUAGE__);

export default localization;