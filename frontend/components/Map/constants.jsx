function getColors(theme) {
  let result = {
    SOLVED: '#419641',
    WRONG: '#d9534f',
    CHECKING: '#ecb436',
    UNKNOWN: '#000000',
  }
  if (theme === 'dark') {
    result.UNKNOWN = '#ffffe0';
  }
  return result;
}


export { getColors };
