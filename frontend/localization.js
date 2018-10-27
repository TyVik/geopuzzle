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
    km2: 'sq. km.',

    loading: 'Loading...',
    loadingError: 'Something wrong :(',
    networkError: "Connecting to server...",

    found: 'Found',
    give_up: 'give up',
    fix_problem: 'game is broken',
    once_again: 'once again',
    congratulations: 'Congratulations!',
    timeOverhead: 'more then day',
    start: 'Start',

    quizInitCaption: "I'll search the regions by",
    quizInitCheck: "Choose at least one option",

    localization: 'Localization',
    enTitle: 'English title',
    ruTitle: 'Russian title',
    availableRegions: 'Available regions',
    preview: 'Preview',
    previewWarning: 'position and zoom will be saved as default for that game',
    publish: 'Publish',
    publishedToMe: 'Allow only you',
    publishedToAll: 'Allow to any users',
    save: 'Save',
    bugReport: 'Something went wrong. Please {0}.',
    tooManyRegions: 'Too many regions',
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
    km2: 'кв. км.',

    loading: 'Загрузка...',
    loadingError: 'Что-то пошло не так :(',
    networkError: "Соединение с сервером...",

    found: 'Найдено',
    give_up: 'сдаюсь',
    fix_problem: 'игра сломалась!',
    once_again: 'ещё раз',
    congratulations: 'Поздравляем!',
    timeOverhead: 'больше, чем за день',
    start: 'Начали!',

    quizInitCaption: "Я буду искать регионы по",
    quizInitCheck: "Выберите хотя бы один вариант",

    localization: 'Перевод названия',
    enTitle: 'Английское название',
    ruTitle: 'Русское название',
    availableRegions: 'Доступные регионы',
    preview: 'Предпросмотр',
    previewWarning: 'позиция и масштаб будут сохранены как настройки по умолчанию',
    publish: 'Опубликовать',
    publishedToMe: 'Доступно только мне',
    publishedToAll: 'Доступно всем пользователям',
    save: 'Сохранить',
    bugReport: 'Что-то пошло не так. Пожалуйста, {0}.',
    tooManyRegions: 'Слишком много регионов',
  }
});

localization.setLanguage(window.__LANGUAGE__);

export default localization;
