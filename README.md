# PiCar L298N KiCad Schematic

## Files

- `picar_l298n.kicad_sch` - KiCad 9 schematic (programmatically generated)
- `gen_schematic.py` - Generator script
- `l298n_driver.png/svg` - Matplotlib preview images

## Viewing

**KiCad GUI**: Open `picar_l298n.kicad_sch` in KiCad 9.x (recommended)
**Quick Preview**: Open `l298n_driver.png` or `l298n_driver.svg` (decorative only)

## Circuit

- Raspberry Pi 5 GPIO → L298N H-Bridge → Dual DC Motors
- GPIO18=PWM, GPIO23=IN1, GPIO24=IN2, GPIO25=IN3, GPIO26=ENB, GPIO27=IN4
- +12V motor supply, +5V logic supply from RPi

## KiCad CLI Limitation

The `.kicad_sch` file is syntactically valid but cannot be exported to SVG via CLI
(`kicad-cli sch export svg`) because KiCad CLI cannot render schematics with
placed symbols headlessly. Use KiCad GUI to open and export.
