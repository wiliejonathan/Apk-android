from pathlib import Path

p = Path('rev346-build/app/src/main/assets/www/assets/dashboard-mobile.js')
s = p.read_text(encoding='utf-8')

s = s.replace(
    'const tfEqAxisFloorV340 = tfEqStartBalanceV340 - 1000;',
    'const tfEqAxisFloorV340 = tfEqStartBalanceV340 - Math.abs(tfEqStartBalanceV340) * 0.05;'
)
s = s.replace(
    '// REV344: tight-axis padding + adaptive-height Candle D1 zoom behavior.',
    '// REV345: percentage-axis padding + adaptive-height Candle D1 zoom behavior.'
)

start_marker = "if (equityMetric === 'usd' && !useSharedActualLogScale) {\n  // REV344: tight $1,000 outer padding."
end_marker = "} else if (tMin === tMax) {"
start = s.find(start_marker)
end = s.find(end_marker, start)
if start < 0 or end < 0:
    raise SystemExit('REV344 equity-axis patch markers not found')

replacement = r'''if (equityMetric === 'usd' && !useSharedActualLogScale) {
  const TF_EQ_AXIS_PAD_RATE_V345 = 0.05;
  const padByValueV345 = function(value) {
    const n = Number(value);
    return Math.max(1, Math.abs(Number.isFinite(n) ? n : 0) * TF_EQ_AXIS_PAD_RATE_V345);
  };
  const compareTopV345 = (compareSameMetric && Number.isFinite(compareMaxYRaw)) ? Number(compareMaxYRaw) : -Infinity;
  const actualLowV345 = Math.min(Number(minYRaw) || tfEqStartBalanceV340, tfEqStartBalanceV340);
  const actualTopV345 = Math.max(Number(maxYRaw) || tfEqStartBalanceV340, compareTopV345, tfEqStartBalanceV340);
  const globalMinV345 = actualLowV345 - padByValueV345(actualLowV345);
  const globalMaxV345 = actualTopV345 + padByValueV345(actualTopV345);

  // Candle D1 keeps the adaptive viewport behavior from REV343/REV344.
  // As the user zooms in, the visible OHLC window also receives exactly 5%
  // padding on each edge, so candle height remains readable without a fixed
  // dollar gap dominating a small visible range.
  if (isCandleMode && candleView && candleView.candles && candleView.candles.length) {
    const totalCandleV345 = Math.max(1, candleView.candles.length);
    const visibleCandleV345 = Math.max(1, candleView.end - candleView.start + 1);
    const visibleRatioV345 = Math.max(0, Math.min(1, visibleCandleV345 / totalCandleV345));
    const localLoV345 = Number(minYRaw);
    const localHiV345 = Number(maxYRaw);
    let localMinV345 = localLoV345 - padByValueV345(localLoV345);
    let localMaxV345 = localHiV345 + padByValueV345(localHiV345);
    if (!(localMaxV345 > localMinV345)) {
      const centerV345 = Number.isFinite(localLoV345) ? localLoV345 : tfEqStartBalanceV340;
      const fallbackPadV345 = padByValueV345(centerV345);
      localMinV345 = centerV345 - fallbackPadV345;
      localMaxV345 = centerV345 + fallbackPadV345;
    }
    const zoomBlendV345 = Math.max(0, Math.min(1, (1 - visibleRatioV345) / 0.45));
    tMin = globalMinV345 * (1 - zoomBlendV345) + localMinV345 * zoomBlendV345;
    tMax = globalMaxV345 * (1 - zoomBlendV345) + localMaxV345 * zoomBlendV345;
    if (!(tMax > tMin)) {
      tMin = localMinV345;
      tMax = localMaxV345;
    }
  } else {
    tMin = globalMinV345;
    tMax = globalMaxV345;
  }
'''
s = s[:start] + replacement + s[end:]
s = s.replace(
    '// REV344: money ticks follow the tightened range instead of forcing the chart',
    '// REV345: money ticks follow the percentage-padded range instead of forcing the chart'
)

p.write_text(s, encoding='utf-8')
print('REV345 percentage equity-axis patch applied')
