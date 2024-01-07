import messages from "../locale/messages";

const prepareInfobox = (json) => {
  if (json.area) {
    json.area = `${Number(json.area).toLocaleString()} ${messages[window.__LANGUAGE__].km2}`;
  }
  if (json.population) {
    json.population = Number(json.population).toLocaleString();
  }
  ['depth', 'length', 'width', 'height'].forEach(item => {
    if (json[item]) {
      json[item] = `${Number(json[item]).toLocaleString()} ${messages[window.__LANGUAGE__].m}`;
    }
  });
  return json;
};

function shuffle(a) {
  for (let i = a.length; i; i--) {
    let j = Math.floor(Math.random() * i);
    [a[i - 1], a[j]] = [a[j], a[i - 1]];
  }
  return a;
}


export {prepareInfobox, shuffle};