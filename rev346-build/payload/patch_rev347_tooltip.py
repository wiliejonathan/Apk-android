from pathlib import Path

p = Path('rev346-build/app/src/main/assets/www/assets/dashboard-mobile.js')
s = p.read_text(encoding='utf-8')

old = """function tf_makeEquityTouchEvent(canvas, touch) {\nreturn {\ncurrentTarget: canvas,\nclientX: touch ? touch.clientX : 0,\nclientY: touch ? touch.clientY : 0\n};\n}\n"""
new = """function tf_makeEquityTouchEvent(canvas, touch) {\nreturn {\ncurrentTarget: canvas,\nclientX: touch ? touch.clientX : 0,\nclientY: touch ? touch.clientY : 0,\ntfTouch: true\n};\n}\nfunction tf_positionEquityTooltip(tooltip, wrapper, evt) {\nif (!tooltip || !wrapper || !evt) return;\nconst wrapRect = wrapper.getBoundingClientRect();\nconst tooltipRect = tooltip.getBoundingClientRect();\nconst pad = 8;\nconst pointX = Number(evt.clientX || 0) - wrapRect.left;\nconst pointY = Number(evt.clientY || 0) - wrapRect.top;\nconst isTouch = evt.tfTouch === true;\nlet tx;\nlet ty;\nif (isTouch) {\nconst clearance = 72;\ntx = pointX - (tooltipRect.width / 2);\nty = pointY - tooltipRect.height - clearance;\nif (ty < pad) {\nconst belowY = pointY + clearance;\nif (belowY + tooltipRect.height <= wrapRect.height - pad) {\nty = belowY;\n}\nelse {\nty = pointY - (tooltipRect.height / 2);\nif (pointX <= wrapRect.width / 2) tx = pointX + clearance;\nelse tx = pointX - tooltipRect.width - clearance;\n}\n}\n}\nelse {\ntx = pointX + 8;\nty = pointY - 8;\n}\nconst maxX = Math.max(pad, wrapRect.width - tooltipRect.width - pad);\nconst maxY = Math.max(pad, wrapRect.height - tooltipRect.height - pad);\ntx = Math.max(pad, Math.min(maxX, tx));\nty = Math.max(pad, Math.min(maxY, ty));\ntooltip.style.left = tx + 'px';\ntooltip.style.top = ty + 'px';\n}\n"""
if old not in s:
    raise SystemExit('touch event block not found')
s = s.replace(old, new, 1)

block = """const wrapRect = wrapper.getBoundingClientRect();\nlet tx = evt.clientX - wrapRect.left + 8;\nlet ty = evt.clientY - wrapRect.top - 8;\nconst tooltipRect = tooltip.getBoundingClientRect();\nconst maxX = wrapRect.width - tooltipRect.width - 8;\nconst maxY = wrapRect.height - tooltipRect.height - 8;\nif (tx < 8)\ntx = 8;\nif (ty < 8)\nty = 8;\nif (tx > maxX)\ntx = maxX;\nif (ty > maxY)\nty = maxY;\ntooltip.style.left = tx + 'px';\ntooltip.style.top = ty + 'px';"""
count = s.count(block)
if count != 2:
    raise SystemExit(f'expected 2 tooltip position blocks, found {count}')
s = s.replace(block, 'tf_positionEquityTooltip(tooltip, wrapper, evt);', 2)
s += "\n// REV347: Touch tooltip uses 72px finger clearance; desktop mouse placement unchanged.\n"
p.write_text(s, encoding='utf-8')
print('REV347 touch tooltip patch applied')
