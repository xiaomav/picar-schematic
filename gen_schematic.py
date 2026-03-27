#!/usr/bin/env python3
"""PiCar L298N KiCad Schematic Generator - Clean Text Output."""
import uuid as _u, os
from datetime import date as _td

G = 2.54
def x(n): return n * G
def y(n): return n * G
uid = lambda: str(_u.uuid4()).upper()
today = _td.today().isoformat()
OUT = "/home/pi/projects/picar-l298n/picar_l298n.kicad_sch"
L = []
def O(s): L.append(s)

def wire(x1,y1,x2,y2):
    O("(wire (pts (xy %s %s) (xy %s %s)) (stroke (width 0) (type default)) (uuid %s))"%(x1,y1,x2,y2,uid()))
def junc(xi,yi):
    O("(junction (at %s %s) (diameter 0) (color 0 0 0 0) (uuid %s))"%(xi,yi,uid()))
def lbl(text,xi,yi):
    O('(label "%s" (at %s %s 0) (effects (font (size 1.27 1.27) (justify left))) (uuid %s))'%(text,xi,yi,uid()))
def txtel(text,xi,yi,sz=2.0):
    O('(text "%s" (at %s %s 0) (effects (font (size %s %s))))'%(text,xi,yi,sz,sz))

def sym_ref(lib_id,ref,val,xi,yi):
    O("(symbol (lib_id %s) (at %s %s 0) (unit 1) (body_style 1) (exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (fields_autoplaced yes) (uuid %s)"%(lib_id,xi,yi,uid()))
    O("  (property Reference %s (at %s %s 0) (effects (font (size 1.27 1.27) (justify left))))"%(ref,xi+2.54,yi-2.54))
    O("  (property Value %s (at %s %s 0) (effects (font (size 1.27 1.27) (justify left))))"%(val,xi+2.54,yi-3.81))
    O("  (property Footprint (at %s %s 0) (hide yes) (effects (font (size 1.27 1.27))))"%(xi,yi))
    O("  (property Datasheet (at %s %s 0) (hide yes) (effects (font (size 1.27 1.27))))"%(xi,yi))
    O("  (instances (project (path (reference %s) (unit 1))))"%(ref))
    O(")")

def power_sym(lib_id,ref,xi,yi):
    O("(symbol (lib_id %s) (at %s %s 0) (unit 1) (body_style 1) (uuid %s)"%(lib_id,xi,yi,uid()))
    O("  (property Reference %s (at %s %s 0) (effects (font (size 1.27 1.27))))"%(ref,xi,yi))
    O("  (property Value %s (at %s %s 0) (effects (font (size 1.27 1.27))))"%(ref,xi,yi))
    O("  (instances (project (path (reference %s) (unit 1))))"%(ref))
    O(")")

ICO = dict(VS=22.86,GND=17.78,VSS=12.70,OUT1=7.62,OUT2=2.54,ISENA=-2.54,
           IN1=22.86,ENA=17.78,IN2=12.70,IN3=7.62,ENB=2.54,IN4=-2.54,
           ISENB=-7.62,OUT3=-12.70,OUT4=-17.78,VS2=-22.86)
ICX=x(50); ICY=y(45); RPY=y(50)
def IY(n): return ICY+ICO[n]

# Header
O("(kicad_sch (version 20250318) (generator \"picar-kicad-gen\") (generator_version \"1.0\") (uuid %s) (paper \"A3\")"%(uid(),))
O("  (lib_symbols")
O("    (symbol L298N (pin_numbers (hide yes)) (pin_names (offset 0)) (exclude_from_sim no) (in_bom yes) (on_board yes)")
O("      (property Reference U (at 0 30.48 0) (effects (font (size 1.27 1.27) (justify left))))")
O("      (property Value L298N (at 0 27.94 0) (effects (font (size 1.27 1.27) (justify left))))")
for nm,val in [("Footprint","Package_DIP:DIP-16_W7.62mm"),("Datasheet","https://www.st.com/resource/en/datasheet/l298.pdf"),("Description","\"Dual full-bridge driver\"")]:
    O("      (property %s %s (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))"%(nm,val))
O("      (symbol L298N_0_1 (rectangle (start -15.24 -27.94) (end 15.24 27.94) (stroke (width 0.254) (type default)) (fill (type background))))")
O("      (symbol L298N_1_1")
for num,px,py,rot,ptype,pname in [
    ("1",-20.32,22.86,0,'passive','VS'),("2",-20.32,17.78,0,'passive','GND'),("3",-20.32,12.70,0,'passive','VSS'),
    ("4",-20.32,7.62,0,'passive','OUT1'),("5",-20.32,2.54,0,'passive','OUT2'),("6",-20.32,-2.54,0,'passive','ISENA'),
    ("7",20.32,22.86,180,'input','IN1'),("8",20.32,17.78,180,'input','ENABLE_A'),
    ("9",20.32,12.70,180,'input','IN2'),("10",20.32,7.62,180,'input','IN3'),
    ("11",20.32,2.54,180,'input','ENABLE_B'),("12",20.32,-2.54,180,'input','IN4'),
    ("13",-20.32,-7.62,0,'passive','ISENB'),("14",-20.32,-12.70,0,'passive','OUT3'),
    ("15",-20.32,-17.78,0,'passive','OUT4'),("16",-20.32,-22.86,0,'passive','VS2')]:
    O("        (pin %s line (at %s %s %s) (length 2.54) (name %s (effects (font (size 1.27 1.27) (justify left)))) (number %s (effects (font (size 1.27 1.27) (justify left)))))"%(ptype,px,py,rot,pname,num))
O("      )")
O("      (embedded_fonts no)")
O("    )")
O("  )")

