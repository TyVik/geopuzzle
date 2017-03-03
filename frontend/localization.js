import LocalizedStrings from "react-localization";


let localization = new LocalizedStrings({
    en: {
        capital: 'Capital',
        area: 'Area',
        population: 'Population',
        currency: 'Currency',
        phone: 'Phone',
        found: 'Found',
        give_up: 'give up',
        once_again: 'once again',
        congratulations: 'Congratulations!',
        km2: 'sq. km.',
        loading: 'Loading...'
    },
    ru: {
        capital: 'Столица',
        area: 'Площадь',
        population: 'Население',
        currency: 'Валюта',
        phone: 'Телефонный код',
        found: 'Найдено',
        give_up: 'сдаюсь',
        once_again: 'ещё раз',
        congratulations: 'Поздравляем!',
        km2: 'кв. км.',
        loading: 'Загрузка...'
    }
});

localization.setLanguage(window.__LANGUAGE__);

export default localization;