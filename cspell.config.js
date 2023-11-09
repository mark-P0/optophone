/* prettier-ignore */
const words = `
asynch
oneline
loguru
powerup
picamera
binarize
binarization
otsu
leds
pytesseract
xlow
xhigh
xslow
xfast
xloud
pico
`.trim().split('\n');

/** @type {import('@cspell/cspell-types').CSpellSettings} */
const config = {
  words,
  allowCompoundWords: true,
};

module.exports = config;