# Power symbols
power_sym("power:+12V","#FLAT8",x(5),y(22))
power_sym("power:GND","#FLGND",x(5),y(28))
power_sym("power:+5V","#FLAT5",x(5),y(36))

# L298N IC
sym_ref("L298N","U1","L298N",ICX,ICY)

# Filter caps
for nm,xp,yp in [("C1",22,16),("C2",26,16),("C3",22,28),("C4",26,28)]:
    sym_ref("Device:CP",nm,"100uF",x(xp),y(yp))

# Diodes
for nm,xp,yp in [("D1",82,17),("D2",82,25),("D3",82,57),("D4",82,65)]:
    sym_ref("Device:D",nm,"1N4007",x(xp),y(yp))

# Motors
sym_ref("Device:Motor_DC","M1","DC12V",x(92),y(21.5))
sym_ref("Device:Motor_DC","M2","DC12V",x(92),y(60.5))
sym_ref("Connector_Generic:Conn_01x06","J1","RPi_GPIO",x(12),RPY)

# Wires: +12V rail
junc(x(5),y(22)); wire(x(5),y(22),x(16),y(22)); wire(x(16),y(22),x(22),y(22))
wire(x(22),y(22),x(29.68),y(22)); junc(x(29.68),y(22))
wire(x(22),y(22),x(22),y(16)); junc(x(22),y(22))
wire(x(26),y(22),x(26),y(16)); junc(x(26),y(22))
junc(x(5),y(28)); wire(x(5),y(28),x(16),y(28))
junc(x(22),y(28)); junc(x(26),y(28)); wire(x(29.68),y(28),x(29.68),y(17.78))
junc(x(5),y(36)); wire(x(5),y(36),x(14),y(36))
wire(x(14),y(36),x(14),y(30)); wire(x(14),y(30),x(29.68),y(30))
wire(x(22),y(30),x(22),y(28)); wire(x(26),y(30),x(26),y(28))
wire(x(22),y(30),x(22),y(36)); wire(x(26),y(30),x(26),y(36))
junc(x(22),y(30)); junc(x(26),y(30))
for gname,pin_nm,xc in [("GPIO18/ENA","ENA",16),("GPIO23/IN1","IN1",14),("GPIO24/IN2","IN2",12),("GPIO25/IN3","IN3",10),("GPIO26/ENB","ENB",8),("GPIO27/IN4","IN4",6)]:
    yp=IY(pin_nm); gpnum=int(gname.split("/")[0][4:]); yh=RPY-y(gpnum*2)
    wire(x(xc),yh,x(xc),yp); wire(x(xc),yp,x(ICX+15.24),yp)
    lbl(gname,x(xc+1),yp-2)
M1P=y(21.5); M1M=y(16.5)
wire(x(ICX-15.24),IY("OUT1"),x(82),IY("OUT1")); junc(x(ICX-15.24),IY("OUT1")); junc(x(82),IY("OUT1")); lbl("M1+",x(84),IY("OUT1"))
wire(x(82),IY("OUT2"),x(82),M1M)
wire(x(ICX-15.24),IY("OUT2"),x(82),IY("OUT2")); junc(x(ICX-15.24),IY("OUT2")); junc(x(82),IY("OUT2"))
wire(x(82),IY("OUT2"),x(82),M1M); lbl("M1-",x(84),M1M)
wire(x(87.63),M1P,x(92),M1P); wire(x(87.63),M1M,x(92),M1M)
M2P=y(60.5); M2M=y(55.5)
wire(x(ICX-15.24),IY("OUT3"),x(82),IY("OUT3")); junc(x(ICX-15.24),IY("OUT3")); junc(x(82),IY("OUT3")); lbl("M2+",x(84),IY("OUT3"))
wire(x(ICX-15.24),IY("OUT4"),x(82),IY("OUT4")); junc(x(ICX-15.24),IY("OUT4")); junc(x(82),IY("OUT4"))
lbl("M2-",x(84),M2M); wire(x(82),IY("OUT4"),x(87.63),M2M)
wire(x(82),IY("OUT3"),x(87.63),M2P); wire(x(87.63),M2P,x(92),M2P); wire(x(87.63),M2M,x(92),M2M)
for txt_c,xp,yp,sz in [("Motor Supply +12V",3,17,1.8),("Logic GND",3,25,1.5),("+5V from RPi",3,33,1.5),("RPi GPIO Header",3,43,1.5),("L298N Enable/PWM/In",30,43,1.5),("Motor Outputs",60,43,1.5),("Flyback Diodes",75,43,1.5),("DC Motors",85,43,1.5)]:
    txtel(txt_c,x(xp),y(yp),sz)

# Sheet
O("(sheet (at 0 0) (size 420 297) (stroke (width 0.254) (type default)) (fill (type none)) (uuid %s))"%(uid(),))
# Title block
O('(title_block (title "PiCar L298N Motor Driver") (company "xiaomav") (rev "v0.2-kicad") (date "%s") (source "picar-l298n")'%(today,))
O('  (comment (id 1) (value "Author: xiaomav / PiCar Project"))')
O('  (comment (id 2) (value "Raspberry Pi 5 + L298N Dual H-Bridge"))')
O('  (comment (id 3) (value "GPIO18=PWM, GPIO23-27=IN1-IN4"))')
for i in range(4,10): O('  (comment (id %d) (value ""))'%i)
O("  )")
O(")")

content = "\n".join(L) + "\n"
with open(OUT,"w") as f: f.write(content)
sz=os.path.getsize(OUT)
opens=content.count("("); closes=content.count(")")
print("Generated:",OUT,"size:",sz,"Parens:",opens,closes,"diff",opens-closes)
