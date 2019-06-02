'use strict';
import {addLocaleData} from "react-intl";
import locale_en from 'react-intl/locale-data/en';
import locale_ru from 'react-intl/locale-data/ru';


addLocaleData([...locale_en, ...locale_ru]);

import messages_ru from "./locale/ru.json";
import messages_en from "./locale/en.json";

const messages = {
  'ru': messages_ru,
  'en': messages_en
};

export default messages;